import asyncio
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from telegram_alert import TelegramAlert

load_dotenv()

# TODO Fill in the main parameters before runing the code
ORIGIN_IATA = "LON"
TRAVEL_CLASS = "ECONOMY"
DEPART_DATE = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
RETURN_DATE = (datetime.today() + timedelta(days=(6 * 30))).strftime("%Y-%m-%d")

# TODO Import the data in Sheety
data_manager = DataManager()
list_of_destinations = data_manager.list_of_destinations

# TODO Establish connection for IATA Codes
flight_search = FlightSearch()

# # TODO -- DEBUGGER. COMMENT OUT AFTER. --
# list_of_destinations = [
#     {"city": "Manila", "iataCode": "MNL", "lowestPrice": 900, "id": 2},
#     {"city": "Paris", "iataCode": "PAR", "lowestPrice": 300, "id": 3},
#     {"city": "Frankfurt", "iataCode": "FRA", "lowestPrice": 42, "id": 4},
#     {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 485, "id": 5},
#     {"city": "Hong Kong", "iataCode": "HKG", "lowestPrice": 551, "id": 6},
#     {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 95, "id": 7},
#     {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 414, "id": 8},
#     {"city": "New York", "iataCode": "NYC", "lowestPrice": 240, "id": 9},
#     {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 260, "id": 10},
#     {"city": "Dublin", "iataCode": "DBN", "lowestPrice": 378, "id": 11}
# ]

# TODO Iterate through the destinations on Sheety and request for the flight data based on the iterator
for destination in list_of_destinations:
    destination_city = destination["city"]

    # This statement updates the iataCode in Google Sheets if the IATA is missing
    if not destination["iataCode"]:
        print("no iataCode found")
        destination["iataCode"] = flight_search.get_iata_code(destination_city)
    else:

        """Call for NON STOP FLIGHT"""
        flight_data = flight_search.search_flight_offers(
            origin_iata=ORIGIN_IATA,
            destination_iata=destination["iataCode"],
            depart_date=DEPART_DATE,
            return_date=RETURN_DATE,
            travel_class=TRAVEL_CLASS,
            non_stop="true"
        )
        outward_date, two_way_return_date, lowest_price_quoted = FlightData.get_two_way_flight_price_data(flight_data)

        # TODO Search results for NON STOP FLIGHT first.
        if lowest_price_quoted:

            departure = DEPART_DATE.split("T")[0]
            arrival = two_way_return_date.split("T")[0]

            print(f"\nSearching flights for {destination_city}...")
            print(f"{destination_city}: £{lowest_price_quoted}")

            if lowest_price_quoted < destination["lowestPrice"]:
                print("sending telegram message")

                non_stop_message = (
                    f"Low price alert! \n"
                    f"Only £{lowest_price_quoted} to fly from {ORIGIN_IATA}-{destination['iataCode']}-{ORIGIN_IATA}, "
                    f"on {departure} until {arrival}."
                )
                # This is a method to call the send_text function on Telegram based on the parameters above
                asyncio.run(TelegramAlert.send_low_price_alert(non_stop_message))
                data_manager.send_email_to_users(non_stop_message)

            time.sleep(1.5)

        # TODO if non-stop flight can't be found, search for ONE WAY flights going to and from destination w/ stopover
        else:
            print(f"\nNo nonstop flight offers found for {destination_city}. Searching multi-stop flights...")

            """OUTWARD FLIGHT"""
            outward_flight_data = flight_search.search_one_way_flight(
                origin_iata=ORIGIN_IATA,
                destination_iata=destination["iataCode"],
                depart_date=DEPART_DATE,
                travel_class=TRAVEL_CLASS,
                non_stop="false"
            )

            # print(outward_flight_data)

            depart_outward_date, _, depart_lowest_price_quoted, depart_stopover \
                = FlightData.get_oneway_flight_price_data(outward_flight_data)

            time.sleep(1.5)

            """RETURN FLIGHT"""
            return_flight_data = flight_search.search_one_way_flight(
                origin_iata=destination["iataCode"],
                destination_iata=ORIGIN_IATA,
                depart_date=RETURN_DATE,
                travel_class=TRAVEL_CLASS,
                non_stop="false"
            )

            time.sleep(1.5)

            # print(return_flight_data)

            _, return_return_date, return_lowest_price_quoted, return_stopover \
                = FlightData.get_oneway_flight_price_data(return_flight_data)

            # If search is successful, check if the multi-stop prices are cheaper than in the table
            if depart_outward_date and return_return_date and depart_lowest_price_quoted and return_lowest_price_quoted:
                multi_stop_depart_date = depart_outward_date.split("T")[0]
                multi_stop_return_date = return_return_date.split("T")[0]
                multi_stop_lowest_price = depart_lowest_price_quoted + return_lowest_price_quoted

                print(f"{destination_city}: £{multi_stop_lowest_price} (MULTI-STOP)")

                if multi_stop_lowest_price < destination["lowestPrice"]:
                    print("sending telegram message")

                    multi_stop_message = (f"Low price alert! "
                                          f"\nOnly £{multi_stop_lowest_price} to fly from "
                                          f"{ORIGIN_IATA}-{depart_stopover}-{destination['iataCode']}, "
                                          f"returning {destination['iataCode']}-{return_stopover}-{ORIGIN_IATA}, "
                                          f"on {multi_stop_depart_date} until {multi_stop_return_date}.")

                    asyncio.run(TelegramAlert.send_low_price_alert(multi_stop_message))
                    data_manager.send_email_to_users(multi_stop_message)
            else:
                print("ALERT: No multi-stop flights found.")

# TODO Comment out to reduce pinging to Sheety APIf
# data_manager.update_iata_code()

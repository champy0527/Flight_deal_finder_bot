import asyncio
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from telegram_alert import TelegramAlert

load_dotenv()

ORIGIN_IATA = "LON"
TRAVEL_CLASS = "ECONOMY"

# TODO Import the data in Sheety
# data_manager = DataManager()
# list_of_destinations = data_manager.list_of_destinations

# TODO Establish connection for IATA Codes
flight_search = FlightSearch()

# TODO -- DEBUGGER. COMMENT OUT AFTER. --
list_of_destinations = [
    {"city": "Manila", "iataCode": "MNL", "lowestPrice": 900, "id": 2},
    {"city": "Paris", "iataCode": "PAR", "lowestPrice": 300, "id": 3},
    {"city": "Frankfurt", "iataCode": "FRA", "lowestPrice": 42, "id": 4},
    {"city": "Tokyo", "iataCode": "TYO", "lowestPrice": 485, "id": 5},
    {"city": "Hong Kong", "iataCode": "HKG", "lowestPrice": 551, "id": 6},
    {"city": "Istanbul", "iataCode": "IST", "lowestPrice": 95, "id": 7},
    {"city": "Kuala Lumpur", "iataCode": "KUL", "lowestPrice": 414, "id": 8},
    {"city": "New York", "iataCode": "NYC", "lowestPrice": 240, "id": 9},
    {"city": "San Francisco", "iataCode": "SFO", "lowestPrice": 260, "id": 10},
    {"city": "Dublin", "iataCode": "DBN", "lowestPrice": 378, "id": 11}
]

# TODO Iterate through the destinations on Sheety and request for the flight data based on the iterator
for destination in list_of_destinations:
    destination_city = destination["city"]
    if not destination["iataCode"]:
        print("no iataCode found")
        # destination["iataCode"] = flight_search.get_iata_code(destination_city)
    else:
        """Establish date"""
        depart_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        return_date = (datetime.today() + timedelta(days=(6 * 30))).strftime("%Y-%m-%d")

        """Call for NON STOP FLIGHT"""
        flight_data = flight_search.search_flight_offers(
            origin_iata=ORIGIN_IATA,
            destination_iata=destination["iataCode"],
            depart_date=depart_date,
            return_date=return_date,
            travel_class=TRAVEL_CLASS,
            non_stop="true"
        )
        outward_date, return_date, lowest_price_quoted = FlightData.get_flight_price_data(flight_data)

        """Search results for NON STOP FLIGHT"""
        if lowest_price_quoted:

            departure = depart_date.split("T")[0]
            arrival = return_date.split("T")[0]

            print(f"\nSearching flights for {destination_city}...")
            print(f"{destination_city}: £{lowest_price_quoted}")

            if lowest_price_quoted < destination["lowestPrice"]:
                print("sending telegram message")

                """This is a method to call the send_text function on Telegram based on the parameters above"""
                async def main():
                    message = (f"Low price alert! "
                               f"Only £{lowest_price_quoted} to fly from {ORIGIN_IATA} to {destination_city}, "
                               f"on {departure} until {arrival}.")
                    await TelegramAlert.telegram_bot_send_text(message)


                asyncio.run(main())

            time.sleep(1.5)

        else: # IF NON-STOP FLIGHTS CANNOT BE FOUND
            print(f"\nNo nonstop flight offers found for {destination_city}. Searching multi-stop flights...")

            depart_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
            return_date = (datetime.today() + timedelta(days=(6 * 30))).strftime("%Y-%m-%d")

            """OUTWARD FLIGHT"""
            outward_flight_data = flight_search.search_one_way_flight(
                origin_iata=ORIGIN_IATA,
                destination_iata=destination["iataCode"],
                depart_date=depart_date,
                travel_class=TRAVEL_CLASS,
                non_stop="false"
            )

            # print(outward_flight_data)

            depart_outward_date, _, depart_lowest_price_quoted, depart_stopover = FlightData.get_oneway_flight_price_data(
                outward_flight_data)

            time.sleep(1.5)

            """RETURN FLIGHT"""
            return_flight_data = flight_search.search_one_way_flight(
                origin_iata=destination["iataCode"],
                destination_iata=ORIGIN_IATA,
                depart_date=return_date,
                travel_class=TRAVEL_CLASS,
                non_stop="false"
            )

            time.sleep(1.5)

            # print(return_flight_data)

            _, return_return_date, return_lowest_price_quoted, return_stopover = FlightData.get_oneway_flight_price_data(
                return_flight_data)

            if depart_outward_date and return_return_date and depart_lowest_price_quoted and return_lowest_price_quoted:
                multi_stop_depart_date = depart_outward_date.split("T")[0]
                multi_stop_return_date = return_return_date.split("T")[0]
                multi_stop_lowest_price = depart_lowest_price_quoted + return_lowest_price_quoted

                print(f"{destination_city}: £{multi_stop_lowest_price} (MULTI-STOP)")

                if multi_stop_lowest_price < destination["lowestPrice"]:
                    print("sending telegram message")


                    async def main():
                        message = (f"Low price alert! "
                                   f"Only £{multi_stop_lowest_price} to fly from {ORIGIN_IATA}-{depart_stopover}-{destination['iataCode']}, returning {destination['iataCode']}-{return_stopover}-{ORIGIN_IATA}. "
                                   f"\non {multi_stop_depart_date} until {multi_stop_return_date}.")
                        await TelegramAlert.telegram_bot_send_text(message)


                    asyncio.run(main())

            else:
                print("ALERT: No multi-stop flights found.")

# TODO Comment out to reduce pinging to Sheety API
# data_manager.update_iata_code()

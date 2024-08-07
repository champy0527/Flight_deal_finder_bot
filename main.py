import asyncio
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from telegram_alert import TelegramAlert

load_dotenv()

ORIGIN_IATA = "LON"
TRAVEL_CLASS = "ECONOMY"

# TODO Import the data in Sheety
data_manager = DataManager()
list_of_destinations = data_manager.list_of_destinations

# TODO Establish connection for IATA Codes
flight_search = FlightSearch()


#  DEBUGGER. COMMENT OUT AFTER.
# list_of_destinations = [
#     {"city": "Manila", "iataCode": "MNL", "lowestPrice": 500, "id": 2},
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

# TODO Get the IATA Code. Comment out once done.
for destination in list_of_destinations:
    destination_city = destination["city"]
    if not destination["iataCode"]:
        print("no iataCode found")
        # destination["iataCode"] = flight_search.get_iata_code(destination_city)
    else:
        """Establish date"""
        depart_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        return_date = (datetime.today() + timedelta(days=(6 * 30))).strftime("%Y-%m-%d")

        flight_data = flight_search.search_flight_offers(
            origin_iata=ORIGIN_IATA,
            destination_iata=destination["iataCode"],
            depart_date=depart_date,
            return_date=return_date,
            travel_class=TRAVEL_CLASS,
            non_stop="true"
        )
        outward_date, return_date, lowest_price_quoted = FlightData.get_flight_price_data(flight_data)

        if lowest_price_quoted:
            print(f"\nSearching flights for {destination_city}...")
            print(f"{destination_city}: £{lowest_price_quoted}")
            if lowest_price_quoted < destination["lowestPrice"]:
                print("sending telegram message")

                """This is a method to call the send_text function on Telegram based on the paramters above"""
                async def main():
                    departure = depart_date.split("T")[0]
                    arrival = return_date.split("T")[0]
                    message = (f"Low price alert! "
                               f"Only £{lowest_price_quoted} to fly from {ORIGIN_IATA} to {destination_city}, "
                               f"on {departure} until {arrival}.")
                    await TelegramAlert.telegram_bot_send_text(message)


                if __name__ == "__main__":
                    asyncio.run(main())

            time.sleep(1500/1000)
        else:
            print(f"\nNo flight offers found for {destination_city}.")
            time.sleep(2)

# TODO Comment out to reduce pinging to Sheety API
# data_manager.update_iata_code()

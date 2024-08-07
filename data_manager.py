import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    API_ENDPOINT = os.getenv("SHEET_API_ENDPOINT")

    def __init__(self):
        self.api_token = os.getenv("SHEETY_BASIC_TOKEN")
        self.list_of_destinations = self.get_sheet()["prices"]

    # TODO Grab the data from Sheety
    def get_sheet(self):
        response = requests.get(url=self.API_ENDPOINT)
        print("Response status code:", response.status_code)
        # print("Response text:", response.text)
        return response.json()

    # TODO Update the IATA code. Once this is done, make sure to comment out on main.py
    def update_iata_code(self):
        for destination in self.list_of_destinations:
            update_code = {
                "price": {
                    "iataCode": destination["iataCode"]
                }
            }

            requests.put(
                url=f"{self.API_ENDPOINT}/{destination['id']}",
                json=update_code
            )


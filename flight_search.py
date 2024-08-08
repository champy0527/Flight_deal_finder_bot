import requests
import os
from dotenv import load_dotenv

load_dotenv()


class FlightSearch:
    TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
    IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    FLIGHT_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_token()

    # TODO Create a token generator
    def _get_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=self.TOKEN_ENDPOINT, headers=header, data=body)
        response_data = response.json()

        if 'access_token' in response_data:
            print(f"ACCESS TOKEN: {response_data['access_token']}")
            print(f"Token type: {response_data['token_type']}")
            print(f"Token expiry: {response_data['expires_in']}")
            return response_data['access_token']
        else:
            raise Exception("Failed to retrieve access token. Please check your API credentials and try again.")

    # TODO Generate a token to grab the IATA code from the Amadeus API
    def get_iata_code(self, destination_city):

        print(f"ACCESS TOKEN: {self._token}")

        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        parameters = {
            "keyword": destination_city,
            "include": "AIRPORTS"
        }

        response = requests.get(self.IATA_ENDPOINT, headers=headers, params=parameters)
        response.raise_for_status()
        response_data = response.json()["data"][0]

        # print(f"Response data: {response_data}")
        try:
            iata_code = response_data["iataCode"]
        except KeyError:
            print(f"KeyError: No airport code found for {destination_city}.")
        else:
            return iata_code

    def search_flight_offers(self, origin_iata, destination_iata, depart_date, return_date, travel_class="BUSINESS",
                             non_stop="true"):

        # 2023-05-02

        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        parameters = {
            "originLocationCode": origin_iata,  # Write LON when you call
            "destinationLocationCode": destination_iata,
            "departureDate": depart_date,
            "returnDate": return_date,
            "adults": 1,
            "travelClass": travel_class,
            "nonStop": non_stop,
            "currencyCode": "GBP",
            "max": "1"
        }

        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, headers=headers, params=parameters)
        response.raise_for_status()
        return response.json()

    def search_one_way_flight(self, origin_iata, destination_iata, depart_date, travel_class="BUSINESS",
                             non_stop="false"):

        # 2023-05-02

        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        parameters = {
            "originLocationCode": origin_iata,  # Write LON when you call
            "destinationLocationCode": destination_iata,
            "departureDate": depart_date,
            "adults": 1,
            "travelClass": travel_class,
            "nonStop": non_stop,
            "currencyCode": "GBP",
            "max": "1"
        }

        response = requests.get(self.FLIGHT_SEARCH_ENDPOINT, headers=headers, params=parameters)
        response.raise_for_status()
        return response.json()


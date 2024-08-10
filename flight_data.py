class FlightData:
    @staticmethod
    def get_two_way_flight_price_data(data):
        if 'data' in data and len(data['data']) > 0:
            flight_data = data['data'][0]
            outward_date = flight_data['itineraries'][0]['segments'][0]['departure']['at']
            # With two-way non-stop flight, itinerary would have a second index, and 0 segment
            return_date = flight_data['itineraries'][1]['segments'][0]['arrival']['at']
            lowest_price = float(flight_data['price']['total'])
            return outward_date, return_date, lowest_price
        else:
            return None, None, None

    @staticmethod
    def get_oneway_flight_price_data(data):
        if 'data' in data and len(data['data']) > 0:
            flight_data = data['data'][0]
            if flight_data['itineraries'][0]['segments'][0]['arrival']['iataCode']:
                outward_date = flight_data['itineraries'][0]['segments'][0]['departure']['at']
                # With one-way multi-stop flight, itinerary would have only one index as it only goes one way.
                # Segment would be +1 per segment added, in this case, it's only 1.
                return_date = flight_data['itineraries'][0]['segments'][1]['arrival']['at']
                lowest_price = float(flight_data['price']['total'])
                # A stopover would be present in the case of a multi-stop flight
                stopover = flight_data['itineraries'][0]['segments'][0]['arrival']['iataCode']
                return outward_date, return_date, lowest_price, stopover
        else:
            # Else statement would have to return one more "None" for stopever
            return None, None, None, None

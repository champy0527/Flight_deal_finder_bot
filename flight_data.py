class FlightData:
    @staticmethod
    def get_flight_price_data(data):
        if 'data' in data and len(data['data']) > 0:
            flight_data = data['data'][0]
            outward_date = flight_data['itineraries'][0]['segments'][0]['departure']['at']
            return_date = flight_data['itineraries'][0]['segments'][-1]['arrival']['at']
            lowest_price = float(flight_data['price']['total'])
            return outward_date, return_date, lowest_price
        else:
            return None, None, None

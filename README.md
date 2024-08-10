This is a capstone project for Udemy's Days 39-40 of 100 Days of Python.

The goal of this project is to utilise REST APIs to create a Flight Deal Finder.
Here are the parameters:
1. A private Google Sheet is created
2. If there are no IATA codes in the Google Sheet, one will be added on. I have commented out the API push request to reduce the number of requests made to Sheety due to the limited number of requests I can make per monmth.
3. Create a static method for Flight Data to create a module for grabbing the variables (departure date, return date, flight price) that will be called in main.py
4. Create another static method for Telegram_Alert to be able to call a telegram_bot_send_text(message)
5. If the lowest price found is lower than the listed price threshold in Google Sheets, a telegram_bot_send_text will be called using __main__ to structure the message.

For revisiting in the future:
- Work on non-stop flight options by looking at the structure of flight_data.py (RESOLVED 10.08.24)
- Reorganise the messaging functions and modules so that the email and telegram modules are all in one file.

# Flight Deal Finder Bot

A Python-based bot that searches for flight deals and sends alerts when prices drop below a specified threshold. The bot pulls destination data from Google Sheets, uses the Amadeus API to find flight offers, and notifies users through Telegram and email.

## Features

- **Search for Flight Deals**: Search for nonstop and multi-stop flights.
- **Price Threshold Alerts**: If the flight price is below a set threshold, the bot sends an alert.
- **Google Sheets Integration**: Use Google Sheets to store destinations and price thresholds.
- **Telegram and Email Notifications**: Receive alerts about flight deals via Telegram and email.
- **Flight Data Handling**: Supports non-stop and multi-stop flight options.

## Technologies Used

- **Python**: Main programming language for implementing the bot.
- **Sheety API**: To manage flight destination data in Google Sheets.
- **Amadeus API**: To get flight details and prices.
- **Telegram API**: To send price alert notifications.
- **SMTP**: To send email alerts.

## Getting Started

### Prerequisites

- **Python 3.6+**: Make sure you have Python installed.
- **Sheety API Access**: To store and manage destination and flight data.
- **Amadeus API Access**: To fetch flight offers and details.
- **Telegram Bot**: Set up a Telegram bot to send notifications.
- **Gmail Account**: Set up for sending email notifications (optional).

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/champy0527/Flight_deal_finder_bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Flight_deal_finder_bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with the following variables:

    ```plaintext
    AMADEUS_API_KEY=<your_amadeus_api_key>
    AMADEUS_API_SECRET=<your_amadeus_api_secret>
    SHEETY_BASIC_TOKEN=<your_sheety_api_token>
    FLIGHT_SHEET_API_ENDPOINT=<your_flight_sheet_endpoint>
    USERS_SHEET_API_ENDPOINT=<your_users_sheet_endpoint>
    SENDER_EMAIL=<your_email>
    SENDER_PASSWORD=<your_email_password>
    ```

### Usage

1. **Define Parameters**: Set up the flight details in the `main.py` file:
   - `ORIGIN_IATA`: The origin airport code.
   - `TRAVEL_CLASS`: Travel class (e.g., ECONOMY).
   - `DEPART_DATE` and `RETURN_DATE`: Travel dates.

2. **Run the Bot**:

    ```bash
    python main.py
    ```

3. The bot will:
   - Retrieve flight data from the Google Sheets using Sheety.
   - Search for flights using the Amadeus API.
   - Send alerts through Telegram and email if a deal is found.

## Code Overview

- **main.py**: Main script that coordinates the flight search, alerts, and data management.
- **FlightSearch Class**:
  - Retrieves IATA codes and searches flight offers using the Amadeus API.
- **FlightData Class**:
  - Extracts flight details like departure, return dates, and prices from the API response.
- **DataManager Class**:
  - Manages data stored in Google Sheets via Sheety API and sends email alerts to users.
- **TelegramAlert Class**:
  - Sends price alerts via Telegram.

## Lessons Learned

- Practiced integrating multiple REST APIs to achieve a unified functionality.
- Gained experience working with Google Sheets via the Sheety API for data storage.
- Improved skills in handling email notifications and Telegram bot integration.
- Learned to use Python's `asyncio` for non-blocking operations.

## Future Improvements

- Add user-defined preferences such as travel class and maximum budget via a web interface.
- Improve error handling, especially for API rate limits and timeouts.
- Store more user details to enable tailored notifications.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## Acknowledgements

- **Udemy**: This project is part of Udemy's "100 Days of Python" course.
- **Amadeus**: For providing a great API to retrieve flight offers.
- **Sheety**: For easy management of Google Sheets as a database.
- **Telegram**: For their user-friendly bot API.

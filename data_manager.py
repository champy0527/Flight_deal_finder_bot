import requests
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()


class DataManager:
    FLIGHT_SHEET_API_ENDPOINT = os.getenv("FLIGHT_SHEET_API_ENDPOINT")
    USERS_SHEET_API_ENDPOINT = os.getenv("USERS_SHEET_API_ENDPOINT")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    def __init__(self):
        self.api_token = os.getenv("SHEETY_BASIC_TOKEN")
        self.list_of_destinations = self.get_sheet()["prices"]
        self.list_of_users = self.get_customer_emails()["users"]

    # TODO Grab the data from Sheety
    def get_sheet(self):
        response = requests.get(url=self.FLIGHT_SHEET_API_ENDPOINT)
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
                url=f"{self.FLIGHT_SHEET_API_ENDPOINT}/{destination['id']}",
                json=update_code
            )

    def get_customer_emails(self):
        response = requests.get(url=self.USERS_SHEET_API_ENDPOINT)
        print("Response status code:", response.status_code)
        # print("Response text:", response.text)
        return response.json()

    def send_email_to_users(self, message_alert):
        for user in self.list_of_users:
            user_email = user["whatIsYourEmailAddress?"]
            user_first_name = user["whatIsYourFirstName?"]
            subject = f"Flight Deal Alert for {user_first_name}"

            message = MIMEMultipart()
            message["From"] = self.SENDER_EMAIL
            message["To"] = user_email
            message["Subject"] = subject

            message.attach(MIMEText(message_alert, "plain", "utf-8"))

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.SENDER_EMAIL, password=self.SENDER_PASSWORD)
                connection.sendmail(
                    from_addr=self.SENDER_EMAIL,
                    to_addrs=user_email,
                    msg=message.as_string()
                )

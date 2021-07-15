import os
import warnings
import random
from datetime import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import psycopg2
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()

# get the postgres db connection parameters from environment variable

name = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")

# connect an instance of postgres DB
con = psycopg2.connect(
    database=name, user=user, password=password, host=host, port=port
)
cursor = con.cursor()


class ActionCustomerDetails(Action):

    def name(self) -> Text:
        return "action_customer_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="You are on a savings account!")

        return []


class ActionPurchaseProducts(Action):

    def name(self) -> Text:
        return "action_purchase_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # import ipdb; ipdb.set_trace()
        print(tracker.sender_id)
        current_product = tracker.get_slot('product')
        product_price = tracker.get_slot('price')
        criteria = tracker.get_slot('criteria')

        # q = "select * from shop where product='{0}' limit 1".format(current_product)
        # result = cursor.query(q)
        # print(result)
        if not criteria:
            dispatcher.utter_message(text="here is {}".format(current_product))
            dispatcher.utter_message(text="https://www.amazon.com/{}/1".format(current_product))
        elif not product_price:
            dispatcher.utter_message(text="here is {} of size {}".format(current_product, criteria))
        elif product_price:
            dispatcher.utter_message(text="here is {} {}".format(product_price, current_product))
        return []


class ActionAddCart(Action):

    def name(self) -> Text:
        return "action_add_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # import ipdb; ipdb.set_trace()
        id = random.randint(110, 9000)
        current_product = tracker.get_slot('product')
        if current_product is not None:
            cursor.execute("INSERT INTO shop (id, product, brand, amount, url, date) VALUES (%s, %s, %s, %s, %s, %s)",
                           (id, current_product, "dunder", 10, "www.amazon.com", datetime.now().strftime("%Y-%m-%d")))
            con.commit()
            dispatcher.utter_message(text="Your {} has been added to cart".format(current_product))

        return [SlotSet('product', None)]


class ActionCheckout(Action):

    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_product = tracker.get_slot('product')
        if current_product is not None:
            cursor.execute("SELECT product FROM shop WHERE amount = '100' ")
            rows = cursor.fetchall()
            dispatcher.utter_message(text="You have {} items to pay for. "
                                          "Click [here](https://www.paystack.com) to proceed".format(len(rows[:4])))
        elif not current_product:
            dispatcher.utter_message(text="sorry you can't make payment without any product in cart")

        return []


class ShowPurchaseHistory(Action):

    def name(self) -> Text:
        return "action_purchase_history"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cursor.execute("SELECT product FROM shop WHERE date = '2021-07-06 00:00:00' ")
        rows = cursor.fetchall()
        all_items = [r[0] for r in rows[:3]]
        if not all_items:
            dispatcher.utter_message(text="purchase history is empty")
        elif all_items:
            dispatcher.utter_message(text="You've purchased {} items in the past 2 weeks".format(len(all_items)))
            dispatcher.utter_message(text="These are the items {}".format(all_items))

        return []

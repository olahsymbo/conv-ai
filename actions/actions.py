import os
import warnings
import random
from datetime import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
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
        result = []
        # import ipdb; ipdb.set_trace()
        current_product = tracker.get_slot('product')
        product_price = tracker.get_slot('price')
        criteria = tracker.get_slot('criteria')

        # q = "select * from shop where product='{0}' limit 1".format(current_product)
        # result = cursor.query(q)
        # print(result)
        if not criteria:
            dispatcher.utter_message(text="here are {}".format(current_product))
        elif not product_price:
            dispatcher.utter_message(text="here are {} of size {}".format(current_product, criteria))
        elif product_price:
            dispatcher.utter_message(text="here are {} {}".format(product_price, current_product))
        return []


class ActionAddCart(Action):

    def name(self) -> Text:
        return "action_add_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        result = []
        # import ipdb; ipdb.set_trace()
        id = random.randint(110,9000)
        current_product = tracker.get_slot('product')
        cursor.execute("INSERT INTO shop (id, product, brand, amount, url, date) VALUES (%s, %s, %s, %s, %s, %s)",
                       (id, current_product, "dunder", 10, "www.amazon.com", datetime.now().strftime("%Y-%m-%d")))
        con.commit()
        dispatcher.utter_message(text="Your {} has been added to cart".format(current_product))

        return []

import os
import psycopg2
from datetime import datetime
import warnings
from faker import Faker
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()

con = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
)
print("Database opened successfully")

cursor = con.cursor()

fake = Faker()

for i in range(1000):
    id = fake.random_digit_not_null()
    product = fake.city()
    brand = fake.city()
    amount = fake.random_digit_not_null()
    url = fake.paragraph()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO shop (id, product, brand, amount, url, date) VALUES (%s, %s, %s, %s, %s, %s)",
        (id, product, brand, amount, url, date),
    )
con.commit()
print("Records created successfully")
con.close()

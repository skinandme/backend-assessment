import os
import logging
import json
import sys
from flask import app
from assessment.app import create_app
from assessment.models import db
from assessment.factory.customer import CustomerFactory
from assessment.models.product import Product

from faker import Faker
# Use predictable data from Faker to load customer data so customer's details are familiar
# print([logging.getLogger(name) for name in logging.root.manager.loggerDict])
Faker.seed(30)

# Turn off logging from Faker - shouldn't be necessary in production.
logging.getLogger('faker').setLevel(logging.INFO)

if __name__ == "__main__":
# Run this file directly to create the database tables.

    logging.basicConfig(
       level=logging.DEBUG, 
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    )

    app=create_app()

    logging.info( f'Dropping database' )
    try:
        db.drop_all(app=app)
    except Exception as e:
        logging.warning(f"drop database returned: {e}")

    logging.info( f'Creating database' )
    db.create_all(app=app)
    logging.info( f'database created, populating tables from {app.config["ASSESSMENT_SEED_DATA"]}' )

    # Load the seed data if the database has been newly created
    if not os.path.isfile(app.config["ASSESSMENT_SEED_DATA"]):
        logging.warning(f'no seeding data found in {app.config["ASSESSMENT_SEED_DATA"]}')
        sys.exit(0)
    
    seed_data = {}
    with open(app.config["ASSESSMENT_SEED_DATA"], 'r', encoding='utf-8') as data:
        seed_data = json.load(data)

    with app.app_context():

        # Load product data from the product node in the seeding file, if there is any
        products = 0
        for p in seed_data.get('product', []):
            products += 1
            product = Product(**p)
            db.session.add(product)
            logging.debug(f"{products:2} {product.name} ({product.description})")
        logging.info(f"products loaded: {products}")

        # Fake the customer data. We couyld use a 'customer' node in the seeding file but it
        # feels like a lot of work for no real gain.
        for i in range(1,10):
            cf = CustomerFactory()
            customer = cf.create()
            db.session.add(customer)
            logging.debug(f"{i:2} {customer.username:20} - {customer.title:4} {customer.first_name} {customer.last_name}")
        logging.info(f"customers loaded: {i}")

        # Commit the data to the database
        db.session.commit()


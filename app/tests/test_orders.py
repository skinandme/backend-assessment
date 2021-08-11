import pytest
import json
from assessment.models.customer import Customer
from assessment.models.product import Product
from assessment.models.order import Order
from assessment.models import db
from application import app as application
import random

"""
   A couple of functional tests to check that our flask route is doing
   what is should. 
"""

def test_order_creation_success( app, queries ):

    """
        Exercise the /order API route by ordering a random quantity
        of a product for a customer and then check to make sure the
        order has been created properly.
    """
    with app.app_context() as ac:

        # Get the first customer and product available in the database
        customer_id = Customer.query.first().id
        product_id = Product.query.first().id
        # Generate a random quantity
        order_quantity = int(random.uniform(1,10))

        # Make the API call to order `order_quantity` of the product for the customer
        with application.test_client() as client:
            response = client.post(
                '/order',
                data=json.dumps({
                    'product': product_id,
                    'customer': customer_id,
                    'quantity': order_quantity
                }),
                content_type='application/json'
            )

            # Successful request?
            assert response.status_code == 200

            # Check to ensure the order exists for the customer and product
            payload = json.loads(response.data.decode())
            assert not payload['error']
            order = Order.query.filter_by(id=payload['order_id']).first()
            assert order
            assert order.product.pop().id == product_id
            assert order.customer_id == customer_id
            assert order.quantity == order_quantity
            assert len(queries) == 8


@pytest.mark.parametrize(
    "customer_generator, product_generator, quantity, status_code, error_text",
    [
        # unknown customer
        pytest.param(
            'customer_factory', 'product_factory', 1, 404, 'NoSuchCustomer',
        ),
        # valid customer, unknown product
        pytest.param(
            'a_customer', 'product_factory', 1, 404, 'NoSuchProduct',
        ),
        # valid customer and product, quantity not an integer
        pytest.param(
            'a_customer', 'a_product', 'test', 406, 'InvalidQuantity'
        ),
        # valid customer and product but quantity not in valid range
        pytest.param(
            'a_customer', 'a_product', -3, 416, 'InvalidQuantityValue'
        ),
    ]
)
def test_order_creation_failure_reasons(
    app, request, customer_generator, product_generator, quantity, status_code, error_text
    ):
    """
        Check failue processing covering status codes and error text.
    """
    with app.app_context():

        """
           customer_generator and product_generator either use the {customer|product}_factory
           functions or they use the helper function to find the first customer or product in
           the database. These have a consistent calling interface and return the valid Customer
           or Product accordingly.
        """
        customer = request.getfixturevalue(customer_generator).create()
        product = request.getfixturevalue(product_generator).create()

        # Make the API call passing the configured customer, product and quantity
        with application.test_client() as client:
            response = client.post(
                '/order',
                data=json.dumps({
                    'product': product.id,
                    'customer': customer.id,
                    'quantity': quantity
                }),
                content_type='application/json'
            )

            # check the status code is the one we wanted
            assert response.status_code == status_code
            # decode the payload
            response_payload = json.loads(response.data)
            """
               Ensure the response is a failure (they all should be) and that the 
               error_text is what we are expecting.
            """
            assert response_payload['error'] == True
            assert error_text == response_payload['reason']

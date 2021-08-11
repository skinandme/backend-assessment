from typing import Any, Tuple
from flask import render_template, request
from assessment.app import create_app
import json
from assessment.models import db
from assessment.models.customer import Customer
from assessment.models.product import Product
from typing import Tuple, Union, Dict

app = create_app()

def _standard_response(
    payload:Union[str,dict], status_code:int
) -> Tuple[str,int,Dict[str,str]]:

    response = {'error': False}
    if status_code != 200:
        response['error'] = True
        response['reason'] = payload
    else:
        response.update(payload)

    return json.dumps(response), status_code, { 'Content-Type': 'application/json'}


@app.route('/')
def index():
    # Default route - blank page
    return render_template('index.html')


@app.route('/order', methods=['POST'])
def order_product():
    # Given a customer and product, order a given quantity.
    # See tests/test_orders.py::test_order_creation for an example payload.

    order = None
    try:
        payload = request.json
    except Exception as e:
        return _standard_response(str(e), 500)

    with app.app_context():

        customer = Customer.query.filter_by(id=payload['customer']).one_or_none()
        if not customer:
            return _standard_response('NoSuchCustomer', 404)

        product = Product.query.filter_by(id=payload['product']).one_or_none()
        if not product:
            return _standard_response('NoSuchProduct', 404)

        try:
            payload['quantity'] = int(payload['quantity'])
            if payload['quantity'] < 0:
                return _standard_response('InvalidQuantityValue', 416)
        except Exception as e:
            return _standard_response('InvalidQuantity', 406)

        try:
            order = customer.purchase(
                product_id=product.id,
                quantity=payload['quantity']
            )
            db.session.add(order)
            db.session.commit()
            return _standard_response({'order_id': order.id}, 200)

        except Exception as e:
            return _standard_response(str(e), 500)


if __name__ == '__main__':
    app.run()
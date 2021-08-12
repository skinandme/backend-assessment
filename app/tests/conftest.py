from typing import List
import pytest
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
from assessment.factory.customer import CustomerFactory
from assessment.factory.product import ProductFactory
from assessment.models.customer import Customer
from assessment.models.product import Product
from assessment.app import create_app
from assessment.models import db as _db

class FirstCustomer(object):
    def create(self):
        return Customer.query.first()

class FirstProduct(object):
    def create(self):
        return Product.query.first()

@pytest.fixture
def logger() -> logging:
    log = logging.getLogger("unit_tests")
    return log

@pytest.fixture
def app() -> Flask:
    return create_app()

@pytest.fixture
def db() -> SQLAlchemy:
    return _db

@pytest.fixture
def customer_factory() -> CustomerFactory:
    return CustomerFactory()

@pytest.fixture
def product_factory() -> ProductFactory:
    return ProductFactory()

@pytest.fixture
def a_customer() -> Customer:
    return FirstCustomer()

@pytest.fixture
def a_product() -> Product:
    return FirstProduct()

@pytest.fixture
def queries() -> List:
    statement_list = []
    def catch_queries(conn, cursor, statement, parameters, context, executemany):
        statement_list.append(statement)
    event.listen(Engine, "before_cursor_execute", catch_queries)
    return statement_list
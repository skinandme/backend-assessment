import os
from assessment.models import db, UUID
import datetime
from assessment.crypto import hash, Cipher
from assessment.models.order import Order

_KEY = os.environ.get("APP_ENCRYPTION_KEY", "default-key")

class Customer(db.Model):
    id = db.Column(db.String(36),primary_key=True,nullable=False)
    title = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, index=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email_encrypted = db.Column(db.String(510), nullable=False)
    email_hash = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    cancelled = db.Column(db.DateTime)
    house_number = db.Column(db.String(50))
    street = db.Column(db.String(50))
    town = db.Column(db.String(50))
    county = db.Column(db.String(50))
    postcode = db.Column(db.String(10))
    orders = db.relationship('Order', back_populates='customer', lazy=True, uselist=True)

    def __init__(self, title:str, first_name:str, last_name:str, username:str, password:str, email:str,
        house_number:str=None, street:str=None, town:str=None, county:str=None, postcode:str=None
    ) -> None:
        self.id = str(UUID())
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = hash(password)
        self.email_hash = hash(email)
        c = Cipher(key=_KEY)
        self.email_encrypted = c.encrypt(email)
        self.house_number = house_number
        self.street = street
        self.town = town
        self.county = county
        self.postcode = postcode

    def __repr__(self) -> str:
        return f'<Customer [{self.id}] {self.first_name} {self.last_name} ({self.username})>'

    def address(self, house_number:str, street:str, town:str, county:str, postcode:str) -> None:
        self.house_number = house_number
        self.street = street
        self.town = town
        self.county = county
        self.postcode = postcode

    def purchase(self, product_id:int, quantity:int) -> Order:
        order = Order(customer_id=self.id, product_id=product_id, quantity=quantity)
        return order

    @property
    def uuid(self):
        return UUID(self.uuid)

    @property
    def email(self):
        c = Cipher(key=_KEY)
        return c.decrypt(self.email_encrypted)

    @classmethod
    def by_email(cls, email:str):
        target = hash(email)
        return db.session.query(cls).filter_by(email_hash=target).first()
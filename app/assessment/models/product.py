from assessment.models import db, UUID
from assessment.models.order import Order

class Product(db.Model):
    id = db.Column(db.String(36),primary_key=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', back_populates='product', lazy=True, uselist=True)

    def __init__(self, name:str, description:str, price:int):
        self.id = str(UUID())
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self) -> str:
        return f'<Product {self.name}>'

    @property
    def uuid(self):
        return UUID(self.uuid)
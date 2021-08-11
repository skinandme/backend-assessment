from assessment.models import db, UUID
import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36),primary_key=True,nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id'), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    customer = db.relationship('Customer', back_populates='orders', lazy=False, uselist=True, foreign_keys=customer_id)
    product = db.relationship('Product', back_populates='orders', lazy=True, uselist=True, foreign_keys=product_id)

    def __init__(
        self,
        customer_id:int,
        product_id:int,
        quantity:int
    ):
        self.id = str(UUID())
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self) -> str:
        if self.customer_id and self.product_id:
            return f'<Order {self.customer_id} <= {self.product_id} ({self.quantity})>'
        else:
            return f'<Order None>'

    @property
    def uuid(self):
        return UUID(self.uuid)
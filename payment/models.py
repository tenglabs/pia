from payment import db
from datetime import datetime


class CustomerPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    currency = db.Column(db.Integer)
    date_sent = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    sign = db.Column(db.String, nullable=True)
    api_id = db.Column(db.Integer, nullable=True)
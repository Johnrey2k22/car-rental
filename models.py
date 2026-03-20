from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(20), default="Automatic")
    seats = db.Column(db.Integer, default=5)
    fuel_type = db.Column(db.String(20), default="Petrol")
    color = db.Column(db.String(30))
    plate_no = db.Column(db.String(20))
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    daily_rate = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

    def is_available_for_dates(self, pickup_dt, return_dt):
        overlap = Booking.query.filter(
            Booking.car_id == self.id,
            Booking.status != 'Cancelled',
            Booking.pickup_datetime < return_dt,
            Booking.return_datetime > pickup_dt
        ).first()
        return overlap is None

    def __repr__(self):
        return f'<Car {self.brand} {self.model}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    return_location = db.Column(db.String(255), nullable=False)
    pickup_datetime = db.Column(db.DateTime, nullable=False)
    return_datetime = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending") # Pending, Confirmed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    car = db.relationship('Car', backref=db.backref('bookings', lazy=True))

class AddOn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="Renter") # Renter, Admin

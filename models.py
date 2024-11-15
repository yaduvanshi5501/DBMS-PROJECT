from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    reservations = db.relationship('Reservation', backref='flight_reservation', lazy=True)  # Changed backref name

    def __repr__(self):
        return f'<Flight {self.origin} to {self.destination}>'

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    reservations = db.relationship('Reservation', backref='passenger_reservation', lazy=True)  # Changed backref name

    def __repr__(self):
        return f'<Passenger {self.name}>'

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    passenger = db.relationship('Passenger', backref='reservations_unique', lazy=True)  # Changed backref name
    flight = db.relationship('Flight', backref='reservations_unique', lazy=True)  # Keep this consistent with Flight model

    def __repr__(self):
        return f'<Reservation {self.id} for {self.passenger.name}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    reservation = db.relationship('Reservation', backref='payment', lazy=True)

    def __repr__(self):
        return f'<Payment {self.amount} for Reservation {self.reservation_id}>'

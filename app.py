from flask import Flask, render_template, request, redirect, url_for
from models import db, Flight, Reservation, Passenger, Payment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    flights = Flight.query.all()  # Querying all flights from the database
    return render_template('index.html', flights=flights)


@app.route('/reserve/<int:flight_id>', methods=['GET', 'POST'])
def reserve(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        passenger = Passenger(name=name, age=age)
        db.session.add(passenger)
        db.session.commit()
        
        reservation = Reservation(flight_id=flight.id, passenger_id=passenger.id)
        db.session.add(reservation)
        db.session.commit()
        
        return redirect(url_for('payment', reservation_id=reservation.id))
    
    return render_template('reserve.html', flight=flight)

@app.route('/payment/<int:reservation_id>', methods=['GET', 'POST'])
def payment(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    
    if request.method == 'POST':
        amount = request.form['amount']
        payment = Payment(amount=amount, reservation_id=reservation.id)
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('payment.html', reservation=reservation)

if __name__ == "__main__":
    app.run(debug=True)

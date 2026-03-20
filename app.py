from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Car, Booking, AddOn, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driveease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    featured_cars = Car.query.limit(3).all()
    return render_template("index.html", featured_cars=featured_cars)

@app.route("/fleet")
def fleet():
    # Get filter parameters
    brands = request.args.getlist('brand')
    categories = request.args.getlist('category')
    transmissions = request.args.getlist('transmission')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = Car.query

    if brands:
        query = query.filter(Car.brand.in_(brands))
    if categories:
        query = query.filter(Car.category.in_(categories))
    if transmissions:
        query = query.filter(Car.transmission.in_(transmissions))
    if min_price:
        query = query.filter(Car.daily_rate >= int(min_price))
    if max_price:
        query = query.filter(Car.daily_rate <= int(max_price))

    cars = query.all()
    
    return render_template("car_listings.html", 
                           cars=cars, 
                           selected_brands=brands,
                           selected_categories=categories,
                           selected_transmissions=transmissions)

@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    similar_cars = Car.query.filter(Car.id != car_id).limit(3).all()
    return render_template("car_detail.html", car=car, similar_cars=similar_cars)

@app.route("/book/<int:car_id>", methods=['GET', 'POST'])
@login_required
def booking(car_id):
    car = Car.query.get_or_404(car_id)
    addons = AddOn.query.all()
    
    if request.method == 'POST':
        try:
            pickup_loc = request.form.get('pickup_location')
            return_loc = request.form.get('return_location')
            pickup_dt = datetime.strptime(request.form.get('pickup_datetime'), '%Y-%m-%dT%H:%M')
            return_dt = datetime.strptime(request.form.get('return_datetime'), '%Y-%m-%dT%H:%M')
            
            # Calculate days (minimum 1 day)
            delta = return_dt - pickup_dt
            days = max(delta.days, 1)
            
            # Base amount
            base_amount = car.daily_rate * days
            
            # Addons
            selected_addons = request.form.getlist('addons')
            addons_amount = 0
            for addon_id in selected_addons:
                addon = AddOn.query.get(addon_id)
                if addon:
                    addons_amount += addon.price_per_day * days
            
            total_amount = base_amount + addons_amount
            
            new_booking = Booking(
                car_id=car.id,
                first_name=request.form.get('first_name'),
                last_name=request.form.get('last_name'),
                email=request.form.get('email'),
                mobile=request.form.get('mobile'),
                pickup_location=pickup_loc,
                return_location=return_loc,
                pickup_datetime=pickup_dt,
                return_datetime=return_dt,
                total_amount=total_amount,
                status="Pending"
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            flash('Booking submitted successfully!', 'success')
            return redirect(url_for('payment'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template("booking_reservation.html", car=car, addons=addons)

@app.route("/payment")
@login_required
def payment():
    return render_template("payment_info.html")

@app.route("/dashboard")
@login_required
def dashboard():
    # In real app, filter by user email or user_id
    bookings = Booking.query.filter_by(email=current_user.email).all()
    return render_template("renter_dashboard.html", bookings=bookings)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check email and password.', 'error')
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
@login_required
def admin():
    if current_user.role != 'Admin':
        abort(403)
    cars = Car.query.all()
    bookings = Booking.query.all()
    return render_template("admin_dashboard.html", cars=cars, bookings=bookings)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Car, Booking, AddOn, User, ContactMessage, NewsletterSubscription
from paymongo import paymongo_service
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driveease.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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
            
            delta = return_dt - pickup_dt
            days = max(delta.days, 1)
            
            base_amount = car.daily_rate * days
            selected_addons = request.form.getlist('addons')
            addons_amount = 0
            for addon_id in selected_addons:
                addon = AddOn.query.get(addon_id)
                if addon:
                    addons_amount += addon.price_per_day * days
            
            total_amount = base_amount + addons_amount
            
            license_front = request.files.get('license_front')
            license_back = request.files.get('license_back')
            front_filename = None
            back_filename = None

            if license_front:
                front_filename = secure_filename(f"front_{current_user.id}_{int(datetime.now().timestamp())}_{license_front.filename}")
                license_front.save(os.path.join(app.config['UPLOAD_FOLDER'], front_filename))
            if license_back:
                back_filename = secure_filename(f"back_{current_user.id}_{int(datetime.now().timestamp())}_{license_back.filename}")
                license_back.save(os.path.join(app.config['UPLOAD_FOLDER'], back_filename))

            new_booking = Booking(
                user_id=current_user.id,
                car_id=car.id,
                first_name=request.form.get('first_name', current_user.first_name),
                last_name=request.form.get('last_name', current_user.last_name),
                email=request.form.get('email', current_user.email),
                mobile=request.form.get('mobile', current_user.mobile_number),
                pickup_location=pickup_loc,
                return_location=return_loc,
                pickup_datetime=pickup_dt,
                return_datetime=return_dt,
                total_amount=total_amount,
                license_front=front_filename,
                license_back=back_filename,
                status="Pending"
            )
            
            db.session.add(new_booking)
            db.session.commit()
            
            flash('Booking submitted successfully!', 'success')
            return redirect(url_for('payment', booking_id=new_booking.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template("booking_reservation.html", car=car, addons=addons)

@app.route("/payment/<int:booking_id>")
@login_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    return render_template("payment_info.html", booking=booking)

@app.route("/checkout/<int:booking_id>", methods=['POST'])
@login_required
def checkout(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    checkout_url = paymongo_service.create_payment_link(
        amount=booking.total_amount,
        description=f"Car Rental: {booking.car.brand} {booking.car.model}",
        booking_id=booking.id
    )
    return redirect(checkout_url)

@app.route("/payment/simulator/<int:booking_id>")
@login_required
def payment_simulator(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)
    return render_template("payment_simulator.html", booking=booking)

@app.route("/payment/confirm/<int:booking_id>", methods=['POST'])
@login_required
def payment_confirm(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        abort(403)

    status = request.args.get('status')
    if status == 'success':
        booking.status = 'Paid'
        db.session.commit()
        flash('Payment successful! Your booking is now pending verification.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Payment failed. Please try again.', 'error')
        return redirect(url_for('payment', booking_id=booking.id))

@app.route("/dashboard")
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("renter_dashboard.html", bookings=bookings)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.mobile_number = request.form.get('mobile')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template("profile.html")

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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        mobile = request.form.get('mobile')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile
        )
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
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    subs = NewsletterSubscription.query.order_by(NewsletterSubscription.created_at.desc()).all()
    return render_template("admin_dashboard.html", cars=cars, bookings=bookings, messages=messages, subs=subs)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/subscribe", methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        existing = NewsletterSubscription.query.filter_by(email=email).first()
        if not existing:
            new_sub = NewsletterSubscription(email=email)
            db.session.add(new_sub)
            db.session.commit()
            flash('Thank you for subscribing!', 'success')
        else:
            flash('You are already subscribed.', 'info')
    return redirect(request.referrer or url_for('home'))

@app.route("/contact", methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    if name and email and message:
        new_msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(new_msg)
        db.session.commit()
        flash('Message sent successfully!', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route("/admin/verify/<int:booking_id>", methods=['GET', 'POST'])
@login_required
def admin_verify(booking_id):
    if current_user.role != 'Admin':
        abort(403)
    booking = Booking.query.get_or_404(booking_id)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'approve':
            booking.status = 'Confirmed'
            booking.rejection_reason = None
            if not booking.user.is_verified:
                booking.user.is_verified = True
        elif action == 'reject':
            booking.status = 'Cancelled'
            booking.rejection_reason = request.form.get('rejection_reason')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("admin_verification.html", booking=booking)

@app.route("/admin/pickup/<int:booking_id>", methods=['POST'])
@login_required
def admin_pickup(booking_id):
    if current_user.role != 'Admin':
        abort(403)
    booking = Booking.query.get_or_404(booking_id)
    booking.status = 'PickedUp'
    booking.car.is_available = False
    db.session.commit()
    flash(f"Vehicle picked up for booking #{booking.id}", "success")
    return redirect(url_for('admin'))

@app.route("/admin/return/<int:booking_id>", methods=['POST'])
@login_required
def admin_return(booking_id):
    if current_user.role != 'Admin':
        abort(403)
    booking = Booking.query.get_or_404(booking_id)
    now = datetime.utcnow()
    booking.actual_return_datetime = now
    booking.status = 'Returned'
    booking.car.is_available = True

    if now > booking.return_datetime:
        time_diff = now - booking.return_datetime
        hours_late = (time_diff.total_seconds() / 3600)
        if (time_diff.total_seconds() % 3600) > 300:
             hours_late = int(hours_late) + 1
        else:
             hours_late = int(hours_late)
        if hours_late > 0:
            booking.late_fee = hours_late * 500.0
            flash(f"Vehicle returned late. Late fee of ₱{booking.late_fee:,.2f} calculated ({hours_late} hours).", "warning")
        else:
            flash("Vehicle returned on time.", "success")
    else:
        flash("Vehicle returned on time.", "success")
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

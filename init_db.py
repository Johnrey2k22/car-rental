from app import app
from models import db, Car, AddOn, User
from werkzeug.security import generate_password_hash

def seed_db():
    with app.app_context():
        db.create_all()

        if Car.query.first():
            print("Database already seeded.")
            return

        cars = [
            Car(
                brand="BMW", model="5 Series", year=2023, 
                transmission="Automatic", seats=5, fuel_type="Hybrid", 
                color="Dark Gray", category="Executive Class", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuAdmzGGopBRtmqT4J3i1x64OM4TiBdioFr6qBzfTUsQLskXlqJQf1ndgth1PCCqK_Y6mdd2eKW6fzaNl8rW1A9PKOUTsbXhWWq7t91ixHvCMcqq2hlgBW5-cPcTJMr6Sf_GRranMyDXaTB9Ald11UM69NUbrMQLxIuJyrJVPjc7Q5SLmMUSR8FVfiQwaWWLDE_u_TojKGs45_TR8E_EqUhYY5JpzidmiHcWRWjZZcinRdbOHVDMnIQrr8P07PkTm88hwf4FDBmeFvTx", 
                daily_rate=8500, description="Modern dark gray executive luxury sedan."
            ),
            Car(
                brand="Land Rover", model="Range Rover Sport", year=2023, 
                transmission="Automatic", seats=7, fuel_type="Diesel", 
                color="Silver", category="Adventure Luxury", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuBkAq5HDTFJpoDMW99BXbLh-pXVvQM5WOmiWSJKceazJG2dr0pzTEJ7bt-33QNo9kxuQySfcgQiMjfDXLvOyLoLf5_6wKh0-dOBfYMzBteL-ZaDR9Nl5DLY9YgPU8nhK6235JGIyP9H30MLuN5vE2YwmUbdFbQJk88b04illoV4R_qg2jIYwGi-MwWmlzqAyamXQXJ6nIa6QENxyHqSNSmH4_zCEygqSwFZrWilOdc7k-x3TF5AmlSMSoxwik5rKeDlGe5hvy1OjK2V", 
                daily_rate=12200, description="Silver luxury SUV driving on a coastal road."
            ),
        ]

        addons = [
            AddOn(name="GPS Navigation", price_per_day=500, description="High-precision satellite navigation with live traffic updates."),
            AddOn(name="Comprehensive Insurance", price_per_day=1200, description="Full collision damage waiver and theft protection."),
        ]

        # Admin User
        admin = User(
            email="admin@driveease.ph",
            password=generate_password_hash("admin123", method='pbkdf2:sha256'),
            role="Admin",
            first_name="Alex",
            last_name="Rivera"
        )

        db.session.add_all(cars)
        db.session.add_all(addons)
        db.session.add(admin)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()

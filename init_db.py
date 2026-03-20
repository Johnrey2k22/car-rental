from app import app
from models import db, Car, AddOn

def seed_db():
    with app.app_context():
        db.create_all()

        # Check if already seeded
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
            Car(
                brand="Tesla", model="Model S", year=2023, 
                transmission="Automatic", seats=5, fuel_type="Electric", 
                color="White", category="Electric Future", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuDjTa-eURh33zTy_g4YC_3fTvmg5_GAuiFbXqAz-4RTwC2ucypx7YEZ3PsjVvFrPsn47smGa_tpn4IiS09p2J1xJRhrxIPL54NZ6sz2uLaFMVDI0GH_5_C8a_EahIv8NAFQ2zqL4yhWwvzTAzP2vjTya5oZIU_Sm6eCYeABq6l1mzHdZk1H7UYKihAoBbsubb2v0VBrhsDlsxlTJx48-VIhlu_kORxqmgTV5jq5jwuwPm1Oa7mPRgd-qYOuugSb6XVZmvniuULxsJ88", 
                daily_rate=15000, description="White modern electric vehicle in front of a clean wall."
            ),
            Car(
                brand="Porsche", model="911 Carrera S", year=2024, 
                transmission="Automatic", seats=2, fuel_type="Petrol", 
                color="Silver", category="Ultra Luxury", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuB94RAduZca2PC0IHRXnmlLRlrnSLtrkAZlV9RYTSgn_cniA550w2w6p26Tme61GCuq1R3uqXeyIallwu5lnDk04tSHyT6JQYT933Gf7f04dm71nH9vrrOySw_m7N-Uf6zaUZ0QTqLGmMR_5Yc59IgNyIfcnYyQ1P2Ysw4S5hYxCARKE9hbtlgFnJpb4qEjhNlDWc1nJNMf3TLBSRe3O26G7KcLI6zeMtroGVrRdvOk3E6T279NVkF9kttaqe44gMJV5YBaxxksHsW3", 
                daily_rate=18500, description="Silver luxury sports coupe parked in an urban setting."
            ),
            Car(
                brand="BMW", model="M5 Competition", year=2024, 
                transmission="Automatic", seats=5, fuel_type="Hybrid", 
                color="Black", category="Executive Class", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCl_pOmdSCsjozxzfFS_TJ9LmdAODguMH-gOGA1qFsi2CgT19BuoDyBANgo69nexTEpw5_FW37ZNVk8HyogJ7TtaZXnPe2lUHZuowqKjGMneadsxui4rvdH8bH8YNviq0uJAAccwdk8BxNAUXkNxrUhib_oLVNBsg1lbYjU8yLr1ugb7W65HidvGe9zchIzZAy7on9hDPSHvA4K9xapfwXkdm4ZxpU8BxcglGMywU84JBD_s8gCdSg6ydMOZBBJKGVmZ1kv4AuZDYWd", 
                daily_rate=12200, description="Sleek black executive sedan parked in front of a modern glass building."
            ),
            Car(
                brand="Mercedes-Benz", model="G63 AMG", year=2024, 
                transmission="Automatic", seats=5, fuel_type="Diesel", 
                color="White", category="Adventure Luxury", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuCuG44LK62Feck53AvJl9YqGcqnqJnQ1QKDq-vY1HGftpT8f73yQKWSzU9BuQqzDsuL9fN3KLCjWMwxwBXvoWo0RqGPsCjnxE_wPEcRNpsnhwh6AR9XoQ1ASwTGWbqZLL_OTlBnCuaXsPbzj5etdqOaBWj7YNEA2rR_QZeB0xYbas6jDyupn-Uz3hSRhlKN-DCx-Z6XcDlUpwrLWfDOemzkuhRO-I1FiYJZohkbPvUbZTBke4z_7tVaIsJ0LJibpXY4-XJcsEOZ-SqY", 
                daily_rate=24500, description="White luxury G-Wagon SUV in a mountain landscape."
            ),
            Car(
                brand="Land Rover", model="Range Rover Vogue", year=2024, 
                transmission="Automatic", seats=5, fuel_type="Diesel", 
                color="Santorini Black", category="Ultra Luxury", 
                image_url="https://lh3.googleusercontent.com/aida-public/AB6AXuDIn52qCE81mElTRCgQzknzwGJofZGQv22UqVxtNinYvGIS5HL38PXFo3KIrOmAwvWg3n5SV595AMquV8wMfJjwRkb26qQ84-jtvk4hxKjS7cWuUbUopojwrDFaJbw__xYf0ULaB6CGSISmEGFQzKf5Ui6qlFXyeuM-DWi_RDeVOGZyucGH-i76KqsE_mjpnT_-GKfxpUGnS4N2nbkuGNXXkkdDD_ahx4RM4NF1ZQYnFz9eoYIqmTgR-xnc7dXdwItxSa68DudUoGVt", 
                daily_rate=18500, description="The 2024 Range Rover Vogue represents the pinnacle of refined travel."
            ),
        ]

        addons = [
            AddOn(name="GPS Navigation", price_per_day=500, description="High-precision satellite navigation with live traffic updates."),
            AddOn(name="Comprehensive Insurance", price_per_day=1200, description="Full collision damage waiver and theft protection."),
            AddOn(name="Child Safety Seat", price_per_day=350, description="ISOFIX-compatible ergonomic safety seats."),
            AddOn(name="Roadside Assistance", price_per_day=250, description="24/7 emergency support, fuel delivery, and tire replacement."),
        ]

        db.session.add_all(cars)
        db.session.add_all(addons)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()

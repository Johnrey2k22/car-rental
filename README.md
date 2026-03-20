# Stitch Flask App

This project contains static UI pages in subfolders and now includes a Flask wrapper to serve them.

## Run locally

1. `cd stitch/stitch`
2. `python -m venv .venv`
3. `source .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Linux/macOS)
4. `pip install -r requirements.txt`
5. `python app.py`
6. Open http://127.0.0.1:5000/ in your browser

## Routes

- `/` => `driveease_home/code.html`
- `/home` => `driveease_home/code.html`
- `/admin_dashboard` => `admin_dashboard/code.html`
- `/admin_verification` => `admin_verification/code.html`
- `/booking_reservation` => `booking_reservation/code.html`
- `/car_detail` => `car_detail/code.html`
- `/car_listings` => `car_listings/code.html`
- `/payment_info` => `payment_info/code.html`
- `/renter_dashboard` => `renter_dashboard/code.html`

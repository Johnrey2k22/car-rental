import requests
import os
import json
import base64

class PayMongoService:
    BASE_URL = "https://api.paymongo.com/v1"

    def __init__(self, public_key=None, secret_key=None):
        self.public_key = public_key or os.environ.get('PAYMONGO_PUBLIC_KEY', 'pk_test_placeholder')
        self.secret_key = secret_key or os.environ.get('PAYMONGO_SECRET_KEY', 'sk_test_placeholder')

        auth_bytes = f"{self.secret_key}:".encode('ascii')
        self.auth_token = base64.b64encode(auth_bytes).decode('ascii')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth_token}"
        }

    def create_payment_link(self, amount, description, booking_id):
        return f"/payment/simulator/{booking_id}"

paymongo_service = PayMongoService()

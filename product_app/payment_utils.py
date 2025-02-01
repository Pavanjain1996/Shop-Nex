import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment_link(order):
    payment_link = client.payment_link.create({
        "amount": int(order.total_amount * 100),
        "currency": "INR",
        "description": "Order placed!",
        "customer": {
            "name": order.user.first_name + order.user.last_name,
            "email": order.user.email,
            "contact": order.user.phone_number
        },
        "callback_method": "get",
        "callback_url": "http://localhost:8000/payment/callback",
        "notify": {
            "sms": True,
            "email": True
        },
        "reference_id": str(order.id),
        "reminder_enable": True,
        "notes": {
            "Order ID": str(order.id),
            "Total Amount": int(order.total_amount * 100)
        }
    })
    return payment_link

def verify_payment(payment):
    try:
        response = client.utility.verify_payment_link_signature(payment)
    except razorpay.errors.SignatureVerificationError:
        response = False
    return response

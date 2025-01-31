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
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
        "notes": {
            "Order ID": str(order.id),
            "Total Amount": int(order.total_amount * 100)
        }
    })
    return payment_link
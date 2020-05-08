import random
import string
import stripe
from stripe import Customer
import settings

stripe.api_key = settings.development_settings.PINAX_STRIPE_SECRET_KEY


def randomDigits(digits):
    """ Return a number of size 'digits' generated randomly """
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)

def getPaymentProcessing():
    """ Get Payment Processing Number generated at random """

    letter_a = random.choice(string.ascii_letters)
    letter_b = random.choice(string.ascii_letters)
    prefix = (letter_a+letter_b).upper()
    suffix = str(randomDigits(6))

    ppn = prefix+suffix

    return ppn

def read_customer(customer_id):
    """ Read customer by customer id """
    stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY
    customer = stripe.Customer.retrieve(customer_id)
    return customer

def create_customer():
    """ """
    customer = stripe.Customer.create(
        source='tok_mastercard',
        email='paying.user@example.com',
    )
    return customer

def update_card():
    """ """


def add_card(card):
    """ """


def read_card(customer_id, card_id):
    """ Given customer id and card id, read the card """
    try:
        customer = stripe.Customer.retrieve(customer_id)
        card = customer.sources.retrieve(card_id)
        return card
    except Exception as e:
        return None

def save_card(card):
    """ """


def process_payment(token):
    # Charge the user's card:
    charge = stripe.Charge.create(
        amount=999,
        currency="usd",
        description="Example charge",
        source=token,
    )
    return charge

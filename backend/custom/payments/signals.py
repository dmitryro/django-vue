from django.dispatch import Signal

payment_send_confirmation_email = Signal(providing_args=["payment","user"])

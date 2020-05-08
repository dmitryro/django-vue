from django.dispatch import Signal

consult_send_confirmation_email = Signal(providing_args=["consult","user"])

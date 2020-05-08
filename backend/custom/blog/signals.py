from django.dispatch import Signal

new_post_created = Signal(providing_args=["user"])
post_edited = Signal(providing_args=["user"])
post_deleted = Signal(providing_args=["user"])
post_commented = Signal(providing_args=["user"])
post_flagged = Signal(providing_args=["user"])
post_upvoted = Signal(providing_args=["user"])
post_downvoted = Signal(providing_args=["user"])

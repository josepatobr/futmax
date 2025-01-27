from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import User


def send_email(user: User, subject: str, template: str, **kwargs):
    if not all(
        [isinstance(user, User), isinstance(subject, str), isinstance(template, str)]
    ):
        msg = "Invalid argument types. Expected (User, str, str)"
        raise TypeError(msg)

    context = {"user": user, "name": user.get_short_name()} | kwargs

    message = render_to_string(template, context)
    send_mail(
        subject=subject,
        message=message,
        html_message=message,
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
    )

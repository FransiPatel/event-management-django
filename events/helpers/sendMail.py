from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_registration_confirmation(user, event):
    try:
        subject = f"Event Registration Confirmation - {event.title}"

        context = {
            "user_name": f"{user.firstName} {user.lastName}",
            "event_title": event.title,
            "event_date": event.datetime.strftime("%Y-%m-%d %H:%M"),
            "event_venue": event.venue,
            "event_description": event.description,
        }

        html_message = render_to_string("registration_confirmation.html", context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return True
    except Exception as error:
        return f"Email send error: {error}"

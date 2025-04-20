from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_email(subject, template_name, context, user):
    email_body = render_to_string(template_name, context)
    try:
        email = EmailMultiAlternatives(subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return True
    except Exception as e:
        return False
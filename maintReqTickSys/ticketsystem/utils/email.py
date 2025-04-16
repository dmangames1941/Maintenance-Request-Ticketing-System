from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_html_email(subject, to_email, template, context):
    html_content = render_to_string(template, context)
    text_content = f"{subject}\n\nThis email requires HTML support."

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

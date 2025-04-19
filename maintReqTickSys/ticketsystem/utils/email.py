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
    # Prints the actual HTML to be sent in the email. This is to show that the content works and compiles, it just doesn't
    # send the email currently. If you want to test the email functionality, the settings.py will need to be reconfigured
    # with the SMTP server information.
    print("--------------------------------------------------")
    print(f"EMAIL SENT TO: {email.to[0]}\nEMAIL SENT FROM: {email.from_email}\nEMAIL SUBJECT: {email.subject}\n" +
          f"EMAIL BODY TEXT (non html): {email.body}")
    print(html_content)
    print("--------------------------------------------------")
    # email.send()  # Uncomment to actually send the email.

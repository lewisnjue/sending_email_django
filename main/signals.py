import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

# Set up logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def welcome(sender, instance, created, **kwargs):
    if not created:
        # Log the creation of a new user
        logger.info(f"New user created: {instance.username}")

        # Render HTML email template
        subject = 'Welcome to the site!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.email]
        text_content = 'Thank you for signing up.'
        html_content = render_to_string('email.html', {'user': instance})

        # Send email
        try:
            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()
            logger.info(f"Welcome email sent to {instance.email}")
        except Exception as e:
            logger.error(f"Error sending welcome email to {instance.email}: {e}")

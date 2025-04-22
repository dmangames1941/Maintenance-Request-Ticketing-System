from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Ticket, Comment
from ticketsystem.utils.email import send_html_email

print("📢 signals.py loaded")

# New Ticket Submitted → Notify assigned admin or all admins
@receiver(post_save, sender=Ticket)
def notify_admin_on_ticket_submission(sender, instance, created, **kwargs):
    if created and instance.submitter.userprofile.role == 'tenant':
        print("✅ Ticket Created Signal Triggered")

        # Send to specific assigned admin
        if instance.assigned_admin:
            print(f"📧 Sending email to assigned admin: {instance.assigned_admin.email}")
            send_html_email(
                subject=f"New Ticket Submitted: {instance.title}",
                to_email=instance.assigned_admin.email,
                template='emails/ticket_submitted.html',
                context={'ticket': instance}
            )
        else:
            # Send to all admins if no one is assigned
            print("📧 No assigned admin — notifying all admins")
            admin_emails = User.objects.filter(userprofile__role='admin').values_list('email', flat=True)
            for email in admin_emails:
                print(f"📧 Sending to: {email}")
                send_html_email(
                    subject=f"New Ticket Submitted: {instance.title}",
                    to_email=email,
                    template='emails/ticket_submitted.html',
                    context={'ticket': instance}
                )


# Ticket Updated → Notify tenant on assignment or status change
@receiver(pre_save, sender=Ticket)
def notify_tenant_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    # Detects if a skip flag was passed in, if so, skips this signal
    if getattr(instance, '_skip', False):
        return

    prev = Ticket.objects.get(pk=instance.pk)

    # Assigned admin changed
    if prev.assigned_admin != instance.assigned_admin and instance.assigned_admin:
        print(f"📧 Ticket Assigned → notifying tenant: {instance.submitter.email}")
        send_html_email(
            subject=f"Ticket Assigned: {instance.title}",
            to_email=instance.submitter.email,
            template='emails/ticket_assigned.html',
            context={'ticket': instance}
        )
        return # An admin being assigned is a different email than status/comment update

    # Comment Added to Ticket (Also reflects any status changes)
    comment = Comment.objects.filter(ticket_id=instance.id).last()
    # if prev.status != instance.status:
    print(f"📧 Ticket Status Changed/Comment added → notifying tenant: {instance.submitter.email}")
    # Checks if the comment has an image attached or not
    hasImage = False
    if comment.image:
        hasImage = True
    # Reformats the status change to display prettily on the email.
    ticket_status = "In Progress"
    if instance.status == "submitted":
        ticket_status = "Submitted"
    elif instance.status == "completed":
        ticket_status = "Completed"
    send_html_email(
        subject=f"Ticket Status Updated: {instance.title}",
        to_email=instance.submitter.email,
        template='emails/status_updated.html',
        context={'ticket': instance, 'ticket_status': ticket_status, 'comment_text': comment.content, 'hasImage': hasImage}
    )

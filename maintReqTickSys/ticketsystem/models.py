from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ROLE_CHOICES = [
        ('tenant', 'Tenant'),
        ('admin', 'Admin'),
    ]

    # admin or tenant?
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

    # Location details for TENANT ONLY (optional field)
    building_name = models.CharField(max_length=100, blank=True, null=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)

    # Employee ID for ADMINS ONLY (optional field)
    employee_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        if self.role == "tenant":
            return f"{self.username} - Apt {self.apartment_number or 'N/A'}, {self.building_name or ''}"
        return f"{self.username} (Admin)"

# -- User model --

# Django's built in User Model already stores username, email, password, first_name, and last_name
# class User(AbstractUser):
#     ROLE_CHOICES = [
#         ('tenant', 'Tenant'),
#         ('admin', 'Admin'),
#     ]
#     # admin or tenant?
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

#     # Location details for TENANT ONLY (optional field)
#     building_name = models.CharField(max_length=100, blank=True, null=True)
#     apartment_number = models.CharField(max_length=10, blank=True, null=True)

#     # Employee ID for ADMINS ONLY (optional field)
#     employee_id = models.CharField(max_length=100, blank=True, null=True)


#     #------- added due to SystemCheckError -----------
#     groups = models.ManyToManyField('auth.Group', related_name='user_groups', blank=True)
#     user_permissions = models.ManyToManyField('auth.Permission', related_name='user_permissions', blank=True)
#     #-------------------------------------------------

#     # Add word "Building"
#     def __str__(self):
#         if self.role == "tenant":
#             return f"{self.username} - Apt {self.apartment_number or 'N/A'}, {self.building_name or ''}"
#         return f"{self.username} (Admin)"


# -- Ticket Model --
class Ticket(models.Model):

    # add ticket ID?
    title = models.CharField(max_length=200)
    description = models.TextField()

    CATEGORY_CHOICES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('general', 'General'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    # ---------------------- Automate update of these fields --------------------
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(null=True, blank=True) # based on status
    # ---------------------------------------------------------------------------

    image = models.ImageField(upload_to='ticket_images/', null=True, blank=True)

    # Submitter: The user who submitted the ticket
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_tickets')

    # Assigned Admin: The admin assigned to the ticket
    assigned_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')

    def __str__(self):
        return f"Ticket: {self.title} (Status: {self.status})"

# -- Comment Model --
class Comment(models.Model):

    # add comment ID?
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    # The comment
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ticket.title} at {self.created_date}"
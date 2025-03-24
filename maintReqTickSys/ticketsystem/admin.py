from django.contrib import admin
from .models import User, Ticket, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Comment)
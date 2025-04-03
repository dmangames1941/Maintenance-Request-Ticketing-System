# Generated by Django 4.2.20 on 2025-03-26 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketsystem', '0002_ticket_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('tenant', 'Tenant'), ('admin', 'Admin')], default='tenant', max_length=10)),
                ('building_name', models.CharField(blank=True, max_length=100, null=True)),
                ('apartment_number', models.CharField(blank=True, max_length=10, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]

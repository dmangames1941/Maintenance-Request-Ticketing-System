# Generated by Django 4.2.20 on 2025-04-15 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketsystem', '0004_alter_comment_id_alter_ticket_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='comment_images/'),
        ),
    ]

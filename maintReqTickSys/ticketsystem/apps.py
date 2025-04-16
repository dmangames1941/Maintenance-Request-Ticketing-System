from django.apps import AppConfig

class TicketsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'ticketsystem'

    def ready(self):
        import ticketsystem.signals  # 👈 this line loads signals!

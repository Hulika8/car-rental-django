from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'
    
    def ready(self):
        """
        Called when Django starts
        Loads and activates signals
        """
        import reservations.signals
from django.apps import AppConfig


class JobproposalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'JobProposal'

# proposal/apps.py

class ProposalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proposal'

    def ready(self):
        import JobProposal.signals  # Import your signals.py file here

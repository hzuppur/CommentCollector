from django.core.management.base import BaseCommand, CommandError
from commentCollector.models import SavedComment


class Command(BaseCommand):
    # python manage.py add_articles_to_table
    help = 'Remove duplicates from saved coments'

    def handle(self, *args, **options):
        for row in SavedComment.objects.all():
            if "ĹÉÈXÍ.NÈŤ" in row.content or "M­­a­­g­­n­ifyIn­­c­­o­­m­e.C­OM":
                row.delete()


    def remove_duplicates(self):
        # assuming which duplicate is removed doesn't matter...
        for row in SavedComment.objects.all().reverse():
            if SavedComment.objects.filter(content=row.content).count() > 1:
                row.delete()

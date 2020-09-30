from django.core.management.base import BaseCommand, CommandError
import commentCollector.Utils.database_utils as db_util


class Command(BaseCommand):
  # python manage.py add_articles_to_table
  help = 'Adds all delfi front page articles to the database'

  def handle(self, *args, **options):
    #db_util.remove_old_articles()
    db_util.add_articles_to_table(False)
    self.stdout.write(self.style.SUCCESS('Successfully added comments to table'))

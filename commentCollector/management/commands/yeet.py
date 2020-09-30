from django.core.management.base import BaseCommand, CommandError
import commentCollector.Utils.database_utils as db_util
import commentCollector.Utils.delfi_comments as dc
import commentCollector.Utils.delfi_articles as da
import pprint
from commentCollector.models import Article, Comment, CommentReply, SavedComment
import time



class Command(BaseCommand):
  # python manage.py add_articles_to_table
  help = 'Yeet tuut Scuut'

  def handle(self, *args, **options):
    start = time.time()
    #db_util.add_articles_to_table(with_replys=False)
    #SavedComment.objects.all().delete()

    delta = round(time.time() - start, 2)
    self.stdout.write(self.style.SUCCESS(f'Successfully yeeted, time elapsed: {delta}s'))

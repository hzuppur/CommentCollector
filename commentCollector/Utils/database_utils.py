from commentCollector.models import Article, Comment, CommentReply, SavedComment
import commentCollector.Utils.delfi_articles as da
import commentCollector.Utils.delfi_comments as dc
from django.utils import timezone
import random


def add_articles_to_table(with_replys=True):
    # Get all delfi front page articles and iterate over them
    articles = da.get_front_page_articles()
    for d_article in articles:
        # Create new article and save it to the db
        article = Article(id=d_article["id"], name=d_article["name"], url=d_article["url"],
                          comments=d_article["comments"], pub_date=timezone.now())
        article.save()

    add_comments(with_replys)


def add_comments(with_replys=False):
    articles = Article.objects.all()
    comments_found_ids = []

    for article in articles:
        # Get all comments for that article and iterate over them
        comments = dc.get_all_comments(article.id, with_replies=with_replys)

        # Add comments to db
        for d_comment in comments:
            # Check if comment has content and subject and save comment
            if d_comment["subject"] is not None and d_comment["content"]:
                comment, created = Comment.objects.get_or_create(id=d_comment["id"], article=article,
                                                                 content=d_comment["content"],
                                                                 subject=d_comment["subject"])

            # If comment has reply´s, add them to the reply table
            if with_replys and d_comment["replies"] is not None:
                for d_reply in d_comment["replies"]:
                    reply, created = CommentReply.objects.get_or_create(comment=comment, content=d_reply["content"],
                                                                        subject=d_reply["subject"])
        comments_found_ids.extend([i["id"] for i in comments])

    # Add removed comments to SavedComments
    find_removed_comments(comments_found_ids)


def remove_old_articles():
    articles = Article.objects.all()
    for article in articles:
        if not article.was_published_recently():
            article.delete()


def get_random_comment():
    comments = []
    # Loop while we get article with atleast 1 comment
    while len(comments) == 0:
        article = random.choice(Article.objects.all())
        comments.extend(article.comment_set.all())
    return random.choice(comments), article


def find_removed_comments(added_comments):
    # Query all comments from the db and find the comments that are in the db and not in queried comments
    # This means that the comment was removed from Delfi
    r_comments = set([i.id for i in Comment.objects.all()]).difference(set(added_comments))
    added_comment_amount = 0
    # Iterate over all of the removed comments and create new SavedComment object if it does not exist
    for r_comment in r_comments:
        r_comment_db = Comment.objects.filter(id=r_comment).first()
        r_comment_db.set_removed(True).save()
        comment, created = SavedComment.objects.get_or_create(id=r_comment_db.id, article=r_comment_db.article.name,
                                                              content=r_comment_db.content,
                                                              subject=r_comment_db.subject, removed=True)
        if created: added_comment_amount += 1
    # For each removed comment, add one not removed comment to SaveComments
    # In this way, we have a balanced dataset
    not_r_comments = list(Comment.objects.filter(removed=False).all())
    while added_comment_amount > 0:
        comment = not_r_comments.pop(random.randrange(len(not_r_comments)))

        comment, created = SavedComment.objects.get_or_create(id=comment.id, article=comment.article.name,
                                                              content=comment.content,
                                                              subject=comment.subject, removed=False)
        if created: added_comment_amount -= 1

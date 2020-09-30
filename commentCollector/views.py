from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from commentCollector.models import Article, Comment, SavedComment
import commentCollector.Utils.database_utils as db_util

def index(request):
    return render(request, 'index.html')

def articles(requests):
    context = {"articles": Article.objects.order_by("comments").reverse(),}
    return render(requests, "articles.html", context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
        'comments': article.comment_set.all().prefetch_related('commentreply_set'),
    }

    return render(request, 'detail.html', context)


def all_comments(request):
    context = {'comments': Comment.objects.order_by("removed").reverse()}

    return render(request, 'all_comments.html', context)

def saved_comments(request):
    context = {'comments': SavedComment.objects.order_by("removed").reverse()}

    return render(request, 'save_comments.html', context)

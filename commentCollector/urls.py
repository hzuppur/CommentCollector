from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.articles, name='comments'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('allComments/', views.all_comments, name='all_comments'),
    path('savedComments/', views.saved_comments, name='saved_comments'),
]

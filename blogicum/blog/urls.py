from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.create_post, name='edit_post'),
    path(
        'posts/<int:pk>/delete/',
         views.delete_post,
         name='delete_post',
    ),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path(
        'posts/<int:post_pk>/edit_comment/<int:comment_pk>/',
        views.edit_comment,
        name='edit_comment',
    ),
    path(
        'posts/<int:post_pk>/delete_comment/<int:comment_pk>/',
         TemplateView.as_view(),
         name='delete_comment',
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts',
    ),
]

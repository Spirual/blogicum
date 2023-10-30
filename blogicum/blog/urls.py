from django.urls import path, include

from . import views

app_name = 'blog'

post_urls = [
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path(
        '<int:pk>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post',
    ),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path(
        '<int:pk>/edit_comment/<int:comment_pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment',
    ),
    path(
        '<int:pk>/delete_comment/<int:comment_pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'profile/edit/',
        views.ProfileEditUpdateView.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<str:username>/',
        views.ProfileListView.as_view(),
        name='profile',
    ),
    path('posts/', include(post_urls)),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts',
    ),
]

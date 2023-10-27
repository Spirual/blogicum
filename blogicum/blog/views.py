from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Post, Category

POSTS_ON_MAIN_PAGE = 5

User = get_user_model()


def get_post_base():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
    ).select_related(
        'location',
        'category',
        'author',
    )


def index(request):
    template = 'blog/index.html'
    post_list = get_post_base()[:POSTS_ON_MAIN_PAGE]
    context = {'page_obj': post_list}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username,
    )
    post_list = Post.objects.filter(
        author=profile,
    )
    context = {
        'page_obj': post_list,
        'profile': profile,
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_post_base(),
        pk=id,
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_post_base().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)

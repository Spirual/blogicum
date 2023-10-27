from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic import CreateView
from django.urls import reverse_lazy

from blog.models import Post, Category
from blog.forms import PostForm, UserForm

POSTS_ON_MAIN_PAGE = 10

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
    posts = get_post_base()
    paginator = Paginator(posts, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(
        User,
        username=username,
    )
    posts = get_post_base().filter(
        author=profile,
    )
    paginator = Paginator(posts, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
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
    posts = get_post_base().filter(category=category)
    paginator = Paginator(posts, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def create_post(request, pk=None):
    author = request.user
    if pk is not None:
        instance = get_object_or_404(Post, pk=pk)
    else:
        instance = None
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance,
    )
    context = {'form': form}
    if form.is_valid():
        post = form.save(commit=False)
        post.author = author
        post.save()
        return redirect('blog:profile', username=author.username)
    return render(request, 'blog/create.html', context)


@login_required
def edit_profile(request):
    form = UserForm()
    context = {'form': form}
    return render(request, 'blog/user.html', context)

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.forms import CommentsForm, PostForm, UserForm
from blog.models import Category, Comments, Post

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
    ).annotate(
        comment_count=Count('comments'),
    ).order_by('-pub_date')


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
    posts = Post.objects.filter(
        author=profile,
    ).select_related(
        'location',
        'category',
        'author',
    ).annotate(
        comment_count=Count('comments'),
    ).order_by('-pub_date')
    paginator = Paginator(posts, POSTS_ON_MAIN_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'profile': profile,
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=pk,
    )
    if post.author != request.user:
        post = get_object_or_404(
            get_post_base(),
            pk=pk,
        )
    form = CommentsForm(request.POST or None)
    context = {
        'post': post,
        'form': form,
        'comments': post.comments.all(),
    }
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
def delete_post(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/create.html', context)


@login_required
def edit_profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    context = {'form': form}
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)
    return render(request, 'blog/user.html', context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(get_post_base(), pk=pk)
    form = CommentsForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    instance = get_object_or_404(Comments, pk=comment_pk)
    form = CommentsForm(request.POST or None, instance=instance)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)
    context = {'form': form, 'comment': instance}
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, comment_pk):
    instance = get_object_or_404(Comments, pk=comment_pk)
    form = CommentsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=post_pk)
    return render(request, 'blog/comment.html', context)

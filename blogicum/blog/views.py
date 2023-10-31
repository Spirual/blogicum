from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from blog.forms import CommentsForm, PostForm, UserForm
from blog.models import Category, Comments, Post

POSTS_ON_PAGE = 10

User = get_user_model()


def get_post_base(filtering=False, annotate=False):
    post = Post.objects.select_related(
        'location',
        'category',
        'author',
    )

    if filtering:
        post = post.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )

    if annotate:
        post = post.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    return post


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = POSTS_ON_PAGE
    queryset = get_post_base(filtering=True, annotate=True)


class ProfileListView(ListView):
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        username = self.kwargs.get('username')
        self.profile = get_object_or_404(User, username=username)
        if self.profile == self.request.user:
            queryset = get_post_base(annotate=True)
        else:
            queryset = get_post_base(filtering=True, annotate=True)
        queryset = queryset.filter(author=self.profile)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile

        return context


class ProfileEditUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=pk,
    )

    is_post_hidden = not post.is_published
    is_category_hidden = not post.category.is_published
    is_post_in_future = post.pub_date > timezone.now()

    if post.author != request.user and any(
        [
            is_post_hidden,
            is_category_hidden,
            is_post_in_future,
        ]
    ):
        raise Http404()

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
    posts = get_post_base(
        filtering=True,
        annotate=True
    ).filter(category=category)
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, template, context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class PostMixinView(LoginRequiredMixin, View):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class EditPostView(PostMixinView, UpdateView):
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class DeletePostView(PostMixinView, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', kwargs={'username': username})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(
        get_post_base(filtering=True, annotate=True),
        pk=pk)
    form = CommentsForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentMixinView(LoginRequiredMixin, View):
    model = Comments
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('blog:post_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context


class CommentUpdateView(CommentMixinView, UpdateView):
    form_class = CommentsForm


class CommentDeleteView(CommentMixinView, DeleteView):
    pass

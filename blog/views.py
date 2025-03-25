from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import PostForm, CommentForm

from django.views.decorators.http import require_POST
# Create your views here.


def post_list(request):
    all_posts = Post.published.all()

    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts
    }
    return render(request,
                  'blog/post/list.html',
                  context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post, slug=slug)

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request,
                  'blog/post/detail.html',
                  context)


def create_post(request):
    context = {}
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_list')
        else:
            context['form'] = form
            return render(request, 'blog/post/create.html', context)
    context['form'] = form
    return render(request, 'blog/post/create.html', context)


@require_POST
def post_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    context = {
        'post': post,
        'form': form
    }
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        context['comment'] = comment

    return render(request, 'blog/post/comment.html', context)

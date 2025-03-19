from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.


def post_list(request):
    posts = Post.published.filter(author=request.user)

    context = {
        'posts': posts
    }
    return render(request,
                  'blog/post/list.html',
                  context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post, slug=slug, author=request.user)
    context = {
        'post': post
    }
    return render(request,
                  'blog/post/detail.html',
                  context)

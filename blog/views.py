from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import PostForm
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
    context = {
        'post': post
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

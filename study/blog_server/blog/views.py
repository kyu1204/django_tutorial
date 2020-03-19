from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog


def home(request):
    blogs = Blog.objects
    return render(request=request, template_name='blog/home.html', context={'blogs': blogs})


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request=request, template_name='blog/detail.html', context={'blog': blog_detail})


def new_post(request):
    return render(request=request, template_name='blog/new.html')


def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.content = request.GET['body']
    blog.published = timezone.datetime.now()
    blog.save()

    return redirect('/blog/'+str(blog.id))

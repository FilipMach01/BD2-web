from django.shortcuts import render
from .models import Post


def index(request):
    recent_posts_count = Post.objects.filter(type__in=['urgent', 'info', 'notice']).count()
    return render(request, 'index.html', {
        'active_page': 'index',
        'recent_posts_count': recent_posts_count,
    })


def nastenka(request):
    posts = Post.objects.all()
    return render(request, 'nastenka/nastenka.html', {
        'active_page': 'nastenka',
        'posts': posts,
    })


def kontakty(request):
    return render(request, 'kontakty.html', {
        'active_page': 'kontakty',
    })


def zakladni_info(request):
    latest_post = Post.objects.order_by('-created_at').first()
    return render(request, 'zakladni-info.html', {
        'active_page': 'zakladni-info',
        'latest_post': latest_post,
    })

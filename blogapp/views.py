from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post


# ---------- AUTH ---------- #

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')

        if pwd1 != pwd2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        User.objects.create_user(username=uname, email=email, password=pwd1)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- BLOG ---------- #

@login_required(login_url='login')
def home(request):
    q = request.GET.get('search', '')
    posts = Post.objects.filter(title__icontains=q).order_by('-date_posted')
    return render(request, 'home.html', {
        'posts': posts,
        'query': q
    })


@login_required(login_url='login')
def new_post(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            image=request.FILES.get('image'),
            author=request.user
        )
        messages.success(request, "Post created successfully")
        return redirect('profile')

    return render(request, 'newpost.html')


@login_required(login_url='login')
def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog_detail.html', {'post': post})


@login_required(login_url='login')
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post")
        return redirect('home')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()
        messages.success(request, "Post updated")
        return redirect('profile')

    return render(request, 'editpost.html', {'post': post})


@login_required(login_url='login')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this post")
        return redirect('home')

    post.delete()
    messages.success(request, "Post deleted")
    return redirect('profile')


# ---------- PROFILE (PROFILE + MY POSTS MERGED) ---------- #

@login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'profile.html', {
        'posts': posts
    })

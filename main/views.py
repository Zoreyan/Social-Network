from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q


# Login Page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'main/login.html', context)

# Register Page
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'main/register.html', {'form': form})

# Logout User
def logoutUser(request):
    logout(request)
    return redirect('home')

# Check User Name
def check_name(request):
    username = request.GET.get('name')
    response = {
        'is_taken': User.objects.filter(name__iexact=username).exists()
    }
    return JsonResponse(response)

# Home Page
@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    posts = Post.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q)
    )
    if request.method == 'POST' and 'like' in request.POST:
        like = request.POST.get('like')
        post = Post.objects.get(id=like)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except:
            Like.objects.create(user = request.user, post=post)

    post_count = posts.count()
    likes = {}

    for i in posts:
        if not Like.objects.filter(user = request.user, post = i):
            likes[i] = False
        else:
            likes[i] = True


    context = {'posts': posts,
               'post_count': post_count,
               'likes':likes,
               }
    return render(request, 'main/home.html', context)

# Create Post Page
@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/create_post.html', context)

# Update Post Page
@login_required(login_url='login')
def updatePost(request, pk):
    page = 'update'
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/create_post.html', context)

# User Page
@login_required(login_url='login')
def userProfile(request, slug):
    users = User.objects.all()
    user = User.objects.get(name=slug)
    if request.method == 'POST' and 'follow' in request.POST:
        try:
            follow = Subscriber.objects.get(user=user, name=request.user)
            follow.delete()
        except:
            Subscriber.objects.create(user=user, name=request.user)
    posts = user.post_set.filter(user=user)
    total_posts = posts.count()
    total_subscribers = user.subscriber_set.filter(user=user).count()
    subscribers = user.subscriber_set.filter(user=user)
    user_subs = Subscriber.objects.filter(user = user)
    subscribes = Subscriber.objects.filter(name=user)
    total_subscribes = subscribes.count()
    subscribe = {}

    for i in users:
        if not Subscriber.objects.filter(name = request.user, user = i):
            subscribe[i] = False
        else:
            subscribe[i] = True
    context = {'user': user,
               'posts': posts,
               'mysubscribes':subscribes,
               'total_subscribes':total_subscribes,
               'total_subscribers':total_subscribers,
               'subscribers':subscribers,
               'total_posts':total_posts,
               'all_subs':user_subs,
               'subscribe':subscribe}
    return render(request, 'main/profile.html', context)

# Favorite Posts Page
@login_required(login_url='login')
def favoritePost(request, slug):
    posts = Post.objects.all()
    user = User.objects.get(name=slug)
    my_likes = Like.objects.filter(user__name=user.name)
    if request.method == 'POST' and 'like' in request.POST:
        like = request.POST.get('like')
        post = Post.objects.get(id=like)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except:
            Like.objects.create(user = request.user, post=post)
        return redirect('favorite', slug=user.name)
    likes = {}

    for i in posts:
        if not Like.objects.filter(user = request.user, post = i):
            likes[i] = False
        else:
            likes[i] = True
    return render(request, 'main/favorite.html', {'my_likes': my_likes, 'likes':likes})

# Update User Page
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=user.name)

    return render(request, 'main/update_user.html', {'form': form})

# Delete Post
@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('home')

# Post Detail Page
@login_required(login_url='login')
def postDetail(request, pk):
    post = Post.objects.get(id=pk)
    related_posts = Post.objects.filter(Q(title__contains=post.title))
    comments = post.comment_set.all()
    total_comments = comments.count()
    form = CommentForm()
    if request.method == 'POST' and request.is_ajax():
        form = CommentForm(request.POST)
        form.instance.user = request.user
        form.instance.post = post
        if form.is_valid():
            form.save()
            
    context = {'post': post,
                'comments':comments, 'form': form,
                'total_comments':total_comments,
                'related_posts':related_posts}
    return render(request, 'main/post_detail.html', context)

# Delete Comment
@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return redirect('post', pk=comment.post.id)

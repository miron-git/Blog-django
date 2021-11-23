from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/index.html", {'paginator': paginator, 'page': page})


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 5) # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, "posts/group.html", {"group": group, "page": page, 'paginator': paginator})

@login_required
def new_post(request):
    #добавить новую запись, если пользователь известен
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('new_post')
        return render(request, 'posts/post_new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/post_new.html', {'form': form})
    

   
@login_required
def profile(request, username):
    #проверка существует ли username
    if User.objects.filter(username=username).exists():
        post_list = Post.objects.filter(author__username=username).order_by("-pub_date").all()
        count_post = Post.objects.filter(author__username=username).all().count() #колличество постов
        author = User.objects.get(username=username)

        following = Follow.objects.filter(user=request.user, author=author)
        subscription = Follow.objects.filter(author__username=username)
        subscribe = Follow.objects.filter(user__username=username)

        paginator = Paginator(post_list, 5)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        contex = {'page': page, 'paginator': paginator, 'post_list': post_list, 'username': username,
        'count_post': count_post,
        'following': following,'subscription': subscription, 'subscribe': subscribe, 'author': author}
        return render(request, 'posts/profile.html', contex)
    else:
        return redirect('index')



@cache_page(3)  #кеширование 
@login_required
def post_view(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id)
    count_post = Post.objects.filter(author__username=username).all().count()
    form = CommentForm()
    items = post.comments.order_by('-created').all()
    author = User.objects.get(username=username)
    subscription = Follow.objects.filter(author__username=username)
    subscribe = Follow.objects.filter(user__username=username)

    return render(request, 'posts/post_view.html', {'post': post, 'username': username, 'count_post': count_post, 'form': form, 'items': items, 
    'author': author, 'subscription': subscription, 'subscribe': subscribe})


@login_required
def post_edit(request, post_id, username):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)

    return render(request, 'posts/post_new.html', {'form': form, 'post': post})


@login_required
def  add_comment(request, post_id, username):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post 
            comment.author = request.user
            comment.save()
            return redirect('post', post_id=post_id, username=username)
    else:
        form = CommentForm()
    return render(request, 'posts/comments.html', {'form': form})


@login_required
def follow_index(request):
    user_list = User.objects.get(pk=request.user.id).follower.all().values('author')
    post_list = Post.objects.filter(author__in=user_list)
    return render(request, "posts/follow.html", {'post_list': post_list})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    follow = Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    follow = Follow.objects.filter(user=request.user, author=author)
    follow.delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)











# def post_edit(request, post_id, username):
#     post = get_object_or_404(Post, id=post_id)
#     if request.method == 'GET':
#         if request.user != post.author:
#             return redirect('post', post_id=post.id, username=username) #переадресация на post_view(name=post)
#         # добавим в form свойство files
#         form = PostForm(instance=post) 

#     if request.method == 'POST':
#         form = PostForm(request.POST, files=request.FILES or None, instance=post)
#         if form.is_valid():
#             form.save()
#         return redirect('post', post_id=post.id, username=username) #переадресация на post_view(name=post)
#     return render(request, 'posts/post_new.html', {'form': form, 'post': post})

    


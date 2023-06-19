#dio koda preuzet sa https://youtu.be/WuyKxdLcw3w

from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm, CreateGroupForm, DeleteGroupForm, AddRemoveUserForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from .models import UserAction, Post
from django.db.models import Count, Avg
from django.views import View
from django.contrib import messages

# Create your views here.

@user_passes_test(lambda u: u.is_staff)
def admin_stats(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    if user_count > 0:  #ne dijeli s nulom
        avg_posts_per_user = post_count / user_count
    else:
        avg_posts_per_user = 0
    avg_posts_per_user = round(avg_posts_per_user, 2)
    # User activity information
    users = User.objects.annotate(num_posts=Count('post')).all()
    # Post statistics
    posts = Post.objects.all()
    # Group statistics
    groups = Group.objects.annotate(num_users=Count('user')).all()
    return render(request, 'main/admin_stats.html', {
        'user_count': user_count,
        'post_count': post_count,
        'avg_posts_per_user': avg_posts_per_user,
        'users': users,
        'posts': posts,
        'groups': groups,
    })

@user_passes_test(lambda u: u.is_staff)
def admin_user_actions(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    actions = UserAction.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'main/admin_user_actions.html', {'actions': actions, 'username': username})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            UserAction.objects.create(user=request.user, action_type='POST')
            return redirect("/home")
    else:
        form = PostForm()
    return render(request, 'main/create_post.html', {"form": form})

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    banned_users = User.objects.filter(groups__name__in=['Banned', 'Bannedmoderator'])
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        ban_user_id = request.POST.get("ban-user-id")
        unban_user_id = request.POST.get("unban-user-id")
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                    #UserAction.objects.create(user=request.user, action_type='DELETE', target_post=post, deleted_post_author=post.author.username)
                    #UserAction.objects.create(user=request.user, action_type='DELETE', target_post=post)
                    UserAction.objects.create(user=request.user, action_type='DELETE', target_user=post.author)
                    post.delete()
        elif ban_user_id:
            user = User.objects.filter(id=ban_user_id).first()
            if user and request.user.is_staff:
                if user.groups.filter(name='Moderator').exists():
                    try:
                        group = Group.objects.get(name='Moderator')
                        group.user_set.remove(user)
                        group = Group.objects.get(name='Bannedmoderator')
                        group.user_set.add(user)
                        UserAction.objects.create(user=request.user, action_type='BANNED', target_user=user)
                    except:
                        pass
                else:
                    try:
                        group = Group.objects.get(name=user.groups.first().name)
                        group.user_set.remove(user)
                        group = Group.objects.get(name='Banned')
                        group.user_set.add(user)
                        UserAction.objects.create(user=request.user, action_type='BANNED', target_user=user)
                    except:
                        pass
        elif unban_user_id:
            user = User.objects.filter(id=unban_user_id).first()
            if user and request.user.is_staff:
                if user.groups.filter(name='Banned').exists():
                    try:
                        group = Group.objects.get(name='Banned') 
                        group.user_set.remove(user)
                        group = Group.objects.get(name='Registrirani')
                        group.user_set.add(user)
                        UserAction.objects.create(user=request.user, action_type='UNBANNED', target_user=user)
                    except:
                        pass
                elif user.groups.filter(name='Bannedmoderator').exists():
                    try:
                        group = Group.objects.get(name='Bannedmoderator')
                        group.user_set.remove(user)
                        group = Group.objects.get(name='Moderator')
                        group.user_set.add(user)
                        UserAction.objects.create(user=request.user, action_type='UNBANNED', target_user=user)
                    except:
                        pass
    return render(request, 'main/home.html', {"posts": posts, "banned_users": banned_users})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})


class UserGroupsView(View):
    def get(self, request):
        groups = Group.objects.all()
        users = User.objects.all()
        create_group_form = CreateGroupForm()
        add_remove_user_form = AddRemoveUserForm()
        delete_group_form = DeleteGroupForm()
        return render(request, 'main/user_groups.html', {
            'groups': groups,
            'users': users,
            'create_group_form': create_group_form,
            'add_remove_user_form': add_remove_user_form,
            'delete_group_form': delete_group_form
        })
    def post(self, request):
        create_group_form = CreateGroupForm(request.POST)
        add_remove_user_form = AddRemoveUserForm(request.POST)
        #delete_group_form = DeleteGroupForm(request.POST)
        if create_group_form.is_valid():
            # Create new group
            group_name = create_group_form.cleaned_data.get('group_name')
            Group.objects.create(name=group_name)
        
        if add_remove_user_form.is_valid():
            # Add/remove users to/from group
            add_user = add_remove_user_form.cleaned_data.get('add_user')
            group_remove = add_user.groups.first() # get the first (and only) group of the user
            group_add = add_remove_user_form.cleaned_data.get('group')
            if add_user and group_add != group_remove: # check if user is already in the group
                group_add.user_set.add(add_user)
                if group_remove: # Check if there's a group to remove the user from
                    group_remove.user_set.remove(add_user)

        return redirect('main:user_groups')
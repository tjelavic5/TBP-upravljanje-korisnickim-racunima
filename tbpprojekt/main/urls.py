#dio koda preuzet sa https://youtu.be/WuyKxdLcw3w

from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test
from .views import UserGroupsView

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    path('admin_stats', views.admin_stats, name='admin_stats'),
    path('admin_stats/user/<str:username>/', views.admin_user_actions, name='admin_user_actions'),
    path('user_groups/', user_passes_test(lambda u: u.is_staff)(UserGroupsView.as_view()), name='user_groups'),
]
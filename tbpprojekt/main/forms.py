#dio koda preuzet sa https://youtu.be/WuyKxdLcw3w

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=80)

class DeleteGroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all())

class AddRemoveUserForm(forms.Form):
    add_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    #remove_user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
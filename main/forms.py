from django.forms import ModelForm, CharField, PasswordInput, EmailInput, TextInput, Textarea, FileInput
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CreateUserForm(UserCreationForm):
    name = CharField(widget=TextInput(attrs={
        'class': 'form-control',
                'type': 'name',
                'placeholder': '@Name',
                'aria-describedby': 'basic-addon1',
                'name': 'name',
                'id': 'name'
    }))

    username = CharField(widget=TextInput(attrs={
                'class': 'form-control',
                'type': 'name',
                'placeholder': 'Username',
                'aria-describedby': 'basic-addon1'
            }))
    email = CharField(widget=EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Email@example.com',
                'aria-describedby': 'basic-addon2'
            }))
    password1 = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
                'type': 'password',
                'placeholder': 'Password',
                'for': 'form3Example4c'
    }))
    password2 = CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
                'type': 'password',
                'placeholder': 'Password',
                'for': 'form3Example4c'
    }))
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'image', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',

            }),
            'description': Textarea(attrs={
                'class': 'form-control form-control-lg',
                'type': 'text',

            }),
            'image': FileInput(attrs={
                'type': 'file',
                'class': 'form-control',

            }),
        }


class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={
                'value':'',
                'class':'form-control',
                'id':'comment_input'
            })
        }
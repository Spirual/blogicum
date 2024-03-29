from django import forms
from django.contrib.auth import get_user_model

from .models import Comments, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local'},
            )
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'email'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

from django import forms

from blog.models import Blog, Comment, Categories, Tag


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'text', 'image']


class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['category']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

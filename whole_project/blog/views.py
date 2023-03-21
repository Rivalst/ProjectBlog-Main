from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator

from .models import Blog, Tag, Categories
from .forms import BlogForm, CategoriesForm, TagForm, CommentForm

from datetime import datetime


class BlogAllView(View):
    def get(self, request):
        blog_list = Blog.objects.all()
        paginator = Paginator(blog_list, 10)
        page = request.GET.get('page')
        blogs = paginator.get_page(page)

        context = {
            'blogs': blogs,
        }

        return render(request, 'blog/blog_all.html', context=context)


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    fields = ['title', 'text', 'image']
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        tags = self.request.POST.get('tags').split(',')
        for tag in tags:
            if tag.strip():
                tag_object, _ = Tag.objects.get_or_create(tag=tag.strip())
                tag_object.blog.add(self.object)

        category = self.request.POST.get('category').strip()
        category_object, _ = Categories.objects.get_or_create(category=category)
        category_object.blog.add(self.object)

        messages.success(self.request, 'Blog create')
        return response


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()

            messages.success(request, 'Comment successful add')
            return redirect('blog-detail', pk=blog.pk)

        comments = blog.comments.all()

        return self.render_to_response(self.get_context_data(blog=blog, comments=comments, form=form))


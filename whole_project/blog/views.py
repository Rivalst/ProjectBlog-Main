from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views import generic
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.core.paginator import Paginator

from django.db.models import Q

from .models import Blog, Tag, Categories, Like
from .forms import CommentForm

from home.views import HomeView
from weather.utils import WeatherData

from datetime import datetime

User = get_user_model()
home_view = HomeView()
weather_view = WeatherData()


# ----- Blogs CRUD -----
class BlogAllView(View):
    def get(self, request):
        blog_list = Blog.objects.all()
        paginator = Paginator(blog_list, 10)
        page = request.GET.get('page')
        blogs = paginator.get_page(page)

        home_context = home_view.get_context_data()
        weather = weather_view.get_weather_data()

        context = {
            'blogs': blogs,
            'right_bar': home_context,
            'weather': weather,
        }

        query = self.request.GET.get('q')
        if query:
            context['blogs'] = Blog.objects.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query))
            context['q'] = query

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
        context['comments'] = self.get_object().comments.all()
        context['like_count'] = self.get_object().likes.count
        context['right_bar'] = home_view.get_context_data()
        context['weather'] = weather_view.get_weather_data()
        if self.request.user.is_authenticated:
            context['is_liked'] = self.get_object().likes.filter(user=self.request.user).exists()
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

        if 'like' in request.POST:
            like, create = Like.objects.get_or_create(blog=blog, user=self.request.user)
            if not create:
                like.delete()
            return redirect('blog-detail', pk=blog.pk)

        return self.render_to_response(
            self.get_context_data(blog=blog, form=form))


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('home')
    fields = ['title', 'text', 'image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.tag.all()
        context['category'] = self.object.category.all()
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['title'] = self.object.title
        initial['text'] = self.object.text
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user

        tags = self.request.POST.get('tags').split(',')
        for tag in tags:
            if tag.strip():
                tag_object, _ = Tag.objects.get_or_create(tag=tag.strip())
                tag_object.blog.add(self.object)

        category = self.request.POST.get('category').strip()
        category_object, _ = Categories.objects.get_or_create(category=category)
        category_object.blog.add(self.object)

        form.instance.updated_at = datetime.now()

        messages.success(self.request, 'Stand successful update')
        return super().form_valid(form)


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('profile')
    context_object_name = 'blog'


# ----- End Blogs CRUD -----


class BlogLikesView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_likes.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = self.get_object().likes.order_by('-id')
        return context


# ----- View for Tags -----
class BlogAllTagView(generic.ListView):
    model = Tag
    template_name = 'blog/blog_tag_all.html'
    context_object_name = 'tag'

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            return queryset.filter(Q(tag__icontains=query))

        return queryset.order_by('-id')


class BlogTagDetailView(generic.DetailView):
    model = Tag
    template_name = 'blog/blog_tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_tags'] = Blog.objects.filter(tag=self.object)

        query = self.request.GET.get('q')
        if query:
            context['blog_tags'] = context['blog_tags'].filter(
                Q(title__icontains=query) | Q(author__username__icontains=query))
            context['q'] = query

        return context


# ----- End View for Tags -----

# ----- View for Categories -----

class BlogCategoryAllView(generic.ListView):
    model = Categories
    template_name = 'blog/blog_category_all.html'
    context_object_name = 'category'

    def get_queryset(self):
        queryset = super().get_queryset()

        query = self.request.GET.get('q')
        if query:
            return queryset.filter(Q(category__icontains=query))

        return queryset.order_by('-id')


class BlogCategoryDetailView(generic.DetailView):
    model = Categories
    template_name = 'blog/blog_category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_categories'] = Blog.objects.filter(category=self.object)

        query = self.request.GET.get('q')
        if query:
            context['blog_categories'] = context['blog_categories'].filter(
                Q(title__icontains=query) | Q(author__username__icontains=query))
            context['q'] = query

        return context


class NotWork(generic.TemplateView):  # View for empty page
    template_name = 'notwork.html'

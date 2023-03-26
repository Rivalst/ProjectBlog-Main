from django.shortcuts import render
from django.views import View

from django.db.models import Q, Count

from weather.utils import WeatherData
from blog.models import Blog, Tag, Categories

from datetime import datetime
import random


class HomeView(View):

    def get(self, request):
        weather_view = WeatherData()
        weather = weather_view.get_weather_data()  # get context for weather

        model_blog_recent = Blog.objects.order_by('-id')[:5]
        model_blog = random.sample(list(Blog.objects.all()), min(5, len(list(Blog.objects.all()))))  # get random blogs
        model_blog_top_likes = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

        model_tag_recent = Tag.objects.order_by('-id')[:5]
        model_tag = random.sample(list(Tag.objects.all()), min(5, len(list(Tag.objects.all()))))  # get random tags

        model_category_recent = Categories.objects.order_by('-id')[:5]
        model_category = random.sample(list(Categories.objects.all()),
                                       min(5, len(list(Categories.objects.all()))))  # get random categories

        context = {
            'weather': weather,
            'date_now': datetime.now(),
            'model_blog': model_blog,
            'model_blog_recent': model_blog_recent,
            'model_blog_top_likes': model_blog_top_likes,
            'model_tag': model_tag,
            'model_category': model_category,
        }

        query = self.request.GET.get('q')  # search for blogs
        if query:
            context['model_blog'] = Blog.objects.filter(
                Q(title__icontains=query) | Q(author__username__icontains=query))
            context['q'] = query

        return render(request, 'home.html', context=context)

    # method for transfer data
    @staticmethod
    def get_context_data():
        model_tag = random.sample(list(Tag.objects.all()), min(5, len(list(Tag.objects.all()))))

        model_category = random.sample(list(Categories.objects.all()), min(5, len(list(Categories.objects.all()))))

        model_blog_recent = Blog.objects.order_by('-id')[:5]
        model_blog = random.sample(list(Blog.objects.all()), min(5, len(list(Blog.objects.all()))))

        context = {
            'model_tag': model_tag,
            'model_category': model_category,
            'model_blog_recent': model_blog_recent,
            'model_blog': model_blog,
        }

        return context

from django.urls import path
from . import views

urlpatterns = [
    path('blog-all/', views.BlogAllView.as_view(), name='blog-all'),
    path('blog-create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('blog-detail/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
]
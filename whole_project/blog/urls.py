from django.urls import path
from . import views

urlpatterns = [
    path('blog-all/', views.BlogAllView.as_view(), name='blog-all'),
    path('blog-create/', views.BlogCreateView.as_view(), name='blog-create'),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog-update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog-update'),
    path('blog-delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog-delete'),
    path('blog-likes/<int:pk>/', views.BlogLikesView.as_view(), name='blog-likes'),

    path('blog-don\'t-work', views.NotWork.as_view(), name='not-work'),  # path for empty page
]

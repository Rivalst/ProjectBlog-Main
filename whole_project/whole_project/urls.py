from django.contrib import admin
from django.urls import path, include
from django.views import generic

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic.TemplateView.as_view(template_name='home.html'), name='home'),

    path('', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
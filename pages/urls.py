from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name = 'about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

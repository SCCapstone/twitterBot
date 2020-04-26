# required django imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
	# home page
    path('home/', views.HomeView.as_view(), name='home'),
    # about page
    path('', views.AboutView.as_view(), name = 'about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

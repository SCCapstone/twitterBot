from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name = 'about'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    #path('bokeh/', views.ResultsView.as_view(), name='bokeh'),
	path('signup/', views.SignUp.as_view(), name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

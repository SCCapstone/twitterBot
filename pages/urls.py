from django.urls import path
from . import views
from .views import HomePageView, AboutPageView, IndexPageView

urlpatterns = [
	path('about/', AboutPageView.as_view(), name = 'about'),
	path('', HomePageView.as_view(), name = 'home'),
	path('index/', IndexPageView.as_view(), name = 'index'),
	path('signup/', views.SignUp.as_view(), name='signup'),
]
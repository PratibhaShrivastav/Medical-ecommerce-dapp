from django.urls import path
from django.contrib.auth import views
from .views import Signup

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', views.LogoutView.as_view(),name='logout',kwargs={'next_page':'/'}),
    path('signup/',Signup.as_view(),name='signup'),
]

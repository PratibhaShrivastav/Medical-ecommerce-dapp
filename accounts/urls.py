from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView,LogoutView
from .views import Signup,Addtocart,Removefromcart

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', LogoutView.as_view(),name='logout',kwargs={'next_page':'/'}),
    path('signup/',Signup.as_view(),name='signup'),
    path('<int:pk>/add-to-cart/',views.Addtocart,name="addtocart"),
    path('<int:pk>/remove-from-cart/',views.Removefromcart,name="removefromcart"),
]

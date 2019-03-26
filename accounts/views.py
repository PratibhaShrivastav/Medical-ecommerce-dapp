from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from products.models import Product

# Create your views here.

class Signup(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')

def Showcart(request):
    return render(request,'cart.html')

def Addtocart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    cart=request.user.cart
    product.cart = cart
    cart.price = cart.price + product.price
    product.save()
    cart.save()
    return redirect('/')
    
def Removefromcart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    cart=request.user.cart
    product.cart = None
    cart.price = cart.price - product.price
    product.save()
    cart.save()
    return redirect('/')
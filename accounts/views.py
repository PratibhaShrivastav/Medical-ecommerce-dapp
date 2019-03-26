from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from products.models import Product, Cart


class Signup(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')

def Showcart(request):
    user = request.user
    cart = user.cart
    products = cart.products.all()
    price = cart.price
    
    products_data = []

    for product in products:
        data = {}
        data['id'] = product.id
        data['name'] = product.name
        data['description'] = product.description
        data['price'] = product.price
        data['amount'] = product.amount
        data['image'] = str(product.product_img)        
        data['total'] = product.price * product.amount
        products_data.append(data)

    if price>10:
        shipping = 5
    else:
        shipping = 0

    context = {
        'products' : products_data,
        'price'    : price,
        'tax'      : price*0.05,
        'shipping' : shipping,
        'g_total'  : (price*1.05)+shipping,
    }
    return render(request,'cart.html', context)

def Addtocart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    try:
        cart=request.user.cart
    except:
        cart = Cart(user=request.user,price=0)
        cart.save()
    product.cart = cart
    product.amount += 1
    cart.price = cart.price + product.price
    product.save()
    cart.save()
    return redirect('/')
    
def Removefromcart(request,pk):
    product = get_object_or_404(Product,pk=pk)
    cart=request.user.cart
    product.cart = None
    print("Cart price", cart.price)
    cart.price = cart.price - (product.price * product.amount)
    print("Cart price", cart.price)
    product.amount = 0
    product.save()
    cart.save()
    return redirect('/accounts/cart/')
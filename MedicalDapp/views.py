from django.views.generic import TemplateView
from django.shortcuts import render
from products.models import Product

def Home(request):
    products = Product.objects.all()

    products_data = []

    for product in products:
        data = {}
        data['id'] = product.id
        data['name'] = product.name
        data['description'] = product.description
        data['price'] = product.price
        data['amount'] = product.amount
        data['image'] = str(product.product_img)        
        products_data.append(data)

    context = {'products' : products_data}
    
    return render(request, 'index.html', context)


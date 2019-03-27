from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from products.models import Product, Cart

import pytesseract
import textrazor
from PIL import Image
from django.conf import settings
import io

class Signup(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:login')

def Showcart(request):
    user = request.user
    
    try:
        cart=request.user.cart
    except:
        cart = Cart(user=request.user,price=0)
        cart.save()

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

"""
This function uses pytessaract library to convert an image into text
"""
def ImageToText(request):
    image = Image.open(io.BytesIO(request.FILES['Image'].read()))
    content = pytesseract.image_to_string(image)
    Generate_Data(request, content, settings.TEXTRAZOR_KEY)
    return redirect('/accounts/cart/')

"""
This function Adds list of medicines to a specified cart
"""
def addListToCart(request, medicines):
    
    try:
        cart=request.user.cart
    except:
        cart = Cart(user=request.user,price=0)
        cart.save()

    for medicine in medicines:
        print(medicine)
        try:
            product = Product.objects.get(name=str(medicine))
            product.cart = cart
            product.amount += 1
            cart.price = cart.price + product.price
            print("Added product ", medicine)
        except:
            continue
        product.save()
    cart.save()
    # print('cart saved')

"""
Converts a string into meaningful data, by recognizing various entities.
"""    
def Generate_Data(request, content, key):
    
    textrazor.api_key = key
    client = textrazor.TextRazor(extractors=["entities", "topics"])

    response = client.analyze(content)
    
    medicines = []
    person = []
    hospital = ""
    date = ""
    doctor = ""
    patient = ""
    
    for entity in response.entities():
        if 'ChemicalSubstance' in entity.dbpedia_types:        #Case when entity is recongnised as ChemicalSubstance
            medicines.append(str(entity.id).lower())
        if 'Person' in entity.dbpedia_types:                   #Case when entity is recongnised as Person
            person.append(entity.id)
        if 'Company' in entity.dbpedia_types:                  #Case when entity is recongnised as Company
            hospital = entity.id        
        if 'Date' in entity.dbpedia_types:                     #Case when entity is recongnised as Date
            date = entity.id
    # print(content)
    # for entity in response.entities():
    #     print(entity.id, entity.dbpedia_types)

    index = content.find(person[0])    
    drindex = content.find(person[1])      
    
    if index > drindex:                
        doctor = person[0]
        patient = person[1]
    else:                              
        doctor = person[1]
        patient = person[0]

    """
    Save Data to Blockchain Here
    """

    addListToCart(request, medicines)

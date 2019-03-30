from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect
from products.models import Product, Cart
from .models import BlockIds

import pytesseract
import textrazor
from PIL import Image
from django.conf import settings
from web3 import Web3
import io
import json

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
    print(content)
    Generate_Data(request, content, settings.TEXTRAZOR_KEY)
    return redirect('/accounts/cart/')

"""
This function Adds list of medicines to a specified cart
"""
def addListToCart(request, medicines):
    
    print("===========Adding to cart============")

    try:
        cart=request.user.cart
        print("Cart fetched")
    except:
        cart = Cart(user=request.user,price=0)
        cart.save()
        print("Cart Created")

    for medicine in medicines:
        print("Medicine :", medicine)
        try:
            product = Product.objects.get(name__iexact=str(medicine))
            product.cart = cart
            product.amount += 1
            cart.price = cart.price + product.price
            print("has been Added")
        except:
            print("was not in store.")
            continue
        product.save()
        cart.save()
    print("===========Added to cart============")

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
        # print(entity.matched_text)
        if 'ChemicalSubstance' in entity.dbpedia_types:        #Case when entity is recongnised as ChemicalSubstance
            medicines.append(str(entity.matched_text).lower())
        elif 'Drug' in entity.dbpedia_types:                     #Case when entity is recongnised as Drug
            medicines.append(str(entity.matched_text).lower())
        elif 'Person' in entity.dbpedia_types:                   #Case when entity is recongnised as Person
            person.append(entity.matched_text)
        elif 'Company' in entity.dbpedia_types:                  #Case when entity is recongnised as Company
            hospital = entity.matched_text        
        elif 'Date' in entity.dbpedia_types:                     #Case when entity is recongnised as Date
            date = entity.matched_text
    
    print(content)
    for entity in response.entities():
        print(entity.matched_text, entity.dbpedia_types)

    if(len(person)<2):
        return 1
    
    index = content.find(person[0])    
    drindex = content.find(person[1])      
    
    if index > drindex:                
        doctor = person[0]
        patient = person[1]
    else:                              
        doctor = person[1]
        patient = person[0]

    """
    Blockchain on duty
    """
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))       #Creating Instance of web3 object
    with open("contracts/data.json", 'r') as f:
        datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]

    w3.eth.defaultAccount = w3.eth.accounts[1]                      #Selecting an account from with trancsactions would happen
    MedicalContractInstance = w3.eth.contract(address=contract_address, abi=abi)   #Getting the instance of deployed contract using ABI and address 

    #Saving data to Blockchain
    MedicalContractInstance.functions.addData(patient, hospital, doctor, medicines).transact()
    block_id = MedicalContractInstance.functions.recordCount().call()

    print("Data stored in Blockchain successfully, id = ", block_id)
    
    new_block = BlockIds(user=request.user, block_id=block_id)
    new_block.save()

    print("Fetching Data ...")
    Data = MedicalContractInstance.functions.showData(int(block_id)).call()
    print(Data)

    addListToCart(request, medicines)


"""
Used to fetch data from blockchain to show back to a user.
"""
def get_receipt_data(request):

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))       #Creating Instance of web3 object
    with open("contracts/data.json", 'r') as f:
        datastore = json.load(f)
        abi = datastore["abi"]
        contract_address = datastore["contract_address"]

    w3.eth.defaultAccount = w3.eth.accounts[1]                      #Selecting an account from with trancsactions would happen
    MedicalContractInstance = w3.eth.contract(address=contract_address, abi=abi)   #Getting the instance of deployed contract using ABI and address 

    blocks = BlockIds.objects.filter(user=request.user)
    
    receipt_data = []

    for block in blocks:
        temp = {}
        data = MedicalContractInstance.functions.showData(block.block_id).call()
        temp['pname'] = data[0]
        temp['hname'] = data[1]
        temp['dname'] = data[2]
        temp['medicines'] = data[3]
        receipt_data.append(temp)
    print(receipt_data)
    
    return render(request, 'Receipts.html', {'receipt_data':receipt_data})

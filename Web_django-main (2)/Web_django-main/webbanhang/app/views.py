from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
# Create your views here.

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    if active_category:
        products =  Product.objects.filter(category__slug = active_category)
    context = {'categories' : categories, 'products':products, 'active_category':active_category}
    return render(request, 'app/category.html', context)


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    
    return render(request, 'app/search.html', {"searched" : searched, "keys":keys, 'products':products, 'cartItems':cartItems, 'user_not_login':user_not_login, 'user_login':user_login})

def register(request):
    user_not_login = "show"
    user_login = "hidden"
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        username_valid = re.match(r'^[A-Za-z0-9_]+$', username)
        password_valid = re.match(r'^[A-Za-z0-9!@#$%^&]+$', password1)

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists!')
        elif username == '' or password1 == '' or password2 == '':
            messages.info(request, 'Username and password cannot be empty!')
        elif not username_valid:
            messages.info(request, 'Username cannot contain spaces or special characters (except underscore).')
        elif len(password1) < 8:
            messages.info(request, 'Password must be at least 8 characters long.')
        elif not password_valid:
            messages.info(request, 'Password contains invalid characters')
        elif password1 != password2:
            messages.info(request, 'Passwords do not match.')
        elif form.is_valid():
            form.save()
            messages.info(request, 'Registration successful. You can now log in.')
            return redirect('login')

    context = {'form': form, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/register.html', context)

def loginPage(request):
    user_not_login = "show"
    user_login = "hidden"
    if request.user.is_authenticated:                
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            messages.info(request, 'username or password not empty!')
        else:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'user or password not correct!')
    context = {'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems, 'user_not_login':user_not_login, 'user_login':user_login, 'categories' : categories, 'active_category':active_category}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user_not_login':user_not_login, 'user_login':user_login, 'categories' : categories}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user_not_login':user_not_login, 'user_login':user_login}
    return render(request, 'app/checkout.html', context)

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
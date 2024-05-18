from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404



@login_required(login_url='log_in')
def index(request):
    admin = User.objects.all()
    entery = models.Entery.objects.all()
    orders = models.Outery.objects.all()
    returns = models.Return.objects.all()

    context = {
        'orders': orders,
        'returns': returns,
        'entery': entery,
        'admin': admin,
    }
    return render(request, 'index.html', context)


#--------Authenticate---------
def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request,'login.html')
        except:
            return redirect('log_in')
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('log_in')


#---------Category---------
@login_required(login_url='log_in')
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name=request.POST.get('name'))
        return redirect('category_list')
    return render(request, 'category/create.html')
        

@login_required(login_url='log_in')
def category_list(request):
    categories = models.Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'category/list.html', context)


@login_required(login_url='log_in')
def category_update(request, code):
    category = models.Category.objects.get(code=code)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('category_list')


@login_required(login_url='log_in')
def category_delete(request, code):
    category = models.Category.objects.get(code=code)
    category.delete()
    return redirect('category_list')


#---------Product---------
@login_required(login_url='log_in')
def product_create(request):
    categories = models.Category.objects.all()
    context = {
        'categories': categories,
    }
    if request.method == 'POST':
        models.Product.objects.create(
            name=request.POST.get('name'),
            category=models.Category.objects.get(id=request.POST.get('category')),
            quantity=request.POST.get('quantity'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')

        )
        return redirect('product_list')
    return render(request, 'product/create.html', context)


@login_required(login_url='log_in')
def product_list(request):
    products = models.Product.objects.all()
    return render(request, 'product/list.html', {'products': products})
    

@login_required(login_url='log_in')
def product_update(request, code):
    categories = models.Category.objects.all()
    product = get_object_or_404(models.Product, code=code)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        try:
            category = models.Category.objects.get(id=category_id)
        except models.Category.DoesNotExist:
            return render(request, 'product/update.html', {
                'categories': categories,
                'product': product,
                'error': 'Selected category does not exist.'
            })
        
        if not name:
            return render(request, 'product/update.html', {
                'categories': categories,
                'product': product,
                'error': 'Product name is required.'
            })
        
        product.name = name
        product.category = category
        product.quantity = quantity
        product.price = price
        product.description = description
        if image:
            product.image = image

        try:
            product.save()
            return redirect('product_list')
        except ValueError as e:
            return render(request, 'product/update.html', {
                'categories': categories,
                'product': product,
                'error': e.message
            })

    context = {
        'categories': categories,
        'product': product,
    }
    return render(request, 'product/update.html', context)


@login_required(login_url='log_in')
def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')


#---------Entery---------   
@login_required(login_url='log_in')
def entry_create(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        enter_product = models.Entery.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('entry_list')
    return render(request, 'entry/create.html', {'products': products})


@login_required(login_url='log_in')
def entry_list(request):
    enter_products = models.Entery.objects.all()
    return render(request, 'entry/list.html', {'enter_products': enter_products})
    

@login_required(login_url='log_in')
def outery_create(request):
    products = models.Product.objects.all()
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        outery_product = models.Outery.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('outery_list')
    
    return render(request, 'outery/create.html', {'products': products})


@login_required(login_url='log_in')
def outery_list(request):
    outery_products = models.Outery.objects.all()
    return render(request, 'outery/list.html', {'outery_products': outery_products})


@login_required(login_url='log_in')
def return_create(request):
    products = models.Outery.objects.all()
    if request.method == 'POST':
        product = models.Outery.objects.get(code=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        return_product = models.Return.objects.create(
            product=product,
            quantity=quantity,
        )
        return redirect('return_list')
    
    return render(request, 'returns/create.html', {'products': products})


@login_required(login_url='log_in')
def return_list(request):
    return_products = models.Return.objects.all()
    return render(request, 'returns/list.html', {'return_products': return_products})




    
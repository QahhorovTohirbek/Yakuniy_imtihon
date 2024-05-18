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
    categories = models.Category.objects.all()
    category_code = request.GET.get('code')

    filter_items = {}
    if category_code:
        filter_items['product__category__code'] = category_code

    for key, value in request.GET.items():
        if value and not value == '0':
            if key == 'start_date':
                key = 'created_at__gte'
            elif key == 'end_date':
                key = 'created_at__lte'
            elif key == 'name':
                key = 'product__name__icontains'
            filter_items[key] = value

    products = models.Product.objects.filter(**filter_items)
    context = {
        'products': products,
        'categories': categories,
        'category_code': category_code,
    }
    return render(request, 'product/list.html', context)
    

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
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    context = {
        'category': category,
        'products': products,
    }
    if request.method == 'POST':
        models.Entery.objects.create(
            product=models.Product.objects.get(id=request.POST.get('product')),
            quantity=request.POST.get('quantity'),
)
        return redirect('entry_list')
    return render(request, 'entry/create.html', context)


@login_required(login_url='log_in')
def entry_list(request):
    category = models.Category.objects.all()
    products = models.Product.objects.filter(category=category)
    category_code = request.GET.get('category_code')
    if category_code:
        filter_items = {}
        for key, value in request.GET.items():
            if value and not value == '0':
                if key == 'start_date':
                    key = 'date__gte'
                elif key == 'end_date':    
                    key = 'date__lte'
                elif key == 'name':
                    key = 'product__name__icontains'
                filter_items[key] = value

        enteries = models.Entery.objects.filter(**filter_items)
    context = {
        'products': products,
        'enteries': enteries,
        'category': category,
        'category_code': category_code,
    }
    return render(request, 'entry/list.html', context)
    

@login_required(login_url='log_in')
def outery_create(request):
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    context = {
        'category': category,
        'products': products,
    }
    if request.method == 'POST':
        models.Outery.objects.create(
            product=models.Product.objects.get(id=request.POST.get('product')),
            quantity=request.POST.get('quantity'),
            date=request.POST.get('date'),
)
        return redirect('outery_list')
    
    return render(request, 'outery/create.html', context)


@login_required(login_url='log_in')
def outery_list(request):
    category = models.Category.objects.all()
    product = models.Product.objects.filter(category=category)
    outery = models.Outery.objects.filter(product=product)

    category_code = request.GET.get('category_code')

    if category_code:
        filter_items = {}
        for key, value in request.GET.items():
            if value and not value == '0':
                if key == 'start_date':
                    key = 'date__gte'
                elif key == 'end_date':    
                    key = 'date__lte'
                elif key == 'name':
                    key = 'product__name__icontains'
                filter_items[key] = value

        outery = models.Outery.objects.filter(**filter_items)
        context = {
            'product': product,
            'outery': outery,
            'category': category,
            'category_code': category_code,
        }
        return render(request, 'outery/list.html', context)
    
    return render(request, 'outery/list.html', context)


@login_required(login_url='log_in')
def return_create(request):
    category = models.Category.objects.all()
    outery = models.Outery.objects.all()
    context = {
        'category': category,
        'outery': outery,}
    if request.method == 'POST':
        models.Return.objects.create(
            outery = models.Outery.objects.get(id=request.POST.get('outery')),
            quantity=request.POST.get('quantity'),
)
        return redirect('return_list')
    
    return render(request, 'returns/create.html', context)


@login_required(login_url='log_in')
def return_list(request):
    category = models.Category.objects.all()
    product = models.Product.objects.filter(category=category)
    returns = models.Return.objects.filter(product=product)

    context = {
        'product': product,
        'returns': returns,
        'category': category,
    }

    return render(request, 'returns/list.html', context)




    
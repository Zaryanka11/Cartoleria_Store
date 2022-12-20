from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import ProductCategory, Product, Basket

# Create your views here.
# Контроллеры = views (вьюхи) = функции

def index(request):
    context = {
        'tittle': 'Store'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = { 'tittle': 'Store - Магазин', 'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page) # по умолчанию 1 страница
    context.update({'products': products_paginator})
    return render(request, 'products/products.html', context)
@login_required
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists(): # для списков
        Basket.objects.create(user=request.user, product=product,quantity=1)
        return HttpResponseRedirect(current_page) # возвращение пользователя на текущую страницу
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(current_page)

@login_required
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

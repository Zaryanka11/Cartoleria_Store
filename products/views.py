from django.shortcuts import render

from products.models import ProductCategory, Product


# Create your views here.
# Контроллеры = views (вьюхи) = функции

def index(request):
    context = {
        'tittle': 'Store'
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'tittle': 'Store - Магазин',
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'products/products.html', context)

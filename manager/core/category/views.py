from django.shortcuts import render
from catalog.models import Category
from .forms import CategoryForm
from django.http import JsonResponse

__all__ = ['category','list_items']

def category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    return render(request,'main/slug.html',{'model':'category','view':'Category','form':form,'item':category})

def list_items(request):
    categories = Category.objects.all()
    return render(request,'category/categories.html',{'panel':'main/panel/default.html','model':'category','view':'CategoryList','items':categories})

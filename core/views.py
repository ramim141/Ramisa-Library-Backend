from django.shortcuts import render
from books.models import Book, Category
# Create your views here.
def home(request,category_slug=None):
    data=Book.objects.all()
    if not category_slug==None:
        categories=Category.objects.get(slug=category_slug)
        data=Book.objects.filter(categories=categories)
    categories=Category.objects.all()
    return render(request,'index.html',{'data':data,'categories':categories})
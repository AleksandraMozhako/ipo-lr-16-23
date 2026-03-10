from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html')

def author(request):
    return render(request, 'shop/author.html')
# Create your views here.

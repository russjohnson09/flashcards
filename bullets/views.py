from django.shortcuts import render

def index(request):
    return render(request,"bullets/bullets.html")

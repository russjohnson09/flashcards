from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,Http404

# Create your views here.


#index
def index(request):
    return render(request,'contacts/index.html',{'test':1})

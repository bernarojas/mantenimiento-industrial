from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from .models import Book 
from django.core.serializers import serialize

def index(request):
    book=Book.objects.all()
    print("Holaxxxx")
    return render(request, "index.html", {'book': book})

def games(request):
    book = serialize("json", Book.objects.all())
    print("Chaoxxxx")
    return HttpResponse(book, content_type="application/json")

from django.shortcuts import render

def home():
    return render(request, "index.html")
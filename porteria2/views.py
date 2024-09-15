from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'porteria2/porteria2.html')
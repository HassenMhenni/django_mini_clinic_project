from django.shortcuts import render

def home(request):
    return render(request, 'myclinic/home.html')

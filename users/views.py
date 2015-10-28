from django.shortcuts import render

def home_page(request):
    return render(request, 'index.html', {})

def user_profile(request):
    return render(request, 'user.html')
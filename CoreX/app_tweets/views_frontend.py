from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    return render(request, 'app_authenticate/landing_page.html')

@login_required(login_url='/')
def homepage(request):
    if not request.user.is_authenticated:
        return redirect('app_authenticate:landing_page')
    return render(request, 'app_tweets/homepage.html')
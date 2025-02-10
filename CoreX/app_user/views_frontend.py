from django.shortcuts import render, redirect


def profile_page(request):
    if request.user.is_authenticated:
        return render(request, 'app_user/profile.html')
    return redirect('homepage')
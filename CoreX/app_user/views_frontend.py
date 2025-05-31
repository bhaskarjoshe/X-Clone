from django.shortcuts import redirect, render


def profile_page(request):
    if request.user.is_authenticated:
        return render(request, "app_user/profile.html")
    return redirect("homepage")

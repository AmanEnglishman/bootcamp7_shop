from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm
from catalog.models import Product


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    print(user)

    if user.is_seller:
        return redirect('seller_dashboard')

    return render(request, 'profile.html', {'user': user})


@login_required
def seller_dashboard(request):
    user = request.user

    if not user.is_seller:
        return redirect('profile')

    products = Product.objects.filter(user=user)

    return render(request, 'seller_dashboard.html',
                  {'products': products, 'user': user})

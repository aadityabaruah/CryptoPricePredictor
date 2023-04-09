from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, "cryptocurrencypricepredictor/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('home')

        if password != confirmpassword:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()

        messages.success(request, "Your account has been created successfully!")

        return redirect('user_login')

    return render(request, "cryptocurrencypricepredictor/signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "cryptocurrencypricepredictor/index.html", {'firstname': user.first_name})
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('home')

    return render(request, "cryptocurrencypricepredictor/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')


def predict(request):
    return render(request, "cryptocurrencypricepredictor/predict.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
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

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()

        messages.success(request, "Your account has been created successfully!")

        return redirect('login')

    return render(request, "cryptocurrencypricepredictor/signup.html")


def login(request):
    return render(request, "cryptocurrencypricepredictor/login.html")


def logout(request):
    pass

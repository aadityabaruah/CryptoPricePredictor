from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
import yfinance as yf
from sklearn.linear_model import LinearRegression
from dateutil.relativedelta import relativedelta


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
            return render(request, "cryptocurrencypricepredictor/index.html", {'firstname': user.first_name.capitalize})
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('home')

    return render(request, "cryptocurrencypricepredictor/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')


def predict(request):
    if request.method == 'POST':
        return predict_result(request)
    else:
        return render(request, 'cryptocurrencypricepredictor/predict.html')


def predict_result(request):
    # Retrieve start and end dates from form input
    start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')

    # Retrieve historical price data for cryptocurrency using yfinance
    ticker = yf.Ticker('BTC-USD')
    history = ticker.history(period='12mo')

    # Check if history is empty
    if history.empty:
        return render(request, 'cryptocurrencypricepredictor/error.html', {'message': 'No historical price data available for the specified date range.'})

    # Extract features and target variable from historical price data
    X = history[['Open', 'High', 'Low', 'Volume']]
    y = history['Close']

    # Train a linear regression model on the historical data
    model = LinearRegression()
    model.fit(X, y)

    # Use the model to predict the future price of the cryptocurrency
    latest_data = X.iloc[-1, :]
    predicted_price = model.predict([latest_data])[0]

    # Render the prediction.html template with the predicted price
    context = {
        'cryptocurrency': 'Bitcoin',
        'start_date': start_date.strftime('%m/%d/%Y'),
        'end_date': end_date.strftime('%m/%d/%Y'),
        'predicted_price': round(predicted_price, 2),
    }
    return render(request, 'cryptocurrencypricepredictor/prediction.html', context)


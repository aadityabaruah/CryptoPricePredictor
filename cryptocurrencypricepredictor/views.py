from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import yfinance as yf
import plotly.graph_objs as go


graph = 0


def home(request):
    data = yf.download(tickers='BTC-USD', period='22h', interval='15m')
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))
    # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Bitcoin Price (kUS Dollars)')
    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    graph = fig.to_html(full_html=False)
    return render(request, 'cryptocurrencypricepredictor/index.html', {'graph': graph})


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
   return render(request, 'cryptocurrencypricepredictor/predict.html')


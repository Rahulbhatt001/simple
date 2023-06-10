from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            beverage = request.POST.get('beverage', '')  
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['beverage'] = beverage  
                return redirect('welcome')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
@login_required
def welcome(request):
    beverage = request.session.pop('beverage', '')  
    message = f"{request.user.username}! "
    if beverage:
        message += f"You have a great taste! Your favorite beverage is {beverage}."
    else:
        message += "Please enter your favorite beverage."

    context = {'message': message}
    return render(request, 'welcome.html', context)


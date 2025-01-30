from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, AccountCreationForm, LoginForm
import logging
from .models import User, Account, Transaction

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Cajero_Pichincha:display_bank_services')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def display_bank_services(request):
    user = User.objects.get(username=request.user)
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')[:3]
    return render(request, 'display_bank_services.html', {
        'user': user,
        'account': account,
        'transactions': transactions
    })

logger = logging.getLogger(__name__)

def logout_view(request):
    print("Iniciando proceso de logout")  # Debug
    print(f"Usuario antes de logout: {request.user}")  # Debug
    
    try:
        logout(request)
        print(f"Usuario después de logout: {request.user}")  # Debug
        messages.success(request, 'Has cerrado sesión exitosamente')
        print("Redirigiendo a index")  # Debug
        return redirect('Cajero_Pichincha:index')
    except Exception as e:
        print(f"Error en logout: {str(e)}")  # Debug
        return redirect('Cajero_Pichincha:index')
    
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        account_form = AccountCreationForm(request.POST)
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            return redirect('Cajero_Pichincha:login')
    else:
        user_form = CustomUserCreationForm()
        account_form = AccountCreationForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'account_form': account_form
    })
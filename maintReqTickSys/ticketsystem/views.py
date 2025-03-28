from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Ticket
from . import forms

def home(request):
    return render(request, 'home.html')

def user_login(request):
    # If Post validate entry and go to dashboard
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # Returns current users information
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')

    # If GET return the form
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/")
def tenant_dashboard(request):
    # Send users name to tenant page
    context = {
        'user': request.user,
        'tickets': Ticket.objects.all()
    }
    return render(request, 'tenant_dashboard.html', context)

@login_required(login_url="/")
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    return render(request, 'admin_dashboard.html')

@login_required(login_url="/")
def ticket_create(request):
    if request.method == 'POST':
        form = forms.CreateTicket(request.POST, request.FILES)

        if form.is_valid():
            # Don't save ticket to DB yet
            ticket = form.save(commit=False) 
            # Automatically fill in the field submitter for ticket
            ticket.submitter = request.user
            ticket.save()
            messages.success(request, 'Ticket has been made')

            # Send users name to tenant page
            context = {
                'user': request.user,
                'tickets': Ticket.objects.all()
            }

            return render(request, 'Tenant_dashboard.html', context)

    else:
        form = forms.CreateTicket()
    return render(request, 'ticket_create.html', {'form':form})
   
@login_required(login_url="/")
def ticket_page(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(request, 'ticket_page.html', {'ticket': ticket})
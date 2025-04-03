from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Ticket, User, UserProfile
from . import forms

def home(request):
    return render(request, 'home.html')

def user_login(request):
    # If Post validate entry and go to dashboard
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # Returns current users information
            print(user.username)
            userProfile = UserProfile.objects.get(user=user)
            login(request, user)
            print("-----------------------------------------")
            print(userProfile)
            if userProfile.role == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('tenant_dashboard')

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
    userProfile = UserProfile.objects.get(user=request.user)
    if userProfile.role == "tenant":
        return redirect('tenant_dashboard')
    
    context = {
        'user': request.user,
        'tickets': Ticket.objects.all()
    }

    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('my_checkboxes[]')
        print(selected_checkboxes)

        for selected_id in selected_checkboxes:
            ticket = Ticket.objects.get(id=selected_id)
            ticket.assigned_admin = request.user

            ticket.save()

    return render(request, 'admin_dashboard.html', context)

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

@login_required(login_url="/")
def update_ticket(request):
    return render(request, 'update_ticket.html')

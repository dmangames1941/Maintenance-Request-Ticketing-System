from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Ticket, User, UserProfile, Comment
from . import forms
from django.db.models import Count

def home(request):
    # If user has already authenticated and their session hasnt expired, automatically redirect to their dashboard
    if request.user.is_authenticated:
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.role == "admin":
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')
    return render(request, 'home.html')

def user_login(request):
    # If user has already authenticated and their session hasnt expired, automatically redirect to their dashboard
    if request.user.is_authenticated:
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.role == "admin":
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')

    # If Post validate entry and go to dashboard
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user() # Returns current users information
            userProfile = UserProfile.objects.get(user=user)
            login(request, user)
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
    form = forms.CreateTicket()
    if request.method == 'POST':
        form = forms.CreateTicket(request.POST, request.FILES)
        if form.is_valid():
            # Don't save ticket to DB yet
            ticket = form.save(commit=False) 
            # Automatically fill in the field submitter for ticket
            ticket.submitter = request.user
            ticket.save()
            messages.success(request, 'Ticket has been made')
            return redirect('tenant_dashboard')  # Redirect to clear POST data

    context = {
        'user': request.user,
        'tickets': Ticket.objects.all(),
        'form': form,
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
def admin_my_maintenance(request):
    userProfile = UserProfile.objects.get(user=request.user)
    if userProfile.role == "tenant":
        return redirect('tenant_dashboard')
    
    # context = {
    #     'user': request.user,
    #     'tickets': Ticket.objects.all()
    # }

    tickets = Ticket.objects.filter(assigned_admin=request.user)

    context = {
        'user': request.user,
        'tickets': tickets,
        'count_all': tickets.count(),
        'count_open': tickets.filter(status='open').count(),
        'count_in_progress': tickets.filter(status='in_progress').count(),
        'count_completed': tickets.filter(status='completed').count(),
    }

    return render(request, 'admin_my_maintenance.html', context)

@login_required(login_url="/")
def ticket_page(request, id):
    ticket = Ticket.objects.get(id=id)
    form_ticket = forms.TenantUpdateTicket(instance=ticket)

    # Added authentication to ensure that the user trying to access this page is the one who submitted the ticket
    if ticket.submitter_id != request.user.id:
        return redirect('tenant_dashboard')
    

    #handling form submission 
    if request.method == 'POST':
        form_ticket = forms.TenantUpdateTicket(request.POST, request.FILES, instance=ticket)
        if form_ticket.is_valid():
            form_ticket.save()
            return redirect(f'/{id}', id=ticket.id)
        else:
            form_ticket = forms.TenantUpdateTicket(instance=ticket)

    context = {
        'ticket': ticket,
        'form_ticket': form_ticket,
        'comments': Comment.objects.filter(ticket_id=id)
    }
    return render(request, 'ticket_page.html', context)


@login_required(login_url="/")
def admin_ticket_page(request, id):
    ticket = Ticket.objects.get(id=id)
    form_ticket = forms.UpdateTicket()
    form_comment = forms.CreateComment()

    if request.method == 'POST':
        form_ticket = forms.UpdateTicket(request.POST, instance=ticket)
        form_comment = forms.CreateComment(request.POST, request.FILES)

        if form_ticket.is_valid() and form_comment.is_valid():
            
            comment = form_comment.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            form_ticket.save()

            return redirect('admin_ticket_page', id=ticket.id)  # Go to ticket individual page
        

    else:
        form_ticket = forms.UpdateTicket(instance=ticket)  # Sets default in form to current status
        form_comment = forms.CreateComment()

    context = {
        'ticket': ticket,
        'comments': Comment.objects.filter(ticket_id=id),
        'form_ticket': form_ticket,
        'form_comment': form_comment
    }
    
    return render(request, 'admin_ticket_page.html', context)

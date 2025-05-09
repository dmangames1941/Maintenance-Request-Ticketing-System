from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Ticket, UserProfile, Comment
from . import forms
from django.db.models import Count
from django.shortcuts import render
from django.db.models import Count
from .models import Ticket
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from .models import Ticket, UserProfile
from datetime import timedelta

def home(request):
    # If user has already authenticated and their session hasnt expired, automatically redirect to their dashboard
    if request.user.is_authenticated:
        userProfile = UserProfile.objects.get(user=request.user)
        if userProfile.role == "admin":
            return redirect('admin_dashboard')
        else:
            return redirect('tenant_dashboard')
    # Send user to login page
    return redirect('login')

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
        'tickets': Ticket.objects.filter(submitter_id=request.user.id),
        'form': form,
    }
    return render(request, 'tenant_dashboard.html', context)


@login_required(login_url="/")
def admin_dashboard(request):
    userProfile = UserProfile.objects.get(user=request.user)
    if userProfile.role == "tenant":
        return redirect('tenant_dashboard')

    # ✅ Handle checkbox assignment
    if request.method == 'POST':
        selected_checkboxes = request.POST.getlist('my_checkboxes[]')
        for selected_id in selected_checkboxes:
            ticket = Ticket.objects.get(id=selected_id)
            ticket.assigned_admin = request.user
            ticket.save()

    tickets = Ticket.objects.all()

    # ✅ Analytics logic
    total_tickets = tickets.count()
    submitted = tickets.filter(status='submitted').count()
    in_progress = tickets.filter(status='in_progress').count()
    completed = tickets.filter(status='completed').count()
    high_priority = tickets.filter(priority='high').count()

    by_category = tickets.values('category').annotate(count=Count('id'))
    by_priority = tickets.values('priority').annotate(count=Count('id'))

    today = timezone.now().date()
    last_7_days = [
        {
            'date': (today - timedelta(days=i)).strftime('%b %d'),
            'count': tickets.filter(created_date__date=(today - timedelta(days=i))).count()
        }
        for i in range(6, -1, -1)
    ]

    context = {
        'user': request.user,
        'tickets': tickets,
        'total_tickets': total_tickets,
        'submitted': submitted,
        'in_progress': in_progress,
        'completed': completed,
        'high_priority': high_priority,
        'by_category': list(by_category),
        'by_priority': list(by_priority),
        'last_7_days': last_7_days,
    }

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
            form_ticket.save(commit=False)
            ticket._skip = True # Passes in the 'skip' flag to the instance so SMTP doesnt trigger
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


@login_required(login_url="/")
def admin_my_analytics(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if user_profile.role != 'admin':
        return redirect('tenant_dashboard')

    tickets = Ticket.objects.filter(assigned_admin=user)

    # Category-wise count
    by_category = list(tickets.values('category').annotate(count=Count('id')))

    # Priority-wise count
    by_priority = list(tickets.values('priority').annotate(count=Count('id')))

    # Ticket trend for the last 7 days
    last_7_days = []
    today = timezone.now().date()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = tickets.filter(created_date__date=day).count()
        last_7_days.append({"date": day.strftime("%b %d"), "count": count})

    context = {
        'user': user,
        'by_category': by_category,
        'by_priority': by_priority,
        'last_7_days': last_7_days
    }

    return render(request, 'admin_my_analytics.html', context)

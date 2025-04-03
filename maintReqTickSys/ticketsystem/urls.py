from django.urls import path
from .views import home, user_login, user_logout, tenant_dashboard, admin_dashboard, ticket_create, ticket_page, update_ticket, admin_ticket_page
from .views import admin_user_dashboard
9
urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tenant-dashboard/', tenant_dashboard, name="tenant_dashboard"),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-user-dashboard/', admin_user_dashboard, name='admin_user_dashboard'),
    path('ticket_create/', ticket_create, name='ticket_create'),
    path('<int:id>', ticket_page, name="page" ),
    path('update_ticket/', update_ticket, name='update_ticket'),
    path('admin_dashboard/<int:id>', admin_ticket_page, name="admin_page" ),
]
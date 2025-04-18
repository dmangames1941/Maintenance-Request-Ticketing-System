from django.urls import path
from .views import home, user_login, user_logout, tenant_dashboard, admin_dashboard, ticket_page, update_ticket, admin_ticket_page
from .views import admin_my_maintenance
9
urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tenant-dashboard/', tenant_dashboard, name="tenant_dashboard"),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-my-maintenance/', admin_my_maintenance, name='admin_my_maintenance'),
    path('<int:id>', ticket_page, name="page" ),
    path('update_ticket/', update_ticket, name='update_ticket'),
    path('update/<int:id>/', update_ticket, name='update_ticket'),
    path('admin_dashboard/<int:id>/', admin_ticket_page, name="admin_ticket_page" ),
]
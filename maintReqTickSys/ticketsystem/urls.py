from django.urls import path
from .views import home, user_login, user_logout, tenant_dashboard, admin_dashboard, ticket_create, ticket_page

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tenant-dashboard/', tenant_dashboard, name="tenant_dashboard"),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('ticket_create/', ticket_create, name='ticket_create'),
    path('<int:id>', ticket_page, name="page" )
]
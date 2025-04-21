from django.urls import path
from .views import home, user_login, user_logout, tenant_dashboard, admin_dashboard, ticket_page, admin_ticket_page
from .views import admin_my_maintenance
from .views import admin_my_analytics


urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tenant-dashboard/', tenant_dashboard, name="tenant_dashboard"),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-my-maintenance/', admin_my_maintenance, name='admin_my_maintenance'),
    path('<int:id>', ticket_page, name="page" ),
    path('admin_dashboard/<int:id>/', admin_ticket_page, name="admin_ticket_page" ),
    path("admin-my-analytics/", admin_my_analytics, name="admin_my_analytics"),
]
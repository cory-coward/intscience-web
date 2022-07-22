from django.urls import path

from .views import dashboard_home_view

app_name = 'dashboard'
urlpatterns = [
    path('', dashboard_home_view, name='dashboard-home'),
    path('<path:path>/', dashboard_home_view, name='dashboard-with-path'),
]

from django.urls import path

from .views import homepage_view

app_name = 'pages'
urlpatterns = [
    path('', homepage_view, name='home'),
]

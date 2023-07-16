from django.urls import path
from . import views

app_name = 'SmartE_app'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration, name='registration'),
path('payment/', views.payment, name='payment'),
    # Add other URL patterns as needed
]

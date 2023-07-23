from django.urls import path
from . import views

app_name = 'SmartE_app'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration, name='registration'),
    path('payment/', views.payment, name='payment'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    #path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('course/<str:course_id>/', views.course_detail, name='course_detail'),
    path('course_dashboard/', views.course_dashboard, name='course_dashboard'),
    path('course/<str:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('course/<str:course_id>/delete/', views.course_delete, name='course_delete'),

    # Other URL patterns...
    # Add other URL patterns as needed
]

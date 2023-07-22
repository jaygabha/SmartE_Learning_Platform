from django.conf.urls.static import static
from django.urls import path

from SmartE import settings
from . import views

app_name = 'SmartE_app'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration, name='registration'),
    path('payment/', views.payment, name='payment'),
    #path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('course/<str:course_id>/', views.course_detail, name='course_detail'),
    path('course_dashboard/', views.course_dashboard, name='course_dashboard'),
    path('course/<str:course_id>/module/<int:module_id>/', views.module_detail, name='module_detail'),
    path('course/<str:course_id>/delete/', views.course_delete, name='course_delete'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:course_id>/', views.course_detail_student, name='course_detail_student'),
    path('attendance', views.attendance, name="attendance"),
    path('attendance/add/<str:course_id>', views.add_attendance, name="add_attendance"),
    # Other URL patterns...
    # Add other URL patterns as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
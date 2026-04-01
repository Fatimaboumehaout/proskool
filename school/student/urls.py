from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('list/', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<str:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<str:student_id>/', views.delete_student, name='delete_student'),
    path('details/<str:student_id>/', views.student_details, name='student_details'),
]
from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('edit/<str:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('view/<str:teacher_id>/', views.view_teacher, name='view_teacher'),
    path('delete/<str:teacher_id>/', views.delete_teacher, name='delete_teacher'),
]

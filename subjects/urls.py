from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    # Dashboard
    path('', views.SubjectDashboardView.as_view(), name='dashboard'),
    
    # Matières (Subjects)
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    
    # Associations matière-groupe (SubjectGroups)
    path('subject-groups/', views.SubjectGroupListView.as_view(), name='subjectgroup_list'),
    path('subject-groups/create/', views.SubjectGroupCreateView.as_view(), name='subjectgroup_create'),
    path('subject-groups/<int:pk>/update/', views.SubjectGroupUpdateView.as_view(), name='subjectgroup_update'),
    path('subject-groups/<int:pk>/delete/', views.SubjectGroupDeleteView.as_view(), name='subjectgroup_delete'),
    
    # API
    path('api/search/', views.subject_search_api, name='subject_search_api'),
]

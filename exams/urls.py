from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Dashboard
    path('', views.ExamDashboardView.as_view(), name='dashboard'),
    
    # Examens
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('exams/create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/update/', views.ExamUpdateView.as_view(), name='exam_update'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),
    
    # Résultats
    path('results/', views.ExamResultListView.as_view(), name='result_list'),
    path('results/create/', views.ExamResultCreateView.as_view(), name='result_create'),
    path('results/<int:pk>/update/', views.ExamResultUpdateView.as_view(), name='result_update'),
    path('results/bulk-grading/', views.BulkGradingView.as_view(), name='bulk_grading'),
    path('results/export/<int:exam_id>/', views.export_exam_results, name='export_results'),
    
    # Sessions d'examens
    path('sessions/', views.ExamSessionListView.as_view(), name='session_list'),
    path('sessions/create/', views.ExamSessionCreateView.as_view(), name='session_create'),
    
    # API
    path('api/search/', views.exam_search_api, name='exam_search_api'),
]

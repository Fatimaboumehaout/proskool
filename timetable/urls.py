from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Emploi du temps
    path('emploi-du-temps/', views.EmploiDuTempsView.as_view(), name='emploi_du_temps'),
    
    # Salles
    path('salles/', views.SalleListView.as_view(), name='salle_list'),
    path('salles/create/', views.SalleCreateView.as_view(), name='salle_create'),
    path('salles/<int:pk>/update/', views.SalleUpdateView.as_view(), name='salle_update'),
    path('salles/<int:pk>/delete/', views.SalleDeleteView.as_view(), name='salle_delete'),
    
    # Enseignants
    path('enseignants/', views.EnseignantListView.as_view(), name='enseignant_list'),
    path('enseignants/create/', views.EnseignantCreateView.as_view(), name='enseignant_create'),
    path('enseignants/<int:pk>/update/', views.EnseignantUpdateView.as_view(), name='enseignant_update'),
    path('enseignants/<int:pk>/delete/', views.EnseignantDeleteView.as_view(), name='enseignant_delete'),
    
    # Groupes
    path('groupes/', views.GroupeListView.as_view(), name='groupe_list'),
    path('groupes/create/', views.GroupeCreateView.as_view(), name='groupe_create'),
    path('groupes/<int:pk>/update/', views.GroupeUpdateView.as_view(), name='groupe_update'),
    path('groupes/<int:pk>/delete/', views.GroupeDeleteView.as_view(), name='groupe_delete'),
    
    # Cours
    path('cours/', views.CoursListView.as_view(), name='cours_list'),
    path('cours/create/', views.CoursCreateView.as_view(), name='cours_create'),
    path('cours/<int:pk>/update/', views.CoursUpdateView.as_view(), name='cours_update'),
    path('cours/<int:pk>/delete/', views.CoursDeleteView.as_view(), name='cours_delete'),
]

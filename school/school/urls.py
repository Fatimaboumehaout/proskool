# school/urls.py 
from django.contrib import admin 
from django.urls import path, include 
 
urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('', include('faculty.urls')), 
    path('student/', include('student.urls')), 
    path('teachers/', include('teachers.urls')),
    path('authentication/', include('home_auth.urls', namespace='auth')),
    path('dashboard/', include('home_auth.urls', namespace='dashboard')),
]
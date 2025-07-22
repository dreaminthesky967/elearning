"""
URL configuration for elearningpart2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import  views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),

    # Dashboard umum
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Dashboard role-based
    path('dashboard/admin/', views.is_admin, name='dashboard_admin'),
    path('dashboard/dosen/', views.is_dosen, name='dashboard_dosen'),
    path('dashboard/mahasiswa/', views.is_mahasiswa, name='dashboard_mahasiswa'),

    # CRUD Mahasiswa
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),

    # CRUD Kursus
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    
    path('modul-materi/', views.ModulMateriListView.as_view(), name='modul_materi_list'),

]


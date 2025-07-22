from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Modul
from django.utils.decorators import method_decorator

from .models import Kursus, User
from .forms import (
    LoginForm,
    StudentCreationForm,
    StudentChangeForm,
    CourseForm
)


# ===================== Role Check =====================

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def is_dosen(user):
    return user.is_authenticated and user.role == "dosen"

def is_mahasiswa(user):
    return user.is_authenticated and user.role == "mahasiswa"

# ===================== Login & Logout =====================

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect sesuai role
            if user.role == 'admin':
                return redirect('dashboard')
            elif user.role == 'mahasiswa':
                return redirect('mahasiswa-dashboard')
            elif user.role == 'dosen':
                return redirect('dosen-dashboard')
            else:
                logout(request)
                return render(request, 'login.html', {
                    'form': form,
                    'error': 'Role tidak dikenali.'
                })
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# ===================== Dashboard View =====================

@login_required
@user_passes_test(is_admin)
def dashboard_view(request):  # Admin dashboard
    total_mahasiswa = User.objects.filter(role='mahasiswa').count()
    total_dosen = User.objects.filter(role='dosen').count()
    total_kursus = Kursus.objects.count()

    kursus_populer = Kursus.objects.annotate(
        jumlah_mahasiswa=Count('mahasiswa_terdaftar')
    ).order_by('-jumlah_mahasiswa')[:5]

    context = {
        'total_mahasiswa': total_mahasiswa,
        'total_dosen': total_dosen,
        'total_kursus': total_kursus,
        'kursus_populer_labels': [k.judul for k in kursus_populer],
        'kursus_populer_data': [k.jumlah_mahasiswa for k in kursus_populer],
    }
    return render(request, 'dashboard_admin.html', context)

@login_required
@user_passes_test(is_mahasiswa)
def mahasiswa_dashboard_view(request):
    return render(request, 'mahasiswa_dashboard.html')

@login_required
@user_passes_test(is_dosen)
def dosen_dashboard_view(request):
    return render(request, 'dosen_dashboard.html')

# ===================== Student (Admin Only) =====================

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class StudentListView(ListView):
    model = User
    template_name = "student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        return User.objects.filter(role="mahasiswa").order_by("first_name")

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class StudentCreateView(CreateView):
    model = User
    form_class = StudentCreationForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student-list")

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class StudentUpdateView(UpdateView):
    model = User
    form_class = StudentChangeForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student-list")

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class StudentDeleteView(DeleteView):
    model = User
    template_name = "student_confirm_delete.html"
    success_url = reverse_lazy("student-list")

# ===================== Course (Admin Only) =====================

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class CourseListView(ListView):
    model = Kursus
    template_name = "course_list.html"
    context_object_name = "courses"

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class CourseCreateView(CreateView):
    model = Kursus
    form_class = CourseForm
    template_name = "course_form.html"
    success_url = reverse_lazy("course-list")

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class CourseUpdateView(UpdateView):
    model = Kursus
    form_class = CourseForm
    template_name = "course_form.html"
    success_url = reverse_lazy("course-list")

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class CourseDeleteView(DeleteView):
    model = Kursus
    template_name = "course_confirm_delete.html"
    success_url = reverse_lazy("course-list")

class ModulMateriListView(ListView):
    model = Modul
    template_name = 'modul_materi_list.html' 
    context_object_name = 'modul_materis'
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Kursus, User
from django.db.models import Count
from .forms import StudentCreationForm, StudentChangeForm 
from django.utils.decorators import method_decorator
from .forms import CourseForm
from django.views.generic import ListView

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@method_decorator([login_required, user_passes_test(is_admin)], name="dispatch")
class CourseListView(ListView):
    model = Kursus
    template_name = "course_list.html"  
    context_object_name = "courses"

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
    success_url = reverse_lazy("student-list")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    total_mahasiswa = User.objects.filter(role='mahasiswa').count()
    total_dosen = User.objects.filter(role='dosen').count()
    total_kursus = Kursus.objects.count()

    # Data untuk chart
    kursus_populer = Kursus.objects.annotate(
        jumlah_mahasiswa = Count('mahasiswa_terdaftar')
    ).order_by('-jumlah_mahasiswa')[:5]

    context = {
        'total_mahasiswa': total_mahasiswa,
        'total_dosen': total_dosen,
        'total_kursus': total_kursus,
        'kursus_populer_labels': [k.judul for k in kursus_populer],
        'kursus_populer_data': [k.jumlah_mahasiswa for k in kursus_populer],
    }
    return render(request, 'dashboard.html', context)

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

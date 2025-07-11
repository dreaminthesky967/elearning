from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User, Kursus

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password'
        })

class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'mahasiswa'
        if commit:
            user.save()
        return user

class StudentChangeForm(UserChangeForm):
    password = None # Hapus field password dari form edit
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Kursus
        fields = ['judul', 'deskripsi', 'dosen', 'program_studi', 'mahasiswa_terdaftar']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'deskripsi': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg', 'rows': 4}),
            'dosen': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'program_studi': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg'}),
            'mahasiswa_terdaftar': forms.SelectMultiple(attrs={'class': 'w-full px-4 py-2 border rounded-lg h-48'}),
        }
        
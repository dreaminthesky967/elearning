from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User, Kursus

base_input_class = 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
base_textarea_class = base_input_class + ' resize-none'

# Login Form
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': base_input_class,
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': base_input_class + ' mt-2',
            'placeholder': 'Password'
        })

# Form Mahasiswa Baru
class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': base_input_class})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'mahasiswa'
        if commit:
            user.save()
        return user

# Form Edit Data Mahasiswa
class StudentChangeForm(UserChangeForm):
    password = None  # Hapus field password dari form edit

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': base_input_class})

# Form Kursus
class CourseForm(forms.ModelForm):
    class Meta:
        model = Kursus
        fields = ['judul', 'deskripsi', 'dosen', 'program_studi', 'mahasiswa_terdaftar']
        widgets = {
            'judul': forms.TextInput(attrs={'class': base_input_class}),
            'deskripsi': forms.Textarea(attrs={'class': base_textarea_class, 'rows': 4}),
            'dosen': forms.Select(attrs={'class': base_input_class}),
            'program_studi': forms.Select(attrs={'class': base_input_class}),
            'mahasiswa_terdaftar': forms.SelectMultiple(attrs={'class': base_input_class + ' h-48'}),
        }

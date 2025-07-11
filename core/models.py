from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class User(AbstractUser):
    ROLE_CHOISE = (
        ("admin", "Admin"),
        ("mahasiswa", "Mahasiswa"),
        ("dosen", "Dosen"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOISE, default="mahasiswa")
    phone_number = models.CharField(max_length=15, blank=True)
    
class programstudi(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    kode = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.nama
    
class Kursus(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    dosen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kursus_dosen', limit_choices_to={'role': 'dosen'})
    program_studi = models.ForeignKey(programstudi, on_delete=models.CASCADE,blank=True, related_name='kursus_terdaftar')
    mahasiswa_terdaftar = models.ManyToManyField(User, related_name='kursus_mahasiswa', blank=True,)
    
    def __str__(self):
        return self.judul
    
class Modul(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE, related_name='modul')
    judul = models.CharField(max_length=200)
    urutan = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['urutan']
        
    def __str__(self):
        return f"{self.kursus.judul} - Modul {self.urutan}: {self.judul}"
    
class Materi(models.Model):
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE, related_name='materi')
    judul = models.CharField(max_length=200)
    konten = models.TextField()
    file = models.FileField(upload_to='materi_files/', blank=True, null=True)
    urutan = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['urutan']
        
    def __str__(self):
        return self.judul
    
class ProgressBelajar(models.Model):
    mahasiswa = models.ForeignKey(User, on_delete=models.CASCADE)
    materi = models.ForeignKey(Materi, on_delete=models.CASCADE)
    selesai = models.BooleanField(default=False)
    tanggal_selesai = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('mahasiswa', 'materi')

    def __str__(self):
        return f"{self.mahasiswa.username} - {self.materi.judul}"
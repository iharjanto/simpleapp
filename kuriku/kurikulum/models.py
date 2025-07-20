from django.db import models

class CPL(models.Model):
    KATEGORI_CHOICES = [
        ('sikap', 'Sikap'),
        ('pengetahuan', 'Pengetahuan'),
        ('keterampilan', 'Keterampilan'),
    ]
    kode = models.CharField(max_length=20, unique=True)
    deskripsi = models.TextField()
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    
    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"

class Matakuliah(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100)
    sks = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    cpls = models.ManyToManyField(CPL, through='MatakuliahCPL', related_name='matakuliahs')
    
    def __str__(self):
        return f"{self.kode} - {self.nama}"

class MatakuliahCPL(models.Model):
    matakuliah = models.ForeignKey(Matakuliah, on_delete=models.CASCADE)
    cpl = models.ForeignKey(CPL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('matakuliah', 'cpl')

class CPMK(models.Model):
    kode = models.CharField(max_length=20)
    deskripsi = models.TextField()
    matakuliah = models.ForeignKey(Matakuliah, on_delete=models.CASCADE, related_name='cpmks')
    cpl = models.ForeignKey(CPL, on_delete=models.CASCADE, related_name='cpmks')
    
    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"
    
    class Meta:
        unique_together = ('kode', 'matakuliah')

class SubCPMK(models.Model):
    BENTUK_CHOICES = [
        ('teori', 'Perkuliahan Tatap Muka'),
        ('seminar', 'Presentasi/Seminar'),
        ('praktek', 'Praktikum/Laboratorium'),
        ('lapangan', 'Kuliah Lapangan/Industri'),
    ]
    kode = models.CharField(max_length=10)
    deskripsi = models.TextField()
    cpmk = models.ForeignKey(CPMK, on_delete= models.CASCADE, related_name = 'subcpmks')
    durasi =models.PositiveIntegerField(blank=True, default=5)
    bentuk = models.TextField(max_length = 20, choices=BENTUK_CHOICES, default = 'teori')
    indikator = models.TextField(blank=True, default = 'Mampu memahami....')
    
    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"
    class Meta:
        unique_together = ('kode', 'cpmk')
    

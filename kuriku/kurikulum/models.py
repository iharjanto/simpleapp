from django.db import models

# from .choices import KelompokMK, Pelaksanaan


class KelompokMK(models.IntegerChoices):
    """
    Jenis-jenis mata kuliah berdasarkan kurikulum
    """

    MKWK = 1, "Mata Kuliah Wajib Kurikulum (MKWK)"
    PENCIRI_UNIV = 2, "Mata Kuliah Penciri Universitas"
    WAJIB_PRODI = 3, "Mata Kuliah Wajib Prodi"
    PILIHAN_PRODI = 4, "Mata Kuliah Pilihan Prodi"
    WAJIB_PEMINATAN = 5, "Mata Kuliah Wajib Peminatan Prodi"
    PILIHAN_PEMINATAN = 6, "Mata Kuliah Pilihan Peminatan Prodi"
    TUGAS_AKHIR = 7, "Mata Kuliah Tugas Akhir"

    __empty__ = "Pilih Jenis Mata Kuliah"


class Pelaksanaan(models.IntegerChoices):
    """
    Jenis pelaksanaan kegiatan pembelajaran
    """

    TEORI = 1, "Teori"
    PRAKTEK = 2, "Praktek"
    SEMINAR_SIMULASI = 3, "Seminar/Simulasi"
    KULIAH_LAPANGAN = 4, "Kuliah Lapangan"
    TUGAS_AKHIR = 5, "Tugas Akhir"

    __empty__ = "-- Pilih Jenis Pelaksanaan --"


class CPL(models.Model):

    kode = models.CharField(max_length=20, unique=True)
    deskripsi = models.TextField()
    kategori = models.CharField(max_length=20, default="KK")
    sumber = models.CharField(max_length=50, default="Asosiasi")
    aspek = models.CharField(max_length=50, default="aspek")
    taksonomi = models.CharField(max_length=50, default="A5")

    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"


class Matakuliah(models.Model):
    kode = models.CharField(max_length=12, unique=True, editable=False)
    nama = models.CharField(max_length=100)
    sks = models.PositiveIntegerField(default=2)
    semester = models.PositiveIntegerField(default=3)
    kodeprodi = models.IntegerField(default=66)
    tahunkurikulum = models.IntegerField(default=25)
    kelompokmk = models.IntegerField(
        default=KelompokMK.WAJIB_PRODI, choices=KelompokMK.choices
    )
    basicscience = models.BooleanField(default=False)
    pelaksanaan = models.IntegerField(
        choices=Pelaksanaan.choices,
        default=Pelaksanaan.TEORI,
        verbose_name="Metode Pelaksanaan",
    )
    kkni = models.CharField(max_length=10, default="6")
    # foreignkey relation
    cpls = models.ManyToManyField(
        CPL, through="MatakuliahCPL", related_name="matakuliahs"
    )

    def _generate_kode(self):
        _kode = f"{self.kodeprodi}{self.tahunkurikulum}{self.kelompokmk}{self.sks}{self.pelaksanaan}{self.kkni}{self.pk:02d}"
        return _kode

    def save(self, *args, **kwargs):
        if not self.kode:
            self.kode = self._generate_kode()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class MatakuliahCPL(models.Model):
    matakuliah = models.ForeignKey(Matakuliah, on_delete=models.CASCADE)
    cpl = models.ForeignKey(CPL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("matakuliah", "cpl")


class CPMK(models.Model):
    kode = models.CharField(max_length=20)
    deskripsi = models.TextField()
    matakuliah = models.ForeignKey(
        Matakuliah, on_delete=models.CASCADE, related_name="cpmks"
    )
    cpl = models.ForeignKey(CPL, on_delete=models.CASCADE, related_name="cpmks")

    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"

    class Meta:
        unique_together = ("kode", "matakuliah")


class SubCPMK(models.Model):
    BENTUK_CHOICES = [
        ("teori", "Perkuliahan Tatap Muka"),
        ("seminar", "Presentasi/Seminar"),
        ("praktek", "Praktikum/Laboratorium"),
        ("lapangan", "Kuliah Lapangan/Industri"),
    ]
    kode = models.CharField(max_length=10)
    deskripsi = models.TextField()
    cpmk = models.ForeignKey(
        CPMK, on_delete=models.CASCADE, related_name="subcpmks", blank=True
    )
    durasi = models.PositiveIntegerField(blank=True, default=5)
    bentuk = models.TextField(max_length=20, choices=BENTUK_CHOICES, default="teori")
    indikator = models.TextField(blank=True, default="Mampu memahami....")
    bobot = models.PositiveIntegerField(default=5)
    jenistugas = models.CharField(
        max_length=40, default="Tugas Latihan Soal", blank=True
    )

    def __str__(self):
        return f"{self.kode} - {self.deskripsi}"

    class Meta:
        unique_together = ("kode", "cpmk")

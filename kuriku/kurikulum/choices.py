from django.db import models
"""
kode kelompok mk
1. Kode 1 untuk Mata Kuliah MKWK
2. Kode 2 untuk Mata Kuliah Penciri Universitas
3. Kode 3 untuk Mata Kuliah Wajib Prodi
4. Kode 4 untuk Mata Kuliah Pilihan Prodi
5. Kode 5 untuk Mata Kuliah Wajib Peminatan Prodi (Jika ada)
6. Kode 6 untuk Mata Kuliah Pilihan Peminatan Prodi (Jika ada)
7. Kode 7 untuk Mata Kuliah Tugas Akhir
"""


class KelompokMK(models.IntegerChoices):
    """
    Jenis-jenis mata kuliah berdasarkan kurikulum
    """
    MKWK = 1, 'Mata Kuliah Wajib Kurikulum (MKWK)'
    PENCIRI_UNIV = 2, 'Mata Kuliah Penciri Universitas'
    WAJIB_PRODI = 3, 'Mata Kuliah Wajib Prodi'
    PILIHAN_PRODI = 4, 'Mata Kuliah Pilihan Prodi'
    WAJIB_PEMINATAN = 5, 'Mata Kuliah Wajib Peminatan Prodi'
    PILIHAN_PEMINATAN = 6, 'Mata Kuliah Pilihan Peminatan Prodi'
    TUGAS_AKHIR = 7, 'Mata Kuliah Tugas Akhir'

    __empty__ = 'Pilih Jenis Mata Kuliah'

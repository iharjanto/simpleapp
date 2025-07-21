from django.contrib import admin
from .models import Matakuliah, CPL, MatakuliahCPL, CPMK, SubCPMK
# Register your models here.

class MKCPLInline(admin.StackedInline):
    model = MatakuliahCPL
    extra = 1

@admin.register(Matakuliah)
class MatakuliahModel(admin.ModelAdmin):
    list_display = ['nama', 'sks', 'semester']
    list_filter = ['semester']
    search_fields = ['nama']
    inlines = [MKCPLInline]


@admin.register(CPL)
class CPLAdmin(admin.ModelAdmin):
    list_display = ('kode', 'deskripsi')

@admin.register(CPMK)
class CPMKAdmin(admin.ModelAdmin):
    list_display = ('kode', 'deskripsi')

@admin.register(SubCPMK)
class SubcpmkAdmin(admin.ModelAdmin):
    list_display = ('kode', 'deskripsi')

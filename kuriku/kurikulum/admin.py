from django.contrib import admin
from .models import Matakuliah, CPL, CPMK, SubCPMK


class MatakuliahAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama")
    search_fields = ("kode", "nama")


class CPLinline(admin.TabularInline):
    model = Matakuliah.cpls.through
    extra = 1


class CPMKInline(admin.TabularInline):
    model = CPMK
    extra = 1


class SUbCPMKInline(admin.TabularInline):
    model = SubCPMK
    extra = 1


admin.site.register(Matakuliah, inlines=[CPMKInline])
admin.site.register(CPL, inlines=[CPLinline])
admin.site.register(CPMK, inlines=[SUbCPMKInline])
admin.site.register(SubCPMK)

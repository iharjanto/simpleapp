from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.shortcuts import render, get_object_or_404
from .models import Matakuliah, CPL, CPMK, SubCPMK
from .serializers import ListMK, MatakuliahSerializer


class MKList(generics.ListCreateAPIView):
    queryset = Matakuliah.objects.all()
    serializer_class = ListMK


class MKDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matakuliah.objects.all()
    serializer_class = MatakuliahSerializer


def matakuliah_table(request):
    matakuliahs = Matakuliah.objects.all().order_by("semester")
    # Group by semester
    grouped = {}
    for mk in matakuliahs:
        grouped.setdefault(mk.semester, []).append(mk)
    return render(
        request,
        "kurikulum/matakuliah_table.html",
        {"grouped_matakuliahs": grouped},
    )


def matakuliah_detail(request, pk):
    mk = Matakuliah.objects.prefetch_related("cpls__cpmks__subcpmks").get(pk=pk)
    data = []
    for cpl in mk.cpls.all():
        cpl_data = {"cpl": cpl, "cpmks": []}
        for cpmk in cpl.cpmks.filter(matakuliah=mk):
            subcpmks = cpmk.subcpmks.all()
            cpl_data["cpmks"].append({"cpmk": cpmk, "subcpmks": subcpmks})
            for subcpmk in subcpmks:
                data.append({"cpl": cpl, "cpmk": cpmk, "subcpmk": subcpmk})
    return render(
        request,
        "kurikulum/matakuliah_detail.html",
        {"matakuliah": mk, "cpl_data": data},
    )


def matriks_cpl_mk(request):
    semesters = sorted(Matakuliah.objects.values_list("semester", flat=True).distinct())
    cpls = CPL.objects.all()
    matakuliahs = Matakuliah.objects.all()

    # Matriks: {cpl: {semester: [(matakuliah, sks), ...]}}
    matriks = {}
    for cpl in cpls:
        matriks[cpl] = {}
        for semester in semesters:
            mks = matakuliahs.filter(semester=semester, cpls=cpl)
            matriks[cpl][semester] = [(mk, mk.sks) for mk in mks]

    context = {
        "semesters": semesters,
        "cpls": cpls,
        "matriks": matriks,
    }
    return render(request, "kurikulum/matriks_cpl_mk.html", context)

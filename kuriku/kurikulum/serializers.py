from rest_framework import serializers
from .models import Matakuliah, CPL, CPMK, MatakuliahCPL, SubCPMK


class SubCPMKSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCPMK
        fields = ["id", "kode", "deskripsi"]


class CPMKSerializer(serializers.ModelSerializer):
    subcpmks = SubCPMKSerializer(many=True, read_only=True)

    class Meta:
        model = CPMK
        fields = ["kode", "deskripsi", "cpl", "subcpmks"]


class CPLSerializer(serializers.ModelSerializer):
    cpmks = CPMKSerializer(many=True, read_only=True)

    class Meta:
        model = CPL
        fields = ["id", "kode", "deskripsi", "aspek", "cpmks"]


class ListMK(serializers.ModelSerializer):
    class Meta:
        model = Matakuliah
        fields = [
            "id",
            "kode",
            "nama",
            "kode",
            "sks",
            "semester",
            "pelaksanaan",
            "kelompokmk",
            "basicscience",
        ]


class MatakuliahSerializer(serializers.ModelSerializer):
    cpls = serializers.SerializerMethodField()

    class Meta:
        model = Matakuliah
        fields = [
            "id",
            "kode",
            "nama",
            "kode",
            "semester",
            "pelaksanaan",
            "kelompokmk",
            "basicscience",
            "cpls",
        ]

    def get_cpls(self, obj):
        # Get all CPLs associated with this matakuliah through MatakuliahCPL
        matakuliah_cpls = MatakuliahCPL.objects.filter(matakuliah=obj).select_related(
            "cpl"
        )

        # For each CPL, get its CPMKs that belong to this matakuliah
        cpl_data = []
        for matakuliah_cpl in matakuliah_cpls:
            cpl = matakuliah_cpl.cpl
            cpmks = CPMK.objects.filter(matakuliah=obj, cpl=cpl)

            cpl_serializer = CPLSerializer(cpl)
            cpl_data_item = cpl_serializer.data
            cpl_data_item["cpmks"] = CPMKSerializer(cpmks, many=True).data
            cpl_data.append(cpl_data_item)

        return cpl_data


class MatakuliahCPLSerializer(serializers.ModelSerializer):
    cpl = CPLSerializer(many=True)
    matakuliah = MatakuliahSerializer(read_only=True, many=True)

    class Meta:
        model = MatakuliahCPL
        fields = ["cpl", "matakuliah"]

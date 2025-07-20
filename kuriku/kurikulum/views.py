from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Matakuliah, CPMK, CPL, MatakuliahCPL, SubCPMK
from .serializers import MatakuliahSerializer, CPMKSerializer, CPLSerializer, MatakuliahCPLSerializer, SubCPMKSerializer

class SubCPMKViewSet(viewsets.ModelViewSet):
    queryset = SubCPMK.objects.all()
    serializer_class = SubCPMKSerializer


class CPLViewSet(viewsets.ModelViewSet):
    queryset = CPL.objects.all().prefetch_related( 'cpmks')
    serializer_class = CPLSerializer
    # lookup_field = 'kode'


class MatakuliahViewSet(viewsets.ModelViewSet):
    queryset = Matakuliah.objects.all().prefetch_related('cpls', 'cpmks')
    serializer_class = MatakuliahSerializer
    # lookup_field = 'kode'
    
    @action(detail=True, methods=['post'])
    def add_cpl(self, request, pk=None):
        """
        Add a CPL to this matakuliah through matakuliahcpl relation.
        Expected input: {'cpl': 'cpl_id'}
        """
        matakuliah = self.get_object()
        cpl_id = request.data.get('cpl')
        
        if not cpl_id:
            return Response(
                {'error': 'CPL field is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cpl = CPL.objects.get(pk=cpl_id)
        except CPL.DoesNotExist:
            return Response(
                {'error': 'CPL not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if relation already exists
        if MatakuliahCPL.objects.filter(matakuliah=matakuliah, cpl=cpl).exists():
            return Response(
                {'error': 'This CPL is already associated with the matakuliah'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the relation
        MatakuliahCPL.objects.create(matakuliah=matakuliah, cpl=cpl)
        
        return Response(
            {'success': f'CPL {cpl.id} added to matakuliah {matakuliah.id}'},
            status=status.HTTP_201_CREATED
        )
    @action(detail=True, methods=['post', 'put'])
    def add_cpmk(self,request, pk=None):
        """_summary_
        Memasukkan data cpmk , dengan mengecek apakah sdh ada cpl di matakuliah ini
        cek table matakuliahcpl, jika ada, masukkan cpmk berdasar id cpl
               
        Args:
        input yang diharapkan: kode, deskripsi, matakuliah, cpl
        Returns:
            _type_: _description_
        """
        # ambil argument : 
        mk = self.get_object()
        cpl_id = request.data.get('cpl')
        kode = request.data.get('kode')
        deskripsi = request.data.get('deskripsi')
        
        if not all([cpl_id, kode, deskripsi]):
            return Response(
                {'error': 'Data tidak lengkap'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # cek apakah cpl dan mk ada di table matakliah cpl
        try:
            cpl = CPL.objects.get(pk=cpl_id)
        except MatakuliahCPL.DoesNotExist:
            return Response(
                {"error": "Tidak ada relasi matakuliah dan CPL"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        if MatakuliahCPL.objects.filter(matakuliah = mk, cpl = cpl).exists():
                CPMK.objects.get_or_create(
                    kode=kode, cpl=cpl, deskripsi = deskripsi, matakuliah = mk
                )
                return Response(
                    {"success": f"data {cpl_id} - {kode} -{deskripsi}"},
                    status=status.HTTP_201_CREATED
                )
        

class MatakuliahCPLViewSet(viewsets.ModelViewSet):
    queryset = MatakuliahCPL.objects.all().prefetch_related('cpls', 'cpmks')
    serializer_class = MatakuliahCPLSerializer


class CPMKViewSet(viewsets.ModelViewSet):
    queryset = CPMK.objects.all()
    serializer_class = CPMKSerializer
    lookup_field = 'kode'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        matakuliah_kode = self.request.query_params.get('matakuliah', None)
        if matakuliah_kode is not None:
            queryset = queryset.filter(matakuliah__kode=matakuliah_kode)
        return queryset
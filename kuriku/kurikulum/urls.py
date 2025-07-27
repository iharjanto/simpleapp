from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kurikulum import views

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("api/matakuliah/", views.MKList.as_view(), name="matakuliah-api"),
    path("api/matakuliah/<int:pk>/", views.MKDetail.as_view(), name="matakuliah-detail-api"),
    path("matakuliah/", views.matakuliah_table, name="matakuliah-table"),
    path(
        "matakuliah/<int:pk>/detail/", views.matakuliah_detail, name="matakuliah-detail"
    ),
    path("matriks-cpl-mk/", views.matriks_cpl_mk, name="matriks-cpl-mk"),
]

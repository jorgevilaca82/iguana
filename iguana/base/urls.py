from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.pessoa_fisica import PessoaFisicaDetail, PessoaFisicaList

urlpatterns = format_suffix_patterns(
    [
        path(
            "api/pessoafisica/",
            PessoaFisicaList.as_view(),
            name="pessoafisica-list",
        ),
        path(
            "api/pessoafisica/<int:pk>/",
            PessoaFisicaDetail.as_view(),
            name="pessoafisica-detail",
        ),
    ]
)

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.pessoa_fisica import PessoaFisicaList

urlpatterns = format_suffix_patterns(
    [
        path("api/pessoafisica/", PessoaFisicaList.as_view(), name="pessoafisica-list"),
        # path('pessoafisica/<int:pk>/', pessoa_fisica),
    ]
)

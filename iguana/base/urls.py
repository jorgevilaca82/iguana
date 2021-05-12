from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns(
    [
        path(
            "api/pessoafisica/",
            views.PessoaFisicaListCreateAPIView.as_view(),
            name="pessoafisica-list",
        ),
        path(
            "api/pessoafisica/<int:pk>/",
            views.PessoaFisicaRetrieveUpdateDestroyAPIView.as_view(),
            name="pessoafisica-detail",
        ),
    ]
)

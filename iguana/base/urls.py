from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

pf_list_view = views.PessoaFisicaListCreateAPIView.as_view()
pf_detail_view = views.PessoaFisicaRetrieveUpdateDestroyAPIView.as_view()
pj_list_view = lambda request: None
pj_detail_view = lambda request: None
user_telefone_list_view = views.UserTelefoneListCreateAPIView.as_view()
user_telefone_detail_view = views.UserTelefoneRetrieveUpdateDestroyAPIView.as_view()
user_endereco_list_view = views.UserEnderecoListCreateAPIView.as_view()
user_endereco_detail_view = views.UserEnderecoRetrieveUpdateDestroyAPIView.as_view()

user_telefone_patterns = lambda prefix: [
    path(
        "<int:user_pk>/",
        include(
            [
                path(
                    "telefone/",
                    user_telefone_list_view,
                    name=f"{prefix}-telefone-list",
                ),
                path(
                    "telefone/<int:pk>/",
                    user_telefone_detail_view,
                    name=f"{prefix}-telefone-detail",
                ),
            ]
        ),
    ),
]

user_endereco_patterns = lambda prefix: [
    path(
        "<int:user_pk>/",
        include(
            [
                path(
                    "endereco/",
                    user_endereco_list_view,
                    name=f"{prefix}-endereco-list",
                ),
                path(
                    "endereco/<int:pk>/",
                    user_endereco_detail_view,
                    name=f"{prefix}-endereco-detail",
                ),
            ]
        ),
    ),
]

urlpatterns = format_suffix_patterns(
    [
        path(
            "api/pessoafisica/",
            include(
                [
                    path("", pf_list_view, name="pessoafisica-list"),
                    path("<int:pk>/", pf_detail_view, name="pessoafisica-detail"),
                ]
                + user_telefone_patterns("pessoafisica")
                + user_endereco_patterns("pessoafisica")
            ),
        ),
        path(
            "api/pessoajuridica/",
            include(
                [
                    path("", pj_list_view, name="pessoajuridica-list"),
                    path("<int:pk>/", pj_detail_view, name="pessoajuridica-detail"),
                ]
                + user_telefone_patterns("pessoajuridica")
                + user_endereco_patterns("pessoajuridica")
            ),
        ),
    ]
)

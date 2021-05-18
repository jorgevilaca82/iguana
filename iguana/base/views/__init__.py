from .pessoa_fisica import (
    PessoaFisicaListCreateAPIView,
    PessoaFisicaRetrieveUpdateDestroyAPIView,
)
from .user import (
    UserTelefoneListCreateAPIView,
    UserTelefoneRetrieveUpdateDestroyAPIView,
    UserEnderecoListCreateAPIView,
    UserEnderecoRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "PessoaFisicaListCreateAPIView",
    "PessoaFisicaRetrieveUpdateDestroyAPIView",
    "UserTelefoneListCreateAPIView",
    "UserTelefoneRetrieveUpdateDestroyAPIView",
    "UserEnderecoListCreateAPIView",
    "UserEnderecoRetrieveUpdateDestroyAPIView",
]

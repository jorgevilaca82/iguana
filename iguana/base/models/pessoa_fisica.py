from iguana.base.models.user import User


class PessoaFisica(User):
    @property
    def nome_completo(self):
        return self.get_full_name()

    @nome_completo.setter
    def nome_completo(self, value):
        splited = value.split()
        self.first_name = splited[0]
        self.last_name = " ".join(splited[1:])

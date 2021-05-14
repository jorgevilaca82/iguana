# Iguana

Iguana é um projeto de uma API Rest base usando Django forncendo funcionalidades para casos comuns de cadastros em sistemas de informação no Brasil.

## Executando o ambiente de desenvolvimento

### Depedências
* [Python >= 3.6](https://www.python.org/)
* [Poetry](https://python-poetry.org/docs/#installation)

No diretório do projeto execute:
```sh
$ poetry install
$ poetry shell
$ echo "from sgi.settings import *" > local_settings.py
$ # 👆 Ajuste suas configurações locais antes de prosseguir!
$ export DJANGO_SETTINGS_MODULE="local_settings"
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py test
$ python manage.py runserver
```

Os comandos acima executam as seguintes tarefas, na seqûencia:
* Instalação das dependências do projeto
* Ativação do ambiente virtual python
* Criação o arquivo local de configurações
* Configuração de variável de ambiente apontando para o arquivo de configurações local
* Migração do banco de dados
* Coleta arquivos estáticos para o diretório correto
* Execução do framework de testes
* Execução do projeto em ambiente de desenvolvimento
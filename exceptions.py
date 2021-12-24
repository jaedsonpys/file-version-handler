class Base(Exception):
    pass


class RepoAlreadyExists(Base):
    def __init__(self):
        super().__init__('Já existe um repositório neste diretório.')

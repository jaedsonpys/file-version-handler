# Copyright © 2021 - Jaedson Silva
#
# O FVH (File Version Handler) foi
# desenvolvido a fins de aprendizado. #

import os
from datetime import datetime

import sys
import json
from base64 import b64encode, b64decode

from exceptions import RepoAlreadyExists

DEFAULT_DIRNAME = '.fvh'
FVH_FILE_LOCAL = '.fvh/.json'


class FVH:
    def __init__(self) -> None:
        self.pwd = os.getcwd()

        # atributos padrões
        self._file_queue = dict()
        self._last_add = None
        self._last_change = None

    @classmethod
    def repo_already_exists(cls) -> bool:
        """Verifica se o repositório
        já existe, retornando True ou False.

        :return: bool
        """

        # Esse método pode ser usado
        # fora da classe para verificar
        # se já existe um repositório antes
        # de criar um, evitando o tratamento
        # de exceções.

        if not os.path.isfile(FVH_FILE_LOCAL):
            return False

        return True

    @staticmethod
    def _get_fvh_file() -> dict:
        try:
            with open(FVH_FILE_LOCAL, 'r') as fvh_file:
                fvh_file_content = json.load(fvh_file)
        except FileNotFoundError:
            raise FileNotFoundError('Arquivo de configuração FVH não encontrado.')

        return fvh_file_content

    @staticmethod
    def _save_fvh_file(fvh_content: dict) -> None:
        try:
            with open(FVH_FILE_LOCAL, 'w') as fvh_file:
                json.dump(fvh_content, fvh_file, indent=2)
        except BaseException as error:
            print(error)

    def create_new_repo(self) -> None:
        """Cria um novo repositório
        no diretório atual.

        Se um repositório já existir,
        uma excecão é lançada.

        :return: None
        """

        repo_exists = self.repo_already_exists()
        if repo_exists:
            raise RepoAlreadyExists

        try:
            os.mkdir(DEFAULT_DIRNAME)
            fvh_default_obj = {'info': {}, 'add': {}, 'changes': {}}

            time = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            fvh_default_obj['info']['create'] = time

            self._save_fvh_file(fvh_default_obj)
        except BaseException as error:
            raise error


if __name__ == '__main__':
    teste = FVH()
    teste.create_new_repo()

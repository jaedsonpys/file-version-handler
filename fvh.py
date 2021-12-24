# Copyright © 2021 - Jaedson Silva
#
# O FVH (File Version Handler) foi
# desenvolvido a fins de aprendizado. #

import os
from datetime import datetime
from random import randint, choice
from string import ascii_letters

import sys
import json
from base64 import b64encode, b64decode
from hashlib import md5

from exceptions import RepoAlreadyExists
from log import log

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
    def _generate_file_prefix():
        prefix = f'p{randint(1000, 9999)}'
        return prefix

    @staticmethod
    def _generate_change_id():
        change_id = ''.join([choice(ascii_letters) for __ in range(12)])
        return change_id

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
                json.dump(fvh_content, fvh_file, indent=4)
        except BaseException as error:
            print(error)

    def _get_last_change_of_file(self, fprefix: str) -> [dict, None]:
        fvh_changes = self._get_fvh_file()['add']
        last_change_info = None

        for change_id in fvh_changes.keys():
            if fprefix in change_id:
                last_change_info = fvh_changes.get(change_id)

        return last_change_info

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

        log('Repositório criado.', 'sucess')

    def add(self, files: list) -> bool:
        """Adiciona os arquivos
        para serem rastreados.

        Após isso, o FVH detectará
        mudanças nos arquivos que foram
        adicionados.

        :param files: Lista de arquivos
        :return: bool
        """

        fvh_content = self._get_fvh_file()
        fvh_added_files = fvh_content.get('add')

        # Se ainda não houver arquivos
        # adicionados, pula para a próxima
        # etapa.

        if fvh_added_files:
            # Filtrando arquivos
            # que já estão sendo rastreados.

            for fprefix, info in fvh_added_files.items():
                if info['file'] in files:
                    files.remove(info['file'])

        for file in files:
            file_prefix = self._generate_file_prefix()

            with open(file, 'rb') as _file:
                file_content = _file.read()
                file_hash = md5(file_content).hexdigest()

            new_add_data = {'file': file, 'hash': file_hash}
            fvh_content['add'][file_prefix] = new_add_data

        log(f'{len(files)} arquivos adicionados.', 'sucess')
        self._save_fvh_file(fvh_content)


if __name__ == '__main__':
    test = FVH()
    test.create_new_repo()

    test.add(['fvh.py', 'exceptions/__init__.py'])

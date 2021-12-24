# Copyright © 2021 - Jaedson Silva
#
# O FVH (File Version Handler) foi
# desenvolvido a fins de aprendizado. #

import os
from datetime import datetime
from random import randint, choice
from string import ascii_letters

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
    def _generate_file_prefix() -> str:
        prefix = f'p{randint(1000, 9999)}'
        return prefix

    @staticmethod
    def _generate_change_id(fprefix: str) -> str:
        change_id = ''.join([choice(ascii_letters) for __ in range(12)])
        return f'{change_id}.{fprefix}'

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
                json.dump(fvh_content, fvh_file, indent=4, ensure_ascii=False)
        except BaseException as error:
            print(error)

    @staticmethod
    def _create_change(file_data: dict, description: str) -> dict:
        # Prepara as informações para criar
        # uma nova change.

        new_change = {'description': description}

        file_data_base64 = b64encode(json.dumps(file_data).encode())

        new_change['time'] = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        new_change['base'] = file_data_base64.decode()

        return new_change

    @staticmethod
    def _set_lines_number(file) -> dict:
        # Esse método define a contagem
        # de linhas em um dicionário para
        # posteriormente, checar mudanças.
        #
        # Resultado: {1: 'Linha 1', 2: 'Linha 2'}

        file_content = file.readlines()
        file.close()

        file_with_lines_number = {}
        for c, l in enumerate(file_content):
            c += 1
            file_with_lines_number[c] = l.replace('\n', '')

        return file_with_lines_number

    def _check_difference(self, pre_change: dict, fprefix: str) -> dict:
        # Para obter a diferença entre as mudanças
        # dos arquivos, é necessário juntar todas
        # as outras mudanças. Assim, obtemos
        # a diferença e retornamos para que seja
        # salva no arquivo FVH na chave "changes".

        joined_changes = self.join_changes(fprefix)
        difference = {}

        for number, line in pre_change.items():
            line_of_all_changes = joined_changes.get(str(number))

            if line_of_all_changes != line:
                difference[number] = line

        return difference

    def _get_all_changes_of_file(self, fprefix: str) -> list:
        fvh_changes = self._get_fvh_file()['changes']
        all_changes = []

        for change_id in fvh_changes.keys():
            if fprefix in change_id:
                all_changes.append(fvh_changes.get(change_id))

        return all_changes

    def _get_last_change_of_file(self, fprefix: str) -> [dict, None]:
        fvh_changes = self._get_fvh_file()['changes']
        last_change_info = None

        for change_id in fvh_changes.keys():
            if fprefix in change_id:
                last_change_info = fvh_changes.get(change_id)

        return last_change_info

    def join_changes(self, fprefix: str) -> dict:
        """Junta todas as alterações de um arquivo.

        :param fprefix: Prefixo do arquivo (ID)
        :return: Retorna o arquivo após juntar as
        mudanças.
        """

        all_changes_file = self._get_all_changes_of_file(fprefix)
        joined_changes = {}

        for change in all_changes_file:
            change_base = change['base'].encode()
            change_file_data = json.loads(b64decode(change_base))

            for number, line in change_file_data.items():
                joined_changes[number] = line

        return joined_changes

    def get_all_changes(self) -> dict:
        fvh_changes = self._get_fvh_file()['changes']
        all_changes = {}

        for change_id, value in fvh_changes.items():
            all_changes[change_id] = value

        return all_changes

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

    def add(self, files: list) -> None:
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

    def change(self, description: str) -> None:
        """Publica uma nova mudança no
        histórico de versões do arquivo.

        :param description: Descrição da change
        :return: None
        """

        fvh_content = self._get_fvh_file()
        fvh_added_files = fvh_content.get('add')

        for fprefix, info in fvh_added_files.items():
            last_change_info = self._get_last_change_of_file(fprefix)

            file_with_lines = self._set_lines_number(open(info['file']))
            change_id = self._generate_change_id(fprefix)

            if not last_change_info:
                new_change = self._create_change(file_with_lines, description)
                fvh_content['changes'][change_id] = new_change
                continue

            difference_of_changes = self._check_difference(file_with_lines, fprefix)

            new_change = self._create_change(difference_of_changes, description)
            fvh_content['changes'][change_id] = new_change

        self._save_fvh_file(fvh_content)


if __name__ == '__main__':
    test = FVH()

    if not test.repo_already_exists():
        test.create_new_repo()
        test.add(['teste.txt'])

    test.change(input('Description: '))

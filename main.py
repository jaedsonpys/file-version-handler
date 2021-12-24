from fvh import FVH
import sys
import os

fvh = FVH()

ARGS = {
    'add': {
        'options': ['-all', '--help'],
        'help': 'Adiciona os arquivos no rastreamento de mudanças.',
    },
    'change': {
        'options': ['-desc', '--help'],
        'help': 'Salva uma versão dos arquivos que estão adicionados.',
    },
    'init': {
        'options': ['--help'],
        'help': 'Inicia um novo repositório vazio.',
    }
}


def get_all_files():
    files = []

    for r, d, f in os.walk(os.getcwd()):
        if f:
            for i in f:
                files.append(f'{r}/{i}')

    return files


def view_args():
    print('Uso do FVH (File Version Handler): \n')
    print('Argumentos: ')

    for key, values in ARGS.items():
        print(f'    {key}: opções: {values["options"]}')
        print(f'    help: {values["help"]}')
        print()


def args_redirect():
    args = sys.argv[1:]

    if args[0] == '--help':
        view_args()
        return

    command = ARGS.get(args[0])

    if not command:
        print(f'Argumento não reconhecido: {args[0]}.')
        print('Digite --help para ver a lista de argumentos.')
        return

    # redirect commands
    if args[0] == 'init':
        if fvh.repo_already_exists():
            print('\033[31mJá existe um repositório neste local.\033[m')
        else:
            fvh.create_new_repo()

    elif args[0] == 'add':
        if 1 < len(args[1:]) > 1:
            print('\033[31mFalta de opções. Tente: add --help\033[m')
            exit(0)

        if args[1] == '-a':
            all_files = get_all_files()
            fvh.add(all_files)
        elif args[1] == '--help':
            print(f'add: options: {command["options"]}')
            print(f'help: {command["help"]}')
        else:
            if os.path.isfile(args[1]):
                fvh.add([args[1]])
            else:
                print(f'add: Erro: {args[1]} não é um arquivo.')

    elif args[0] == 'change':
        if 2 < len(args[1:]) > 2:
            print('\033[31mFalta de opções. Tente: change --help\033[m')
            exit(0)

        if args[1] == '-desc':
            description = args[2].replace("'", '')
            fvh.change(description)

            print()
            print(fvh.join_changes('p8211'))
        elif args[1] == '--help':
            print(f'change: options: {command["options"]}')
            print(f'help: {command["help"]}')
        else:
            print(f'\033[31m{args[1]} não foi reconhecido. Tente: change --help\033[m')


args_redirect()

def log(message: str, _type: str):
    """Imprime uma mensagem
    no console.

    Tipos de erros:
        error
        warning
        sucess
        debug
    """

    red = '\033[1;31m'
    green = '\033[1;32m'
    yellow = '\033[1;33m'

    close = '\033[m'

    if _type == 'error':
        print(red + message + close)
    elif _type == 'warning':
        print(yellow + message + close)
    elif _type == 'sucess':
        print(green + message + close)
    elif _type == 'debug':
        print(message)

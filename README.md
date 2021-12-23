# FVH - File Version Handler

Um gerenciador de versões de arquivos escrito em Python. Acompanhe todo o histórico de versões do seu arquivo
e consiga recuperar desde a primeira atualização. 🐍

## Guia

- [Funcionamento](#Funcionamento)
  - [Rastrear arquivos](#Rastrear-arquivos)
  - [Detectar mudanças](#Detectar-mudanças)
  - [Realizar uma change](#Realizar-uma-change)
  
 # Funcionamento
 
Entenda como funciona o FVH.

## Rastrear arquivos

Para que as mudanças sejam detectadas, os arquivos primeiro precisam ser adicionados ao rastreamento,que,quando
adicionado, um hash do arquivo é gerado e gravado no arquivo JSON no diretório .fvh.

Outra informação, também muito importante para o funcionamento é o prefixo do arquivo. O prefixo do arquivo é uma
identificação para o arquivo que está sendo adicionado, que será usado mais a frente para realizar uma change.

A partir disso, podemos comparar os hashes e saber se houve alguma mudança.

Após adicionar um arquivo, o arquivo JSON do FVH ficará assim:

```json
{
  "info": {
      "create": "23/12/2021, 17:28:02"
  },
  "changes": {}
  "add": {
      "p2504": {
        "file": "fvh.py",
        "hash": "1bfc026dac92bbf8c1a98983cd5c7871"
      },
  },
}
```

Um novo objeto com as informações citadas acima sempre é adicionando em **"add"** quando um arquivo é adicionado.

## Detectar mudanças



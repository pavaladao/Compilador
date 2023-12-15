import pandas as pd
from scanner import Scanner
from static import palavras_reservadas
from scanner import Token

if __name__ == "__main__":
    # print(TokenType.NUM.value, type(TokenType.NUM))
    # inicializa tabela de simbolos:
    tabela_simbolos = {}
    for item in palavras_reservadas:
        tabela_simbolos[item] = Token(item, item, item)

    with Scanner("tabelas\\automato lexico tabela.csv", "teste.txt") as scanner:
        n = ""
        while n != "EOF":
            token = scanner.gerar_token(tabela_simbolos)
            n = token.classe
            print(
                "Classe : ",
                token.classe,
                "|Lexema : ",
                token.lexema,
                "|Tipo : ",
                token.tipo,
            )

import pandas as pd
from scanner import Scanner
from sintatico import AnalisadorSintaticoLR
from tabela_de_simblos import tabela_simbolos

if __name__ == "__main__":
    scanner = Scanner(
        tabela_simbolos,
        tabela_estados="tabelas\\automato lexico tabela.csv",
        entrada="entradas\\teste.txt",
    )

    analisador = AnalisadorSintaticoLR(
        scanner,
        tabela_slr1=".\\tabelas\\slr1-parsing-table.csv",
        producoes=".\\tabelas\\producoes.csv",
        tabela_follow=".\\tabelas\\conjunto_follow.csv",
    )

    analisador.analisar()

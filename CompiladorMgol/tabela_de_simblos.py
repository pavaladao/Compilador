from static import palavras_reservadas
from scanner import Token

tabela_simbolos = {}
for item in palavras_reservadas:
    tabela_simbolos[item] = Token(item, item, item)

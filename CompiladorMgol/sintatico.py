import pandas as pd
from ler import ler_tabela_sintatico, ler_producoes, ler_tabela_follow


def ler_tabelas_slr(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, skiprows=2, index_col=0)

    acoes = df.filter(like="s", axis=1)
    gotos = df.drop(acoes.columns, axis=1)

    return acoes, gotos


class AnalisadorSintaticoLR:
    def __init__(self, scanner, tabela_slr1, producoes, tabela_follow):
        self.pilha = [0]
        self.scanner = scanner
        self.acoes, self.gotos = ler_tabela_sintatico(tabela_slr1)
        self.producoes = producoes
        self.tabela_follow = ler_tabela_follow(tabela_follow)

    def shift(self, estado, simbolo):
        self.pilha.append(simbolo)
        self.pilha.append(estado)

    def reduce(self, producao):
        lado_esquerdo, lado_direito, qtd_pop = producao

        for _ in range(2 * qtd_pop):
            self.pilha.pop()

        estado_atual = int(self.pilha[-1])
        estado_goto = self.gotos.loc[estado_atual, lado_esquerdo]
        self.pilha.append(lado_esquerdo)
        self.pilha.append(estado_goto)

        print(f"Reduzido: {lado_esquerdo} -> {lado_direito}")

    def obter_producao(self, id_producao):
        tabela_producoes = ler_producoes(self.producoes)
        return (
            tabela_producoes["LE"][id_producao],
            tabela_producoes["LD"][id_producao],
            tabela_producoes["POPS"][id_producao],
        )

    def analisar(self):
        simbolo_atual = self.scanner.gerar_token().classe
        while True:
            estado_atual = int(self.pilha[-1])
            acao = self.acoes[simbolo_atual][estado_atual]

            if acao.startswith("s"):
                _, proximo_estado = acao.split("s")
                self.shift(int(proximo_estado), simbolo_atual)
                print(
                    "estado atual: {}, leu o token : {}, shift para o estado : {} || pilha : {}".format(
                        estado_atual, simbolo_atual, proximo_estado, self.pilha
                    )
                )
                simbolo_atual = self.scanner.gerar_token().classe

            elif acao.startswith("r"):
                _, producao = acao.split("r")
                self.reduce(self.obter_producao(int(producao)))
                print(
                    "estado atual: {}, leu o token : {}, reduce para o estado : {} || pilha : {}".format(
                        estado_atual, simbolo_atual, proximo_estado, self.pilha
                    )
                )
            elif acao == "ACC":
                print("Análise completa. Aceito.")
                break
            else:
                print("ERRO! - PANIC MODE")
                self.panic_mode(simbolo_atual)

    def panic_mode(self, simbolo_atual):
        while True:
            estado_atual = int(self.pilha[-1])
            print(
                "estado atual: {}, simbolo atual: {}".format(
                    estado_atual, simbolo_atual
                )
            )
            acao = self.acoes["$"][
                estado_atual
            ]  # Considere $ como o símbolo de recuperação

            if acao == "ACC":
                print("Análise completa. Aceito.")
                break
            else:
                self.pilha.pop()
                print("deu pop e a pilha ficou assim: {}".format(self.pilha))

                # Remova tokens até encontrar um estado de recuperação ou o símbolo de recuperação ($)
                while simbolo_atual not in self.tabela_follow and acao != "$":
                    simbolo_atual = self.scanner.gerar_token().classe
                    print("Token removido: {}".format(simbolo_atual))

                    estado_atual = int(self.pilha[-1])
                    acao = self.acoes[simbolo_atual][estado_atual]

                # Verifique se é possível retomar a análise
                if simbolo_atual in self.tabela_follow:
                    expected_follow_set = self.tabela_follow[simbolo_atual]
                    if acao in expected_follow_set:
                        return


class Scanner1:
    def get_token(self):
        return input("Digite o próximo token: ")

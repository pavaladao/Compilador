import pandas as pd
from scanner import Scanner
from tabela_de_simblos import tabela_simbolos


def read_parsing_table_from_csv(file_path):
    parsing_table_df = pd.read_csv(file_path, index_col="State")
    parsing_table = parsing_table_df.to_dict(orient="index")
    return parsing_table


def read_productions_from_csv(file_path):
    productions = pd.read_csv(file_path)
    productions.set_index("Production", inplace=True)
    return productions


class SLRParser:
    def __init__(self, parsing_table):
        self.stack = [0]
        self.input_buffer = []
        self.parsing_table = parsing_table
        self.scanner = Scanner(
            tabela_simbolos,
            ".\\tabelas\\automato lexico tabela.csv",
            ".\\entradas\\entrada.txt",
        )

    def parse(self, input_string):
        self.input_buffer = list(input_string) + ["$"]
        current_token = self.scanner.gerar_token()

        while True:
            state = self.stack[-1]
            action = self.parsing_table[state].get(current_token.classe, "ERR")

            if action == "ACC":
                print("Input accepted!")
                break
            elif action.startswith("s"):
                self.shift(int(action[1:]), current_token)
                current_token = self.scanner.gerar_token()
            elif action.startswith("r"):
                production_num = int(action[1:])
                self.reduce(production_num)
            elif action == "ERR":
                print("Error: Invalid input!")
                break

    def shift(self, next_state, current_token):
        self.stack.append(current_token)
        self.stack.append(next_state)

    def reduce(self, production_num):
        production = productions.loc[production_num]
        lhs = production["LHS"]
        rhs = production["RHS"].split()

        for _ in range(len(rhs) * 2):
            self.stack.pop()

        goto_state = self.parsing_table[self.stack[-1]][lhs]
        self.stack.append(lhs)
        self.stack.append(goto_state)

        print(f"Reduced: {lhs} -> {' '.join(rhs)}")

    def SCANNER(self):
        return self.scanner.gerar_token({})  # Pass an empty symbol table initially


# File paths for parsing table and productions CSV files
parsing_table_file = ".\\tabelas\\teste_sintatico_parse.csv"
productions_file = ".\\tabelas\\teste_sintatico_prod.csv"

# Read parsing table and productions
parsing_table = read_parsing_table_from_csv(parsing_table_file)
productions = read_productions_from_csv(productions_file)

# Initialize the parser
parser = SLRParser(parsing_table)

# Example usage
input_string = "ab_p ab_p id $"
parser.parse(input_string)

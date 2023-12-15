import pandas as pd
from scanner import Scanner


class SLRParser:
    def __init__(self, parsing_table):
        self.stack = [0]
        self.input_buffer = []
        self.parsing_table = parsing_table

    def parse(self, input_string):
        self.input_buffer = list(input_string) + ["$"]
        current_token = self.SCANNER()  # Placeholder, replace with actual code

        while True:
            state = self.stack[-1]
            action = self.parsing_table[state].get(current_token, "ERR")

            if action == "ACC":
                print("Input accepted!")
                break
            elif action.startswith("s"):
                self.shift(int(action[1:]), current_token)
                current_token = self.SCANNER()  # Placeholder, replace with actual code
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
        # Placeholder for the SCANNER function, replace with actual code
        # Call your lexical analyzer (T1) here and return the next token class
        pass


# Read parsing table from CSV using pandas
def read_parsing_table_from_csv(file_path):
    parsing_table_df = pd.read_csv(file_path, index_col="State")
    parsing_table = parsing_table_df.to_dict(orient="index")
    return parsing_table


# Read productions from CSV using pandas
def read_productions_from_csv(file_path):
    productions = pd.read_csv(file_path)
    productions.set_index("Production", inplace=True)
    return productions


# File paths for parsing table and productions CSV files
parsing_table_file = "parsing_table.csv"
productions_file = "productions.csv"

# Read parsing table and productions
parsing_table = read_parsing_table_from_csv(parsing_table_file)
productions = read_productions_from_csv(productions_file)

# Initialize the parser
parser = SLRParser(parsing_table)

# Example usage
input_string = "ab_p ab_p id $"
parser.parse(input_string)

import pandas as pd


def replace_x(value):
    return value.strip("[]'")


def ler_tabela_sintatico(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, index_col=0)

    unique_headers = set(df.columns.str.extract(r"(\w+)", expand=False))

    # Initialize empty DataFrames for 'action' and 'goto'
    action = pd.DataFrame(index=df.index)
    goto = pd.DataFrame(index=df.index)

    # Iterate through unique headers
    for header in unique_headers:
        # Select columns with the current header
        selected_columns = [col for col in df.columns if header in col]

        # Create a new DataFrame with the selected columns
        selected_df = df[selected_columns]

        # Determine if it's an 'action' or 'goto' DataFrame
        if "ACTION" in header:
            action = pd.concat([action, selected_df], axis=1)
        elif "GOTO" in header:
            goto = pd.concat([goto, selected_df], axis=1)

    # Format action
    action = action.rename(columns=action.iloc[0])
    action = action.reset_index(drop=True)
    action.drop(0, inplace=True)
    action = action.reset_index(drop=True)

    # Replace values in the format ['x'] in the 'action' DataFrame
    action = action.map(replace_x)

    # Format goto
    goto = goto.rename(columns=goto.iloc[0])
    goto = goto.reset_index(drop=True)
    goto.drop(0, inplace=True)
    goto = goto.reset_index(drop=True)

    # Replace values in the format ['x'] in the 'goto' DataFrame
    goto = goto.map(replace_x)

    # Print the resulting DataFrames
    # print("Action DataFrame:")
    # print(action)
    # print("\nGoto DataFrame:")
    # print(goto)

    return action, goto


def ler_producoes(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)
    df["POPS"] = df["LD"].apply(lambda x: len(x.split()))
    return df


def ler_tabela_follow(filename):
    follow_df = pd.read_csv(filename)
    follow_df["Follow"] = follow_df["Follow"].apply(lambda x: set(x.split(",")))
    follow_table = dict(zip(follow_df["NT"], follow_df["Follow"]))
    return follow_table


# teste = ler_tabela_follow(".\\tabelas\\conjunto_follow.csv")
# print(teste)
# if "se" in teste["V"]:
#     print("esta")

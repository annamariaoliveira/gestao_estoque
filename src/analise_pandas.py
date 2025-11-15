import pandas as pd
import numpy as np
import json
import os

PRODUTOS_JSON = "dados/produtos_data.json"
MOV_JSON = "dados/movimentacoes_data.json"

def carregar_json():
    with open(PRODUTOS_JSON, "r") as f:
        produtos = json.load(f)

    with open(MOV_JSON, "r") as f:
        movimentacoes = json.load(f)

    return produtos, movimentacoes


def gerar_datasets():
    produtos, movimentacoes = carregar_json()

    # DataFrame de produtos
    df_prod = pd.DataFrame.from_dict(produtos, orient="index")
    df_prod['codigo'] = df_prod.index

    # DataFrame de movimentações
    df_mov = pd.DataFrame(movimentacoes)

    # Criar pasta dados se não existir
    os.makedirs("dados", exist_ok=True)

    df_prod.to_csv("dados/produtos.csv", index=False)
    df_mov.to_csv("dados/movimentacoes.csv", index=False)

    print("✔ produtos.csv criado!")
    print("✔ movimentacoes.csv criado!")

    df_inv = gerar_dataset_inventario(df_prod, df_mov)
    return df_prod, df_mov, df_inv


def gerar_dataset_inventario(df_prod, df_mov):

    df_mov['quant_signed'] = np.where(
        df_mov['tipo'] == 'entrada',
        df_mov['quantidade'],
        -df_mov['quantidade']
    )

    estoque_series = df_mov.groupby('produto_codigo')['quant_signed'].sum()

    df_prod['estoque_atual'] = df_prod['codigo'].map(estoque_series).fillna(0).astype(int)
    df_prod['valor_total'] = df_prod['estoque_atual'] * df_prod['preco_unitario']
    df_prod['status'] = np.where(
        df_prod['estoque_atual'] < df_prod['estoque_minimo'],
        'EM FALTA',
        'OK'
    )

    df_prod.to_csv("dados/inventario.csv", index=False)

    print("✔ inventario.csv criado!")
    return df_prod

"""
main.py
---------
Orquestra todo o sistema:
1. Gera datasets com Pandas
2. Gera gráficos (Matplotlib + Seaborn)
3. Executa o sistema de estoque interativo
"""
from src.analise_pandas import gerar_datasets
from src.visualizacoes import (
    grafico_estoque,
    grafico_movimentacoes,
    heatmap_correlacao
)
from src.funcao_estoque import main as sistema_interativo


def main():

    print("\n GERANDO DATASETS ")
    try:
        df_prod, df_mov, df_inv = gerar_datasets()
        print("Datasets gerados com sucesso!")
    except Exception as e:
        print(f"ERRO ao gerar datasets: {e}")
        df_prod = df_mov = df_inv = None

    print("\n GERANDO GRÁFICOS ")
    try:
        if df_inv is not None:
            grafico_estoque(df_inv)

        if df_mov is not None:
            grafico_movimentacoes(df_mov)

        if df_inv is not None:
            heatmap_correlacao(df_inv)

        print("Gráficos gerados com sucesso!")
    except Exception as e:
        print(f"ERRO ao gerar gráficos: {e}")

    print("\n INICIANDO SISTEMA INTERATIVO")
    try:
        sistema_interativo()
    except Exception as e:
        print(f" ERRO ao executar o sistema interativo: {e}")


if __name__ == "__main__":
    main()

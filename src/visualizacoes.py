import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def salvar(fig, nome):
    os.makedirs("relatorios/graficos", exist_ok=True)
    fig.savefig(f"relatorios/graficos/{nome}.png", bbox_inches="tight")
    print(f"Gráfico salvo em relatorios/graficos/{nome}.png")


def grafico_estoque(df):
    fig = plt.figure(figsize=(10,5))
    sns.barplot(x='nome', y='estoque_atual', data=df)
    plt.xticks(rotation=45, ha="right")
    plt.title("Estoque Atual por Produto")
    salvar(fig, "estoque")
    plt.close()


def grafico_movimentacoes(df_mov):
    df_mov['data'] = pd.to_datetime(df_mov['data'])
    df_group = df_mov.groupby(['data','tipo'])['quantidade'].sum().unstack()

    fig = plt.figure(figsize=(10,5))
    df_group.plot(ax=plt.gca(), marker='o')
    plt.title("Movimentações ao Longo do Tempo")
    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    salvar(fig, "movimentos")
    plt.close()


def heatmap_correlacao(df):
    fig = plt.figure(figsize=(8,5))
    sns.heatmap(df[['estoque_atual','preco_unitario','valor_total']].corr(), annot=True)
    plt.title("Correlação Entre Variáveis")
    salvar(fig, "correlacao")
    plt.close()

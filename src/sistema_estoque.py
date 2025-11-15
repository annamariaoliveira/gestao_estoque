import json
import pprint
import os

# Caminhos dos arquivos JSON
PRODUTOS_FILE = 'dados/produtos_data.json'
MOVIMENTACOES_FILE = 'dados/movimentacoes_data.json'

# Estruturas principais
produtos = {}          # {codigo: {...}}
movimentacoes = []     # lista de movimentações


# carregar e salvar

def carregar_dados():
    """Carrega produtos e movimentações dos arquivos JSON."""
    global produtos, movimentacoes

    # Garantir que a pasta existe
    os.makedirs("dados", exist_ok=True)

    # Carregar produtos
    try:
        with open(PRODUTOS_FILE, 'r') as f:
            produtos.update(json.load(f))
        print(f"Produtos carregados ({len(produtos)}).")
    except:
        print("Nenhum produto encontrado. Criando arquivo novo depois.")

    # Carregar movimentações
    try:
        with open(MOVIMENTACOES_FILE, 'r') as f:
            movimentacoes.extend(json.load(f))
        print(f"Movimentações carregadas ({len(movimentacoes)}).")
    except:
        print("Nenhuma movimentação encontrada. Criando arquivo novo depois.")


def salvar_dados():
    """Salva produtos e movimentações nos JSON."""
    try:
        with open(PRODUTOS_FILE, 'w') as f:
            json.dump(produtos, f, indent=4)
        print("Produtos salvos.")
    except Exception as e:
        print("Erro ao salvar produtos:", e)

    try:
        with open(MOVIMENTACOES_FILE, 'w') as f:
            json.dump(movimentacoes, f, indent=4)
        print("Movimentações salvas.")
    except Exception as e:
        print("Erro ao salvar movimentações:", e)


# funções sistema

def cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco):
    """Cadastra novo produto."""
    if codigo in produtos:
        print(f"🚫 Produto {codigo} já existe.")
        return

    produtos[codigo] = {
        "nome": nome,
        "categoria": categoria,
        "estoque_minimo": estoque_minimo,
        "preco_unitario": preco
    }

    print(f"✅ Produto {nome} cadastrado com sucesso!")


def registrar_movimentacao(produto_codigo, tipo, quantidade, data, motivo):
    """Cadastra movimentação de entrada ou saída."""
    if produto_codigo not in produtos:
        print("🚫 Produto não existe!")
        return

    # Bloquear saídas acima do estoque
    if tipo == "saida":
        estoque = calcular_estoque_atual(produto_codigo)
        if quantidade > estoque:
            print(f"🚫 ERRO: Estoque insuficiente ({estoque}).")
            return

    registro = {
        "produto_codigo": produto_codigo,
        "tipo": tipo,
        "quantidade": quantidade,
        "data": data,
        "motivo": motivo
    }

    movimentacoes.append(registro)
    print("📦 Movimentação registrada.")


def calcular_estoque_atual(codigo):
    """Calcula estoque atual de um produto."""
    estoque = 0
    for m in movimentacoes:
        if m["produto_codigo"] == codigo:
            if m["tipo"] == "entrada":
                estoque += m["quantidade"]
            else:
                estoque -= m["quantidade"]
    return estoque


def identificar_produtos_em_falta():
    """Lista os produtos abaixo do estoque mínimo."""
    return [
        {
            "codigo": cod,
            "nome": dados["nome"],
            "estoque_atual": calcular_estoque_atual(cod),
            "estoque_minimo": dados["estoque_minimo"]
        }
        for cod, dados in produtos.items()
        if calcular_estoque_atual(cod) < dados["estoque_minimo"]
    ]


def calcular_valor_total_estoque():
    """Valor total do estoque."""
    total = 0
    for cod, dados in produtos.items():
        qtd = calcular_estoque_atual(cod)
        total += qtd * dados["preco_unitario"]
    return round(total, 2)


def gerar_relatorio_inventario():
    """Relatório detalhado do estoque."""
    print("\n RELATÓRIO DE INVENTÁRIO")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for cod, dados in produtos.items():
        estoque = calcular_estoque_atual(cod)
        valor = estoque * dados["preco_unitario"]

        status = "OK"
        if estoque < dados["estoque_minimo"]:
            status = "⚠ EM FALTA"

        print(f"""
Código: {cod}
Nome: {dados['nome']}
Categoria: {dados['categoria']}
Preço: R$ {dados['preco_unitario']:.2f}
Estoque Atual: {estoque}  |  Mínimo: {dados['estoque_minimo']}
Status: {status}
Valor Total: R$ {valor:.2f}
----------------------------------------
""")

    print("Valor TOTAL do estoque:", calcular_valor_total_estoque())


# Menu interface

def menu():
    print("\n MENU PRINCIPAL")
    print("1 - Cadastrar Produto")
    print("2 - Registrar Movimentação")
    print("3 - Gerar Relatório")
    print("4 - Produtos em Falta")
    print("5 - Valor total do estoque")
    print("0 - Sair")


def main():
    carregar_dados()

    while True:
        menu()
        op = input("Escolha: ")

        if op == "1":
            codigo = input("Código: ").upper()
            nome = input("Nome: ")
            categoria = input("Categoria: ")
            estoque_minimo = int(input("Estoque mínimo: "))
            preco = float(input("Preço: "))
            cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco)

        elif op == "2":
            codigo = input("Código do produto: ").upper()
            tipo = input("Tipo (entrada/saida): ")
            quantidade = int(input("Quantidade: "))
            data = input("Data (AAAA-MM-DD): ")
            motivo = input("Motivo: ")
            registrar_movimentacao(codigo, tipo, quantidade, data, motivo)

        elif op == "3":
            gerar_relatorio_inventario()

        elif op == "4":
            pprint.pprint(identificar_produtos_em_falta())

        elif op == "5":
            total = calcular_valor_total_estoque()
            print(f"💰 Valor total: R$ {total:.2f}")

        elif op == "0":
            salvar_dados()
            print("Encerrando...")
            break

        else:
            print("Opção inválida")


# Execução direta
if __name__ == "__main__":
    main()

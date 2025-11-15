import json
import pprint

produtos = {} # {codigo: {dados do produto}}
movimentacoes = [] # lista de dicts

PRODUTOS_FILE = 'dados/produtos_data.json'
MOVIMENTACOES_FILE = 'dados/movimentacoes_data.json'


def carregar_dados():
    """Carrega produtos e movimentações dos arquivos JSON."""
    global produtos, movimentacoes

    # Carregar produtos
    try:
        with open(PRODUTOS_FILE, 'r') as f:
            produtos.update(json.load(f))
        print(f"📥 {len(produtos)} produtos carregados.")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ Arquivo de produtos não encontrado. Criando vazio.")

    # Carregar movimentações
    try:
        with open(MOVIMENTACOES_FILE, 'r') as f:
            movimentacoes.extend(json.load(f))
        print(f"📥 {len(movimentacoes)} movimentações carregadas.")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ Arquivo de movimentações não encontrado. Criando vazio.")


def salvar_dados():
    """Salva os dados de produtos e movimentações nos arquivos JSON."""
    try:
        with open(PRODUTOS_FILE, 'w') as f:
            json.dump(produtos, f, indent=4)
        print("💾 Produtos salvos com sucesso.")
    except Exception as e:
        print(f"❌ Erro salvando produtos: {e}")

    try:
        with open(MOVIMENTACOES_FILE, 'w') as f:
            json.dump(movimentacoes, f, indent=4)
        print("💾 Movimentações salvas com sucesso.")
    except Exception as e:
        print(f"❌ Erro salvando movimentações: {e}")


#Cadastro de produtos

def cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco):
    """Cadastra um novo produto no sistema."""
    codigo = codigo.upper()

    if codigo in produtos:
        print(f"🚫 ERRO: Produto {codigo} já cadastrado.")
        return

    produtos[codigo] = {
        'nome': nome,
        'categoria': categoria,
        'estoque_minimo': estoque_minimo,
        'preco_unitario': preco
    }

    print(f"✅ Produto {nome} ({codigo}) cadastrado com sucesso!")


#Registro de Movimentação

def registrar_movimentacao(produto_codigo, tipo, quantidade, data, motivo):
    """Registra entrada ou saída de estoque."""
    produto_codigo = produto_codigo.upper()

    if produto_codigo not in produtos:
        print(f"🚫 ERRO: Produto {produto_codigo} não encontrado.")
        return

    if tipo not in ["entrada", "saida"]:
        print("🚫 Tipo inválido! Use 'entrada' ou 'saida'.")
        return

    # Validar saída maior que estoque atual
    if tipo == "saida":
        estoque_atual = calcular_estoque_atual(produto_codigo)
        if quantidade > estoque_atual:
            print(f"🚫 ERRO: Estoque insuficiente! Atual: {estoque_atual}")
            return

    nova_mov = {
        'produto_codigo': produto_codigo,
        'tipo': tipo,
        'quantidade': quantidade,
        'data': data,
        'motivo': motivo
    }

    movimentacoes.append(nova_mov)
    print(f"📦 Movimentação registrada: {tipo.upper()} {quantidade} un. ({produto_codigo})")


# Cálculo estoque

def calcular_estoque_atual(codigo):
    """Retorna o estoque atual do produto somando entradas e saídas."""
    estoque = 0

    for mov in movimentacoes:
        if mov['produto_codigo'] == codigo:

            if mov['tipo'] == 'entrada':
                estoque += mov['quantidade']
            else:
                estoque -= mov['quantidade']

    return estoque


def calcular_valor_total_estoque():
    """Retorna valor total do estoque."""
    total = 0

    for codigo, dados in produtos.items():
        estoque = calcular_estoque_atual(codigo)
        total += estoque * dados['preco_unitario']

    return round(total, 2)


# Identificar faltas 

def identificar_produtos_em_falta():
    """Retorna os produtos abaixo do estoque mínimo."""
    produtos_falta = []

    for codigo, dados in produtos.items():
        estoque = calcular_estoque_atual(codigo)

        if estoque < dados['estoque_minimo']:
            produtos_falta.append({
                'codigo': codigo,
                'nome': dados['nome'],
                'estoque_atual': estoque,
                'estoque_minimo': dados['estoque_minimo']
            })

    return produtos_falta


# Relatório

def gerar_relatorio_inventario():
    """Exibe relatório completo do inventário no terminal."""
    print("\n" + "="*50)
    print("          RELATÓRIO DE INVENTÁRIO")
    print("="*50)

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for codigo, dados in produtos.items():
        estoque = calcular_estoque_atual(codigo)
        valor_total = estoque * dados['preco_unitario']

        status = "OK"
        if estoque < dados['estoque_minimo']:
            status = "⚠️ EM FALTA"

        print(f"\n🔹 {dados['nome']} ({codigo})")
        print(f"   Categoria: {dados['categoria']}")
        print(f"   Estoque atual: {estoque}")
        print(f"   Estoque mínimo: {dados['estoque_minimo']}")
        print(f"   Valor total: R${valor_total:.2f}")
        print(f"   Status: {status}")

    print("\nValor total do estoque:", calcular_valor_total_estoque())
    print("="*50)


# inputs

def input_cadastrar_produto():
    print("\n--- CADASTRO DE PRODUTO ---")

    codigo = input("Código: ")
    nome = input("Nome: ")
    categoria = input("Categoria: ")

    try:
        estoque_minimo = int(input("Estoque mínimo: "))
        preco = float(input("Preço unitário: "))
    except ValueError:
        print("❌ ERRO: Estoque mínimo e preço devem ser números.")
        return

    cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco)


def input_registrar_movimentacao():
    print("\n--- REGISTRO DE MOVIMENTAÇÃO ---")

    codigo = input("Código do produto: ")
    tipo = input("Tipo (entrada/saida): ").lower()

    try:
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("❌ Quantidade inválida.")
        return

    data = input("Data (AAAA-MM-DD): ")
    motivo = input("Motivo: ")

    registrar_movimentacao(codigo, tipo, quantidade, data, motivo)


# Menu

def main():
    carregar_dados()

    while True:
        print("\n" + "="*40)
        print("        SISTEMA DE ESTOQUE")
        print("="*40)
        print("1 - Cadastrar Produto")
        print("2 - Registrar Movimentação")
        print("3 - Gerar Relatório de Inventário")
        print("4 - Listar Produtos em Falta")
        print("5 - Calcular Valor Total do Estoque")
        print("0 - Sair")
        print("="*40)

        opcao = input("Escolha: ")

        if opcao == "1":
            input_cadastrar_produto()

        elif opcao == "2":
            input_registrar_movimentacao()

        elif opcao == "3":
            gerar_relatorio_inventario()

        elif opcao == "4":
            falta = identificar_produtos_em_falta()
            pprint.pprint(falta)

        elif opcao == "5":
            print(f"\n💰 Valor total do estoque: R$ {calcular_valor_total_estoque():.2f}")

        elif opcao == "0":
            salvar_dados()
            print("Encerrando...")
            break

        else:
            print("❌ Opção inválida.")

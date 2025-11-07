# sistema_estoque.py

import json
import pprint

# --- Dicionário (Exemplos de Estrutura do Enunciado - Mantidos conforme pedido) ---

# Entrada
produto = {
    'codigo': 'PROD001',
    'nome': 'Notebook Dell',
    'categoria': 'Informática',
    'estoque_minimo': 5,
    'preco_unitario': 3500.00
}

movimentacao = {
    'produto_codigo': 'PROD001',
    'tipo': 'entrada', 
    'quantidade': 10,
    'data': '2024-01-15',
    'motivo': 'Compra'
}

# Saída
estoque_atual = {
    'PROD001': {
        'nome': 'Notebook Dell',
        'quantidade': 15,
        'valor_total': 52500.00,
        'status': 'OK'
    }
}

# --- VARIÁVEIS GLOBAIS (ESTRUTURAS DE DADOS REAIS DO SISTEMA) ---
produtos = {} 
movimentacoes = []

# Configuração de arquivos para persistência (usando JSON para estruturar os dados)
PRODUTOS_FILE = 'produtos_data.json'
MOVIMENTACOES_FILE = 'movimentacoes_data.json'

# --- FUNÇÕES DE PERSISTÊNCIA (MANIPULAÇÃO DE ARQUIVOS) ---

def carregar_dados():
    """Carrega produtos e movimentações de arquivos JSON."""
    global produtos, movimentacoes
    
    # 1. Carregar Produtos
    try:
        with open(PRODUTOS_FILE, 'r') as f:
            produtos.update(json.load(f)) 
        print(f"📥 {len(produtos)} produtos carregados de {PRODUTOS_FILE}.")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ Arquivo {PRODUTOS_FILE} não encontrado ou inválido. Iniciando produtos vazios.")
        
    # 2. Carregar Movimentações
    try:
        with open(MOVIMENTACOES_FILE, 'r') as f:
            movimentacoes.extend(json.load(f))
        print(f"📥 {len(movimentacoes)} movimentações carregadas de {MOVIMENTACOES_FILE}.")
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠️ Arquivo {MOVIMENTACOES_FILE} não encontrado ou inválido. Iniciando movimentações vazias.")

def salvar_dados():
    """Salva produtos e movimentações em arquivos JSON."""
    
    # 1. Salvar Produtos
    try:
        with open(PRODUTOS_FILE, 'w') as f:
            json.dump(produtos, f, indent=4)
        print(f"✅ Produtos salvos em {PRODUTOS_FILE}.")
    except Exception as e:
        print(f"❌ Erro ao salvar produtos: {e}")
        
    # 2. Salvar Movimentações
    try:
        with open(MOVIMENTACOES_FILE, 'w') as f:
            json.dump(movimentacoes, f, indent=4)
        print(f"✅ Movimentações salvas em {MOVIMENTACOES_FILE}.")
    except Exception as e:
        print(f"❌ Erro ao salvar movimentações: {e}")


# --- FUNÇÕES DE LÓGICA DE NEGÓCIO E CÁLCULO ---

def cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco):
    """Cadastra novo produto."""
    
    if codigo in produtos:
        print(f"🚫 ERRO: Produto com código {codigo} já existe.")
        return
        
    dados_produto = {
        'nome': nome,
        'categoria': categoria,
        'estoque_minimo': estoque_minimo,
        'preco_unitario': preco
    }
    
    produtos[codigo] = dados_produto
    print(f"Produto {nome} ({codigo}) cadastrado com sucesso.")

# A linha de teste (cadastrar_produto('PROD001', ...)) foi movida para o main() ou removida.

def registrar_movimentacao(produto_codigo, tipo, quantidade, data, motivo):
    """Registra movimentação de estoque."""
    
    # Validação de estoque mínimo (sugestão do projeto)
    if tipo == 'saida':
        estoque_atual = calcular_estoque_atual(produto_codigo)
        if quantidade > estoque_atual:
            print(f"🚫 ERRO: Saída de {quantidade} é maior que o estoque atual ({estoque_atual}).")
            return
            
    novo_registro = {
        'produto_codigo': produto_codigo,
        'tipo': tipo,
        'quantidade': quantidade,
        'data': data,
        'motivo': motivo
    }
    
    movimentacoes.append(novo_registro)
    
    print(f"Movimentação de {tipo.upper()} para {produto_codigo} de {quantidade} unidades registrada.")

def calcular_estoque_atual(codigo):
    """Calcula estoque atual de um produto (somando entradas e subtraindo saídas)."""
    
    estoque = 0 
    
    for registro in movimentacoes: 
        
        if registro['produto_codigo'] == codigo: 
            
            if registro['tipo'] == 'entrada':
                estoque += registro['quantidade'] 
            
            elif registro['tipo'] == 'saida':
                estoque -= registro['quantidade'] 
                
    return estoque

def calcular_valor_total_estoque():
    """Calcula valor total do estoque (somatório de (estoque * preço))."""
    
    valor_total = 0.0 # Inicializa o somatório
    
    for codigo in produtos:
        
        estoque_atual = calcular_estoque_atual(codigo)
        preco_unitario = produtos[codigo]['preco_unitario']
        
        valor_do_produto_em_estoque = estoque_atual * preco_unitario
        
        valor_total += valor_do_produto_em_estoque
        
    return round(valor_total, 2)

def identificar_produtos_em_falta():
    """Identifica produtos abaixo do estoque mínimo."""
    
    produtos_em_falta = []
    
    for codigo in produtos:
        
        dados = produtos[codigo]
        estoque_minimo = dados['estoque_minimo']
        estoque_atual = calcular_estoque_atual(codigo)
        
        if estoque_atual < estoque_minimo:
            produtos_em_falta.append({
                'codigo': codigo,
                'nome': dados['nome'],
                'estoque_atual': estoque_atual,
                'estoque_minimo': estoque_minimo
            })
            
    return produtos_em_falta

def gerar_relatorio_inventario():
    """Gera relatório completo de inventário."""
    
    print("\n" + "="*50)
    print("      RELATÓRIO COMPLETO DE INVENTÁRIO")
    print("="*50)
    
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
        
    total_estoque_geral = 0
    
    # 1. Relatório Detalhado por Produto
    for codigo, dados in produtos.items():
        
        estoque_atual = calcular_estoque_atual(codigo)
        valor_total_produto = round(estoque_atual * dados['preco_unitario'], 2)
        total_estoque_geral += estoque_atual
        
        status = "OK"
        if estoque_atual < dados['estoque_minimo']:
            status = "**EM FALTA**"
            
        print(f"\nCódigo: {codigo} | Produto: {dados['nome']}")
        print(f"  Categoria: {dados['categoria']} | Preço: R${dados['preco_unitario']:.2f}")
        print(f"  Estoque Atual: {estoque_atual} | Mínimo: {dados['estoque_minimo']} | STATUS: {status}")
        print(f"  Valor em Estoque: R${valor_total_produto:.2f}")
    
    print("\n" + "-"*50)
    
    # 2. Resumo e Alertas
    valor_total_geral = calcular_valor_total_estoque()
    produtos_em_falta_list = identificar_produtos_em_falta()
    
    print(f"VALOR TOTAL DO ESTOQUE GERAL: R${valor_total_geral:.2f}")
    print(f"QUANTIDADE TOTAL DE ITENS: {total_estoque_geral}")
    print(f"ALERTAS (Produtos em Falta): {len(produtos_em_falta_list)} produto(s)")
    
    if produtos_em_falta_list:
        print("\nPRODUTOS ABAIXO DO ESTOQUE MÍNIMO:")
        for item in produtos_em_falta_list:
            print(f"  -> {item['nome']} ({item['codigo']}). Atual: {item['estoque_atual']}. Mínimo: {item['estoque_minimo']}")
    
    print("="*50)

# --- FUNÇÕES DE INTERFACE (INPUT DO USUÁRIO) ---

def input_cadastrar_produto():
    """Coleta dados do usuário e chama a função de cadastro."""
    print("\n--- CADASTRO DE NOVO PRODUTO ---")
    
    codigo = input("Digite o código do produto: ").upper()
    nome = input("Digite o nome do produto: ")
    categoria = input("Digite a categoria: ")
    
    try:
        estoque_minimo = int(input("Digite o estoque mínimo: "))
        preco = float(input("Digite o preço unitário (ex: 1500.50): "))
        
        cadastrar_produto(codigo, nome, categoria, estoque_minimo, preco)
        
    except ValueError:
        print("\n🚫 ERRO: Estoque mínimo ou preço devem ser números. Tente novamente.")

def input_registrar_movimentacao():
    """Coleta dados do usuário e registra a movimentação."""
    print("\n--- REGISTRO DE MOVIMENTAÇÃO ---")
    
    produto_codigo = input("Digite o código do produto: ").upper()
    
    if produto_codigo not in produtos:
        print(f"🚫 ERRO: Produto {produto_codigo} não encontrado. Cadastre-o primeiro.")
        return
    
    tipo = input("Tipo (entrada/saida): ").lower()
    
    if tipo not in ['entrada', 'saida']:
        print("🚫 ERRO: Tipo de movimento inválido. Use 'entrada' ou 'saida'.")
        return
        
    try:
        quantidade = int(input("Quantidade: "))
        data = input("Data (AAAA-MM-DD): ")
        motivo = input("Motivo: ")
        
        registrar_movimentacao(produto_codigo, tipo, quantidade, data, motivo)

    except ValueError:
        print("\n🚫 ERRO: Quantidade deve ser um número inteiro. Tente novamente.")

# --- FUNÇÃO PRINCIPAL (CONTROLE DE EXECUÇÃO) ---

def main():
    """Função principal que orquestra o sistema com menu interativo."""
    
    carregar_dados()
    
    while True:
        print("\n" + "="*30)
        print("SISTEMA DE GESTÃO DE ESTOQUE")
        print("="*30)
        print("1 - Cadastrar Novo Produto")
        print("2 - Registrar Movimentação (Entrada/Saída)")
        print("3 - Gerar Relatório de Inventário")
        print("4 - Listar Produtos em Falta")
        print("5 - Calcular Valor Total do Estoque")
        print("0 - Sair e Salvar Dados")
        
        escolha = input("Digite sua opção: ")
        
        if escolha == '1':
            input_cadastrar_produto()
            
        elif escolha == '2':
            input_registrar_movimentacao()
            
        elif escolha == '3':
            gerar_relatorio_inventario()
            
        elif escolha == '4':
            lista_falta = identificar_produtos_em_falta()
            if lista_falta:
                print("\n** PRODUTOS EM FALTA **")
                pprint.pprint(lista_falta)
            else:
                print("\n🎉 Nenhum produto está abaixo do estoque mínimo.")

        elif escolha == '5':
            valor = calcular_valor_total_estoque()
            print(f"\n💰 VALOR TOTAL DO ESTOQUE: R${valor:.2f}")

        elif escolha == '0':
            salvar_dados()
            print("\nObrigado por usar o sistema. Encerrando.")
            break
            
        else:
            print("\nOpção inválida. Digite um número de 0 a 5.")

# --- INÍCIO DA EXECUÇÃO ---

if __name__ == "__main__":
    main()
c# Projeto 08: Sistema de Gestão de Estoque

**Disciplina:** Programação para Ciência de Dados
**Curso:** MBA Ciência de Dados - Universidade de Fortaleza - UNIFOR
**Instrutor:** Cassio Pinheiro
**Integrante:** Anna Maria do Nascimento Oliveira (2527027)

**Repositório GitHub:** https://github.com/annamariaoliveira/gestao_estoque
**Entrega:** 14/11/2025

## Objetivo:
Desenvolver um sistema para gestão de estoque que permita cadastrar produtos, registrar movimentações (entrada/saída), calcular níveis de estoque, identificar produtos em falta e gerar relatórios de inventário.

## Diagrama
<img width="1007" height="674" alt="image" src="https://github.com/user-attachments/assets/425e6278-fde4-4d16-a9ef-d253be090f45" />


## Funcionalidades:
- Dicionário: Possui as especificações de cada produtos;
- Cadastrar Produto: Cadastrar um novo produto no sistema de acordo com as especificações do dicionário;
- Registrar Movimentação: Registrar entrada/saída dos itens;
- Calcular estoque atual: Calcula os estoques atuais dos itens de acordo com as entradas e saídas;
- Calcular valor total do estoque: Valor contábil do estoque com o total dos itens;
- Identificar itens em falta: De acordo com os estoques mínimos de cada produtos, o sistema informará o que precisará de reposição.
- Gerar relatórios: Puxar todos os itens que estão cadastrados no sistemas com seus respectivos estoques;

  ## Menu
  <img width="209" height="140" alt="image" src="https://github.com/user-attachments/assets/083a7696-c9f4-49f2-8ae0-d82aa8b9a83a" />

  ## Cadastrar Produto
  <img width="324" height="232" alt="image" src="https://github.com/user-attachments/assets/e1e3a24f-0293-45b9-9641-3ece8d0717a8" />

  ## Movimentar Estoque
  <img width="230" height="229" alt="image" src="https://github.com/user-attachments/assets/90f37af6-79b9-41df-89c6-fcfa20585ffb" />

  ## Relatório
  <img width="269" height="499" alt="image" src="https://github.com/user-attachments/assets/85d0571d-d626-43c9-aa07-a3e42aae8d98" />

  ##  Produtos em Falta
  <img width="253" height="323" alt="image" src="https://github.com/user-attachments/assets/b1609bc5-9f39-47d2-9325-cc0a74a4cd91" />
  
  ##  Saldo Estoque
  <img width="240" height="173" alt="image" src="https://github.com/user-attachments/assets/452335c5-b2c0-48f2-9add-f6d209401b32" />
  
# Requisitos Técnicos:
- Python 3.11;
- Bibliotecas: Json;

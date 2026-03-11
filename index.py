from dataclasses import dataclass
from datetime import datetime



@dataclass
class Usuario:
    nome: str
    email: str
    senha: str

@dataclass
class Produto:
    id: int
    nome: str
    categoria: str
    tamanho: str
    cor: str
    codigo_barras: str
    valor_custo: float
    valor_venda: float
    estoque: int
    fornecedor_id: int
    
@dataclass
class MovimentoEstoque:
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    data_hora: str
    
@dataclass
class Compra:
    id: int
    produto_id: int
    quantidade: int
    total: float
    data_hora: int
    
fornecedores = []
produtos = []
movimentos = []
compras = []
lista_usuarios = [("Cliente", "cliente@gmail.com", "Cliente123"), ("Admin", "admin@gmail.com", "Admin123")]
carrinho = []

def proximo_id(lista):
    return len(lista) + 1
    
def agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def criar_usuario():
    nome = input("Qual o seu nome: ")
    email = input("Qual o seu email: ")
    senha = input("Qual a sua senha: ")
    usuario_digitado = Usuario(nome,email,senha)
    lista_usuarios.append(usuario_digitado)
    print("Cadastro efetuado com sucesso")
            
def fazer_login():
    login_email = input("Qual o seu email: ")
    login_senha = input("Qual a sua senha: ")
        
    for usuario in lista_usuarios:
        if usuario.email == login_email and usuario.senha == login_senha:
            print("Acesso autorizado")
            return usuario  # ✅ Retorna o usuário logado

    print("Email ou senha incorreto")
    return None  # ❌ Login falhou
    
def cadastrar_fornecedor():
    print("\n----- CADASTRO DE FORNECEDOR -----")
    nome = input("Digite o nome da empresa: ")
    cnpj = input("Digite seu CNPJ: ")
    
    fornecedor = fornecedor(
        proximo_id(fornecedores),
        nome,
        cnpj
        )
        
    fornecedores.append(fornecedor)
    print("Fornecedor Cadastrado com Sucesso🚀")
    
    
def listar_fornecedores():
    for f in fornecedores:
        print(f)
        
def cadastrar_produtos():
    if len(fornecedores) == 0:
        print("Cadastre um fornecedor primeiro")
        return
    
    print("\n----- Cadastrar Produtos -----")
    nome = input("NOME: ")
    categoria = input("CATEGORIA: ")
    tamanho = input("TAMANHO: ")
    cor = input("COR: ")
    codigo_barras = input("CÓDIGO DE BARRAS: ")
    custo = float(input("CUSTO: "))
    venda = float(input("VENDA: "))
    estoque = int(input("ESTOQUE: "))
    
    print("\nFORNECEDORES:")
    listar_fornecedores()
    fornecedor_id = int(input("ID DO FORNECEDOR: "))
    
    produto = Produto(
        proximo_id(produtos),
        nome,
        categoria, 
        tamanho,
        cor,
        codigo_barras,
        custo,
        venda,
        estoque,
        fornecedor_id
    )

    produtos.append(produto)
    
    if estoque > 0:
        movimento = MovimentoEstoque(
            proximo_id(movimento),
            produto.id,
            "ENTRADA",
            estoque,
            agora()
        )
        
        movimentos.append(movimento)
    
    print("PRODUTO CADASTRADO COM SUCESSO🚀")
    
def listar_produtos():
    print("\n----- PRODUTOS -----")
    for p in produtos:
        print(p)
    
def entrada_estoque():
    print("\n----- ENTRADA DE ESTOQUE -----")
    listar_produtos()
    
    pid = int(input("ID do Produto: "))
    quantidade = int(input("Quantidade: "))
    
    for p in produtos:
        if p.id == pid:
            p.estoque += quantidade
            
            movimento = MovimentoEstoque(
            proximo_id(movimentos),
            pid,
            "ENTRADA",
            quantidade,
            agora()
        )
        movimentos.append(movimento)
        
        print("Entrada Registrada🚀")
        
def saida_estoque(tipo):
    print("\n----- SAÍDA ESTOQUE -----")
    listar_produtos()
    
    pid = int(input("ID do Produto: "))
    quantidade = int(input("Quantidade: "))
    
    for p in produtos:
        if p.id == pid:
            if quantidade <= p.estoque:
                p.estoque -= p.quantidade
                
                movimento = MovimentoEstoque(
                proximo_id(movimentos),
                pid,
                tipo,
                quantidade,
                agora()
            )
            movimentos.append(movimento)
            
            print("Saída Registrada")
        else:
            print("Estoque Insuficiente❌")
            
def comprar():
    print("\n----- COMPRA -----")
    listar_compras()
    
    pid = int(input("ID do Produto: "))
    quantidade = int(input("Quantidade: "))
    
    for p in produtos:
        if p.id == pid:
            if quantidade <= p.estoque:
                p.estoque -= p.quantidade
                
                total = p.valor_venda * quantidade
                
                compra = Compra(
                    proximo_id(movimentos),
                    pid,
                    quantidade,
                    total,
                    agora()
                    )
                compras.append(compra)
                
                movimento = MovimentoEstoque(
                proximo_id(movimentos),
                pid,
                "SAÍDA VENDA",
                quantidade,
                agora()
            )
            movimentos.append(movimento)
            
            print("Compra Realizada! Total: ", total)

def listar_compras():
    print("\n----- COMPRAS -----")
    for c in compras:
     print(c)
     
def listar_movimentos():
    print("\n----- MOVIMENTO -----")
    for m in movimentos:
        print(m)

def listar_produtos():
    if len(produtos) == 0:
        print("❌ Nenhum produto disponível.")
        return

    print("\n--- PRODUTOS DISPONÍVEIS ---")
    for i, p in enumerate(produtos):
        if len(p["avaliacoes"]) > 0:
            media = sum(p["avaliacoes"]) / len(p["avaliacoes"])
        else:
            media = 0

        print(f"{i} - {p['nome']} | R$ {p['preco']} | Estoque: {p['estoque']} | ⭐ {media:.1f}")

def pesquisar_produto():
    termo = input("Digite o nome do produto: ").lower()

    for i, p in enumerate(produtos):
        if termo in p["nome"].lower():
            print(f"{i} - {p['nome']} | R$ {p['preco']} | Estoque: {p['estoque']}")

def adicionar_carrinho():
    listar_produtos()
    if len(produtos) == 0:
        return

    indice = int(input("Digite o número do produto: "))
    quantidade = int(input("Quantidade: "))

    produto = produtos[indice]

    if quantidade <= produto["estoque"]:
        carrinho.append({
            "nome": produto["nome"],
            "preco": produto["preco"],
            "quantidade": quantidade
        })
        produto["estoque"] -= quantidade
        print("🛒 Produto adicionado ao carrinho!")
    else:
        print("❌ Estoque insuficiente.")

def ver_carrinho():
    if len(carrinho) == 0:
        print("🛒❌ Carrinho vazio.")
        return

    total = 0
    print("\n--- CARRINHO ---")
    for item in carrinho:
        subtotal = item["preco"] * item["quantidade"]
        total += subtotal
        print(f"{item['nome']} | {item['quantidade']}x | R$ {subtotal}")

    print(f"💰 Total: R$ {total}")

def finalizar_compra():
    if len(carrinho) == 0:
        print("❌ Carrinho vazio.")
        return

    ver_carrinho()
    confirmar = input("Confirmar compra? (s/n): ")

    if confirmar.lower() == "s":
        carrinho.clear()
        print("✅ Compra realizada com sucesso!")
    else:
        print("❌ Compra cancelada.")

def avaliar_produto():
    listar_produtos()
    if len(produtos) == 0:
        return

    indice = int(input("Digite o número do produto: "))
    nota = int(input("Nota (1 a 5): "))

    if 1 <= nota <= 5:
        produtos[indice]["avaliacoes"].append(nota)
        print("⭐ Avaliação registrada!")
    else:
        print("❌ Nota inválida.")

def pesquisar_produto():
    termo = input("Digite o nome do produto: ").lower()

    for i, p in enumerate(produtos):
        if termo in p["nome"].lower():
            print(f"{i} - {p['nome']} | R$ {p['preco']} | Estoque: {p['estoque']}")

def menu():
    while True:
        print("\n ----- Menu Inicial -----")
        print("1 - Cadastro")
        print("2 - Login")
        print("0 - Sair")

        op = input("Escolha: ")




def menuCliente():
        print("\n ----- Cliente Menu -----")
        print("1 - Pesquisar produtos")
        print("2 - Adicionar ao carrinho")
        print("3 - Finalizar compra")
        print("4 - Avaliação")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            pesquisar_produto()
        elif op == "2":
            adicionar_carrinho()
        elif op == "3":
            finalizar_compra()
        elif op == "4":
            avaliar_produto()
        elif op == "5":
            menu()
        else: 
            print("Erro ao sair, tente novamente")

def menuAdmin():
    
        print("\n ----- Admin Menu -----")
        print("1 - Cadastrar fornecedor")
        print("2 - Cadastrar produto")
        print("3 - Entrada de estoque")
        print("4 - Saída por venda")
        print("5 - Saída por troca")
        print("6 - Saída por avaria")
        print("7 - Comprar produto")
        print("8 - Listar produtos")
        print("9 - Listar compras")
        print("10 - Listar movimentos")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_fornecedor()
        elif op == "2":
            cadastrar_produtos()
        elif op == "3":
            entrada_estoque()
        elif op == "4":
            saida_estoque("SAIDA_VENDA")
        elif op == "5":
            saida_estoque("SAIDA_TROCA")
        elif op == "6":
            saida_estoque("SAIDA_AVARIA")
        elif op == "7":
            comprar()
        elif op == "8":
            listar_produtos()
        elif op == "9":
            listar_compras()
        elif op == "10":
            listar_movimentos()
        elif op == "0":
            menu()
        else:
            print("Erro ao sair, tente novamente")
        
menu()

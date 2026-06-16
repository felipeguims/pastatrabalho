import os
import hashlib

def hash_sha256(texto):
    """Gera o hash SHA-256 para trancar as senhas (Requisito 5 do PDF)"""
    return hashlib.sha256(texto.encode()).hexdigest()

def cifra(texto, chave=4):
    """Criptografa o texto do inventário empurrando os caracteres"""
    return "".join(chr((ord(c) + chave) % 256) for c in texto)

def decifra(texto, chave=4):
    """Decifra o texto do inventário puxando os caracteres de volta"""
    return "".join(chr((ord(c) - chave) % 256) for c in texto)

# --- ALGORITMOS DE ORDENAÇÃO ---

def bubble_sort(lista):
    """Ordena a lista por nome usando Bubble Sort (Até 100 produtos)"""
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j][1].lower() > lista[j + 1][1].lower():
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

def merge_sort(lista):
    """Ordena a lista por nome usando Merge Sort (Mais de 100 produtos)"""
    if len(lista) > 1:
        meio = len(lista) // 2
        esquerda = lista[:meio]
        direita = lista[meio:]

        merge_sort(esquerda)
        merge_sort(direita)

        i = j = k = 0
        while i < len(esquerda) and j < len(direita):
            if esquerda[i][1].lower() < direita[j][1].lower():
                lista[k] = esquerda[i]
                i += 1
            else:
                lista[k] = direita[j]
                j += 1
            k += 1

        while i < len(esquerda):
            lista[k] = esquerda[i]
            i += 1
            k += 1

        while j < len(direita):
            lista[k] = direita[j]
            j += 1
            k += 1

def ordenar_produtos_automatico(lista):
    """Seleciona o algoritmo correto com base no tamanho do inventário (Conforme exigido pelo PDF)"""
    if len(lista) <= 100:
        
        bubble_sort(lista)
    else:
        
        merge_sort(lista)

# --- ALGORITMOS DE BUSCA ---

def busca_linear(dicionario, nome_pesquisa):
    """Busca Linear diretamente no dicionário"""
    resultados = []
    for p_id, dados in dicionario.items():
        if nome_pesquisa in dados[0].lower():
            resultados.append((p_id, dados))
    return resultados

def busca_binaria(lista_ordenada, nome_pesquisa):
    """Busca Binária em uma lista previamente ordenada por nome"""
    esquerda = 0
    direita = len(lista_ordenada) - 1
    
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        nome_atual = lista_ordenada[meio][1].lower()
        
        if nome_pesquisa == nome_atual:
            return [lista_ordenada[meio]]
        elif nome_pesquisa < nome_atual:
            direita = meio - 1
        else:
            esquerda = meio + 1
            
    return [p for p in lista_ordenada if nome_pesquisa in p[1].lower()]

# --- SISTEMA DE AUTENTICAÇÃO ---

def aba_criar_conta():
    print("\n========================================")
    print("  ABA: CRIAR NOVA CONTA (CADASTRO) ")
    print("========================================")
    user = input(" Escolha o nome de usuário: ").strip().lower()
    
    if not user:
        print(" Erro: O nome de usuário não pode ser vazio.")
        return

    if os.path.exists("login.txt"):
        with open("login.txt", "r", encoding="utf-8") as f:
            for linha in f:
                linha_limpa = linha.strip()
                if linha_limpa:
                    u_salvo = linha_limpa.split(";")[0]
                    if u_salvo == user:
                        print(" Erro: Este usuário já está cadastrado!")
                        return

    senha = input(" Escolha a sua senha: ").strip()
    if not senha:
        print(" Erro: A senha não pode ser vazia.")
        return
    
    with open("login.txt", "w", encoding="utf-8") as f:
        f.write(f"{user};{hash_sha256(senha)}\n")
    print(f"\n SUCESSO: Conta '{user.upper()}' criada!")

def aba_fazer_login():
    print("\n========================================")
    print("  ABA: ENTRAR NO SISTEMA (LOGIN) ")
    print("========================================")
    
    if not os.path.exists("login.txt") or os.path.getsize("login.txt") == 0:
        print(" Alerta: Arquivo de login vazio/inexistente.")
        return None

    u_input = input(" Usuário: ").strip().lower()
    s_input = input(" Senha: ").strip()
    
    hash_digitado = hash_sha256(s_input)
    
    with open("login.txt", "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                u_salvo, s_salvo = linha.strip().split(";")
                if u_input == u_salvo and hash_digitado == s_salvo:
                    print(f"\n Bem-vindo à ROCKET GAMES, {u_input.upper()}!")
                    return u_input
                    
    print(" Erro: Usuário ou senha incorretos!")
    return None

def alterar_credenciais():
    print("\n========================================")
    print("  ALTERAR USUÁRIO E SENHA DE ACESSO ")
    print("========================================")
    novo_user = input("Novo usuário: ").strip().lower()
    nova_senha = input("Nova senha: ").strip()
    
    if novo_user and nova_senha:
        with open("login.txt", "w", encoding="utf-8") as f:
            f.write(f"{novo_user};{hash_sha256(nova_senha)}\n")
        print(" Credenciais alteradas e salvas com Hash SHA-256!")
        return novo_user
    print(" Erro: Campos não podem ser vazios.")
    return None

# --- BANCO DE DADOS EM ARQUIVO (CRIPTOGRAFADO) ---

def carregar_produtos():
    produtos = {}
    if not os.path.exists("inventario.csv"):
        print("  Criando inventário...")
        produtos[101] = ["Consola PlayStation 5", 15, 549.99, True]
        produtos[102] = ["Jogo EA Sports FC 26 PS5", 40, 69.99, False]
        produtos[103] = ["Comando DualSense Edge", 25, 239.99, True]
        produtos[104] = ["Nintendo Switch OLED", 10, 349.99, True]
        produtos[105] = ["Jogo Chrono Trigger SNES (Raro)", 1, 899.99, True]
        produtos[106] = ["Consola Sega Mega Drive", 5, 120.00, False]
        salvar_produtos(produtos)
        return produtos

    with open("inventario.csv", "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip():
                campos = [decifra(c) for c in linha.strip().split(";")]
                p_id = int(campos[0])
                produtos[p_id] = [campos[1], int(campos[2]), float(campos[3]), campos[4] == "True"]
    return produtos

def salvar_produtos(produtos):
    with open("inventario.csv", "w", encoding="utf-8") as f:
        for p_id, d in produtos.items():
            linha = f"{cifra(str(p_id))};{cifra(d[0])};{cifra(str(d[1]))};{cifra(str(d[2]))};{cifra(str(d[3]))}\n"
            f.write(linha)
    print("\n Dados salvos em lote com Cifra de César no arquivo 'inventario.csv'!")

# --- FLUXO PRINCIPAL ---

def main():
    usuario_ativo = None

    while not usuario_ativo:
        print("\n===  LOJA ROCKET ===")
        print("1. Criar uma Conta (Primeiro Acesso)")
        print("2. Fazer Login")
        print("3. Fechar Programa")
        opcao_inicio = input("Escolha uma opção: ").strip()

        if opcao_inicio == "1":
            aba_criar_conta()
        elif opcao_inicio == "2":
            usuario_ativo = aba_fazer_login()
        elif opcao_inicio == "3":
            return
        else:
            print("Opção inválida.")

    loja = carregar_produtos()

    while True:
        print(f"\n === PAINEL DE CONTROLE ROCKET GAMES: {usuario_ativo.upper()} ===")
        print("1. Cadastrar Produto")
        print("2. Remover Produto")
        print("3. Atualizar Produto")
        print("4. Lista Estoque ")
        print("5. Buscar Produto (NOME ou ID)")
        print("6. Ver o Inventário (Estatísticas)")
        print("7. Configurações (Mudar Login/Senha)")
        print("8. Salvar e Sair (Processamento em Lote)")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            try:
                p_id = int(input("ID do Produto: "))
                if p_id in loja:
                    print(" Erro: Esse ID já está cadastrado!")
                    continue
                nome = input("Nome do artigo: ").strip()
                qtd = int(input("Quantidade: "))
                preco = float(input("Preço unitário: R$ "))
                # CORREÇÃO: Adicionada a pergunta sobre o campo importado que faltava e causava o travamento
                imp_input = input("É um artigo Importado? (S/N): ").strip().upper()
                imp = (imp_input == "S")

                loja[p_id] = [nome, qtd, preco, imp]
                print(f" '{nome}' adicionado com sucesso!")
            except ValueError:
                print(" Erro: Validação falhou! Insira números válidos para ID, Quantidade e Preço.")

        elif opcao == "2":
            try:
                p_id = int(input("Digite o ID do Produto que deseja remover: "))
                if p_id in loja:
                    removido = loja.pop(p_id)
                    print(f" Produto '{removido[0]}' foi removido da memória!")
                else:
                    print(" ID não encontrado.")
            except ValueError:
                print(" ID inválido.")

        elif opcao == "3":
            try:
                p_id = int(input("Digite o ID do artigo que deseja atualizar: "))
                if p_id in loja:
                    print(f"Modificando: {loja[p_id][0]}")
                    loja[p_id][0] = input("Novo Nome: ").strip()
                    loja[p_id][1] = int(input("Nova Quantidade: "))
                    loja[p_id][2] = float(input("Novo Preço: R$ "))
                    print(" Produto atualizado com sucesso!")
                else:
                    print(" ID não encontrado.")
            except ValueError:
                print(" Entrada inválida.")

        elif opcao == "4":
            print("\n---  ESTOQUE ATUAL ---")
            if not loja:
                print("O estoque está vazio.")
                continue
            
            lista_produtos = [[p_id] + dados for p_id, dados in loja.items()]
            ordenar_produtos_automatico(lista_produtos)
            
            for p in lista_produtos:
                print(f"ID: {p[0]} | Produto: {p[1]} | Qtd: {p[2]} | Preço: R$ {p[3]:.2f} | Importado: {'Sim' if p[4] else 'Não'}")

        elif opcao == "5":
            print("\n[MÉTODOS DE BUSCA]")
            print("1 - Busca por Nome")
            print("2 - Busca por ID")
            tipo_busca = input("Escolha o tipo de busca: ").strip()
            
            if tipo_busca == "1":
                nome_busca = input("Nome a pesquisar: ").strip().lower()
                resultados = busca_linear(loja, nome_busca)
                if resultados:
                    for p_id, d in resultados:
                        print(f" [Achado] ID: {p_id} | {d[0]} | Qtd: {d[1]} | Preço: R$ {d[2]:.2f} | Importado: {'Sim' if d[3] else 'Não'}")
                else:
                    print(" Nenhum item localizado com esse nome.")
                    
            elif tipo_busca == "2":
                try:
                    id_busca = int(input("Digite o ID a pesquisar: "))
                    # CORREÇÃO: Busca por ID agora verifica diretamente a chave do dicionário (Complexidade O(1))
                    if id_busca in loja:
                        d = loja[id_busca]
                        print(f" [Achado] ID: {id_busca} | {d[0]} | Qtd: {d[1]} | Preço: R$ {d[2]:.2f} | Importado: {'Sim' if d[3] else 'Não'}")
                    else:
                        print(" Nenhum item localizado com esse ID.")
                except ValueError:
                    print(" Erro: O ID deve ser um número inteiro.")
            else:
                print("Opção de busca inválida.")

        elif opcao == "6":
            total_itens = len(loja)
            total_estoque = sum(item[1] for item in loja.values())
            valor_total = sum(item[1] * item[2] for item in loja.values())
            total_importados = sum(1 for item in loja.values() if item[3])
 
            print(f"\n --- LOJA ROCKET  ---")
            print(f" Tipos de Produtos Diferentes: {total_itens}")
            print(f" Total de Unidades no Estoque: {total_estoque}")
            print(f" Quantidade de Itens Importados: {total_importados}")
            print(f" Valor Total Líquido do Estoque: R$ {valor_total:.2f}")

        elif opcao == "7":
            novo_u = alterar_credenciais()
            if novo_u:
                usuario_ativo = novo_u

        elif opcao == "8":
            salvar_produtos(loja)
            print("Sessão encerrada com segurança.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
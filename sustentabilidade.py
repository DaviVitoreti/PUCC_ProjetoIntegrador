import mysql.connector
menu = ""

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="Davi",
    password="JDM7Fqv",
    database="sustentabilidade"
)
cursor = conexao.cursor()
cursor.execute("USE sustentabilidade")

cursor.execute("""""""""
    CREATE TABLE IF NOT EXISTS cadastro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    data DATE,
    consumo_agua FLOAT,
    consumo_energia FLOAT,
    residuos_reciclavel INT,
    residuos_nao_reciclaveis INT,
    transporte VARCHAR(50)           
)
""""""""")

cursor.execute("""""""""
    CREATE TABLE IF NOT EXISTS sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    data DATE,
    media_agua VARCHAR(50),
    media_energia VARCHAR(50),
    media_residuos VARCHAR(50),
    transporte VARCHAR(50)
    )
""""""""")

def susten_agua(consumo_agua):
    if (consumo_agua < 150):
        media_agua = "Alta Sustentabilidade"
    elif (consumo_agua > 200):
        media_agua = "Baixa Sustentabilidade"
    else:
        media_agua = "Moderada Sustentabilidade"
    return media_agua
    

def susten_energia(consumo_energia):
    if (consumo_energia < 5):
        media_energia = "Alta Sustetabilidade"
    elif (consumo_energia > 10):
        media_energia = "Baixa Sustetabilidade"
    else:
        media_energia = "Moderada Sustetabilidade"
    return media_energia

def susten_residuos(geracao_residuos):
    geracao_residuos_nao_reciclaveis = 100 - geracao_residuos
    if (geracao_residuos_nao_reciclaveis < 50):
        media_residuos = "Alta Sustetabilidade"
    elif (geracao_residuos_nao_reciclaveis > 80):
        media_residuos = "Baixa Sustetabilidade"
    else:
        media_residuos = "Moderada Sustetabilidade"
    return media_residuos, geracao_residuos_nao_reciclaveis

def susten_transporte():
    cont_transporte_sustentavel = 0
    cont_transporte_nao_sustentavel = 0
    # Considerar otimização com "for"
    print("\nResponda as pergunta a seguir com S/N com base no seu uso diário")
    transporte_publico = input("Você usa transporte público? ") 
    bicicleta = input("Você usa bicicleta no seu dia a dia? ")
    caminhada = input("Você caminha até os lugares? ")
    carro_fossil = input("Você usa carro a combustível fóssil? ")
    carro_eletrico = input("Você usa carro elétrico? ")
    carona = input("Você pega caronas (fossil)? ")

    transporte_publico = transporte_publico.upper()
    bicicleta = bicicleta.upper()
    caminhada = caminhada.upper()
    carro_fossil = carro_fossil.upper()
    carro_eletrico = carro_eletrico.upper()
    carona = carona.upper()

    if (transporte_publico == "S"):
        cont_transporte_sustentavel += 1
    if (carona == "S"):
        cont_transporte_nao_sustentavel += 1
    if (bicicleta == "S"):
        cont_transporte_sustentavel += 1
    if (caminhada == "S"):
        cont_transporte_sustentavel += 1
    if (carro_eletrico == "S"):
        cont_transporte_sustentavel += 1
    if (carro_fossil == "S"):
        cont_transporte_nao_sustentavel += 1

    if (cont_transporte_sustentavel == 0):
        transporte = "Baixa Sustentabilidade" 
    elif (cont_transporte_nao_sustentavel == 0):
        transporte = "Alta Sustentabilidade"
    else:   
        transporte = "Moderada Sustentabilidade"
    return transporte

def cadastro(id):
    print("\n// Cadastro de Sustentabilidade //")
    nome = input("Digite o seu nome: ")
    nome = nome.title()
    data = input("Digite a data de hoje (AAAA-MM-DD): ")
    consumo_agua = float(input("Digite o seu consumo diário de água (em litros): "))
    consumo_energia = float(input("Digite o seu consumo diário de energia (em kWh): "))
    geracao_residuos = int(input("Digite a porcentagem de geração de resíduos recicláveis: "))
    
    # Primeiro insere os dados básicos no cadastro
    sql_cadastro = "INSERT INTO cadastro (nome, data, consumo_agua, consumo_energia, residuos_reciclavel) VALUES (%s, %s, %s, %s, %s)"
    dados_cadastro = (nome, data, consumo_agua, consumo_energia, geracao_residuos)
    cursor.execute(sql_cadastro, dados_cadastro)
    conexao.commit()
    
    print(id)
    # Agora chama as funções de sustentabilidade que vão atualizar os dados
    agua = susten_agua(consumo_agua)
    energia = susten_energia(consumo_energia)
    residuos, nao_reciclavel = susten_residuos(geracao_residuos)
    transporte = susten_transporte()

    sql = "INSERT INTO sustentabilidade (nome, data,  media_agua, media_energia, media_residuos, transporte) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, data, agua, energia, residuos, transporte))
    conexao.commit()
    
    # Atualiza os campos restantes no cadastro
    sql_update = "UPDATE cadastro SET residuos_nao_reciclaveis = %s, transporte = %s WHERE id = %s"
    cursor.execute(sql_update, (nao_reciclavel, transporte, id))
    conexao.commit()
    
def update_linha(tabela, coluna, valor_cadastro, id):
        sql_alterar = f"UPDATE {tabela} SET {coluna} = %s WHERE id = %s"
        cursor.execute(sql_alterar, (valor_cadastro, id))
        conexao.commit()

def mostrar_linha(linha):
        print(f"1. Nome: {linha[1]}\n"
              f"2. Data: {linha[2]}\n"
              f"3. Consumo Água: {linha[3]}\n"
              f"4. Consumo Energia: {linha[4]}\n"
              f"5. Resíduos Recicláveis: {linha[5]}\n"
              f"6. Resíduos Não Recicláveis: {linha[6]}\n"
              f"7. Transporte: {linha[7]}\n")

def alterar_cadastro(id):
    menu_cadastro = ""
    print("\n// Alterar Cadastro //")
    if (id == None):
        print("Nenhum cadastro encontrado.\n")
        return

    cursor.execute("SELECT * FROM cadastro WHERE id = %s", (id,))
    linha = cursor.fetchone()
    mostrar_linha(linha)

    print(f"Digite o número correspondente ao nome dado que deseja alterar (Ex: 1): ")
    print("Digite \"Sair\" para sair.")
    while (menu_cadastro != "Sair"):
        menu_cadastro = input("< Alterar >: ")
        menu_cadastro = menu_cadastro.title()
        if (menu_cadastro != "Sair"):
            if (menu_cadastro == "7"):
                valor_cadastro = susten_transporte()
                update_linha("cadastro", "transporte", valor_cadastro, id)
                update_linha("sustentabilidade", "transporte", valor_cadastro, id)
            else:
                valor_cadastro = input("< Novo Dado >: ")
                if (menu_cadastro == "1"):
                    update_linha("cadastro", "nome", valor_cadastro, id)
                elif (menu_cadastro == "2"):
                    update_linha("cadastro", "data", valor_cadastro, id)
                else:
                    valor_cadastro = int(valor_cadastro)
                    if (menu_cadastro == "3"):
                        update_linha("cadastro", "consumo_agua", valor_cadastro, id)
                        agua = susten_agua(valor_cadastro)
                        update_linha("sustentabilidade", "media_agua", agua, id)
                    elif (menu_cadastro == "4"):
                        update_linha("cadastro", "consumo_energia", valor_cadastro, id)
                        energia = susten_energia(valor_cadastro)
                        update_linha("sustentabilidade", "media_energia", energia, id)
                    elif (menu_cadastro == "5"):
                        update_linha("cadastro", "residuos_reciclavel", valor_cadastro, id)
                        residuos = susten_residuos(valor_cadastro)
                        update_linha("sustentabilidade", "media_residuos", residuos, id)
                        update_linha("cadastro", "residuos_nao_reciclaveis", valor_cadastro, id)
                    elif (menu_cadastro == "6"):
                        update_linha("cadastro", "residuos_nao_reciclaveis", valor_cadastro, id)
                        valor_cadastro = 100 - valor_cadastro
                        update_linha("cadastro", "residuos_reciclavel", valor_cadastro, id)
                        residuos = susten_residuos(valor_cadastro)
                        update_linha("sustentabilidade", "media_residuos", residuos, id)
                    else:
                        print(f"Opção Inválida!\nVerifique se digitou corretamente.")

def excluir_cadastro(id):
    print("\n// Excluir Cadastro //")

    if (id == None):
        print("Nenhum cadastro encontrado.\n")
        return

    cursor.execute("SELECT * FROM cadastro WHERE id = %s", (id,))
    linha = cursor.fetchone()
    mostrar_linha(linha)
    confirmacao = input("Deseja realmente excluir o cadastro? (S/N): ")

    if (confirmacao.upper() == "S"):
        cursor.execute("DELETE FROM cadastro WHERE id = %s", (id,))
        conexao.commit()
        print("Cadastro excluído com sucesso!\n")
    else:
        print("Cadastro não excluído.\n")

print("// Cadastro de Sustentabilidade //")
while (menu != "Sair"):
    # Obtém o ID do último registro inserido
    cursor.execute("SELECT MAX(id) FROM cadastro")
    last_id = cursor.fetchone()[0]

    print(f"1. Cadastrar dados diários de sustentabilidade.")
    print(f"2. Alterar dados diários de sustentabilidade.")
    print(f"3. Excluir dados diários de sustentabilidade.")
    print(f"Digite \"Menu\" para mostrar este menu novamente.\nDigite \"Sair\" para encerrar o programa.")
    menu = input("< Menu >: ")
    menu = menu.title()

    if (menu != "Sair"):
        if (menu == "1"):
            cadastro(last_id)
        elif (menu == "2"):
            alterar_cadastro(last_id)
        elif (menu == "3"):
            excluir_cadastro(last_id)
import mysql.connector
menu = ""

conexao = mysql.connector.connect(
    host="localhost",
    user="Davi",
    password="<colocar senha>",
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

def cadastro():
    cont_transporte_sustentavel = 0
    cont_transporte_nao_sustentavel = 0
    print("\n// Cadastro de Sustentabilidade //")
    nome = input("Digite o seu nome: ")
    data = input("Digite a data de hoje (AAAA-MM-DD): ")
    consumo_agua = float(input("Digite o seu consumo diário de água (em litros): "))
    consumo_energia = float(input("Digite o seu consumo diário de energia (em kWh): "))
    geracao_residuos = int(input("Digite a porcentagem de geração de resíduos recicláveis: "))

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

    if (consumo_agua < 150):
        media_agua = "Alta Sustentabilidade"
    elif (consumo_agua > 200):
        media_agua = "Baixa Sustentabilidade"
    else:
        media_agua = "Moderada Sustentabilidade"

    if (consumo_energia < 5):
        media_energia = "Alta Sustetabilidade"
    elif (consumo_energia > 10):
        media_energia = "Baixa Sustetabilidade"
    else:
        media_energia = "Moderada Sustetabilidade"

    geracao_residuos_nao_reciclaveis = 100 - geracao_residuos
    if (geracao_residuos_nao_reciclaveis < 50):
        media_residuos = "Alta Sustetabilidade"
    elif (geracao_residuos_nao_reciclaveis > 80):
        media_residuos = "Baixa Sustetabilidade"
    else:
        media_residuos = "Moderada Sustetabilidade"

    if (cont_transporte_sustentavel == 0):
        transporte = "Baixa Sustentabilidade" 
    elif (cont_transporte_nao_sustentavel == 0):
        transporte = "Alta Sustentabilidade"
    else:   
        transporte = "Moderada Sustentabilidade"

    sql_cadastro = "INSERT INTO cadastro (nome, data, consumo_agua, consumo_energia, residuos_reciclavel, residuos_nao_reciclaveis, transporte) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    dados_cadastro = (nome, data, consumo_agua, consumo_energia, geracao_residuos, geracao_residuos_nao_reciclaveis, transporte)
    cursor.execute(sql_cadastro, dados_cadastro)
    conexao.commit()
    sql_sustentabilidade = "INSERT INTO sustentabilidade (nome, data, media_agua, media_energia, media_residuos, transporte) VALUES (%s, %s, %s, %s, %s, %s)"
    dados_sustentabilidade = (nome, data, media_agua, media_energia, media_residuos, transporte)
    cursor.execute(sql_sustentabilidade, dados_sustentabilidade)
    conexao.commit()

    global last_id
    last_id = cursor.lastrowid

def update():
    menu_cadastro = ""
    print("\n// Alterar Cadastro //")
    cursor.execute("SELECT * FROM cadastro")
    linha = cursor.fetchone(last_id)
    def mostrar_linha():
        print(f"1. Nome: {linha[1]}\n"
              f"2. Data: {linha[2]}\n"
              f"3. Consumo Água: {linha[3]}\n"
              f"4. Consumo Energia: {linha[4]}\n"
              f"5. Resíduos Recicláveis: {linha[5]}\n"
              f"6. Resíduos Não Recicláveis: {linha[6]}\n"
              f"7. Transporte: {linha[7]}\n\n")
        mostrar_linha()
    def update_linha(coluna):
        sql_alterar = "UPDATE cadastro SET %s = '%s' WHERE id =",last_id
        cursor.execute(coluna, valor_cadastro)
        conexao.commit

    while (menu_cadastro != "Sair"):
        print(f"Digite o número correspondente ao nome dado que deseja alterar (Ex: 1): ")
        print("Digite \"Sair\" para sair.")
        menu_cadastro = input("< Alterar >: ")
        valor_cadastro = input("< Novo Dado >: ")
        menu_cadastro = menu_cadastro.title()
        
        if (menu_cadastro == "1"):
            update_linha("nome")
        elif (menu_cadastro == "2"):
            update_linha("data")
        elif (menu_cadastro == "3"):
            update_linha("consumo_agua")
        elif (menu_cadastro == "4"):
            update_linha("consumo_energia")
        elif (menu_cadastro == "5"):
            geracao_residuos_nao_reciclaveis = 100 - valor_cadastro
            update_linha("residuos_reciclavel")

print("// Cadastro de Sustentabilidade //")
while (menu != "Sair"):
    print(f"1. Cadastrar dados diários de sustentabilidade.")
    print(f"2. Alterar dados diários de sustentabilidade.")
    print(f"3. Excluir dados diários de sustentabilidade.")
    print(f"Digite \"Menu\" para mostrar este menu novamente.\nDigite \"Sair\" para encerrar o programa.")
    menu = input("< Menu >: ")
    menu = menu.title()

    if (menu == "1"):
        cadastro()
    elif (menu == "2"):
        update()


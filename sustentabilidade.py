import mysql.connector
from sympy import Matrix

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="Davi",
    password="JDM7Fqv",
    database="sustentabilidade"
)

# Cria e usar o banco de dados
cursor = conexao.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS sustentabilidade")
cursor.execute("USE sustentabilidade")

# Criação das tabelas se não existirem
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

# Matriz chave de Hill 2x2
CHAVE_HILL = Matrix([[4, 3], [1, 2]])

# Criptografia Hill
def hill_criptografar(texto):
    texto = texto.upper().replace(" ", "")
    if len(texto) % 2 != 0:
        texto += 'X'  # Padding se necessário

    numeros = [ord(c) - ord('A') for c in texto]
    texto_cifrado = []

    for i in range(0, len(numeros), 2):
        vetor = Matrix([numeros[i], numeros[i+1]])
        vetor_cifrado = CHAVE_HILL * vetor
        vetor_cifrado = vetor_cifrado % 26
        texto_cifrado.extend([chr(int(c) + ord('A')) for c in vetor_cifrado])

    return ''.join(texto_cifrado)

# Descriptografia Hill
def hill_descriptografar(texto_cifrado):
    chave_inversa = CHAVE_HILL.inv_mod(26)  # Se não for invertível, dará erro padrão do Python
    numeros = [ord(c) - ord('A') for c in texto_cifrado]
    texto_original = []

    for i in range(0, len(numeros), 2):
        vetor = Matrix([numeros[i], numeros[i+1]])
        vetor_decifrado = chave_inversa * vetor
        vetor_decifrado = vetor_decifrado % 26
        texto_original.extend([chr(int(c) + ord('A')) for c in vetor_decifrado])

    if (texto_original[-1] == "X"):
        texto_original = texto_original[:-1]

    return ''.join(texto_original)

def descriptografar_campo(campo):
    # Descriptografa apenas se o campo for string e tiver só letras maiúsculas (Hill)
    if isinstance(campo, str) and campo.isalpha() and campo.isupper():
        return hill_descriptografar(campo)
    return campo

# Funções para pegar o último ID
def pegar_ultimo_id():
    cursor.execute("SELECT MAX(id) FROM cadastro")
    last_id = cursor.fetchone()[0]
    return last_id

# Calcula as médias de água
def susten_agua(consumo_agua):
    if consumo_agua < 150:
        media_agua = "ALTA"
    elif consumo_agua > 200:
        media_agua = "BAIXA"
    else:
        media_agua = "MODERADA"
    
    # Criptografar a classificação antes de retornar
    return hill_criptografar(media_agua)

# Calcula as médias de energia
def susten_energia(consumo_energia):
    if consumo_energia < 5:
        media_energia = "ALTA"
    elif consumo_energia > 10:
        media_energia = "BAIXA"
    else:
        media_energia = "MODERADA"
    
    return hill_criptografar(media_energia)

# Calcula as médias de resíduos
def susten_residuos(geracao_residuos):
    geracao_residuos_nao_reciclaveis = 100 - geracao_residuos
    if geracao_residuos_nao_reciclaveis < 50:
        media_residuos = "ALTA"
    elif geracao_residuos_nao_reciclaveis > 80:
        media_residuos = "BAIXA"
    else:
        media_residuos = "MODERADA"
    
    return hill_criptografar(media_residuos), geracao_residuos_nao_reciclaveis

# Calcula as médias de transporte
def susten_transporte():
    cont_transporte_sustentavel = 0
    cont_transporte_nao_sustentavel = 0
    
    print("\nResponda as perguntas a seguir com S/N com base no seu uso diário")
    transporte_publico = input("Você usa transporte público? ").upper()
    bicicleta = input("Você usa bicicleta no seu dia a dia? ").upper()
    caminhada = input("Você caminha até os lugares? ").upper()
    carro_fossil = input("Você usa carro a combustível fóssil? ").upper()
    carro_eletrico = input("Você usa carro elétrico? ").upper()
    carona = input("Você pega caronas (fossil)? ").upper()

    if transporte_publico == "S":
        cont_transporte_sustentavel += 1
    if carona == "S":
        cont_transporte_nao_sustentavel += 1
    if bicicleta == "S":
        cont_transporte_sustentavel += 1
    if caminhada == "S":
        cont_transporte_sustentavel += 1
    if carro_eletrico == "S":
        cont_transporte_sustentavel += 1
    if carro_fossil == "S":
        cont_transporte_nao_sustentavel += 1

    if cont_transporte_sustentavel == 0:
        transporte = "BAIXA" 
    elif cont_transporte_nao_sustentavel == 0:
        transporte = "ALTA"
    else:   
        transporte = "MODERADA"
    
    return hill_criptografar(transporte)

# Função para cadastrar os dados de sustentabilidade
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
    
    # Agora chama as funções de sustentabilidade que vão atualizar os dados
    agua = susten_agua(consumo_agua)
    energia = susten_energia(consumo_energia)
    residuos, nao_reciclavel = susten_residuos(geracao_residuos)
    transporte = susten_transporte()

    sql = "INSERT INTO sustentabilidade (nome, data,  media_agua, media_energia, media_residuos, transporte) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (nome, data, agua, energia, residuos, transporte))
    conexao.commit()
    
    id = pegar_ultimo_id()

    # Atualiza os campos restantes no cadastro
    sql_update = "UPDATE cadastro SET residuos_nao_reciclaveis = %s, transporte = %s WHERE id = %s"
    cursor.execute(sql_update, (nao_reciclavel, transporte, id))
    conexao.commit()

    print("\nCadastro realizado com sucesso!")

# Função para atualizar uma linha específica na tabela
def update_linha(tabela, coluna, valor_cadastro, id):
        sql_alterar = f"UPDATE {tabela} SET {coluna} = %s WHERE id = %s"
        cursor.execute(sql_alterar, (valor_cadastro, id))
        conexao.commit()

# Funções para mostrar os dados do cadastro
def mostrar_cadastro_diario(linha):
    nome = linha[1]
    data = linha[2]
    consumo_agua = linha[3]
    consumo_energia = linha[4]
    residuos_reciclavel = linha[5]
    residuos_nao_reciclaveis = linha[6]

    print(f"1. Nome: {nome}\n"
          f"2. Data: {data}\n"
          f"3. Consumo de Água: {consumo_agua} L\n"
          f"4. Consumo de Energia: {consumo_energia} kWh\n"
          f"5. Resíduos Recicláveis: {residuos_reciclavel} %\n"
          f"6. Resíduos Não Recicláveis: {residuos_nao_reciclaveis} %\n")

# Função para mostrar as médias dos parâmetros
def mostrar_medias(linha):
    media_agua = descriptografar_campo(linha[3]).title() + " Sustentabilidade"
    media_energia = descriptografar_campo(linha[4]).title() + " Sustentabilidade"
    media_residuos = descriptografar_campo(linha[5]).title() + " Sustentabilidade"
    media_transporte = descriptografar_campo(linha[6]).title() + " Sustentabilidade"

    print(f"1. Média Água: {media_agua}\n"
          f"2. Média Energia: {media_energia}\n"
          f"3. Média Residuos: {media_residuos}\n"
          f"4. Média Transporte: {media_transporte}\n")

# Funções para alterar
def alterar_cadastro(id):
    menu_cadastro = ""

    cursor.execute("SELECT * FROM cadastro WHERE id = %s", (id,))
    linha = cursor.fetchone()

    if (linha == None):
        print("Nenhum cadastro encontrado.")
        return
    
    transporte = descriptografar_campo(linha[7]).title() + " Sustentabilidade"

    def printar_linhas(linha):
        print(f"\n/ id = {id} /\n"
            f"1. Nome: {linha[1]}\n"
            f"2. Data: {linha[2]}\n"
            f"3. Consumo de Água: {linha[3]}L\n"
            f"4. Consumo de Energia: {linha[4]}kWh\n"
            f"5. Resíduos Recicláveis: {linha[5]}%\n"
            f"6. Resíduos Não Recicláveis: {linha[6]}%\n"
            f"7. Transporte: {transporte}\n")

    print(f"\nDigite o número correspondente ao nome dado que deseja alterar (Ex: 1): ")
    print("Digite \"Sair\" para sair.")
    while (menu_cadastro != "Sair"):
        printar_linhas(linha)

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
        print("\nCadastro alterado com sucesso!")
        menu_cadastro = input("Digite \"Sair\" para sair ou pressione Enter para continuar: ")

# Função para excluir um cadastro específico
def excluir_cadastro(id):
    cursor.execute("SELECT * FROM cadastro WHERE id = %s", (id,))
    linha = cursor.fetchone()

    if (linha == None):
        print("Nenhum cadastro encontrado.")
        return
    
    transporte = descriptografar_campo(linha[7]).title() + " Sustentabilidade"

    print(f"/ id = {id} /\n"
        f"1. Nome: {linha[1]}\n"
        f"2. Data: {linha[2]}\n"
        f"3. Consumo de Água: {linha[3]} L\n"
        f"4. Consumo de Energia: {linha[4]} kWh\n"
        f"5. Resíduos Recicláveis: {linha[5]} %\n"
        f"6. Resíduos Não Recicláveis: {linha[6]} %\n"
        f"7. Transporte: {transporte}\n")
    
    confirmacao = input("Deseja realmente excluir o cadastro? (S/N): ")

    if (confirmacao.upper() == "S"):
        cursor.execute("DELETE FROM cadastro WHERE id = %s", (id,))
        conexao.commit()
        print("Cadastro excluído com sucesso!")
    else:
        print("Cadastro não excluído.")

# Mostrar todos os cadastros
def mostrar_cadastro(id):
    print("\n// Mostrar Cadastro //")
    if (id == None):
        print("Nenhum cadastro encontrado.")
        return

    temp_id = id + 1
    id = 1

    while (id != temp_id):
        cursor.execute("SELECT * FROM sustentabilidade WHERE id = %s", (id,))
        linha1 = cursor.fetchone()
        cursor.execute("SELECT * FROM cadastro WHERE id = %s", (id,))
        linha2 = cursor.fetchone()
        if (id != temp_id):
            print(f"// Cadastro id N°{id} //:")
            print(f"-- Cadastro Diário --")
            mostrar_cadastro_diario(linha2)
            print(f"-- Médias dos parâmetros --")
            mostrar_medias(linha1)
            print("-----\n")
        id += 1

menu = ""
# Menu principal
print("// Cadastro de Sustentabilidade //")
while (menu != "Sair"):
    id = pegar_ultimo_id()

    print("\n// Menu //")
    print(f"1. Cadastrar dados diários de sustentabilidade.")
    print(f"2. Alterar dados diários de sustentabilidade.")
    print(f"3. Excluir dados diários de sustentabilidade.")
    print(f"4. Mostrar dados diários de sustentabilidade.")
    print(f"Digite \"Menu\" para mostrar este menu novamente.\nDigite \"Sair\" para encerrar o programa.")
    menu = input("< Menu >: ")
    menu = menu.title()

    if (menu != "Sair"):
        if (menu == "1"):
            cadastro(id)
        elif (menu == "2"):
            print("\n// Alterar Cadastro //")
            id = int(input("Digite o ID do cadastro que deseja alterar: "))
            alterar_cadastro(id)
        elif (menu == "3"):
            print("\n// Excluir Cadastro //")
            id = int(input("Digite o ID do cadastro que deseja alterar: "))
            excluir_cadastro(id)
        elif (menu == "4"):
            mostrar_cadastro(id)
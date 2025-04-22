import mysql.connector
cont_transporte_sustentavel = 0
cont_transporte_nao_sustentavel = 0

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

print("// Cadastro de Sustentabilidade //")
nome = input("Digite o seu nome: ")
data = input("Digite a data de hoje (AAAA-MM-DD): ")
consumo_agua = float(input("Digite o seu consumo diário de água (em litros): "))
consumo_energia = float(input("Digite o seu consumo diário de energia (em kWh): "))
geracao_residuos = int(input("Digite a porcentagem de geração de resíduos recicláveis: "))

geracao_residuos_nao_reciclaveis = 100 - geracao_residuos

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

print("\n// Resultado de {nome} //")
print(f"Data: {data}")
print(f"Consumo de Água: {media_agua}")
print(f"Consumo de Energia: {media_energia}")
print(f"Geração de resíduos não reciclaveis: {media_residuos}")
print(f"Uso de Transporte: {transporte}")
print(f"\nOs dados foram registrados no banco de dados.\n")

sql_cadastro = "INSERT INTO cadastro (nome, data, consumo_agua, consumo_energia, residuos_reciclavel, residuos_nao_reciclaveis, transporte) VALUES (%s, %s, %s, %s, %s, %s, %s)"
dados_cadastro = (nome, data, consumo_agua, consumo_energia, geracao_residuos, geracao_residuos_nao_reciclaveis, transporte)
cursor.execute(sql_cadastro, dados_cadastro)
conexao.commit()

sql_sustentabilidade = "INSERT INTO sustentabilidade (nome, data, media_agua, media_energia, media_residuos, transporte) VALUES (%s, %s, %s, %s, %s, %s)"
dados_sustentabilidade = (nome, data, media_agua, media_energia, media_residuos, transporte)
cursor.execute(sql_sustentabilidade, dados_sustentabilidade)
conexao.commit()
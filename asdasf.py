import mysql.connector
from datetime import datetime, timedelta, date

# Conexão com o banco de dados
conexao_bd = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jv23696406",
    database="testebanco"
)

# Função para registrar a entrada do veículo
def registrar_entrada(placa, modelo):
    cursor = conexao_bd.cursor()
    data_entrada = date.today()
    horario_entrada = datetime.now()
    cursor.execute("INSERT INTO sua_tabela (data, placa, modelo, horario_entrada) VALUES (%s, %s,%s, %s)", (data_entrada, placa, modelo, horario_entrada))
    conexao_bd.commit()
    print("Entrada registrada com sucesso.")

# Função para registrar a saída do veículo e calcular o preço
def registrar_saida(placa):
    cursor = conexao_bd.cursor()
    #data_saida = date.today()
    horario_saida = datetime.now()
    cursor.execute("UPDATE sua_tabela SET horario_saida = %s WHERE placa = %s AND horario_saida is NULL ", (horario_saida, placa))

    # cursor.execute("SELECT entrada, modelo FROM registro_veiculos WHERE placa = %s ORDER BY id DESC LIMIT 1", (placa,))
    #entrada, modelo = cursor.fetchone()
    #tempo_permanencia = saida - entrada
    #preco_por_hora = 10  # Valor fixo por hora
    #preco_total = round((tempo_permanencia.total_seconds() / 3600) * preco_por_hora, 2)
    #cursor.execute("UPDATE testedatahora SET data_saida = %s, horario_saida = %s WHERE data_saida IS NULL AND horario_saida IS NULL", (data_saida, horario_saida))
    conexao_bd.commit()

def exibe():

    cursor = conexao_bd.cursor()
    cursor.execute("SELECT data, placa, modelo, horario_entrada, horario_saida FROM sua_tabela ORDER BY id DESC LIMIT 1")
    linha_mais_recente = cursor.fetchone()

    data = linha_mais_recente[0].strftime("%d/%m/%Y")
    placa = linha_mais_recente[1]
    modelo = linha_mais_recente[2]
    horario_entrada = linha_mais_recente[3]
    horario_saida = linha_mais_recente[4]


    print(f"Data:{data} | Placa: {placa} | Modelo: {modelo} |Horario entrada {horario_entrada} |Horario saida: {horario_saida}")

#horario_atual = datetime.now().strftime("%H:%M:%S")
#print(horario_atual)
#data = date.today().strftime("%d/%m/%Y")
#print(data)
#registrar_entrada('CBA4312', 'GOL')
registrar_saida('CBA4312')
exibe()

# Fechar conexão com o banco de dados
conexao_bd.close()
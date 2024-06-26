from flask import Flask, request, render_template, json, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, date
import MySQLdb.cursors


app = Flask(__name__)
app.static_folder = 'static'

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "jv23696406"
app.config["MYSQL_DB"] = "parkinho"

mysql = MySQL(app)

@app.route('/')
def home():

    return render_template('index.html')

@app.route('/entrada', methods=['POST', 'GET'])
def entrada():

    if request.method == 'POST':
        # _data = date.today().strftime("%d/%m/%Y") > apenas data formatada br

        _placa = request.form['inputPlacaEntrada']
        _modelo = request.form['inputModelo']
         #_horario = datetime.now().strftime("%H:%M:%S") > apenas horario formatado br
        if _placa and _modelo:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Verifica se já existe um registro de entrada sem saída para a placa fornecida
            cur.execute("SELECT * FROM historico WHERE placa = %s AND horario_saida IS NULL", (_placa,))
            existing_record = cur.fetchone()

            if existing_record:

                error_message = "Placa fornecida já possui registro de entrada em aberto"
                cur.close()
                return render_template('index.html', errorEntrada=error_message)
            else:

                data = date.today()
                horario_entrada = datetime.now()
                cur.execute("INSERT INTO historico (data, placa, modelo, horario_entrada) VALUES (%s, %s, %s, %s)", (data, _placa, _modelo, horario_entrada))
                mysql.connection.commit()


            cur.close()

            return redirect(url_for('entrada'))

    return render_template('index.html')

@app.route('/saida', methods=['POST', 'GET'])
def saida():
    if request.method == 'POST':
        if 'inputPlacaSaida' in request.form:
            _placa = request.form['inputPlacaSaida']

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cur.execute("SELECT * FROM historico WHERE placa = %s AND horario_saida IS NULL", (_placa,))
            vehicle = cur.fetchone()

            if vehicle:
                entrada = vehicle['horario_entrada']
                horario_saida = datetime.now()

                cur.execute("SELECT * FROM mensalistas WHERE placa = %s", (_placa,))
                mensalista_vehicle = cur.fetchone()

                if mensalista_vehicle:
                    preco = 0
                else:
                    preco = calculate_fee(entrada, horario_saida)

                cur.execute("UPDATE historico SET horario_saida = %s WHERE placa = %s AND horario_saida is NULL", (horario_saida, _placa))
                mysql.connection.commit()
                cur.close()

                return render_template('index.html', preco=preco)
            else:
                error_message = "Nenhum registro de entrada em aberto encontrado para a placa fornecida."
                cur.close()
                return render_template('index.html', errorSaida=error_message)
        

            
    return render_template('index.html')




@app.route('/mensalista' , methods=['POST', 'GET'])
def mensalista():
    if request.method == 'POST':

        _placa = request.form['inputPlacaMensalista']
        _nome = request.form['inputName']

        if _placa and _nome:

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Verifica se a placa já está registrada como mensalista
            cur.execute("SELECT * FROM mensalistas WHERE placa = %s", (_placa,))
            existing_record = cur.fetchone()

            if existing_record:
                error_message = "Placa fornecida já existente"
                cur.close()
                return render_template('index.html', errorInsertMensalista=error_message)
            
            else:
                cur.execute ("INSERT INTO mensalistas (placa, nome) VALUES( %s, %s)", (_placa, _nome))

                mysql.connection.commit()

                return redirect(url_for('mensalista'))
    
    return render_template('index.html')

@app.route('/delete_plate', methods=['POST'])
def delete_plate():
    if request.method == 'POST':
        plate = request.form['plate']

        # Delete the entry from the database
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM mensalistas WHERE placa = %s", (plate,))
        rows_affected = cur.rowcount
        mysql.connection.commit()
        cur.close()

        if rows_affected >0: 
            return render_template('index.html')
        else:
            error_message = "Não há veículo mensalista registrado com a placa fornecida"
            return render_template('index.html', errorDeleteMensalista=error_message)

        
    

@app.route('/excluir_mensalista' , methods=['post'])
def excluir_mensalista():
    if request.method == ['post']:
        _placa = request.form['inputExcluirMensalista']

        if _placa:

            cur = mysql.connection.cursor()
            cur.execute ("DELETE FROM mensalistas WHERE placa=%s", (_placa))

            mysql.connection.commit()

            return redirect(url_for('mensalista'))

    return render_template('index.html')  
    



@app.route('/historico_data')
def get_historico_data():
    

    cur = mysql.connection.cursor()
    query = "SELECT * FROM historico ORDER BY id DESC"
    cur.execute(query)
    result = cur.fetchall()

    data = []
    for row in result:
        data.append({
            'id': row[0],
            'data': row[1].strftime("%d/%m/%Y"),
            'placa': row[2],
            'modelo': row[3],
            'entrada': str(row[4]),
            'saida': str(row[5]),
            
        })

    return jsonify(data)

@app.route('/mensalista_data')
def get_mensalist_data():

    cur = mysql.connection.cursor()
    query = "SELECT * FROM mensalistas ORDER BY id DESC"
    cur.execute(query)
    result = cur.fetchall()

    data = []
    for row in result:
        data.append({
            'id':row[0],
            'placa':row[1],
            'nome': row[2]
        })
    
    return jsonify(data)


def calculate_fee(entrada, saida):
    fmt = '%Y-%m-%d %H:%M:%S'
    
    if isinstance(entrada, str):
        d1 = datetime.strptime(entrada, fmt)
    else:
        d1 = entrada
    
    if isinstance(saida, str):
        d2 = datetime.strptime(saida, fmt)
    else:
        d2 = saida
    
    diff = d2 - d1

    diferenca = str(diff)

    if diferenca[12] == '0':
        fee = 5
    
    if diferenca[12] == '1' :
        fee = 10

    if diferenca[12] == '2':
        fee = 15

    if diferenca[12] == '3':
        fee = 20

    if diferenca[12] == '4':
        fee = 25

    if diferenca[12] > '4':
        fee = 30

    print(diferenca[12])

    return fee

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

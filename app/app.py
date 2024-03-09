from flask import Flask, request, render_template, json, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, date


app = Flask(__name__)
app.static_folder = 'static'

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "jv23696406"
app.config["MYSQL_DB"] = "testebanco"

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

            data = date.today()
            horario_entrada = datetime.now()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO sua_tabela (data, placa, modelo, horario_entrada) VALUES (%s, %s,%s, %s)", (data, _placa, _modelo, horario_entrada))

            mysql.connection.commit()


            return redirect(url_for('entrada'))
    
    return render_template('index.html')

@app.route('/saida', methods=['POST', 'GET'])
def saida():

    if request.method == 'POST':

        _placa = request.form['inputPlacaSaida']

        if _placa:

            horario_saida = datetime.now()
            cur = mysql.connection.cursor()
            cur.execute("UPDATE sua_tabela SET horario_saida = %s WHERE placa = %s AND horario_saida is NULL", (horario_saida, _placa))


            mysql.connection.commit()

            return redirect(url_for('saida'))
            
    return render_template('index.html')


@app.route('/mensalista' , methods=['POST', 'GET'])
def mensalista():
    if request.method == 'POST':

        _placa = request.form['inputPlacaMensalista']
        _nome = request.form['inputName']

        if _placa and _nome:

            cur = mysql.connection.cursor()
            cur.execute ("INSERT INTO mensalistas (placa, nome) VALUES( %s, %s)", (_placa, _nome))

            mysql.connection.commit()

            return redirect(url_for('mensalista'))
    
    return render_template('index.html')


@app.route('/historico_data')
def get_historico_data():
    

    cur = mysql.connection.cursor()
    query = "SELECT * FROM sua_tabela ORDER BY id DESC"
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
            # Adicione mais campos conforme necessário
        })

    return jsonify(data)

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)

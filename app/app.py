from flask import Flask, request, render_template
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

@app.route('/entrada', methods=['POST'])
def entrada():

    if request.method == 'POST':

        # _data = date.today().strftime("%d/%m/%Y") > apenas data formatada br

        _placa = request.form['inputPlacaEntrada']
        _modelo = request.form['inputModelo']
         #_horario = datetime.now().strftime("%H:%M:%S") > apenas horario formatado br
        data = date.today()
        horario_entrada = datetime.now()

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sua_tabela (data, placa, modelo, horario_entrada) VALUES (%s, %s,%s, %s)", (data, _placa, _modelo, horario_entrada))

        mysql.connection.commit()

        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)

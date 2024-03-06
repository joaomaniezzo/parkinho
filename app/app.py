from flask import Flask, request, render_template
from flask_mysqldb import MySQL


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

        _placa = request.form['inputPlacaEntrada']
        _modelo = request.form['inputModelo']

        print(f"Placa: {_placa}, Modelo: {_modelo}")

        cur = mysql.connection.cursor()
        cur.execute(""" insert into testeplacaentrada (placa, modelo) VALUES (%s, %s)""", (_placa,_modelo))

        mysql.connection.commit()

        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)

from flask import Flask, request, render_template


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():


    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
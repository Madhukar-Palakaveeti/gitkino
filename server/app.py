import os
from helper import get_user_data, predict
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect',methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        user = request.form['input_text']
        user_data = get_user_data(user)
        result = 'SLOP' if predict(user_data) else 'KINO'
        return render_template('index.html', result=result)

app.run(debug=True)
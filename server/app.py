import os
from helper import get_user_data, predict
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect',methods=['GET', 'POST'])
def detect(result=None):
    if request.method == 'POST':
        user = request.form['input_text']
        user_data = get_user_data(user) if user else None
        if user_data:
            avatar_url = user_data[0]
            result = 'SLOP' if predict(user_data[1:]) else 'KINO' 
        # print(user_data)
        return render_template('detect.html', result=result, avatar_url=avatar_url, user_data=user_data[1:])

app.run(debug=True)
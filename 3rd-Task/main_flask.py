from flask import Flask, render_template, request, redirect, url_for
from map_render import main


app = Flask(__name__)

@app.route('/home', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        artist_name = request.form['artist']
        main(artist_name)
        return render_template(f'Map_{artist_name}.html')
    else:
        return render_template('index.html')

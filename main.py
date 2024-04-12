from flask import Flask, render_template
import psycopg2
import sys
import logging


app = Flask(__name__)

pg = psycopg2.connect('''
    host=localhost
    port=5432
    user=postgres
    password=rootroot
    dbname=postgres
''')

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format="%(asctime)s - %(message)s", # - %(levelname)s - %(name)s -
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    app.run(host='0.0.0.0', debug=True)
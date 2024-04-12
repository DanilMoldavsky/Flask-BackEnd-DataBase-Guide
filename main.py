from flask import Flask, render_template
import redis
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

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/cities')
def read_count():
    pair = 'cities:count'
    redisCount = r.get(pair)
    if redisCount:
        result = redisCount + ' (из кэша)'
        return render_template('cities.html', value=result)
    
    cursos = pg.cursor()
    cursos.execute("SELECT COUNT(*) FROM city WHERE countrycode = 'USA';")
    pgCount = cursos.fetchone()[0]
    
    result = str(pgCount) + ' (из постгри)'
    
    r.set(pair, pgCount)
    
    return render_template('cities.html', value=result)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
        format="%(asctime)s - %(message)s", # - %(levelname)s - %(name)s -
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    app.run(host='0.0.0.0', debug=True)
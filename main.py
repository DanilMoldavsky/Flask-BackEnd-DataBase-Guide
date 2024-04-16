# Код создан на основе гайда от Winderton - https://www.youtube.com/watch?v=jcsG-IlJ-SA&list=WL&index=6&ab_channel=Winderton
from flask import Flask, render_template, jsonify, request
import redis
import psycopg2
import sys
import logging

from gpt import Gpt

app = Flask(__name__)

gpt_respose = Gpt()

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

@app.route('/gpt')
def gpt():
    return render_template('gpt.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = 'Отвечай с форматированием языка html, а не markdown, пожалуйста' + data['message']
    
    response_from_gpt = gpt_respose.talk_valid_markdown(prompts=user_message)
    # Здесь вы будете обрабатывать сообщение с помощью ChatGPT
    # и возвращать ответ. Предположим, что функция chat_with_gpt
    # отправляет сообщение в ChatGPT и возвращает ответ.
    # response_from_gpt = chat_with_gpt(user_message)
    
    # Пока что мы вернем заглушку для ответа
    # response_from_gpt = "This is a response from ChatGPT."

    return jsonify({'reply': response_from_gpt})

@app.route("/countries")
def countries_api():
    cursos = pg.cursor()
    cursos.execute("SELECT code, name, headofstate FROM country")
    countries = cursos.fetchall()

    countries_data = []
    for country in countries:
        countries_data.append({
            'tag': country[0],
            'name': country[1],
            'headofstate': country[2]
        })
        
    return jsonify(
        countries=countries_data
    )

# @app.route("/countries/roulette")
# def countries_api():
#     cursos = pg.cursor()
#     cursos.execute("SELECT code, name, headofstate FROM country")
#     countries = cursos.fetchall()

#     countries_data = []
#     for country in countries:
#         countries_data.append({
#             'tag': country[0],
#             'name': country[1],
#             'headofstate': country[2]
#         })
    
    
#     return render_template

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename=".log",
        filemode="a",
        format="%(asctime)s - %(message)s", # - %(levelname)s - %(name)s -
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    app.run(host='0.0.0.0', debug=True)
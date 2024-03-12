#!/usr/bin/python
from flask import Flask, request, render_template
import parser_lordfilm

app = Flask(__name__)

@app.route('/')
def start_page():
    return render_template('index.html')

@app.route('/movies', methods=['GET', 'POST'])
def downlad():
    message=''
    if request.method == 'POST':
        user_link = request.form.get('search_bar')
        try:
            data = parser_lordfilm.main(user_link)
            message = data          
        except: message = '<b>Что-то пошло не так:</b> видео ненайдено или отправлена некоректная ссылка'
    return render_template('movies.html', message=message)


# @app.route('/movies', methods=['GET', 'POST'])
# def download_movie():
#     message = ''
#     if request.method == 'POST':
#         user_link = request.form.get('search_bar')
#         try:
#             link = parser_lordfilm.get_film(user_link)
#             message = f'Нажмите, чтобы <b><a href={link} style="color:#7BA7AB">СКАЧАТЬ</a></b> фильм'
           
#         except: message = '<b>Что-то пошло не так:</b> видео ненайдено или отправлена некоректная ссылка'
#     return render_template('movies.html', message=message)
   
# @app.route('/serials', methods=['GET', 'POST'])
# def download_movie():
#     pass

if __name__ == '__main__':
    app.run(port=8000)

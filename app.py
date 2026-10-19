from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
db_name = "database.db"


def create_connection(db_file):
    connection=None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return connection


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/players')
def players():
    query = "SELECT * from uwhplayers"
    con = create_connection(db_name)
    cur = con.cursor()
    cur.execute(query)
    player_list = cur.fetchall()
    con.close()
    return render_template('players.html', player=player_list)


@app.route('/search')
def search():
    search_query = request.args.get('query')
    players = query('SELECT * FROM players WHERE name LIKE ?', (search_query,))
    return render_template('players.html', players=players)


if __name__ == '__main__':
    app.run()

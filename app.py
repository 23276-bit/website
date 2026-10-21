from click import Tuple
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
db_name = "identifier.sqlite"


def create_connection(db_file):
    connection=None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return connection

def query(cmd, args=()):
    con = create_connection(db_name)
    cur = con.cursor()
    out = cur.execute(cmd, args)
    res = out.fetchall()
    con.close()

    return res
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/players')
def players():
    player_list = query("SELECT * from uwhplayers")
    return render_template('players.html', player=player_list)


@app.route('/search')
def search():
    search_query = request.args.get('query')
    players = query('SELECT * FROM uwhplayers WHERE Name LIKE ? OR Cap_Number LIKE ? OR Age LIKE ? OR Position LIKE ? OR Stick LIKE ? OR Ghost LIKE ? OR Stick_Type LIKE ? OR Club', (f'%{search_query}%',) * 7)
    return render_template('players.html', player=players)


if __name__ == '__main__':
    app.run()

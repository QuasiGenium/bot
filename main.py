from flask import Flask, make_response, jsonify
from flask_restful import Api
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'kkkk'
api = Api(app, catch_all_404s=True)


def main():
    db_session.global_init("db/players.db")

    app.run()


if __name__ == '__main__':
    main()
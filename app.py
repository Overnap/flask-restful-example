from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from database import db
from route import initialize

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

initialize(api)

if __name__ == '__main__':
    app.run(host="0.0.0.0")

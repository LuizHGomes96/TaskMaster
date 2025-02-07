from flask import Flask
from flask_sqlalchemy import SQLAlchemy #type: ignore
from flask_migrate import Migrate #type: ignore


app = Flask(__name__)

# OLD SQLITE DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

#NEW MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://luizhgomes96:!Luiz0443@localhost/mytasks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'i dont know why i need this for'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import db
from app import routes

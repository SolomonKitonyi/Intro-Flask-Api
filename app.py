from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///school.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from routes import student_routes,tm_routes

app.register_blueprint(tm_routes.bp)
app.register_blueprint(student_routes.bp)

if __name__== '__main__':
    app.run(debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantes.bd'    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import crud_bp
    app.register_blueprint(crud_bp)

    from .admin import init_admin
    init_admin(app)
    return app
import os
from datetime import datetime, timedelta
from flask import Flask
from models import db, User
# from routes import init_routes
from resources import api
from jwt_authorization import generate_token, verify_token, token_required, admin_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
# ----------------- Initialize Flask App ------------------ #
app = Flask(__name__)
CORS(app)
app.secret_key = "astitva"  # For session-based login

# RESTful API Init
api.init_app(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = "astitva-jwt-secret"  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)
# ----------------- Database Config ------------------ #
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'mydatabase.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

# Initialize the database
db.init_app(app)

# ----------------- Attach JWT Utils to app ------------------ #
app.generate_token = generate_token
app.verify_token = verify_token
app.token_required = token_required
app.admin_required = admin_required

# ----------------- Route Initialization ------------------ #
# init_routes(app)

# ----------------- Create Admin if Missing ------------------ #
def create_admin():
    with app.app_context():
        admin = User.query.filter_by(Role="admin").first()
        if not admin:
            new_admin = User(
                Username="admin",
                Email="admin@example.com",
                Fullname="Admin User",
                Qualification="System Admin",
                DOB=datetime.strptime("2000-01-01", "%Y-%m-%d").date(),
                Role="admin"
            )
            new_admin.set_password("admin123")
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            # Upgrade to hashed password if needed
            if not admin.Password.startswith("pbkdf2:"):
                print("Updating admin password to hashed version")
                admin.set_password("admin123")
                db.session.commit()

# ----------------- Main Entry Point ------------------ #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)

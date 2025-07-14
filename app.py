import os 
from flask import Flask
from datetime import datetime

# Import models and database
from models import db, User
from routes import init_routes

# Initializing Flask app
app = Flask(__name__)
app.secret_key = "astitva"

# Database configuration
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'mydatabase.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

# Initializing the database
db.init_app(app)

# Initialize routes
init_routes(app)

# Predefined admin details 
def create_admin():
    with app.app_context():
        admin = User.query.filter_by(Role="admin").first()
        if not admin:
            new_admin = User(
                Username="admin",
                Email="admin@example.com",
                Password="admin123", 
                Fullname="Admin User",
                Qualification="System Admin",
                DOB=datetime.strptime("2000-01-01", "%Y-%m-%d").date(), 
                Role="admin")
            db.session.add(new_admin)
            db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        create_admin()  # Creating admin before running flask 
    app.run(debug=True)
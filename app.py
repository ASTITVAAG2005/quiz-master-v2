import os
from datetime import datetime, timedelta
from flask import Flask
from models import db, User
from resources import api
from jwt_authorization import generate_token, verify_token, token_required, admin_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_mail import Mail
from celery import Celery
from caching import cache
import sqlite3

# Enable foreign key constraints in SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

app = Flask(__name__, template_folder='.')
CORS(app)
app.secret_key = "astitva"

# Configurations
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 20

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'mydatabase.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

app.config['JWT_SECRET_KEY'] = "astitva-jwt-secret"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@quizmaster.com'

# Init Extensions
jwt = JWTManager(app)
mail = Mail(app)
db.init_app(app)
api.init_app(app)
cache.init_app(app)

# Custom JWT
app.generate_token = generate_token
app.verify_token = verify_token
app.token_required = token_required
app.admin_required = admin_required

# Celery Setup
def make_celery(app):
    celery = Celery(app.import_name,
                    broker='redis://localhost:6379/1',
                    backend='redis://localhost:6379/2')
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

from celery.schedules import crontab
celery.conf.beat_schedule = {
    'send_daily_reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(minute=0, hour=18),
    },
    'send_monthly_activity_report': {
        'task': 'tasks.send_monthly_activity_report',
        'schedule': crontab(minute=0, hour=6, day_of_month=1),
    },
}

# Admin init
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
        else:
            if not admin.Password.startswith("pbkdf2:"):
                admin.set_password("admin123")
                db.session.commit()

def create_app():
    return app

@app.route("/test-daily")
def trigger_test():
    from tasks import send_daily_reminders
    send_daily_reminders.delay()
    return "Task triggered!"

@app.route("/test-monthly")
def trigger_monthly():
    from tasks import send_monthly_activity_report
    send_monthly_activity_report.delay()
    return "Monthly report task triggered!"

from flask import send_from_directory

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path and os.path.exists(os.path.join("dist", path)):
        return send_from_directory("dist", path)
    return send_from_directory("dist", "index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    import tasks  
    app.run(debug=True)


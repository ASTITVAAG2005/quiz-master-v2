import os 
from flask import Flask
from datetime import datetime, timedelta
import jwt
from functools import wraps

# Import models and database
from models import db, User
from routes import init_routes

# Initializing Flask app
app = Flask(__name__)
app.secret_key = "astitva"

# JWT Configuration
app.config['JWT_SECRET_KEY'] = "astitva-jwt-secret"  # Change this to a secure secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Database configuration
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(current_dir, 'mydatabase.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'

# Initializing the database
db.init_app(app)

# JWT utility functions
def generate_token(user_id, username, role):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify
        
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        current_user = verify_token(token)
        if current_user is None:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask import request, jsonify
        
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        current_user = verify_token(token)
        if current_user is None:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Make decorators available globally
app.token_required = token_required
app.admin_required = admin_required
app.generate_token = generate_token
app.verify_token = verify_token

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
                Fullname="Admin User",
                Qualification="System Admin",
                DOB=datetime.strptime("2000-01-01", "%Y-%m-%d").date(), 
                Role="admin")
            new_admin.set_password("admin123")  # Use hashed password
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            # Check if existing admin has plain text password and update it
            if not admin.Password.startswith('pbkdf2:'):  # Werkzeug hash starts with pbkdf2:
                print("Updating admin password to hashed version")
                admin.set_password("admin123")
                db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
        create_admin()  # Creating admin before running flask 
    app.run(debug=True)
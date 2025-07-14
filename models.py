from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize db object (will be imported and configured in app.py)
db = SQLAlchemy()


# -------------------------------- Models and Tables ---------------------------------------- #


class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(500), nullable=False, unique=True)
    Email = db.Column(db.String(500), nullable=False, unique=True)
    Password = db.Column(db.String(500), nullable=False)
    Fullname = db.Column(db.String(500), nullable=False)
    Qualification = db.Column(db.String(500), nullable=False)
    DOB = db.Column(db.Date, nullable=False)
    Role = db.Column(db.String(10), nullable=False, default="user")
    
    def set_password(self, password):
        """Hash and set password"""
        self.Password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hashed password"""
        return check_password_hash(self.Password, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'Email': self.Email,
            'Fullname': self.Fullname,
            'Qualification': self.Qualification,
            'DOB': self.DOB.isoformat() if self.DOB else None,
            'Role': self.Role
        }


class Subject(db.Model):
    __tablename__ = 'subject'
    SubjectID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Subjectname = db.Column(db.String(500), nullable=False)
    Description = db.Column(db.String(500), nullable=False)


class Chapter(db.Model):
    __tablename__ = 'chapter'
    ChapterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Chaptername = db.Column(db.String(500), nullable=False)
    Description = db.Column(db.String(500), nullable=False)

    QuizR = db.relationship('Quiz', backref='chapter', lazy=True)
    SubjectID = db.Column(db.Integer, db.ForeignKey('subject.SubjectID'), nullable=False)
    subject = db.relationship('Subject', backref='chapters')


class Quiz(db.Model):
    __tablename__ = 'quiz'
    QuizID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_of_quiz = db.Column(db.Date, nullable=False)
    Time_duration = db.Column(db.String(5), nullable=False)
    Remarks = db.Column(db.String(500))
    ChapterID = db.Column(db.Integer, db.ForeignKey('chapter.ChapterID'), nullable=False)
    QuestionsR = db.relationship('Questions', backref='quiz', lazy=True)


class Questions(db.Model):
    __tablename__ = 'questions'
    QuestionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Question_statement = db.Column(db.String(500), nullable=False)
    Option1 = db.Column(db.String(500), nullable=False)
    Option2 = db.Column(db.String(500), nullable=False)
    Option3 = db.Column(db.String(500), nullable=False)
    Option4 = db.Column(db.String(500), nullable=False)
    Correct_option = db.Column(db.String(500), nullable=False)
    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID'), nullable=False)


class UserAnswers(db.Model):
    __tablename__ = 'user_answers'
    AnswerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ScoreID = db.Column(db.Integer, db.ForeignKey('score.ScoreID'), nullable=False)
    QuestionID = db.Column(db.Integer, db.ForeignKey('questions.QuestionID'), nullable=False)
    SelectedAnswer = db.Column(db.String(500), nullable=True)

    score = db.relationship('Score', backref='user_answers')
    question = db.relationship('Questions', backref='user_answers')


class Score(db.Model):
    __tablename__ = 'score'
    ScoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    TimeStamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Auto-fills time of attempt
    TotalScore = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='scores')
    quiz = db.relationship('Quiz', backref='scores')

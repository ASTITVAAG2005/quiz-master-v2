from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


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

    scores = db.relationship('Score', backref='user', cascade='all, delete', passive_deletes=True)

    def set_password(self, password):
        self.Password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.Password, password)

    def to_dict(self):
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

    chapters = db.relationship('Chapter', backref='subject', cascade='all, delete', passive_deletes=True)


class Chapter(db.Model):
    __tablename__ = 'chapter'
    ChapterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Chaptername = db.Column(db.String(500), nullable=False)
    Description = db.Column(db.String(500), nullable=False)

    SubjectID = db.Column(db.Integer, db.ForeignKey('subject.SubjectID', ondelete='CASCADE'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', cascade='all, delete', passive_deletes=True)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    QuizID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Date_of_quiz = db.Column(db.Date, nullable=False)
    Time_duration = db.Column(db.String(5), nullable=False)
    Remarks = db.Column(db.String(500))

    ChapterID = db.Column(db.Integer, db.ForeignKey('chapter.ChapterID', ondelete='CASCADE'), nullable=False)
    questions = db.relationship('Questions', backref='quiz', cascade='all, delete', passive_deletes=True)
    scores = db.relationship('Score', backref='quiz', cascade='all, delete', passive_deletes=True)


class Questions(db.Model):
    __tablename__ = 'questions'
    QuestionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Question_statement = db.Column(db.String(500), nullable=False)
    Option1 = db.Column(db.String(500), nullable=False)
    Option2 = db.Column(db.String(500), nullable=False)
    Option3 = db.Column(db.String(500), nullable=False)
    Option4 = db.Column(db.String(500), nullable=False)
    Correct_option = db.Column(db.String(500), nullable=False)

    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID', ondelete='CASCADE'), nullable=False)
    user_answers = db.relationship('UserAnswers', backref='question', cascade='all, delete', passive_deletes=True)


class Score(db.Model):
    __tablename__ = 'score'
    ScoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    QuizID = db.Column(db.Integer, db.ForeignKey('quiz.QuizID', ondelete='CASCADE'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID', ondelete='CASCADE'), nullable=False)
    TimeStamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    TotalScore = db.Column(db.Float, nullable=False)

    user_answers = db.relationship('UserAnswers', backref='score', cascade='all, delete', passive_deletes=True)


class UserAnswers(db.Model):
    __tablename__ = 'user_answers'
    AnswerID = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ScoreID = db.Column(db.Integer, db.ForeignKey('score.ScoreID', ondelete='CASCADE'), nullable=False)
    QuestionID = db.Column(db.Integer, db.ForeignKey('questions.QuestionID', ondelete='CASCADE'), nullable=False)
    SelectedAnswer = db.Column(db.String(500), nullable=True)

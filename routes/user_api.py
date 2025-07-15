# routes/user_api.py

from flask_restful import Resource
from flask import request, current_app
from models import db, User
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Import models and database
from models import db, User, Subject, Chapter, Quiz, Questions, UserAnswers, Score

# -------------------------------- User signup , login and logout -------------------------------- #


class UserSignup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400

        required_fields = ['username', 'email', 'password', 'fullname', 'qualification', 'dob']
        for field in required_fields:
            if not data.get(field):
                return {"message": f"{field} is required"}, 400

        try:
            dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        existing_user = User.query.filter(
            (User.Username == data['username']) | (User.Email == data['email'])
        ).first()

        if existing_user:
            return {"message": "Username or Email already exists"}, 400

        new_user = User(
            Username=data['username'],
            Email=data['email'],
            Fullname=data['fullname'],
            Qualification=data['qualification'],
            DOB=dob
        )
        new_user.set_password(data['password'])

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registration successful"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Registration failed due to a database error"}, 500


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username and password required"}, 400

        user = User.query.filter_by(Username=username).first()

        if user and user.check_password(password):
            token = create_access_token(
                identity=str(user.UserID),
                additional_claims={
                    "username": user.Username,
                    "role": user.Role
                }
            )
            return {
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user.UserID,
                    "username": user.Username,
                    "email": user.Email,
                    "role": user.Role
                }
            }, 200
        else:
            return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    def post(self):
        # JWTs are stateless; logout is handled on client side by deleting token
        return {"message": "Logout successful"}, 200


class VerifyToken(Resource):
    def get(self):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return {"message": "Invalid token format"}, 401

        if not token:
            return {"message": "Token is missing"}, 401

        current_user = current_app.verify_token(token)
        if current_user is None:
            return {"message": "Token is invalid or expired"}, 401

        return {
            "message": "Token is valid",
            "user": {
                "user_id": current_user['user_id'],
                "username": current_user['username'],
                "role": current_user['role']
            }
        }, 200

# -------------------------------- User Dashboard  -------------------------------- #


from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import User, Subject, Chapter, Quiz, Score


class UserDashboardData(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or user.Role != 'user':
            return {"message": "Unauthorized access"}, 403

        query = request.args.get('query', '').strip().lower()
        today = datetime.today().date()

        # Filter subjects (with or without search query)
        if query:
            subjects = Subject.query.filter(Subject.Subjectname.ilike(f"%{query}%")).all()
        else:
            subjects = Subject.query.all()

        upcoming_quizzes = []

        for subject in subjects:
            chapters = Chapter.query.filter_by(SubjectID=subject.SubjectID).all()
            for chapter in chapters:
                quizzes = Quiz.query.filter_by(ChapterID=chapter.ChapterID).all()
                for quiz in quizzes:
                    is_expired = quiz.Date_of_quiz < today
                    upcoming_quizzes.append({
                        "quiz": {
                            "id": quiz.QuizID,
                            "date": quiz.Date_of_quiz.strftime('%Y-%m-%d'),
                            "duration": quiz.Time_duration,
                            "total_questions": len(quiz.QuestionsR)
                        },
                        "chapter": {
                            "id": chapter.ChapterID,
                            "name": chapter.Chaptername
                        },
                        "subject": {
                            "id": subject.SubjectID,
                            "name": subject.Subjectname,
                            "description": subject.Description
                        },
                        "is_expired": is_expired
                    })

        # Fetch user scores
        scores = Score.query.filter_by(UserID=user.UserID).all()
        score_data = [
            {
                "score_id": score.ScoreID,
                "quiz_id": score.QuizID,
                "score": score.Score,
                "timestamp": score.Timestamp.isoformat()
            }
            for score in scores
        ]

        return {
            "message": "User dashboard data retrieved successfully",
            "user": {
                "id": user.UserID,
                "username": user.Username,
                "email": user.Email,
                "fullname": user.Fullname
            },
            "subjects": [
                {
                    "id": subject.SubjectID,
                    "name": subject.Subjectname,
                    "description": subject.Description
                }
                for subject in subjects
            ],
            "upcoming_quizzes": upcoming_quizzes,
            "scores": score_data,
            "query": query
        }, 200
# -------------------------------- User Functionalities --------------------------------- #

# routes/user_api.py


# Store quiz progress in-memory dictionary (use Redis/DB for production)
quiz_sessions = {}

class StartQuiz(Resource):
    @jwt_required()
    def post(self, quiz_id):
        user_id = get_jwt_identity()
        quiz = Quiz.query.get_or_404(quiz_id)
        today = datetime.today().date()

        if quiz.Date_of_quiz < today:
            return {"message": "This quiz is no longer available."}, 403

        questions = Questions.query.filter_by(QuizID=quiz_id).all()
        if not questions:
            return {"message": "No questions found for this quiz."}, 404

        # Initialize quiz session
        quiz_sessions[user_id] = {
            'quiz_id': quiz_id,
            'current_question': 0,
            'user_answers': {},
            'questions': [q.QuestionID for q in questions]
        }

        return {"message": "Quiz started", "quiz_id": quiz_id, "total_questions": len(questions)}, 200


class NextQuestion(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        session_data = quiz_sessions.get(user_id)
        if not session_data:
            return {"message": "Quiz session expired or not found."}, 403

        index = session_data['current_question']
        question_ids = session_data['questions']

        if index >= len(question_ids):
            return {"message": "All questions answered."}, 200

        question = Questions.query.get(question_ids[index])
        return {
            "question_id": question.QuestionID,
            "statement": question.Question_statement,
            "options": [question.Option1, question.Option2, question.Option3, question.Option4],
            "index": index + 1,
            "total": len(question_ids)
        }, 200


class SaveAnswer(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        session_data = quiz_sessions.get(user_id)
        if not session_data:
            return {"message": "Quiz session not active."}, 403

        data = request.get_json()
        selected_answer = data.get("selected_answer")
        question_id = str(data.get("question_id"))

        if selected_answer and question_id:
            session_data['user_answers'][question_id] = selected_answer
            session_data['current_question'] += 1
            return {"message": "Answer saved."}, 200

        return {"message": "Missing answer or question_id."}, 400


class SubmitQuiz(Resource):
    @jwt_required()
    def post(self, quiz_id):
        user_id = get_jwt_identity()
        session_data = quiz_sessions.pop(user_id, None)
        if not session_data:
            return {"message": "No active quiz session."}, 403

        questions = Questions.query.filter_by(QuizID=quiz_id).all()
        score = 0
        answers = session_data['user_answers']

        for q in questions:
            submitted = answers.get(str(q.QuestionID))
            if submitted == q.Correct_option:
                score += 1

        final_score = (score / len(questions)) * 100
        new_score = Score(QuizID=quiz_id, UserID=user_id, TotalScore=final_score)
        db.session.add(new_score)
        db.session.commit()

        for question_id, selected in answers.items():
            ua = UserAnswers(ScoreID=new_score.ScoreID, QuestionID=int(question_id), SelectedAnswer=selected)
            db.session.add(ua)
        db.session.commit()

        return {"message": "Quiz submitted", "score": final_score}, 200


class UserScores(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        scores = Score.query.filter_by(UserID=user_id).all()
        result = []

        IST_OFFSET = timedelta(hours=5, minutes=30)

        for score in scores:
            ist_time = score.TimeStamp + IST_OFFSET

            quiz = score.quiz
            chapter = quiz.chapter if quiz else None
            subject = chapter.subject if chapter else None

            questions_data = []
            for question in quiz.QuestionsR:
                user_answer_obj = next((ua for ua in score.user_answers if ua.QuestionID == question.QuestionID), None)
                questions_data.append({
                    "id": question.QuestionID,
                    "statement": question.Question_statement,
                    "user_answer": user_answer_obj.SelectedAnswer if user_answer_obj else "Not Answered",
                    "correct_answer": question.Correct_option
                })

            result.append({
                "score_id": score.ScoreID,
                "quiz_id": quiz.QuizID,
                "total_score": score.TotalScore,
                "timestamp": ist_time.strftime('%d-%m-%Y %H:%M:%S'),
                "chapter_name": chapter.Chaptername if chapter else "N/A",
                "subject_name": subject.Subjectname if subject else "N/A",
                "retake_allowed": score.TotalScore < 40,
                "questions": questions_data
            })

        return {"scores": result}, 200

# -------------------------------- Summary Charts --------------------------------- #


class UserSummary(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.Role != 'user':
            return {"message": "Unauthorized access"}, 403

        scores = Score.query.filter_by(UserID=user_id).all()
        IST_OFFSET = timedelta(hours=5, minutes=30)

        chapter_scores = {}
        for score in scores:
            chapter_name = score.quiz.chapter.Chaptername if score.quiz and score.quiz.chapter else f"Quiz {score.QuizID}"
            ist_time = score.TimeStamp + IST_OFFSET
            chapter_scores.setdefault(chapter_name, []).append((ist_time, score.TotalScore))

        plt.figure(figsize=(12, 6))
        for chapter, data in chapter_scores.items():
            timestamps, values = zip(*sorted(data))
            plt.plot(timestamps, values, marker='o', linestyle='-', label=chapter)

        plt.xlabel("Time (IST)")
        plt.ylabel("Score (%)")
        plt.title("User Performance Over Time")
        plt.legend(title="Chapters", loc="upper left", bbox_to_anchor=(1, 1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y, %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig("static/user_performance_chart.png")
        plt.close()

        return {
            "message": "User summary generated",
            "chart": "/static/user_performance_chart.png"
        }, 200

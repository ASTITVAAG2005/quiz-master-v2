# routes/admin_api.py

from flask_restful import Resource
from flask import request, current_app
from models import User
from werkzeug.security import check_password_hash  # If using werkzeug-style password checking
from flask_jwt_extended import create_access_token
from datetime import timedelta
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity


import matplotlib.pyplot as plt
import os


# Import models and database
from models import db, User, Subject, Chapter, Quiz, Questions, UserAnswers, Score


class AdminLogin(Resource):
    def post(self):
        try:
            username = request.json.get('username')
            password = request.json.get('password')

            if not username or not password:
                return {
                    "status": "error",
                    "message": "Username and password are required."
                }, 400

            admin = User.query.filter_by(Username=username, Role='admin').first()

            if admin and admin.check_password(password):
                token = create_access_token(
                    identity=str(admin.UserID),
                    additional_claims={"username": admin.Username, "role": admin.Role},
                    expires_delta=timedelta(hours=2)
                )

                return {
                    "status": "success",
                    "message": "Admin login successful.",
                    "token": token,
                    "user": {
                        "id": admin.UserID,
                        "username": admin.Username,
                        "role": admin.Role
                    }
                }, 200

            else:
                return {
                    "status": "error",
                    "message": "Invalid admin credentials."
                }, 401

        except Exception as e:
            return {
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }, 500




    # -------------------------------- Admin and Dashboard  -------------------------------- #




class AdminDashboardData(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user or current_user.Role != 'admin':
            return {"message": "Unauthorized access!"}, 403

        query = request.args.get('query', '').strip()

        def serialize_user(u):
            return {
                "id": u.UserID,
                "username": u.Username,
                "email": u.Email,
                "role": u.Role
            }

        def serialize_subject(s):
            return {
                "id": s.SubjectID,
                "name": s.Subjectname,
                "description": s.Description
            }

        def serialize_quiz(q):
            return {
                "id": q.QuizID,
                "title": q.Quizname,
                "subject_id": q.SubjectID,
                "total_questions": q.TotalQuestions
            }

        def serialize_question(q):
            return {
                "id": q.QuestionID,
                "question": q.Question_statement,
                "quiz_id": q.QuizID
            }

        def serialize_chapter(c):
            return {
                "id": c.ChapterID,
                "name": c.Chaptername,
                "subject_id": c.SubjectID
            }

        if query:
            users = User.query.filter(User.Username.ilike(f"%{query}%")).all()
            subjects = Subject.query.filter(Subject.Subjectname.ilike(f"%{query}%")).all()
            quizzes = Quiz.query.filter(Quiz.Quizname.ilike(f"%{query}%")).all()
            questions = Questions.query.filter(Questions.Question_statement.ilike(f"%{query}%")).all()
            chapters = Chapter.query.filter(Chapter.Chaptername.ilike(f"%{query}%")).all()
        else:
            users = User.query.all()
            subjects = Subject.query.all()
            quizzes = Quiz.query.all()
            questions = Questions.query.all()
            chapters = Chapter.query.all()

        return {
            "message": "Admin dashboard data retrieved successfully",
            "users": [serialize_user(u) for u in users],
            "subjects": [serialize_subject(s) for s in subjects],
            "quizzes": [serialize_quiz(q) for q in quizzes],
            "questions": [serialize_question(q) for q in questions],
            "chapters": [serialize_chapter(c) for c in chapters],
        }, 200



# ---------- USERS ----------
class UserListAPI(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.Role != 'admin':
            return {"message": "Unauthorized access."}, 403

        users = User.query.filter(User.Role != 'admin').all()
        data = [
            {
                "id": u.UserID,
                "username": u.Username,
                "email": u.Email,
                "fullname": u.Fullname,
                "qualification": u.Qualification,
                "dob": u.DOB.strftime('%Y-%m-%d') if u.DOB else None,
                "role": u.Role
            }
            for u in users
        ]
        return {"users": data}, 200
# -------------------------------- Admin Functionalities --------------------------------- #




# ---------- SUBJECTS ----------
class SubjectAPI(Resource):
    @jwt_required()
    def get(self):
        subjects = Subject.query.all()
        return [
            {
                "id": s.SubjectID,
                "name": s.Subjectname,
                "description": s.Description
            }
            for s in subjects
        ], 200


    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get("name")
        desc = data.get("description")

        if not name:
            return {"message": "Subject name is required."}, 400

        subject = Subject(Subjectname=name, Description=desc)
        db.session.add(subject)
        db.session.commit()
        return {"message": "Subject added successfully."}, 201

    @jwt_required()
    def put(self, subject_id):
        data = request.get_json()
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found."}, 404

        subject.Subjectname = data.get("name", subject.Subjectname)
        subject.Description = data.get("description", subject.Description)
        db.session.commit()
        return {"message": "Subject updated successfully."}, 200

    @jwt_required()
    def delete(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found."}, 404

        db.session.delete(subject)
        db.session.commit()
        return {"message": "Subject deleted successfully."}, 200

# ---------- CHAPTERS ----------
class ChapterAPI(Resource):
    @jwt_required()
    def get(self):
        chapters = Chapter.query.all()
        return [
            {
                "id": c.ChapterID,
                "name": c.Chaptername,
                "subject_id": c.SubjectID,
                "description": c.Description
            }
            for c in chapters
        ], 200
    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get("name")
        subject_id = data.get("subject_id")
        description = data.get("description")

        if not name or not subject_id or not description:
            return {"message": "Chapter name, subject_id, and description are required."}, 400

        chapter = Chapter(Chaptername=name, SubjectID=subject_id, Description=description)
        db.session.add(chapter)
        db.session.commit()
        return {"message": "Chapter added successfully."}, 201

    @jwt_required()
    def put(self, chapter_id):
        data = request.get_json()
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found."}, 404

        chapter.Chaptername = data.get("name", chapter.Chaptername)
        chapter.Description = data.get("description", chapter.Description)
        chapter.SubjectID = data.get("subject_id", chapter.SubjectID)
        db.session.commit()
        return {"message": "Chapter updated successfully."}, 200


    @jwt_required()
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found."}, 404

        db.session.delete(chapter)
        db.session.commit()
        return {"message": "Chapter deleted successfully."}, 200

# ---------- QUIZZES ----------
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from models import db, Quiz
from datetime import datetime

class QuizAPI(Resource):
    @jwt_required()
    def get(self):
        quizzes = Quiz.query.all()
        result = []
        for q in quizzes:
            chapter = Chapter.query.get(q.ChapterID)
            subject = Subject.query.get(chapter.SubjectID) if chapter else None

            result.append({
                "id": q.QuizID,
                "chapter_id": q.ChapterID,
                "date": q.Date_of_quiz.strftime('%Y-%m-%d') if q.Date_of_quiz else None,
                "time_duration": q.Time_duration,
                "remarks": q.Remarks or "",
                "chapter": {
                    "ChapterID": chapter.ChapterID,
                    "Chaptername": chapter.Chaptername,
                    "SubjectID": chapter.SubjectID,
                    "subject": {
                        "SubjectID": subject.SubjectID,
                        "Subjectname": subject.Subjectname
                    } if subject else None
                } if chapter else None
            })

        return result, 200


    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            quiz = Quiz(
                ChapterID=data.get("chapter_id"),
                Date_of_quiz=datetime.strptime(data.get("date"), "%Y-%m-%d").date(),
                Time_duration=data.get("time_duration"),
                Remarks=data.get("remarks", "")
            )
            db.session.add(quiz)
            db.session.commit()
            return {"message": "Quiz added successfully."}, 201
        except Exception as e:
            return {"message": "Failed to add quiz", "error": str(e)}, 500

    @jwt_required()
    def put(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found."}, 404

        data = request.get_json()
        try:
            quiz.ChapterID = data.get("chapter_id", quiz.ChapterID)
            quiz.Date_of_quiz = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
            quiz.Time_duration = data.get("time_duration", quiz.Time_duration)
            quiz.Remarks = data.get("remarks", quiz.Remarks)
            db.session.commit()
            return {"message": "Quiz updated successfully."}, 200
        except Exception as e:
            return {"message": "Failed to update quiz", "error": str(e)}, 500

    @jwt_required()
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found."}, 404

        db.session.delete(quiz)
        db.session.commit()
        return {"message": "Quiz deleted successfully."}, 200

# ---------- QUESTIONS ----------
class QuestionAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or current_user.Role != 'admin':
            return {"message": "Unauthorized access."}, 403

        questions = Questions.query.all()
        data = [
            {
                "id": q.QuestionID,
                "quiz_id": q.QuizID,
                "question": q.Question_statement,
                "option1": q.Option1,
                "option2": q.Option2,
                "option3": q.Option3,
                "option4": q.Option4,
                "correct_option": q.Correct_option
            }
            for q in questions
        ]
        return data, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        q = Questions(
            QuizID=data.get("quiz_id"),
            Question_statement=data.get("question"),
            Option1=data.get("option1"),
            Option2=data.get("option2"),
            Option3=data.get("option3"),
            Option4=data.get("option4"),
            Correct_option=data.get("correct_option")
        )
        db.session.add(q)
        db.session.commit()
        return {"message": "Question added successfully."}, 201

    @jwt_required()
    def put(self, question_id):
        q = Questions.query.get(question_id)
        if not q:
            return {"message": "Question not found."}, 404

        data = request.get_json()
        q.Question_statement = data.get("question", q.Question_statement)
        q.Option1 = data.get("option1", q.Option1)
        q.Option2 = data.get("option2", q.Option2)
        q.Option3 = data.get("option3", q.Option3)
        q.Option4 = data.get("option4", q.Option4)
        q.Correct_option = data.get("correct_option", q.Correct_option)
        db.session.commit()
        return {"message": "Question updated successfully."}, 200

    @jwt_required()
    def delete(self, question_id):
        q = Questions.query.get(question_id)
        if not q:
            return {"message": "Question not found."}, 404

        db.session.delete(q)
        db.session.commit()
        return {"message": "Question deleted successfully."}, 200


    # -------------------------------- Summary Charts --------------------------------- #

    # routes/admin_api.py


class AdminSummary(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        admin = User.query.get(user_id)

        if not admin or admin.Role != 'admin':
            return {"message": "Unauthorized access"}, 403

        # Generate summary
        users = User.query.all()
        quizzes = Quiz.query.all()

        user_names = [user.Username for user in users]
        user_scores = [Score.query.filter_by(UserID=user.UserID).count() for user in users]

        plt.figure(figsize=(8, 5))
        plt.barh(user_names, user_scores, color='blue')
        plt.xlabel("Quizzes Taken")
        plt.ylabel("Username")
        plt.title("User Participation")
        plt.tight_layout()
        plt.savefig("static/admin_user_participation.png")
        plt.close()

        quiz_labels = [quiz.Remarks if quiz.Remarks else f"Quiz {quiz.QuizID}" for quiz in quizzes]
        quiz_attempts = [Score.query.filter_by(QuizID=quiz.QuizID).count() for quiz in quizzes]

        plt.figure(figsize=(8, 5))
        plt.bar(quiz_labels, quiz_attempts, color='green')
        plt.xlabel("Quiz")
        plt.ylabel("Attempts")
        plt.title("Quiz Statistics")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("static/admin_quiz_statistics.png")
        plt.close()

        return {
            "message": "Admin summary generated",
            "charts": [
                "/static/admin_user_participation.png",
                "/static/admin_quiz_statistics.png"
            ]
        }, 200

# tasks.py
from celery import shared_task
from datetime import datetime
from flask import render_template
from flask_mail import Message
from celery_tasker import FlaskTask
from app import celery, mail
from models import User, Quiz, Score

@celery.task(base=FlaskTask)
def send_daily_reminders():
    users = User.query.all()
    for user in users:
        # Check logic: if they haven’t visited recently or new quiz exists
        # You'll need a `last_login` and `created_on` timestamp logic
        email_subject = "Quiz Reminder"
        email_body = f"Hi {user.Fullname},\n\nDon't forget to check for new quizzes today!"
        msg = Message(subject=email_subject, recipients=[user.Email], body=email_body)
        mail.send(msg)
    return "Daily reminders sent."

@celery.task(base=FlaskTask)
def send_monthly_activity_report():
    users = User.query.all()
    for user in users:
        scores = Score.query.filter_by(UserID=user.UserID).all()
        total = len(scores)
        avg_score = sum(s.TotalScore for s in scores) / total if total else 0

        email_body = render_template('monthly_report.html',
                                     username=user.Fullname,
                                     quiz_count=total,
                                     average_score=round(avg_score, 2),
                                     report_date=datetime.now().strftime('%B %Y'))

        msg = Message(subject=f"Your Monthly Quiz Report - {datetime.now().strftime('%B')}",
                      recipients=[user.Email],
                      html=email_body)
        mail.send(msg)
    return "Monthly reports sent."
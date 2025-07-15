from flask_restful import Api

# Admin imports
from routes.admin_api import (
    AdminLogin,
    AdminDashboardData,
    UserListAPI,
    SubjectAPI,
    ChapterAPI,
    QuizAPI,
    QuestionAPI,
    AdminSummary,
    AdminSearchAPI
)

# User imports
from routes.user_api import (
    UserSignup,
    UserLogin,
    UserLogout,
    VerifyToken,
    UserDashboardData,
    StartQuiz,
    NextQuestion,
    SaveAnswer,
    SubmitQuiz,
    UserScores,
    UserSummary
)

# Initialize API with '/api' prefix
api = Api(prefix='/api')

# -------------------------------
# 🔐 Auth Routes (shared)
# -------------------------------
api.add_resource(AdminLogin, '/adminlogin')
api.add_resource(UserSignup, '/usersignup')
api.add_resource(UserLogin, '/userlogin')
api.add_resource(UserLogout, '/logout')
api.add_resource(VerifyToken, '/verify-token')


# -------------------------------
# 🛠️ Admin Routes
# -------------------------------
api.add_resource(AdminDashboardData, '/admin/dashboard-data')
api.add_resource(AdminSearchAPI, '/admin/search')
api.add_resource(UserListAPI, '/admin/users')
api.add_resource(SubjectAPI, '/admin/subjects', '/admin/subjects/<int:subject_id>')
api.add_resource(ChapterAPI, '/admin/chapters', '/admin/chapters/<int:chapter_id>')
api.add_resource(QuizAPI, '/admin/quizzes', '/admin/quizzes/<int:quiz_id>')
api.add_resource(QuestionAPI, '/admin/questions', '/admin/questions/<int:question_id>')
api.add_resource(AdminSummary, '/admin/summary')


# -------------------------------
# 👤 User Routes
# -------------------------------
api.add_resource(UserDashboardData, '/user/dashboard-data')
api.add_resource(StartQuiz, '/user/quiz/start/<int:quiz_id>')
api.add_resource(NextQuestion, '/user/quiz/next')
api.add_resource(SaveAnswer, '/user/quiz/save')
api.add_resource(SubmitQuiz, '/user/quiz/submit/<int:quiz_id>')
api.add_resource(UserScores, '/user/scores')
api.add_resource(UserSummary, '/user/summary')

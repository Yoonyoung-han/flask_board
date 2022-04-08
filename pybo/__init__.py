from flask import Flask
import os
import locale
from dotenv import load_dotenv 
locale.setlocale(locale.LC_ALL, '')

#This is the application factory
def create_app():
    app = Flask(__name__)
    load_dotenv('config.env')
    #blueprint (기능별 뷰 관리)
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
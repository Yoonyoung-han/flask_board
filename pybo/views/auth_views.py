from flask import Blueprint, url_for, render_template, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models.board_models import User
from pybo.exception import ExceptionError
import functools


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.objects().filter(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            User.objects.insert(user)
            return redirect(url_for('main.index'))
        else:
            ExceptionError('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.objects().filter(username=form.username.data).first()
        user = User.to_mongo(user).to_dict()
        
        if not user:
            raise ExceptionError("존재하지 않는 사용자입니다.")
        elif not check_password_hash(user['password'], form.password.data):
            raise ExceptionError("비밀번호가 올바르지 않습니다.")
        
        session.clear()
        session['user_id'] = str(user['_id'])
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.objects.get(id=user_id)
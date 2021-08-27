from flask import Blueprint, url_for, flash, g
from werkzeug.utils import redirect

from pybo.models.board_models import Question,Answer
from pybo.views.auth_views import login_required

bp = Blueprint('vote', __name__, url_prefix='/vote')


@bp.route('/question/<question_id>/')
@login_required
def question(question_id):
    _question = Question.objects(id=question_id).get_or_404()
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        Question.objects(id=question_id).update(
            set__voter=[g.user.id]
            ,upsert = True
        )
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/answer/<answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.objects(id=answer_id).get_or_404()
    question_id = Answer.to_mongo(_answer).to_dict()['question_id']
    if g.user == _answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user)
        Answer.objects(id=answer_id).update(
            set__voter=[g.user.id]
            ,upsert = True
        )
    return redirect(url_for('question.detail', question_id=question_id))
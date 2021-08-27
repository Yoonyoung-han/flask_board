from datetime import datetime
from flask import Blueprint, url_for, request, render_template,g
from pybo.exception import ExceptionError
from werkzeug.utils import redirect
from pybo.models.board_models import Answer,Question,Comment
from ..forms import AnswerForm
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<question_id>', methods=('POST',))
@login_required
def create(question_id):
    # result = {}
    # question_id = ObjectId(question_id)
    # result['question_id']= question_id
    # result['content'] = str(request.form['content'])
    # result['create_date']= datetime.now()
    # result = Answer(**result)
    # Answer.objects.insert(result)
    # answer_list = search(question_id)
    # return redirect(url_for('question.detail', question_id=question_id, answer_list = answer_list))
    form = AnswerForm()
    question = Question.objects(id= question_id).get_or_404()
    answer_list, a_comment_list , q_comment_list = search(question_id)
    voter = Question.to_mongo(question).to_dict()
    result = {
        "answer_list" : answer_list
        ,"a_comment_list" : a_comment_list
        ,"q_comment_list" : q_comment_list
        ,"voter" : voter['voter']
    }
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(question_id=question_id,content=content, create_date=datetime.now(), user = g.user)
        Answer.objects.insert(answer)
        return redirect(url_for('question.detail', question_id=question_id, params= result))
    return render_template('question/question_detail.html', question=question, form=form, params= result)

def search(question_id):
    answer_list = Answer.objects(question_id=question_id).order_by('create_date').all()
    a_comment_list = Comment.objects(question_id=question_id,answer_id__exists=True).order_by('create_date').all()
    q_comment_list = Comment.objects(question_id=question_id,answer_id__exists=False).order_by('create_date').all()
    return answer_list, a_comment_list,q_comment_list

@bp.route('/modify/<answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.objects(id=answer_id).get_or_404()
    question_id = Answer.to_mongo(answer).to_dict()['question_id']
    if g.user != answer.user:
        ExceptionError('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            Answer.objects(id=answer_id).update(
                set__modify_date=datetime.now()
                ,set__content=form.content.data
                )
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.objects(id=answer_id).get_or_404()
    question_id = Answer.to_mongo(answer).to_dict()['question_id']
    if g.user != answer.user:
        ExceptionError('삭제권한이 없습니다')
    else:
        Answer.objects(id=answer_id).delete()
    return redirect(url_for('question.detail', question_id=question_id))
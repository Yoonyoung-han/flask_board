# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g
from mongoengine.fields import ListField
from werkzeug.utils import redirect
from pybo.models.board_models import Question
from pybo.views.answer_views import search
from pybo.views.auth_views import login_required
from ..forms import QuestionForm, AnswerForm
from pybo.exception import ExceptionError
bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.objects.order_by('create_date').all() if Question.objects.order_by('create_date') is not None else None
    print(question_list)
    question_list = question_list.paginate(page, per_page=10) if question_list is not None else None
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.objects(id=question_id).get_or_404()
    answer_list, a_comment_list , q_comment_list = search(question_id)
    voter = Question.to_mongo(question).to_dict()
    result = {
        "answer_list" : answer_list
        ,"a_comment_list" : a_comment_list
        ,"q_comment_list" : q_comment_list
        ,"voter" : voter['voter']
    }
    return render_template('question/question_detail.html', question=question, form=form,params=result)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject = form.subject.data, content = form.content.data, create_date= datetime.now(), user=g.user)
        Question.objects.insert(question)
        return redirect(url_for('main.index')) 
    return render_template('question/question_form.html', form=form)


@bp.route('/modify/<question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.objects(id= question_id).get_or_404()
    if g.user != question.user:
        ExceptionError('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            Question.objects(id=question_id).update(
                set__modify_date=datetime.now()
                ,set__content=form.content.data
                )
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<question_id>')
@login_required
def delete(question_id):
    question = Question.objects(id= question_id).get_or_404()
    if g.user != question.user:
        ExceptionError('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    Question.objects(id=question_id).delete()
    return redirect(url_for('question._list'))
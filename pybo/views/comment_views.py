from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from flask.helpers import flash
from werkzeug.utils import redirect

from pybo.forms import CommentForm
from pybo.models.board_models import Question, Comment, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/question/<question_id>', methods=('GET', 'POST'))
@login_required
def create_question(question_id):
    form = CommentForm()
    question = Question.objects(id= question_id).get_or_404()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(
            user=g.user,
            content=form.content.data,
            create_date=datetime.now(), 
            question_id=question['id'])
        Comment.objects.insert(comment)
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/question/<comment_id>', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id):
    comment_obj = Comment.objects(id=comment_id).get_or_404()
    comment = Comment.to_mongo(comment_obj).to_dict()
    question_id = comment['question_id']
    if g.user.id != comment['user']:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            Comment.objects(id=comment_id).update(
            set__modify_date=datetime.now()
            ,set__content=form.content.data
            )
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = CommentForm(obj=comment_obj)
    
    return render_template('comment/comment_form.html', form=form)

@bp.route('/delete/question/<comment_id>')
@login_required
def delete_question(comment_id):
    comment = Comment.objects(id=comment_id).get_or_404()
    comment = Comment.to_mongo(comment).to_dict()
    question_id = comment['question_id']
    if g.user.id != comment['user']:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    Comment.objects(id=comment_id).delete()
    return redirect(url_for('question.detail', question_id=question_id))



@bp.route('/create/answer/<answer_id>', methods=('GET', 'POST'))
@login_required
def create_answer(answer_id):
    form = CommentForm()
    answer = Answer.objects(id= answer_id).get_or_404()
    answer = Answer.to_mongo(answer).to_dict()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(
            user=g.user,
            content=form.content.data,
            create_date=datetime.now(), 
            answer_id=answer['_id'],
            question_id=answer['question_id']
            )
        Comment.objects.insert(comment)
        return redirect(url_for('question.detail', question_id=answer['question_id']))
    return render_template('comment/comment_form.html', form=form)

@bp.route('/modify/answer/<comment_id>', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    comment_obj = Comment.objects(id=comment_id).get_or_404()
    comment = Comment.to_mongo(comment_obj).to_dict()
    question_id = comment['question_id']
    if g.user.id != comment['user']:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':
        form = CommentForm()
        if form.validate_on_submit():
            Comment.objects(id=comment_id).update(
            set__modify_date=datetime.now()
            ,set__content=form.content.data
            )
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = CommentForm(obj=comment_obj)
    return render_template('comment/comment_form.html', form=form)


@bp.route('/delete/answer/<comment_id>')
@login_required
def delete_answer(comment_id):
    comment = Comment.objects(id=comment_id).get_or_404()
    comment= Comment.to_mongo(comment).to_dict()
    question_id = comment['question_id']
    if g.user.id != comment['user']:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    Comment.objects(id=comment_id).delete()
    return redirect(url_for('question.detail', question_id=question_id))
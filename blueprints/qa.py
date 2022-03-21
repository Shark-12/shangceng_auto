#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2022/2/17 4:41 PM
# @Author  : yuanhaidong
# @File    : qa.py
from flask import Blueprint, g, request, redirect, url_for, flash
from flask import render_template
from decorators import login_required
from blueprints.forms import QuestionFrom, UpdateQuestionForm
from models import QuestionModel
from exts import db
from datetime import datetime
from sqlalchemy import or_
from classlib.qa_class.qa_paging import paging

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
@login_required
def index():
    return render_template("user/first.html")


@bp.route("/first")
@login_required
def first():
    return render_template("user/first.html")


@bp.route("/question/list")
@login_required
def question_list():
    paginate = paging(QuestionModel)
    question_list = paginate.items
    return render_template("qa/questionlist.html", questions_list=question_list, paginate=paginate)


@bp.route("/question/search")
@login_required
def search():
    q = request.args.get("q")
    questions_list = QuestionModel.query.filter(
        or_(QuestionModel.title.contains(q), QuestionModel.modular.contains(q)),
        QuestionModel.isDelete.contains(0)).order_by(db.text("-create_time"))

    paginate = paging(QuestionModel)
    return render_template("qa/questionlist.html", questions_list=questions_list, paginate=paginate)


# @bp.route("/question/delete/<int:question_id>")
# @login_required
# def delete_question(question_id):
#     QuestionModel.query.filter_by(id=question_id).delete()
#     db.session.commit()
#     return redirect(url_for("qa.question_list"))


@bp.route("/question/new_delete/<int:question_id>")
@login_required
def new_delete(question_id):
    question = QuestionModel.query.filter_by(id=question_id).first()
    if question:
        question.isDelete = '1'
        db.session.commit()
        return redirect(url_for("qa.question_list"))
    else:
        flash("此数据不可删除！")
        return render_template("qa/questionlist.html")


@bp.route("/update/<update_id>", methods=['GET', 'POST'])
@login_required
def update(update_id):
    if request.method == 'GET':
        list = QuestionModel.query.filter_by(id=update_id).first()
        return render_template("qa/question_update.html", update_id=update_id, list=list)
    else:
        question = QuestionModel.query.filter_by(id=update_id).first()
        if question:
            form = UpdateQuestionForm(request.form)
            if form.validate():
                if len(form.modular.data) > 0:
                    question.modular = form.modular.data
                else:
                    flash("请输入接口所属模块！")
                    return redirect(url_for("qa.update", update_id=update_id))
                if len(form.title.data) > 0:
                    question.title = form.title.data
                else:
                    flash("请输入接口路径！")
                    return redirect(url_for("qa.update", update_id=update_id))
                question.request_method = form.request_method.data
                if len(form.content.data) > 0:
                    question.content = form.content.data
                else:
                    flash("请输入入参！")
                    return redirect(url_for("qa.update", update_id=update_id))
                question.author = g.user
                question.update_time = datetime.now()
                db.session.commit()
                return redirect(url_for("qa.question_list"))
            else:
                return render_template("qa/questionlist.html")

        else:
            return render_template("qa/questionlist.html")


@bp.route("/question/public", methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template("qa/public_question.html")
    else:
        form = QuestionFrom(request.form)
        if form.validate():
            if len(form.modular.data) > 0:
                modular = form.modular.data
            else:
                flash("请输入接口所属模块！")
                return render_template("qa/public_question.html")
            if len(form.title.data) > 0:
                title = form.title.data
            else:
                flash("请输入接口路径！")
                return render_template("qa/public_question.html")

            request_method = form.request_method.data

            if len(form.content.data) > 0:
                content = form.content.data
            else:
                flash("请输入入参！")
                return render_template("qa/public_question.html")

            is_delete = '0'
            question = QuestionModel(title=title, content=content, author=g.user, request_method=request_method,
                                     modular=modular, isDelete=is_delete)
            question.create_time = datetime.now()
            db.session.add(question)
            db.session.commit()
            return redirect(url_for("qa.question_list"))
        else:
            flash("输入的数据不正确")
            return render_template("qa/public_question.html")


# @bp.route("/stupage")
# def stu_page():
#     page = int(request.args.get('page', 1))
#     per_page = int(request.args.get('per_page', 2))
#
#     questions_list = QuestionModel.query.filter_by(isDelete=0).order_by(db.text("-create_time")).paginate(page,
#                                                                                                           per_page,
#                                                                                                           error_out=False)
#     stus = questions_list.itmes
#     return render_template("questionlist.html", questions_list=questions_list, stus=stus)


@bp.route("/about_more", methods=['GET'])
def about_more():
    return render_template("more.html")

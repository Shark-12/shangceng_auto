#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2022/3/11 11:35 AM
# @Author  : yuanhaidong
# @File    : api.py
from flask import Blueprint, render_template, url_for, request, flash, redirect
from exts import db
from decorators import login_required
from datetime import datetime
from api.token import login_token
from api.ding_send import send_message
from api import data_storage

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/", methods=['GET', 'POST'])
def make_number():
    pass


@bp.route("/get_token", methods=['GET', 'POST'])
@login_required
def get_token():
    if request.method == 'GET':
        return render_template("api/get_token.html")
    else:
        account = request.form.get("account")
        if len(account) > 0:
            login_token(account=account)
            token = data_storage.data_token
            return render_template("api/get_token.html", token=token)
        else:
            error = "请输入正确的账号！"
            return render_template("api/get_token.html", error=error)


@bp.route("/send_ding", methods=['GET', 'POST'])
@login_required
def send_ding():
    message = '[日志提醒]记得按时提交日志！'
    send_message(message)
    return render_template("user/first.html")

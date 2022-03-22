#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2022/2/17 4:38 PM
# @Author  : yuanhaidong
# @File    : user.py
from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash, session
from flask_mail import Message

from exts import mail
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from exts import db
from blueprints.forms import LoginFrom, RegisterForm, UpdatePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("user/login.html")
    else:
        form = LoginFrom(request.form)
        if form.validate():
            password = form.password.data
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id  # 登录成功后生成session
                return redirect("/first")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for("user.login"))


@bp.route("/update_password", methods=['GET', 'POST'])
def update_password():
    if request.method == 'GET':
        return render_template("user/update_password.html")
    else:
        form = UpdatePasswordForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            hash_password = generate_password_hash(password)

            user = UserModel.query.filter_by(email=email).first()
            if user:
                user.password = hash_password
                user.join_time = datetime.now()
                db.session.commit()
                return redirect(url_for("user.login"))
            else:
                flash("该账号不存在！")
                return redirect(url_for("user.update_password"))
        else:
            flash("账号输入错误！")
            return redirect(url_for("user.update_password"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("user.login"))


@bp.route("/mail", methods=['POST'])
def my_email():
    email = request.form.get("email")
    letter = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letter, 4))
    print("验证码：", captcha)
    if email:
        message = Message(
            subject="邮箱",
            recipients=[email],
            body=f"【尚层装饰】您的验证码为：{captcha},请不要告诉任何人！"
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "请先传递邮箱"})


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("user/new_register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            flash("邮箱重复或验证码错误，请重新输入注册信息！")
            return redirect(url_for("user.register"))


@bp.route("/user_list", methods=['GET', 'POST'])
def user_list():
    user_list = UserModel.query.filter_by().all()
    return render_template("user/user_list.html", user_list=user_list)

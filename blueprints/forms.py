#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2022/2/19 12:11 AM
# @Author  : yuanhaidong
# @File    : forms.py
import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel, QuestionModel

"""
注册表单
"""


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误! ")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱存在")

    """
    修改密码
    """


class UpdatePasswordForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

    """
    登陆表单
    """


class LoginFrom(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])

    """
    新增接口表单
    """


class QuestionFrom(wtforms.Form):
    title = wtforms.StringField(validators=[length(max=100)])
    request_method = wtforms.StringField(validators=[length(max=10)])
    content = wtforms.StringField(validators=[length(max=200)])
    modular = wtforms.StringField(validators=[length(max=50)])

    # def validate_len(self, field):
    #     title = field.data
    #     request_method = field.data
    #     content = field.data
    #     modular = field.data
    #     if len(title) < 0:
    #         raise wtforms.ValidationError("请输入接口请求路径！")
    #     elif len(modular) <0:
    #         raise wtforms.ValidationError("请输入接口所属模块！")
    #     elif len(request_method) < 0:
    #         raise wtforms.ValidationError("请选择请求方式！")
    #     elif len(content) < 0:
    #         raise wtforms.ValidationError("请输入入参！")

    """
    修改接口表单
    """


class UpdateQuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(max=100)])
    request_method = wtforms.StringField(validators=[length(max=10)])
    content = wtforms.StringField(validators=[length(max=200)])
    modular = wtforms.StringField(validators=[length(max=50)])

    """
    新增个人信息表单
    """


class AddPersonalCenterForm(wtforms.Form):
    age = wtforms.StringField(validators=[length(min=1, max=5)])
    sex = wtforms.StringField(validators=[length(max=5)])
    mobile = wtforms.StringField(validators=[length(min=1, max=12)])
    address = wtforms.StringField(validators=[length(min=1, max=50)])


    """
    新增测试需求
    """


class AddDemandForm(wtforms.Form):
    demand_name = wtforms.StringField(validators=[length(max=50)])
    demand_href = wtforms.StringField(validators=[length(max=200)])
    pm_name = wtforms.StringField(validators=[length(max=10)])
    rd_name = wtforms.StringField(validators=[length(max=10)])
    test_name = wtforms.StringField(validators=[length(max=10)])




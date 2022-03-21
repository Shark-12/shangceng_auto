#!/usr/bin/ python
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @Time    : 2022/3/15 1:50 PM
# @Author  : yuanhaidong
# @File    : demand.py
from flask import Blueprint, render_template, redirect, flash, request, g, url_for
from exts import db
from models import DemandModel
from blueprints.forms import AddDemandForm
from datetime import datetime
from classlib.demand_class.demand_paging import paging
from decorators import login_required

bp = Blueprint("demand", __name__, url_prefix="/demand")


@bp.route("/list", methods=['GET', 'POST'])
@login_required
def demand_list():
    paginate = paging(DemandModel)
    demand = paginate.items
    return render_template('demand/demand.html', demand=demand, paginate=paginate)


@bp.route("/status/<int:id>", methods=['GET', 'POST'])
@login_required
def demand_status(id):
    demand = DemandModel.query.filter_by(id=id).first()
    if demand.status == 0:
        demand.status = 1
        db.session.commit()
        return redirect(url_for("demand.demand_list"))
    elif demand.status == 1:
        demand.status = 2
        db.session.commit()
        return redirect(url_for("demand.demand_list"))
    else:
        return render_template("demand/demand.html")


@bp.route("/add", methods=['GET', 'POST'])
@login_required
def demand_add():
    if request.method == 'GET':
        return render_template("demand/add_demand.html")
    else:
        form = AddDemandForm(request.form)
        if form:
            if len(form.demand_name.data) > 0:
                demand_name = form.demand_name.data
            else:
                flash("请输入需求名称！")
                return render_template("demand/add_demand.html")
            if len(form.demand_href.data) > 0:
                demand_href = form.demand_href.data
            else:
                flash("请输入需求链接！")
                return render_template("demand/add_demand.html")
            if len(form.pm_name.data) > 0:
                pm_name = form.pm_name.data
            else:
                flash("请输入产品经理！")
                return render_template("demand/add_demand.html")
            if len(form.rd_name.data) > 0:
                rd_name = form.rd_name.data
            else:
                flash("请输入开发人员！")
                return render_template("demand/add_demand.html")
            if len(form.test_name.data) > 0:
                test_name = form.test_name.data
            else:
                flash("请输入测试人员！")
                return render_template("demand/add_demand.html")
            if len(request.form.get("test_time")):
                test_time = request.form.get("test_time")
            else:
                flash("请选择提测时间！")
                return render_template("demand/add_demand.html")
            if len(request.form.get("online_time")):
                online_time = request.form.get("online_time")
            else:
                flash("请选择上线时间")
                return render_template("demand/add_demand.html")
            create_time = datetime.now()
            isDelete = '0'
            status = '0'

            demand_add = DemandModel(demand_name=demand_name, demand_href=demand_href, pm_name=pm_name,
                                     rd_name=rd_name, test_name=test_name, test_time=test_time,
                                     online_time=online_time, create_time=create_time,
                                     isDelete=isDelete, status=status, author=g.user)
            db.session.add(demand_add)
            db.session.commit()
            return redirect(url_for("demand.demand_list"))
        else:
            flash("请检查输入内容！")
            return render_template("demand/add_demand.html")


@bp.route("/update/<int:update_id>", methods=['GET', 'POST'])
@login_required
def demand_update(update_id):
    if request.method == 'GET':
        list = DemandModel.query.filter_by(id=update_id).first()
        return render_template("demand/update_demand.html", update_id=update_id, list=list)
    else:
        form = AddDemandForm(request.form)
        if form:
            demand = DemandModel.query.filter_by(id=update_id).first()
            demand.demand_name = form.demand_name.data
            demand.demand_href = form.demand_href.data
            demand.pm_name = form.pm_name.data
            demand.rd_name = form.rd_name.data
            demand.test_name = form.test_name.data
            demand.test_time = request.form.get("test_time")
            demand.online_time = request.form.get("online_time")
            demand.update_time = datetime.now()
            if demand.test_time and demand.online_time:
                db.session.commit()
                return redirect(url_for("demand.demand_list"))
            else:
                flash("请选择测试时间和上线时间！")
                return redirect(url_for("demand.demand_update", update_id=update_id))
        else:
            flash("数据校验未通过！")
            return render_template("demand/demand.html")


@bp.route("/delete/<int:delete_id>", methods=['GET', 'POST'])
@login_required
def demand_delete(delete_id):
    list = DemandModel.query.filter_by(id=delete_id).first()
    if list:
        list.isDelete = 1
        db.session.commit()
        return redirect(url_for("demand.demand_list"))
    else:
        flash("此数据不可删除！")
        return render_template("demand/demand.html")

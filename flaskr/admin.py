# coding: utf-8
from flask import Blueprint, render_template, request, redirect, make_response, flash
from flask_login import login_required, current_user
from .model import User, Log
from . import db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def is_admin(func):
    def inner():
        if current_user.admin:
            return func()
        flash('没有权限')
        return redirect('/')
    return inner


@bp.route('/')
@login_required
def admin_home():
    if not current_user.admin:
        return redirect('/')
    return render_template('admin/index.html',title='后台管理')


@bp.route('/user')
@login_required
def usr():
    if not current_user.admin:
        return redirect('/')
    users = User.query.all()
    return render_template('admin/users.html', title='用户管理', users=users)


@bp.route('/user/edit/<id>', methods=['POST'])
@login_required
def edit_user(id):
    if not current_user.admin:
        return redirect('/')
    if request.method == 'POST':
        u = User.query.filter_by(id=id).first()
        u.username = request.form['username']
        if request.form['password']:
             u.password = request.form['password']
        u.sex = request.form['sex']
        u.school = request.form['school']
        u.major = request.form['major']
        u.phone = request.form['phone']
        if User.query.filter(User.id != id).filter_by(username=u.username).first():
            flash("用户名已存在")
            return redirect('/admin/user')
        print(u)
        try:
            db.session.add(u)
            db.session.commit()
            flash(u.username+'已修改')
        except :
            flash("系统错误")
        return redirect('/admin/user')


@bp.route('/user/delete/<id>')
@login_required
def delete_user(id):
    if not current_user.admin:
        return redirect('/')
    try:
        u = User.query.filter_by(id=id).first()
        db.session.delete(u)
        db.session.commit()
        flash(u.username + '已删除')
    except:
        flash("系统错误")
    return redirect('/admin/user')


@bp.route('/log')
@login_required
def log():
    if not current_user.admin:
        return redirect('/')
    logs = Log.query.order_by(Log.id.desc()).all()
    return render_template('admin/log.html', logs=logs)
from flask import Blueprint, render_template, request, redirect, make_response
from .model import User
from . import db, login_manager
from flask_login import login_user, logout_user, login_required


bp = Blueprint('auth', __name__, url_prefix='/')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/')
@login_required
def index():
    return render_template("base.html", title='欢迎')


@bp.route('/login', methods=('GET','POST'))
def login():
    title = "登录"
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if not u or not u.verify_password(request.form['password']):
            msg = '用户名或密码错误'
            response = make_response(render_template("auth/login.html", title=title, msg=msg))
            return response
        login_user(u)
        return redirect('/')
    return render_template("auth/login.html",  title=title)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        u = User()
        u.username = request.form['username']
        u.password = request.form['password']
        u.sex = request.form['sex']
        u.school = request.form['school']
        u.major = request.form['major']
        u.phone = request.form['phone']
        if not u.username:
            msg = "用户名不能为空"
            return render_template("auth/register.html", msg=msg)
        if User.query.filter_by(username=u.username).first():
            msg = "用户名已存在"
            return render_template("auth/register.html", msg=msg)
        try:
            db.session.add(u)
            db.session.commit()
        except :
            msg = "系统错误"
            return render_template("auth/register.html", msg=msg)
        return redirect('/login')
    return render_template("auth/register.html")





from flask import Blueprint, render_template, request, redirect, make_response
from .model import User
from . import db
import functools

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/login', methods=('GET','POST'))
@bp.route('/', methods=('GET','POST'))
def login():
    title = "登录"
    if request.method == 'POST':
        u = User.query.filter_by(username=request.form['username']).first()
        if not u or not u.verify_password(request.form['password']):
            msg = '用户名或密码错误'
            response = make_response(render_template("auth/login.html", title=title, msg=msg))
            return response
        response = make_response(render_template("base.html", title=title))
        LoginManger.login(u, response)
        return response
    return render_template("auth/login.html",  title=title)


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


class LoginManger:
    @staticmethod
    def login(user, response):
        response.set_cookie('user_id', str(user.user_id))


    def is_login(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            user_id = request.cookies.get('user_id').encode('ascii')


            u = User.query.filter_by(user_id=int(user_id)).first()
            if not u:
                return redirect('/')
            print(u)
            return func(*args, **kwargs)
        return inner

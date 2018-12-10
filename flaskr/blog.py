from flask import Blueprint, render_template, request, redirect, make_response
from .model import  Blog
from . import db
from .auth import LoginManger
from .model import Blog, User
import json

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
@LoginManger.is_login
def home():
    blogs = db.session.query(Blog.title,Blog.text,Blog.create_time,Blog.id,User.username).filter(Blog.public==True).\
        join(User, User.user_id==Blog.uid).\
        all()
    return render_template('blog/bloglist.html', blogs=blogs)


@bp.route('/myblog')
@LoginManger.is_login
def myblog():
    blogs = Blog.query.filter_by(uid=int(request.cookies.get('user_id')))
    return render_template('blog/myblog.html', blogs=blogs)


@bp.route('/newblog', methods=['GET','POST'])
@LoginManger.is_login
def newblog():
    if request.method == 'POST':
        b = Blog()

        b.title = request.form['title']
        b.text = request.form['text']
        b.uid = request.cookies.get('user_id')

        try:
            b.public = int(request.form['public']):
        except:
            b.public = 0

        print(b.title+" "+str(b.public)+" "+b.text+" "+str(b.uid))
        db.session.add(b)
        db.session.commit()
        try:
            db.session.add(b)
            db.session.commit()
        except:
            msg = "系统错误"
            response = make_response(render_template('blog/newblog.html', title="新博客", msg=msg))
            return response
        return redirect('/blog/myblog')
    response = make_response(render_template('blog/newblog.html', title="新博客"))
    return response

@bp.route('/<id>')
@LoginManger.is_login
def showablog(id):
    blog = db.session.query(Blog.title, Blog.text, Blog.create_time, Blog.id, User.username).filter(
        Blog.public == True, Blog.id==id). \
        join(User, User.user_id == Blog.uid). \
        first()
    msg=''
    title=''
    if not blog:
        title=msg="无权限访问"
    else:
        title=blog.title
    return render_template('blog/showablog.html', blog=blog,msg=msg,title=title)


@bp.route('/myblog/<id>')
@LoginManger.is_login
def showmyblog(id):
    blog = db.session.query(Blog.title, Blog.text, Blog.create_time, Blog.uid,Blog.id, User.username).filter(
         Blog.id==id). \
        join(User, User.user_id == Blog.uid). \
        first()
    msg=''
    title=''
    if not blog:
        title=msg="博客不存在"
    elif blog.uid != int(request.cookies.get("user_id", default=0)):
        title = msg = "无权限访问"
        blog=None
    else:
        title=blog.title
    return render_template('blog/showablog.html', blog=blog,msg=msg,title=title)
# coding: utf-8
from flask import Blueprint, render_template, request, redirect, make_response, flash
from . import db
from .model import Blog, User
from flask_login import login_required, current_user


bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
@login_required
def home():
    blogs = db.session.query(Blog.title,Blog.text,Blog.create_time,Blog.id,User.username).filter(Blog.public==True).\
        join(User, User.id==Blog.uid).\
        all()
    return render_template('blog/bloglist.html', blogs=blogs)


@bp.route('/myblog')
@login_required
def myblog():
    blogs = Blog.query.filter_by(uid=current_user.id)
    return render_template('blog/myblog.html', blogs=blogs)


@bp.route('/newblog', methods=['GET','POST'])
@login_required
def newblog():
    if request.method == 'POST':
        b = Blog()

        b.title = request.form['title']
        b.text = request.form['text']
        b.uid = current_user.id

        try:
            b.public = int(request.form['public'])
        except:
            b.public = 0
        try:
            db.session.add(b)
            db.session.commit()
        except:
            flash("系统错误")
            response = make_response(render_template('blog/newblog.html', title="新博客"))
            return response
        return redirect('/blog/myblog')
    blog = Blog()
    blog.title = ''
    blog.text = ''
    response = make_response(render_template('blog/newblog.html', title="新博客", blog=blog))
    return response


@bp.route('/edit/<id>', methods=['GET','POST'])
@login_required
def editblog(id):
    blog = Blog.query.filter_by(id=int(id)).first()
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.text = request.form['text']

        try:
            blog.public = int(request.form['public'])
        except:
            blog.public = 0
        try:
            db.session.add(blog)
            db.session.commit()
        except:
            flash("系统错误")
            response = make_response(render_template('blog/newblog.html', title="新博客"))
            return response
        return redirect('/blog/myblog')
    response = make_response(render_template('blog/newblog.html', title=blog.title, blog=blog))
    return response


@bp.route('/<id>')
@login_required
def showablog(id):
    blog = db.session.query(Blog.title, Blog.text, Blog.create_time, Blog.id, Blog.uid, User.username).\
        filter(Blog.public == True, Blog.id==id). \
        join(User, User.id == Blog.uid). \
        first()
    title=''
    if not blog:
        flash("无权限访问")
        title="无权限访问"
    else:
        title=blog.title
    return render_template('blog/showablog.html', blog=blog,title=title)


@bp.route('/myblog/<id>')
@login_required
def showmyblog(id):
    blog = db.session.query(Blog.title, Blog.text, Blog.create_time, Blog.uid, Blog.id, User.username).filter(
         Blog.id==id). \
        join(User, User.id == Blog.uid). \
        first()

    title=''
    if not blog:
        flash("博客不存在")
        title="博客不存在"
    elif blog.uid != current_user.id:
        flash( "无权限访问")
        title = "无权限访问"
        blog=None
    else:
        title=blog.title
    return render_template('blog/showablog.html', blog=blog,title=title)


@bp.route('/delete/<id>')
@login_required
def delete_a_blog(id):
    id = int(id)
    blog = Blog.query.filter_by(id=id).first()
    if not blog:
        flash('博客不能存在')
    elif blog.uid != current_user.id:
        flash('没有权限')
    else:
        try:
            db.session.delete(blog)
            db.session.commit()
        except :
            flash('系统错误')
            db.session.rollback()
    return redirect('/blog/myblog')

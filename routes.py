from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ext import db
from models import News, User, Info, Comment, Log
from forms import NewsForm, RegistrationForm, LoginForm, DeleteForm, InfoForm, CommentForm
from functools import wraps

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'Admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.mainpage'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def mainpage():
    return render_template('mainpage.html')

@main.route('/news')
def news():
    news_list = News.query.all()
    delete_form = DeleteForm()
    return render_template('news.html', news_list=news_list, delete_form=delete_form)

@main.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news_post = News(title=form.title.data, content=form.content.data)
        db.session.add(news_post)
        db.session.commit()

        log = Log(user_id=current_user.id, action=f"Added news: {news_post.title}")
        db.session.add(log)
        db.session.commit()

        flash('News added successfully!', 'success')
        return redirect(url_for('main.news'))
    return render_template('add_news.html', form=form)

@main.route('/news/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news_post = News.query.get_or_404(news_id)
    if current_user.role != 'Admin' and news_post.user_id != current_user.id:
        flash("You can't edit someone else's news!", 'danger')
        return redirect(url_for('main.news'))

    form = NewsForm(obj=news_post)
    if form.validate_on_submit():
        news_post.title = form.title.data
        news_post.content = form.content.data
        db.session.commit()

        log = Log(user_id=current_user.id, action=f"Edited news: {news_post.title}")
        db.session.add(log)
        db.session.commit()

        flash('News updated successfully!', 'success')
        return redirect(url_for('main.news'))
    return render_template('edit_news.html', form=form, news=news_post)

@main.route('/news/delete/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    news_post = News.query.get_or_404(news_id)
    if current_user.role != 'Admin' and news_post.user_id != current_user.id:
        flash("You can't delete someone else's news!", 'danger')
        return redirect(url_for('main.news'))

    db.session.delete(news_post)

    log = Log(user_id=current_user.id, action=f"Deleted news: {news_post.title}")
    db.session.add(log)
    db.session.commit()

    flash('News deleted successfully!', 'success')
    return redirect(url_for('main.news'))

@main.route('/news/<int:news_id>', methods=['GET', 'POST'])
def view_news(news_id):
    news_post = News.query.get_or_404(news_id)
    comments = Comment.query.filter_by(News_id=news_id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, News_id=news_id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('main.view_news', news_id=news_id))
    return render_template('view_news.html', news=news_post, comments=comments, form=form)

@main.route('/tanks')
def tanks():
    return render_template('tanks.html')

@main.route('/jets')
def jets():
    return render_template('jets.html')

@main.route('/interestinginfo')
def interestinginfo():
    infos = Info.query.order_by(Info.created_at.desc()).all()
    pages = [
        {"name": "Tanks", "emoji": "🛡️", "desc": "Explore tank types, rounds, and specs", "url": "/tanks"},
        {"name": "Military Jets", "emoji": "✈️", "desc": "Dive into aircraft models and tech", "url": "/jets"},
    ]
    delete_form = DeleteForm()
    return render_template('interestinginfo.html', pages=pages, infos=infos, delete_form=delete_form)

@main.route('/interestinginfo/add', methods=['GET', 'POST'])
@login_required
def add_info():
    form_info = InfoForm()
    if form_info.validate_on_submit():
        info_post = Info(title=form_info.title.data, content=form_info.content.data)
        db.session.add(info_post)
        db.session.commit()

        log = Log(user_id=current_user.id, action=f"Added info: {info_post.title}")
        db.session.add(log)
        db.session.commit()

        flash('Info added successfully!', 'success')
        return redirect(url_for('main.interestinginfo'))
    return render_template('add_info.html', form=form_info)

@main.route('/interestinginfo/edit/<int:info_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_info(info_id):
    info_post = Info.query.get_or_404(info_id)
    form = InfoForm(obj=info_post)
    if form.validate_on_submit():
        info_post.title = form.title.data
        info_post.content = form.content.data
        db.session.commit()

        log = Log(user_id=current_user.id, action=f"Edited info: {info_post.title}")
        db.session.add(log)
        db.session.commit()

        flash('Info updated successfully!', 'success')
        return redirect(url_for('main.interestinginfo'))
    return render_template('add_info.html', form=form)

@main.route('/interestinginfo/delete/<int:info_id>', methods=['POST'])
@login_required
@admin_required
def delete_info(info_id):
    info_post = Info.query.get_or_404(info_id)
    db.session.delete(info_post)

    log = Log(user_id=current_user.id, action=f"Deleted info: {info_post.title}")
    db.session.add(log)

    db.session.commit()
    flash('Info deleted.', 'danger')
    return redirect(url_for('main.interestinginfo'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Username already taken, pick another!', 'danger')
            return render_template('signup.html', form=form)
        if existing_email:
            flash('Email already registered, please use another.', 'danger')
            return render_template('signup.html', form=form)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='User',
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        log = Log(user_id=new_user.id, action="Registered a new account.")
        db.session.add(log)
        db.session.commit()

        login_user(new_user)
        flash('Signed up and logged in!', 'success')
        return redirect(request.args.get('next') or url_for('main.mainpage'))
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            log = Log(user_id=user.id, action="Logged in.")
            db.session.add(log)
            db.session.commit()

            flash('Logged in successfully!', 'success')
            return redirect(request.args.get('next') or url_for('main.mainpage'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.mainpage'))

@main.route('/become_admin', methods=['GET', 'POST'])
@login_required
def become_admin():
    if request.method == 'POST':
        secret = request.form.get('secret')
        if secret == "godmode":
            current_user.role = 'Admin'
            db.session.commit()

            log = Log(user_id=current_user.id, action="Became Admin via godmode.")
            db.session.add(log)
            db.session.commit()

            flash('Congrats! You are now an Admin! 🎉', 'success')
            return redirect(url_for('main.mainpage'))
        else:
            flash('Wrong password. Try again.', 'danger')
    return render_template('become_admin.html')

@main.route('/admin')
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    logs = Log.query.order_by(Log.timestamp.desc()).limit(50).all()
    delete_form = DeleteForm()
    return render_template('admin_panel.html', users=users, delete_form=delete_form, logs=logs)

@main.route('/admin/promote/<int:user_id>')
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'Admin'
    db.session.commit()

    log = Log(user_id=current_user.id, action=f"Promoted user {user.username} to Admin.")
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.username} promoted to Admin!', 'success')
    return redirect(url_for('main.admin_panel'))

@main.route('/admin/demote/<int:user_id>')
@login_required
@admin_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'User'
    db.session.commit()

    log = Log(user_id=current_user.id, action=f"Demoted user {user.username} to User.")
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.username} demoted to User.', 'info')
    return redirect(url_for('main.admin_panel'))

@main.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)

    log = Log(user_id=current_user.id, action=f"Deleted user {user.username}.")
    db.session.add(log)

    db.session.commit()
    flash(f'User {user.username} deleted.', 'danger')
    return redirect(url_for('main.admin_panel'))

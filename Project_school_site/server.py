from flask import Flask, request, render_template, redirect, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session

from data.users import User
from data.news import News
from data.comments import Comments
from data.school_class import School_class
from data.class_news import Class_news
from data.surveys import Survey
from data.survey_result import SurveyResult

from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from forms.comment import CommentForm
from forms.class_news import NewsClassForm
from forms.make_survey import MakeSurvey
from forms.do_survey import DoSurvey

import sqlalchemy.ext.declarative as dec

import requests
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
SqlAlchemyBase = dec.declarative_base()
image_timing = datetime.date(year=2023, month=4, day=21)


def get_image():
    map_skl_file = "static/image/map_skl.png"
    map_sat_file = "static/image/map_sat.png"
    map_skl_request = "http://static-maps.yandex.ru/1.x/?ll=38.052842,55.948992&spn=0.0025,0.0025&l=skl"
    map_sat_request = "http://static-maps.yandex.ru/1.x/?ll=38.052842,55.948992&spn=0.002,0.002&l=sat"
    response_skl = requests.get(map_skl_request)
    response_sat = requests.get(map_sat_request)

    if not response_skl or not response_sat:
        return

    with open(map_skl_file, "wb") as file1:
        file1.write(response_skl.content)
    with open(map_sat_file, "wb") as file2:
        file2.write(response_sat.content)


@app.route("/")
def index():
    global image_timing
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    print(image_timing < datetime.date.today())
    print(image_timing)
    if image_timing < datetime.date.today():
        get_image()
        image_timing = datetime.date.today()
    return render_template("index.html",
                           news=news,
                           title="Главная страница")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.password == form.password.data:#user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.photo = "image/" + form.photo.data
        db_sess.merge(news)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
def show_news(id):
    try:
        form = CommentForm()
        if form.validate_on_submit() and current_user:
            db_sess = db_session.create_session()
            comment = Comments()
            comment.content = form.content.data
            comment.id_news = id
            comment.user_id = current_user.id
            comment.user_name = current_user.name
            db_sess.merge(comment)
            db_sess.commit()
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id)
        comments = db_sess.query(Comments).filter(Comments.id_news == id)
    except:
        pass
    return render_template('one_news.html', title='Новость', news=news, comments=comments, form=form)


@app.route('/news_red/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    if current_user.email == '123@123':
        form = NewsForm()
        if request.method == "GET":
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id).first()
            if news:
                form.title.data = news.title
                form.content.data = news.content
                form.photo.data = news.photo
            else:
                abort(404)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id).first()
            if news:
                news.title = form.title.data
                news.content = form.content.data
                news.photo = "image/" + form.photo.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('news.html',
                               title='Редактирование новости',
                               form=form
                               )
    else:
        return "<h1> Вам не доступна данная страница</h1>"


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    if current_user.email == '123@123':
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            db_sess.delete(news)
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    else:
        return "<h1> Вам не доступна данная страница</h1>"


@app.route("/classes")
def show_classes():
    db_sess = db_session.create_session()
    class_info = db_sess.query(School_class).all()
    return render_template("classes.html", class_info=class_info, title="Наши классы")


@app.route("/class/<int:id>", methods=['GET', 'POST'])
def show_class(id):
    db_sess = db_session.create_session()
    info_class = db_sess.query(School_class).filter(Class_news.id_class == id)
    main_news = db_sess.query(Class_news).filter(Class_news.id_class == id, Class_news.primary_news == 1)
    news = db_sess.query(Class_news).filter(Class_news.id_class == id, Class_news.primary_news == 0)
    return render_template("class_news.html", info_class=info_class, main_news=main_news, news=news, title="Наши классы")


@app.route('/class/create',  methods=['GET', 'POST'])
@login_required
def add_class_news():
    d = {'email@.com': 1, '123@123': 2}
    form = NewsClassForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Class_news()
        news_id = d.get(current_user.email, False)
        if news_id:
            news.id_class = news_id
        else:
            return "<h1> Вам не доступна данная страница</h1>"
        news.title = form.title.data
        news.content = form.content.data
        news.photo = "image/" + form.photo.data
        all_news = db_sess.query(Class_news).filter(Class_news.id_class == news_id)
        news.primary_news = form.primary_news.data
        if news.primary_news:
            for item in all_news:
                item.primary_news = 0
                db_sess.commit()
        db_sess.merge(news)
        db_sess.commit()
        return redirect('/')
    return render_template('class_news_create.html', title='Добавление новости',
                           form=form)


@app.route('/surveys')
@login_required
def show_surveys():
    db_sess = db_session.create_session()
    surveys = db_sess.query(Survey).all()
    return render_template('surveys.html', surveys=surveys, title='Опросы')


@app.route('/makesurveys/<int:id>/<int:id_question>',  methods=['GET', 'POST'])
@login_required
def make_surveys(id, id_question):
    if id == 0:
        db_sess = db_session.create_session()
        num_surveys = db_sess.query(Survey).count()
        return redirect(f'/makesurveys/{num_surveys + 1}/1')
    form = MakeSurvey()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if id_question == 1:
            main_surv = Survey()
            main_surv.user_id = current_user.id
            main_surv.user_name = current_user.name
            main_surv.title = form.title.data
            db_sess.merge(main_surv)
            db_sess.commit()
        surv = SurveyResult()
        surv.id_survey = id
        surv.user_id = current_user.id
        surv.id_question = id_question
        surv.question = form.question.data
        surv.answer1 = form.content1.data
        surv.answer2 = form.content2.data
        surv.answer3 = form.content3.data
        surv.answer4 = form.content4.data
        db_sess.merge(surv)
        db_sess.commit()
        return redirect(f'/makesurveys/{id}/{id_question + 1}')
    return render_template('makesurveys.html', form=form, title='Создание Опроса')


@app.route('/mysurveys')
@login_required
def show_my_surveys():
    db_sess = db_session.create_session()
    surveys = db_sess.query(SurveyResult).filter(SurveyResult.user_id == current_user.id)
    return render_template('mysurveys.html', surveys=surveys, title='Ваши Опросы')


@app.route('/dosurvey/<int:id>/<int:id_question>',  methods=['GET', 'POST'])
@login_required
def do_surveys(id, id_question):
    db_sess = db_session.create_session()
    surveys = db_sess.query(SurveyResult).filter(
        SurveyResult.id_survey == id,
        SurveyResult.id_question == id_question)
    num_surveys = db_sess.query(SurveyResult).filter(
        SurveyResult.id_survey == id,
        SurveyResult.id_question == id_question).count()

    form = DoSurvey()

    if form.validate_on_submit():
        surv = db_sess.query(SurveyResult).filter(
                SurveyResult.id_survey == id,
                SurveyResult.id_question == id_question)
        for item in surv:
            print(form.content1.data)
            print()
            if form.content1.data:
                item.num_answers1 += 1
            if form.content2.data:
                item.num_answers2 += 1
            if form.content3.data:
                item.num_answers3 += 1
            if form.content4.data:
                item.num_answers4 += 1
            db_sess.merge(item)
        db_sess.commit()
        if num_surveys + 1 == id_question:
            return redirect('/surveys')
        return redirect(f'/dosurvey/{id}/{id_question + 1}')
    return render_template('dosurveys.html', form=form, surveys=surveys, title='Прохождение Опроса')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    db_sess.commit()
    app.run(port=8080, host='127.0.0.1')
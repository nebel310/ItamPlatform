import psycopg2
from psycopg2.extras import DictCursor
import os
from flask import Flask, render_template, request, g, flash, redirect, url_for, session, abort
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length




#Конфигурация
DATABASE = '/tmp/app.py'
DEBUG = True
SECRET_KEY = 'fljahglahlvfdvln.n.xbvrea;ih3#5434343!'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'ITAM.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите в аккаунт для доступа к закрытым страницам'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


#Функции для взаимодействия с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


#Перед каждым запоросом будет выполнена эта функция
dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)



#WTForms - безопасный метод взятия данных из форм
#Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

#Форма авторизации
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

#Форма сброса пароля
class PasswordResetForm(FlaskForm):
    email = StringField('Ваш Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    submit = SubmitField('Сменить пароль')



#Базовые функции - обработчики
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('login'))


#Эти функции - обработчики можно использовать по желанию
@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user_exists = dbase.getUserByEmail(form.email.data)
        if not user_exists:
            dbase.addUser(form.username.data, form.email.data, hashed_password)
            flash('Регистрация прошла успешно! Теперь вы можете войти в систему.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Пользователь с таким email уже существует', 'error')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user_row = dbase.getUserByEmail(form.email.data)  # получаем строку из базы данных
        if user_row and check_password_hash(user_row['password'], form.password.data):
            user_login = UserLogin().create(user_row)  # создаем объект UserLogin
            login_user(user_login, remember=True if form.remember_me.data else False)  # передаем объект UserLogin в login_user
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверный email или пароль', 'error')
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user:
            new_password_hash = generate_password_hash(form.new_password.data)
            dbase.updatePassword(user['id'], new_password_hash)
            flash('Пароль успешно изменен!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Пользователь с таким email не найден', 'error')
    return render_template('forgot_password.html', form=form, title='Восстановление пароля')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin():
        abort(403)  # Доступ запрещен
    
    #Основная логика админ-панели
    return render_template('admin.html')



#Функция запуска кода
if __name__ == '__main__':
    create_db() #Временное решение для ускорения разработки
    app.run(debug=True)
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from data import db_session
from data.users import User
from data import exchanges

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Курс криптовалют')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Курс криптовалют',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Курс криптовалют',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/exchanges')
    return render_template('register.html', title='Курс криптовалют', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/exchanges")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Курс криптовалют')
    return render_template('login.html', title='Курс криптовалют', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/exchanges', methods=['GET', 'POST'])
def exchange():
    f, s = request.args.get('fromForm'), request.args.get('toForm')
    if not f and not s:
        f, s = 'BTC', 'USDT'
    prices = get_prices(f.upper(), s.upper())
    return render_template('exchanges.html', pair=f'{f.upper()}/{s.upper()}', binance_price=prices[0],
                           okx_price=prices[1], bybit_price=prices[2], bitget_price=prices[3], f=f.upper(), s=s.upper(),
                           title='Курс криптовалют')


def get_prices(f, s):
    try:
        binance_price = round(float(exchanges.get_binance_pair(f, s)['price']), 2)
    except KeyError:
        binance_price = 'нет на бирже'
    try:
        okx_price = round(float(exchanges.get_okx_pair(f, s)['data'][0]['last']), 2)
    except IndexError:
        okx_price = 'нет на бирже'
    try:
        bybit_price = exchanges.get_bybit_pair(f, s)['result']['list'][0]['lastPrice']
    except KeyError:
        bybit_price = 'нет на бирже'
    try:
        bitget_price = exchanges.get_bitget_pair(f, s)['data']['close']
    except TypeError:
        bitget_price = 'нет на бирже'
    return [binance_price, okx_price, bybit_price, bitget_price]


def main():
    db_session.global_init("db/users.db")
    app.run()


if __name__ == '__main__':
    main()

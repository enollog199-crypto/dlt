import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from core.models import db, LotteryData, User
from core.crawler import start_scheduler
from core.predictor import generate_ai_prediction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/lottery.db' # Render 建议路径
app.config['SECRET_KEY'] = 'cyberpunk_secret_key_2026'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- 路由逻辑 ---

@app.route('/')
def index():
    history = LotteryData.query.order_by(LotteryData.period.desc()).limit(10).all()
    ai_results = generate_ai_prediction()
    return render_template('index.html', history=history, ai_results=ai_results)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('register'))
        
        # 创建新用户，初始积分 1000
        new_user = User(username=username, 
                        password=generate_password_hash(password, method='pbkdf2:sha256'),
                        points=1000)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        flash('登录失败，请检查用户名或密码')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# 初始化数据库
with app.app_context():
    db.create_all()
    start_scheduler(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

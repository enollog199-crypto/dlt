import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from core.models import db, LotteryData
from core.crawler import start_scheduler

app = Flask(__name__)

# Render 环境下使用 SQLite 的配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'lottery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cyberpunk_dlt_2026'

db.init_app(app)

@app.route('/')
def index():
    # 获取最近20期数据用于展示
    history = LotteryData.query.order_by(LotteryData.period.desc()).limit(20).all()
    return render_template('index.html', history=history)

# 自动初始化数据库并启动爬虫
with app.app_context():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    db.create_all()
    start_scheduler(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

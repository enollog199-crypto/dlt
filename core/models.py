from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LotteryData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(20), unique=True, nullable=False) # 期号
    draw_date = db.Column(db.String(20)) # 开奖日期
    front_balls = db.Column(db.String(50)) # 前区 01,02,03,04,05
    back_balls = db.Column(db.String(20))  # 后区 01,02

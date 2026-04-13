from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户模型：存储账号信息与虚拟积分"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # 初始虚拟积分设为 1000 (需求文档 5.2 节)
    points = db.Column(db.Integer, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 建立与投注记录的关联（可选扩展）
    # bets = db.relationship('BetRecord', backref='user', lazy=True)


class LotteryData(db.Model):
    """开奖数据模型：存储历史开奖记录"""
    __tablename__ = 'lottery_data'
    
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(20), unique=True, nullable=False) # 期号
    draw_date = db.Column(db.String(20)) # 开奖日期
    front_balls = db.Column(db.String(50)) # 前区号码 (例如: "01,05,12,23,30")
    back_balls = db.Column(db.String(20))  # 后区号码 (例如: "02,11")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BetRecord(db.Model):
    """虚拟投注模型：存储用户的选号记录"""
    __tablename__ = 'bet_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    period = db.Column(db.String(20), nullable=False) # 投注期号
    front_choice = db.Column(db.String(50)) # 用户选的前区
    back_choice = db.Column(db.String(20))  # 用户选的后区
    is_checked = db.Column(db.Boolean, default=False) # 是否已开奖对比
    win_points = db.Column(db.Integer, default=0) # 中奖积分

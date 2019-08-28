from datetime import datetime
from faker import Faker
# 链接服务器用的代码
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@47.107.98.254:3306/yiban?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100), unique=True)  # 用户名　（唯一的）
    nickname = db.Column(db.String(100))  # 昵称（唯一的）
    pwd = db.Column(db.String(100))  # 密码
    sex = db.Column(db.Integer, default=0)  # 性别
    school = db.Column(db.String(100))  # 学校
    face = db.Column(db.String(255))  # 头像
    shhistory = db.Column(db.String(255))  # 搜索历史
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间

    blogcol = db.relationship('Blogcol', backref='user')  # 博客收藏外键关系关联
    search = db.relationship('Search', backref='user')  # 搜索历史外键关系关联
    cptcol = db.relationship('Cptcol', backref='user')  # 竞赛收藏外键关系关联
    actcol = db.relationship('Actcol', backref='user')  # 活动收藏外键关系关联
    myblog = db.relationship('Blog', backref='user')  # 我的博客外键关系关联

    """回复评论　私聊　关注　关系关联"""
    reply_sent = db.relationship('Reply', foreign_keys='Reply.sender_id',
                                 backref='author', lazy='dynamic')  # 我发的
    reply_received = db.relationship('Reply', foreign_keys='Reply.recipient_id',
                                     backref='recipient', lazy='dynamic')  # 我收的

    followed = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')  # 我关注的
    followers = db.relationship('Follow',
                                foreign_keys='Follow.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 关注我的

    def __repr__(self):
        return "<User %r>" % self.nickname


# 博客
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    content = db.Column(db.Text)  # 内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    commentnum = db.Column(db.BigInteger)  # 评论量
    replys = db.relationship('Reply', backref='blog')  # 评论外键关系关联
    blogcol = db.relationship('Blogcol', backref='blog')  # 博客收藏外键关系关联

    def __repr__(self):
        return "<Blog %r>" % self.title


# 竞赛
class Competition(db.Model):
    __tablename__ = "competition"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    type = db.Column(db.String(10))  # 类型
    content = db.Column(db.Text)  # 内容
    url = db.Column(db.String(255))  # 封面图url
    author = db.Column(db.String(255))  # 网站url
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    cptcol = db.relationship('Cptcol', backref='competition')  # 竞赛收藏外键关系关联
    replys = db.relationship('Reply', backref='competition')  # 评论外键关系关联

    def __repr__(self):
        return "<Competition %r>" % self.title


# 活动
class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    type = db.Column(db.String(10))  # 类型
    content = db.Column(db.Text)  # 内容
    url = db.Column(db.String(255))  # 封面图url
    author = db.Column(db.String(255))  # 网站url
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    replys = db.relationship('Reply', backref='activity')  # 评论外键关系关联
    actcol = db.relationship('Actcol', backref='activity')  # 博客收藏外键关系关联

    def __repr__(self):
        return "<Activity %r>" % self.title


# 回复及评论
class Reply(db.Model):
    __tablename__ = "reply"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    comment_id = db.Column(db.Integer)  # 评论对象
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 接收者
    content = db.Column(db.TEXT)  # 回复内容
    type = db.Column(db.Integer)  # 类型，1是评论，2是回复
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))  # 所属活动
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Reply %r>" % self.id


# 博客收藏
class Blogcol(db.Model):
    __tablename__ = "blogcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Blogcol %r>" % self.id


# 活动收藏
class Actcol(db.Model):
    __tablename__ = "actcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))  # 所属活动
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Actcol %r>" % self.id


# 竞赛收藏
class Cptcol(db.Model):
    __tablename__ = "cptcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Cptcol %r>" % self.id


# 搜索历史
class Search(db.Model):
    __tablename__ = "search"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    keyword = db.Column(db.String(255))  # 搜索关键字
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    cp_or_act = db.Column(db.Integer)  # 数字１代表活动，数字２代表竞赛


# 关注
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 关注者
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 被关注者
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


if __name__ == "__main__":
    # db.drop_all()
    db.create_all()

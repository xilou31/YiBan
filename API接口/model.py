from datetime import datetime

# from . import db

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@47.107.98.254:3306/yiban'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    sex = db.Column(db.Integer)  # 性别
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    school = db.Column(db.String(100))  # 学校
    level = db.Column(db.String(100))  # 年级
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    blogcol = db.relationship('Blogcol', backref='user')  # 博客收藏外键关系关联
    search = db.relationship('Search', backref='user')  # 搜索历史外键关系关联
    chat = db.relationship('Chat', backref='user')  # 聊天私聊外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


# 博客
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    content = db.Column(db.Text)  # 内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    face = db.Column(db.String(255))  # 头像的地址
    blog_url = db.Column(db.String(255))  # 博客的地址
    commentnum = db.Column(db.BigInteger)  # 评论量
    comments = db.relationship('Comment', backref='blog')  # 评论外键关系关联
    blogcol = db.relationship('Blogcol', backref='blog')  # 博客收藏外键关系关联

    def __repr__(self):
        return "<Blog %r>" % self.name



# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))  # 所属活动
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id




# 博客收藏
class Blogcol(db.Model):
    __tablename__ = "blogcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Blogcol %r>" % self.id


# 竞赛
class Competition(db.Model):
    __tablename__ = "competition"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    content = db.Column(db.Text)  # 内容
    author = db.Column(db.String(100))  # 作者
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='competition')  # 评论外键关系关联
    search = db.relationship('Search', backref='competition')  # 搜索历史外键关系关联


# 活动
class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    content = db.Column(db.Text)  # 内容
    author = db.Column(db.String(100))  # 作者
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='activity')  # 评论外键关系关联
    search = db.relationship('Search', backref='activity')  # 搜索历史外键关系关联


# 搜索历史
class Search(db.Model):
    __tablename__ = "search"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    keyword = db.Column(db.String(255))  # 搜索关键字
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    cp_or_act = db.Column(db.Integer) # 数字１代表活动，数字２代表竞赛
    #competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    #activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))  # 所属活动


# 关注
class Like(db.Model):
    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_like_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    user_liked_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户


# 私聊
class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.String(255))  # 聊天内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    # user_to_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户


if __name__ == "__main__":



"""
    cp = Competition.query.get(2)
    print(cp)
    cps = cp.comments
    for cpps in cps:
        print(cpps.id)



    u = User.query.get(2)
    print(u)
    coms = u.comments
    for com in coms:
        print(com.content)

    comment1 = Comment(content="评论内容测试１", user_id=1, competition_id=1)
    comment2 = Comment(content="评论内容测试2", user_id=2, competition_id=1)
    comment3 = Comment(content="评论内容测试3", user_id=2, competition_id=2)

    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)

    db.session.commit()
    print("yesss")
    cop1 = Competition(title="标题测试１", content="内容测试１", author="网站发布人1")
    cop2 = Competition(title="标题测试２", content="内容测试2", author="网站发布人2")

    db.session.add(cop1)
    db.session.add(cop2)


    db.session.commit()
    print("yes!")
    db.create_all()
    user1 = User(name="lmp", pwd='123456', sex=1, email='382552192@qq.com', phone=123456789, school="hnnydx",
                 level="大二", face="/root/face/123456.png")
    user2 = User(name="lzk", pwd='12345622', sex=2, email='38255219222@qq.com', phone=1234522222, school="hnnydx222",
                 level="大22", face="/root/face/123456222.png")

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()
    print("hello")
"""

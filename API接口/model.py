from datetime import datetime
from faker import Faker

# 链接服务器用的代码
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@47.107.98.254:3306/yibantest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)

# 本地测试用的代码
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)
"""


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100), unique=True)  # 用户名　（唯一的）
    nickname = db.Column(db.String(100))  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    sex = db.Column(db.Integer)  # 性别
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    school = db.Column(db.String(100))  # 学校
    level = db.Column(db.String(100))  # 年级
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间

    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    team = db.relationship('Team', backref='user')  # 组队外键关系关联.
    blogcol = db.relationship('Blogcol', backref='user')  # 博客收藏外键关系关联
    search = db.relationship('Search', backref='user')  # 搜索历史外键关系关联
    cptcol = db.relationship('Cptcol', backref='user')  # 竞赛收藏外键关系关联
    actcol = db.relationship('Actcol', backref='user')  # 活动收藏外键关系关联
    myblog = db.relationship('Blog', backref='user')  # 我的博客外键关系关联

    """私聊和关注关联"""
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')  # 看我发给谁
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')  # 看谁发给我
    followed = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')  # 看谁关注我
    followers = db.relationship('Follow',
                                foreign_keys='Follow.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 看我关注谁

    def __repr__(self):
        return "<User %r>" % self.name


# 博客
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    content = db.Column(db.Text)  # 内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    face = db.Column(db.String(255))  # 头像的地址
    commentnum = db.Column(db.BigInteger)  # 评论量
    comments = db.relationship('Comment', backref='blog')  # 评论外键关系关联
    blogcol = db.relationship('Blogcol', backref='blog')  # 博客收藏外键关系关联

    def __repr__(self):
        return "<Blog %r>" % self.name


# 竞赛
class Competition(db.Model):
    __tablename__ = "competition"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    content = db.Column(db.Text)  # 内容
    author = db.Column(db.String(100))  # 作者
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    cptcol = db.relationship('Cptcol', backref='competition')  # 竞赛收藏外键关系关联
    team = db.relationship('Team', backref='competition')  # 组队外键关系关联


# 活动
class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    content = db.Column(db.Text)  # 内容
    author = db.Column(db.String(100))  # 作者
    num_of_view = db.Column(db.Integer, default=0)  # 浏览次数
    commentnum = db.Column(db.BigInteger)  # 评论量
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='activity')  # 评论外键关系关联
    actcol = db.relationship('Actcol', backref='activity')  # 博客收藏外键关系关联


# 组队
class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属队长
    teamname = db.Column(db.String(100))  # 队伍名字
    need = db.Column(db.Integer)  # 需要的队伍人数
    info = db.Column(db.Text)  # 队伍简介内容
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
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
    __tablename__ = "Cptcol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))  # 所属竞赛
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


# 搜索历史
class Search(db.Model):
    __tablename__ = "search"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    keyword = db.Column(db.String(255))  # 搜索关键字
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    cp_or_act = db.Column(db.Integer)  # 数字１代表活动，数字２代表竞赛


# 聊天
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.TEXT)
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Message {}>'.format(self.body)


# 关注
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 关注者
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 被关注者
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


if __name__ == "__main__":
    db.create_all()

"""
    db.drop_all()
    db.create_all()
    user1 = User(username="lmp", pwd='123456', sex=1, email='382552192@qq.com', phone=123456789, school="hnnydx",
                 level="大二", face="/root/face/123456.png")
    user2 = User(username="lzk", pwd='12345622', sex=2, email='382552192s22@qq.com', phone=123, school="hnnydx222",
                 level="大一", face="/root/face/123456222.png")
    user3 = User(username="abc", pwd='123456', sex=1, email='3825521sdas92@qq.com', phone=123489, school="hnnsdsasydx",
                 level="大二", face="/root/face/123456ss.png")
    user4 = User(username="lhb", pwd='12345622', sex=2, email='3825521s9sdas222@qq.com', phone=1234522222,
                 school="hnnydxss222",
                 level="大一", face="/root/face/123456222d.png")
    user5 = User(username="cyj", pwd='123456', sex=1, email='382552s1sdas92@qq.com', phone=1234829,
                 school="hnnsdsasydx",
                 level="大二", face="/root/face/123456ssss.png")
    user6 = User(username="qxj", pwd='12345622', sex=2, email='38255219dsdas222@qq.com', phone=12345422222,
                 school="hnnydxss222",
                 level="大一", face="/root/face/123456222dsd.png")
    cop1 = Competition(title="竞赛标题测试１", content="竞赛内容测试１", author="网站发布人1")
    cop2 = Competition(title="竞赛标题测试２", content="竞赛内容测试2", author="网站发布人2")
    cop3 = Competition(title="竞赛标题测试3", content="竞赛内容测试3", author="网站发布人3")
    cop4 = Competition(title="竞赛标题测试4", content="竞赛内容测试4", author="网站发布人4")
    cop5 = Competition(title="竞赛标题测试5", content="竞赛内容测试5", author="网站发布人5")
    cop6 = Competition(title="竞赛标题测试6", content="竞赛内容测试6", author="网站发布人6")
    team1 = Team(master_id=1, teamname="咸鱼队１", need=40, info="咸鱼１队简介，我们需要最帅的人40来", competition_id=1)
    team2 = Team(master_id=2, teamname="咸鱼队2", need=50, info="咸鱼２队简介，我们需要最帅的人50来", competition_id=1)
    team3 = Team(master_id=3, teamname="咸鱼队3", need=105, info="咸鱼３队简介，我们需要最帅的人105来", competition_id=1)
    team4 = Team(master_id=4, teamname="咸鱼队4", need=104, info="咸鱼４队简介，我们需要最帅的人104来", competition_id=2)
    team5 = Team(master_id=5, teamname="咸鱼队5", need=108, info="咸鱼５队简介，我们需要最帅的人108来", competition_id=2)
    team6 = Team(master_id=6, teamname="咸鱼队6", need=110, info="咸鱼６队简介，我们需要最帅的人110来", competition_id=2)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(cop1)
    db.session.add(cop2)
    db.session.add(cop3)
    db.session.add(cop4)
    db.session.add(cop5)
    db.session.add(cop6)
    db.session.add(team1)
    db.session.add(team2)
    db.session.add(team3)
    db.session.add(team4)
    db.session.add(team5)
    db.session.add(team6)
    db.session.commit()
    col1 = Cptcol(competition_id=1,user_id=1)
    col2 = Cptcol(competition_id=1,user_id=2)
    col3 = Cptcol(competition_id=1,user_id=3)
    col4 = Cptcol(competition_id=2,user_id=4)
    col5 = Cptcol(competition_id=2,user_id=5)
    col6 = Cptcol(competition_id=2,user_id=6)
    db.session.add(col1)
    db.session.add(col2)
    db.session.add(col3)
    db.session.add(col4)
    db.session.add(col5)
    db.session.add(col6)
    db.session.commit()
    
"""

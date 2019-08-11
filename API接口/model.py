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
    face = db.Column(db.String(255))  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间

    team = db.relationship('Team', backref='user')  # 组队外键关系关联.
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
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')  # 我发的
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')  # 我收的
    followed = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')  # 关注我的
    followers = db.relationship('Follow',
                                foreign_keys='Follow.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 我关注的

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
    commentnum = db.Column(db.BigInteger)  # 评论量
    replys = db.relationship('Reply', backref='blog')  # 评论外键关系关联
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
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    replys = db.relationship('Reply', backref='activity')  # 评论外键关系关联
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
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


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
    # db.drop_all()
    # follow1 = Follow(follower_id=1,followed_id=2)
    # follow2 = Follow(follower_id=2, followed_id=3)
    # follow3 = Follow(follower_id=3, followed_id=4)
    # follow4 = Follow(follower_id=4, followed_id=5)
    # follow5 = Follow(follower_id=5,followed_id=6)
    # follow6 = Follow(follower_id=6, followed_id=1)
    # db.session.add_all([follow1,follow2,follow3,follow4,follow5,follow6])
    # db.session.commit()
    db.create_all()
    #
    # user1 = User(username="lmp", pwd='123456', sex=1, email='382552192@qq.com', phone=123456789, school="hnnydx",
    #              level="大二", face="/static/photo/8.jpeg")
    # user2 = User(username="lzk", pwd='12345622', sex=2, email='382552192s22@qq.com', phone=123, school="hnnydx222",
    #              level="大一", face="/static/photo/123.jpg")
    # user3 = User(username="abc", pwd='123456', sex=1, email='3825521sdas92@qq.com', phone=123489, school="hnnsdsasydx",
    #              level="大二", face="/static/photo/12.png")
    # user4 = User(username="lhb", pwd='12345622', sex=2, email='3825521s9sdas222@qq.com', phone=1234522222,
    #              school="hnnydxss222",
    #              level="大一", face="/static/photo/12.png")
    # user5 = User(username="cyj", pwd='123456', sex=1, email='382552s1sdas92@qq.com', phone=1234829,
    #              school="hnnsdsasydx",
    #              level="大二", face="/static/photo/123.jpg")
    # user6 = User(username="qxj", pwd='12345622', sex=2, email='38255219dsdas222@qq.com', phone=12345422222,
    #              school="hnnydxss222",
    #              level="大一", face="/static/photo/8.jpeg")
    #
    # db.session.add(user1)
    # db.session.add(user2)
    # db.session.add(user3)
    # db.session.add(user4)
    # db.session.add(user5)
    # db.session.add(user6)
    #
    # act1 = Activity(title='活动我是活动1', content="活动内容内容内容"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/12.png\"/>　活动内容内容内容　"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/123.jpg\"/>活动"
    #                                          "内容内容内容　", num_of_view=12, author="lmp")
    # act2 = Activity(title='活动我是活动2', content="活动内容内容内容"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/8.jpeg\"/>　活动内容内容内容　"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/123.jpg\"/>活动"
    #                                          "内容内容内容　", num_of_view=12, author="cyj")
    # act3 = Activity(title='活动我是活动3', content="活动内容内容内容"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/12.png\"/>　活动内容内容内容　"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/12.png\"/>活动"
    #                                          "内容内容内容　", num_of_view=12, author='lzk')
    # act4 = Activity(title='活动我是活动4', content="活动内容内容内容"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/123.jpg\"/>　活动内容内容内容　"
    #                                          "<img src=\"http://188888888.xyz:5000/static/photo/12.png\"/>活动"
    #                                          "内容内容内容　", num_of_view=12, author='abc')
    #
    # acl1 = Actcol(activity_id=1, user_id=1)
    # acl2 = Actcol(activity_id=1, user_id=2)
    # acl3 = Actcol(activity_id=1, user_id=3)
    # acl4 = Actcol(activity_id=2, user_id=4)
    # acl5 = Actcol(activity_id=2, user_id=5)
    # acl6 = Actcol(activity_id=2, user_id=6)
    #
    # comment1 = Reply(sender_id=2, content="我是号我评论一号文章1", type=1, activity_id=1)
    # comment2 = Reply(sender_id=3, content="我是号我评论二号文章2", type=1, activity_id=1)
    # comment3 = Reply(sender_id=4, content="我是号我评论一号文章3", type=1, activity_id=1)
    # comment4 = Reply(sender_id=5, content="我是号我评论一号文章4", type=1, activity_id=1)
    # comment5 = Reply(sender_id=6, content="我是号我评论一号文章5", type=1, activity_id=1)
    # comment6 = Reply(sender_id=2, content="我是二号我评论一号文章6", type=1, activity_id=1)
    # comment7 = Reply(sender_id=2, content="我是二号我评论2号文章7", type=1, activity_id=2)
    # comment8 = Reply(sender_id=2, content="我是二号我评论2号文章8", type=1, activity_id=2)
    # comment9 = Reply(sender_id=2, content="我是二号我评论2号文章9", type=1, activity_id=2)
    # comment0 = Reply(sender_id=2, content="我是二号我评论2号文章0", type=1, activity_id=2)
    #
    # reply1 = Reply(comment_id=11, sender_id=1, content="我是1号，我在2号发的第一条评论里面，回复了1", type=2)
    # reply2 = Reply(comment_id=11, sender_id=2, content="我是2号，我在2号发的第一条评论里面，回复了2", type=2)
    # reply3 = Reply(comment_id=1, sender_id=2, content="我是2号，我在2号发的第一条评论里面，回复了3", type=2)
    # reply4 = Reply(comment_id=1, sender_id=1, content="我是1号，我在2号发的第一条评论里面，回复了4", type=2)
    # reply5 = Reply(comment_id=1, sender_id=1, content="我是1号，....我在2号发的第一条评论里面，回复了5", type=2)
    # reply6 = Reply(comment_id=2, sender_id=3, content="我是2号，我在2号发的第一条评论里面，回复了6", type=2)
    # db.session.add_all(
    #     [act1, act2, act3, act4, acl1, acl2, acl3, acl4, acl5, acl6, comment1, comment2, comment3, comment4, comment5,
    #      comment6, comment7, comment8, comment9, comment0])
    # db.session.add_all([reply6, reply5, reply4, reply3, reply2, reply1])
    # db.session.commit()
    #
    #
    # blog1 = Blog(title="博客测试测试？111", content="博客内容测试我是博客内容，我就是博客内容,　我是　1号用户", user_id=1)
    # blog2 = Blog(title="博客测试测试？222", content="博客内容测试我是博客内容，我就是博客内容,　我是　2号用户", user_id=2)
    # blog3 = Blog(title="博客测试测试？333", content="博客内容测试我是博客内容，我就是博客内容,　我是　3号用户", user_id=3)
    # blog4 = Blog(title="博客测试测试？444", content="博客内容测试我是博客内容，我就是博客内容,　我是　4号用户", user_id=4)
    #
    # bcol1 = Blogcol(blog_id=1, user_id=1)
    # bcol2 = Blogcol(blog_id=1, user_id=2)
    # bcol3 = Blogcol(blog_id=1, user_id=3)
    # bcol4 = Blogcol(blog_id=2, user_id=4)
    # bcol5 = Blogcol(blog_id=2, user_id=5)
    # bcol6 = Blogcol(blog_id=3, user_id=6)
    #
    # db.session.add_all(
    #     [bcol1, bcol2, bcol3, bcol4, bcol5, bcol6, blog1, blog2, blog3, blog4])
    # db.session.commit()

    # comment1 = Reply(sender_id=2, content="我是号我评论一号文章1", type=1, blog_id=1)
    # comment2 = Reply(sender_id=3, content="我是号我评论二号文章2", type=1, blog_id=2)
    # comment3 = Reply(sender_id=4, content="我是号我评论一号文章3", type=1, blog_id=1)
    # comment4 = Reply(sender_id=5, content="我是号我评论一号文章4", type=1, blog_id=1)
    # comment5 = Reply(sender_id=6, content="我是号我评论一号文章5", type=1, blog_id=1)
    # comment6 = Reply(sender_id=2, content="我是二号我评论一号文章6", type=1, blog_id=1)
    # comment7 = Reply(sender_id=2, content="我是二号我评论2号文章7", type=1, blog_id=2)
    # comment8 = Reply(sender_id=2, content="我是二号我评论2号文章8", type=1, blog_id=2)
    # comment9 = Reply(sender_id=2, content="我是二号我评论2号文章9", type=1, blog_id=2)
    # comment0 = Reply(sender_id=2, content="我是二号我评论2号文章0", type=1, blog_id=2)
    # comment11 = Reply(sender_id=2, content="我是号我评论一号文章1", type=1, blog_id=1)
    # comment22 = Reply(sender_id=3, content="我是号我评论二号文章2", type=1, blog_id=2)
    # comment33 = Reply(sender_id=4, content="我是号我评论一号文章3", type=1, blog_id=1)
    # comment44 = Reply(sender_id=5, content="我是号我评论一号文章4", type=1, blog_id=1)
    # comment55 = Reply(sender_id=6, content="我是号我评论一号文章5", type=1, blog_id=1)
    # comment66 = Reply(sender_id=2, content="我是二号我评论一号文章6", type=1, blog_id=1)
    # comment77 = Reply(sender_id=2, content="我是二号我评论2号文章7", type=1, blog_id=2)
    # comment88 = Reply(sender_id=2, content="我是二号我评论2号文章8", type=1, blog_id=2)
    # comment99 = Reply(sender_id=2, content="我是二号我评论2号文章9", type=1, blog_id=2)
    # comment00 = Reply(sender_id=2, content="我是二号我评论2号文章0", type=1, blog_id=2)
    # db.session.add_all([comment1,comment2,comment3,comment4,comment5,comment6,comment7,comment8,
    #                     comment9,comment0,comment11,comment22,comment33,comment44,comment55,comment66,
    #                     comment77,comment88,comment99,comment00])
    # db.session.commit()

    # reply1 = Reply(comment_id=22, sender_id=1, content="我是1号，我在号发的第一条评论里面，回复了1", type=2)
    # reply2 = Reply(comment_id=19, sender_id=2, content="我是2号，我号发的第一条评论里面，回复了2", type=2)
    # reply3 = Reply(comment_id=22, sender_id=2, content="我是2号，我在号发的第一条评论里面，回复了3", type=2)
    # reply4 = Reply(comment_id=22, sender_id=1, content="我是1号，我在号发的第一条评论里面，回复了4", type=2)
    # reply5 = Reply(comment_id=22, sender_id=1, content="我是1号，....我在2号发的第一条评论里面，回复了5", type=2)
    # reply6 = Reply(comment_id=22, sender_id=3, content="我是2号，我在号发的第一条评论里面，回复了6", type=2)
    # db.session.add_all([reply6, reply5, reply4, reply3, reply2, reply1])
    # db.session.commit()

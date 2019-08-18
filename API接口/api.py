# coding: utf-8
from model import *
import json
from flask import request
import os
from sqlalchemy import and_
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

"""
已经完成的功能
.获取竞赛推文/home/compete 
.竞赛内容详情/compete/detail
.收藏竞赛接口/compete/collection
.取消收藏竞赛接口/compete/deletecollection


.搜索功能/search

.获取活动推文/home/activity
.活动内容详情/activity/detail
.收藏活动接口/activity/collection
.取消收藏活动接口/activity/deletecollection


.社区首页接口/community
.创建博客/blog/edit
.获取博客的详情/blog/detail
.收藏博客接口/blog/collection
.取消收藏博客接口/blog/deletecollection

.获取回复/reply
.评论及回复/comment

.获取个人资料/user/data
.修改个人资料/user/edit
.关注/follow
.取消关注/unfollow
.上传照片/uploadpic
.查看我的博客/user/myblog
.查看我关注的人/user/following
.查看我收藏的竞赛/user/colcompete
.查看我收藏的活动/user/colactivity
.查看我收藏的博客/user/colblog

"""


# 组队改为评论ok
# 查看关注竞赛活动博客ok
# 查看我的博客ok
# 修改头像ok
# 查看我关注的人ok
# 创建博客ok
# 竞赛和活动改加url（并且作者是文章的url）ok
# 浏览次数ok


# 获取竞赛推文
@app.route("/home/compete", methods=['POST', 'GET'])
def HomeCpt():
    if request.method == 'POST' and request.form.get('sort') == '0':
        c = Competition.query.order_by(Competition.num_of_view.desc()).all()  # desc()是从大到小，没有desc就是从小到大
        payload = []
        content = {}
        for cc in c:
            datetime = cc.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': cc.id, 'title': cc.title, 'author': cc.author, 'pageviews': cc.num_of_view,
                       'time': time}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200
    else:
        # 新发布的文章时间比较大，就先出现用ｄｅｓｃ从大到小排序
        c = Competition.query.order_by(Competition.create_time.desc()).all()
        payload = []
        content = {}
        for cc in c:
            datetime = cc.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': cc.id, 'title': cc.title, 'author': cc.author, 'pageviews': cc.num_of_view,
                       'time': time}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200


# 竞赛内容详情
@app.route("/compete/detail", methods=["GET", "POST"])
def CptDetail():
    id = request.form.get('id')  # 获取竞赛的内容id
    user_id = request.form.get('userid')  # 获取用户的id
    if user_id == '-1':  # 如果未登录，则将收藏设置为-1
        collection = -1
    else:  # 在收藏竞赛的表中查找用户名和文章id是否关联
        c = Cptcol.query.filter(Cptcol.user_id == user_id, Cptcol.competition_id == id).first()
        if c == None:
            collection = -1  # 未收藏
        else:
            collection = 1  # 已经收藏

    com = Competition.query.get(id)  # 找到对应的表
    if com == None:
        data = {"msg": "could not find this compete id"}
        payload = json.dumps(data)
        return payload, 400

    title = com.title  # 竞赛表的标题
    content = com.content  # 竞赛表的内容
    time = com.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 竞赛表的发布时间
    pageviews = com.num_of_view  # 竞赛的浏览次数
    author = com.author  # 竞赛的发布者
    pageviews = pageviews + 1  # 浏览量加1
    com.num_of_view = pageviews
    db.session.add(com)
    db.session.commit()

    '''评论'''
    payload = []
    contentss = {}
    cs = com.replys
    for c in cs:
        if c.type == 1:
            comid = c.id  # 评论表的id
            comauthor = User.query.get(c.sender_id).username  # 评论者的名字
            comauthorid = User.query.get(c.sender_id).id  # 评论者的id
            comauthorface = User.query.get(c.sender_id).face  # 评论者的头像
            comcontent = c.content  # 评论的内容
            comtime = c.addtime.strftime('%Y-%m-%d %H:%M:%S')  # 评论的时间
            replyss = Reply.query.filter_by(comment_id=comid).all()
            num = 0
            for reply in replyss:
                num = num + 1
            contentss = {'id': comid, 'author': comauthor, 'avatar': comauthorface,
                         'content': comcontent, 'time': comtime, "number": num, "userid": comauthorid}
            payload.append(contentss)
            contentss = {}
    data = {"title": title, "content": content, "time": time, "pageviews": pageviews, "author": author,
            "collection": collection, "comments": payload}

    payload = json.dumps(data)
    return payload, 200


# 收藏竞赛接口
@app.route("/compete/collection", methods=["GET", "POST"])
def CpCollection():
    id = request.form.get('id')  # 竞赛的id
    user_id = request.form.get('userid')  # 用户的id

    com = Competition.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        comcol = Cptcol(competition_id=id, user_id=user_id)
        db.session.add(comcol)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 取消收藏竞赛接口
@app.route("/compete/deletecollection", methods=["GET", "POST"])
def decompCollection():
    id = request.form.get('id')  # 竞赛的id
    user_id = request.form.get('userid')  # 用户的id

    com = Competition.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        comcol = Cptcol.query.filter_by(competition_id=id, user_id=user_id).first()
        db.session.delete(comcol)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 搜索
@app.route("/search", methods=["GET", "POST"])
def HomeSearchcp():
    js = request.form.get('competition')
    hd = request.form.get('activity')
    userid = request.form.get('userid')
    if userid == None or User.query.get(userid) == None:
        data = {'msg': "请输入正确的用户id"}
        payload = json.dumps(data)
        return payload, 400
    if js == None and hd != None:
        key_remark = hd
        aa = Activity.query.filter(Activity.title.like("%" + key_remark + "%")).all()
        payload = []
        contentss = {}
        for a in aa:
            contentss = {"title": a.title, "id": a.id, "pageviews": a.num_of_view,
                         "time": a.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            payload.append(contentss)
            contentss = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200

    elif hd == None and js != None:
        key_remark = js
        aa = Competition.query.filter(Competition.title.like("%" + key_remark + "%")).all()
        payload = []
        contentss = {}
        for a in aa:
            contentss = {"title": a.title, "id": a.id, "pageviews": a.num_of_view,
                         "time": a.create_time.strftime('%Y-%m-%d %H:%M:%S')}
            payload.append(contentss)
            contentss = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200
    else:
        data = {'msg': "请选择竞赛或者活动"}
        payload = json.dumps(data)
        return payload, 400


# 获取活动推文
@app.route("/home/activity", methods=['POST', 'GET'])
def HomeAct():
    if request.method == 'POST' and request.form.get('sort') == '0':
        # 默认是时间顺序排列，直接ｇｅｔ和ｐｏｓｔ上来的不是０的时候，就时间排序，
        A = Activity.query.order_by(Activity.num_of_view.desc()).all()  # desc()是从大到小，没有desc就是从小到大
        payload = []
        content = {}
        for AA in A:
            datetime = AA.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': AA.id, 'title': AA.title, 'author': AA.author, 'pageviews': AA.num_of_view,
                       'time': time}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200

    else:
        # 新发布的文章时间比较大，就先出现用ｄｅｓｃ从大到小排序
        A = Activity.query.order_by(Activity.create_time.desc()).all()
        payload = []
        content = {}
        for AA in A:
            datetime = AA.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': AA.id, 'title': AA.title, 'author': AA.author, 'pageviews': AA.num_of_view,
                       'time': time}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200


# 活动内容详情
@app.route("/activity/detail", methods=["GET", "POST"])
def ActDetail():
    id = request.form.get('id')  # 获取活动的内容id
    user_id = request.form.get('userid')  # 获取用户的id
    act = Activity.query.get(id)  # 找到对应的活动表
    if act == None:
        data = {"msg": "could not find this activity id"}
        payload = json.dumps(data)
        return payload, 400

    if user_id == '-1':  # 如果未登录，则将收藏设置为-1
        collection = -1
    else:  # 在收藏活动的表中查找用户名和文章id是否关联
        a = Actcol.query.filter(Actcol.user_id == user_id, Actcol.activity_id == id).first()
        if a == None:
            collection = -1  # 未收藏
        else:
            collection = 1  # 已经收藏

    title = act.title  # 活动表的标题
    content = act.content  # 活动表的内容
    time = act.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 活动表的发布时间
    pageviews = act.num_of_view  # 活动的浏览次数
    author = act.author  # 活动的发布者
    pageviews = pageviews + 1
    act.num_of_view = pageviews
    db.session.add(act)
    db.session.commit()

    '''评论'''
    payload = []
    contentss = {}
    cs = act.replys
    for c in cs:
        if c.type == 1:
            comid = c.id  # 评论表的id
            comauthor = User.query.get(c.sender_id).username  # 评论者的名字
            comauthorid = User.query.get(c.sender_id).id  # 评论者的id
            comauthorface = User.query.get(c.sender_id).face  # 评论者的头像
            comcontent = c.content  # 评论的内容
            comtime = c.addtime.strftime('%Y-%m-%d %H:%M:%S')  # 评论的时间
            replyss = Reply.query.filter_by(comment_id=comid).all()
            num = 0
            for reply in replyss:
                num = num + 1
            contentss = {'id': comid, 'author': comauthor, 'avatar': comauthorface,
                         'content': comcontent, 'time': comtime, "number": num, "userid": comauthorid}
            payload.append(contentss)
            contentss = {}
    data = {"title": title, "content": content, "time": time, "pageviews": pageviews, "author": author,
            "collection": collection, "comments": payload}

    payload = json.dumps(data)
    return payload, 200


# 收藏活动接口
@app.route("/activity/collection", methods=["GET", "POST"])
def ActCollection():
    id = request.form.get('id')  # 活动的id
    user_id = request.form.get('userid')  # 用户的id

    com = Activity.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        actcol = Actcol(activity_id=id, user_id=user_id)
        db.session.add(actcol)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 取消收藏活动接口
@app.route("/activity/deletecollection", methods=["GET", "POST"])
def deactCollection():
    id = request.form.get('id')  # 竞赛的id
    user_id = request.form.get('userid')  # 用户的id

    com = Activity.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        Actcols = Actcol.query.filter_by(activity_id=id, user_id=user_id).first()
        db.session.delete(Actcols)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200

    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 社区首页接口
@app.route("/community", methods=["GET", "POST"])
def Community():
    user = request.form.get('userid')
    if request.method == 'POST' and request.form.get('sort') == '0':
        # 默认是时间顺序排列，和ｐｏｓｔ上来的是０的时候，就热度排序，
        A = Blog.query.order_by(Blog.num_of_view.desc()).all()  # desc()是从大到小，没有desc就是从小到大
        payload = []
        content = {}
        for AA in A:
            name = User.query.get(AA.user_id).username
            face = User.query.get(AA.user_id).face
            datetime = AA.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': AA.id, 'title': AA.title, 'authorid': AA.user_id, 'pageviews': AA.num_of_view,
                       'time': time, "author": name, "avatar": face}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200

    if request.method == 'POST' and request.form.get('sort') == '2':
        if user == None:
            return "error"
        # 默认是时间顺序排列，和ｐｏｓｔ上来的是2的时候，就只看关注的
        A = User.query.get(user).followed  # 我关注的人
        payload = []
        content = {}

        for a in A:
            bloguserid = a.followed_id  # 我关注的人的id
            userblogs = User.query.get(bloguserid).myblog
            for blog in userblogs:
                AA = blog  # 找到对应的博客
                name = User.query.get(AA.user_id).username
                face = User.query.get(AA.user_id).face
                datetime = AA.create_time
                time = datetime.strftime('%Y-%m-%d %H:%M:%S')
                content = {'id': AA.id, 'title': AA.title, 'authorid': AA.user_id, 'pageviews': AA.num_of_view,
                           'time': time, "author": name, "avatar": face}
                payload.append(content)
                content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200

    # 新发布的文章时间比较大，就先出现用ｄｅｓｃ从大到小排序
    A = Blog.query.order_by(Blog.create_time.desc()).all()
    payload = []
    content = {}
    for AA in A:
        name = User.query.get(AA.user_id).username
        face = User.query.get(AA.user_id).face
        datetime = AA.create_time
        time = datetime.strftime('%Y-%m-%d %H:%M:%S')
        content = {'id': AA.id, 'title': AA.title, 'author': name, 'pageviews': AA.num_of_view,
                   'time': time, "authorid": AA.user_id, "avatar": face}
        payload.append(content)
        content = {}
    data = {"data": payload}
    payload = json.dumps(data)
    return payload, 200


# 创建博客
@app.route("/blog/edit", methods=['POST', 'GET'])
def blogedit():
    id = request.form.get('userid')
    title = request.form.get('title')
    content = request.form.get('content')
    if id == None or title == None or content == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    try:
        blog = Blog(title=title, content=content, user_id=id)
        db.session.add(blog)
        db.session.commit()
        data = {"msg": "success"}
        payload = json.dumps(data)
        return payload, 200

    except:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400


# 获取博客的详情
@app.route("/blog/detail", methods=["GET", "POST"])
def BlogDe():
    id = request.form.get('id')  # 获取博客的的内容id
    user_id = request.form.get('userid')  # 获取用户的id

    blog = Blog.query.get(id)  # 找到对应的博客表
    if blog == None:
        data = {"msg": "could not find this blog id"}
        payload = json.dumps(data)
        return payload, 400

    if user_id == '-1':  # 如果未登录，则将收藏设置为-1,则将关注设置为-1
        collection = -1
        follow = -1
    else:  # 在收藏博客的表中查找用户名和文章id是否关联
        a = Blogcol.query.filter(Blogcol.user_id == user_id, Blogcol.blog_id == id).first()
        b = Follow.query.filter(Follow.follower_id == user_id, Follow.followed_id == blog.user_id).first()
        if a == None:
            collection = -1  # 未收藏
        else:
            collection = 1  # 已经收藏
        if b == None:
            follow = -1  # 则将收藏设置为-1
        else:
            follow = 1  # 则将关注设置为1
    id = blog.id
    authorid = blog.user_id
    title = blog.title  # 博客表的标题
    content = blog.content  # 博客表的内容
    time = blog.create_time.strftime('%Y-%m-%d %H:%M:%S')  # 博客表的发布时间
    pageviews = blog.num_of_view  # 博客的浏览次数
    author = User.query.get(blog.user_id).username  # 博客的发布者
    face = User.query.get(blog.user_id).face  # 发布者的头像
    pageviews = pageviews + 1
    blog.num_of_view = pageviews
    db.session.add(blog)
    db.session.commit()

    '''评论'''
    payload = []
    contentss = {}
    cs = blog.replys
    # cs = Reply.query.order_by(Reply.addtime.desc()).paginate(1, per_page=10, error_out=False).items
    for c in cs:
        if c.type == 1:
            comid = c.id  # 评论表的id
            comauthor = User.query.get(c.sender_id).username  # 评论者的名字
            comauthorid = User.query.get(c.sender_id).id  # 评论者的id
            comauthorface = User.query.get(c.sender_id).face  # 评论者的头像
            comcontent = c.content  # 评论的内容
            comtime = c.addtime.strftime('%Y-%m-%d %H:%M:%S')  # 评论的时间
            replyss = Reply.query.filter_by(comment_id=comid).all()
            # replyss = Reply.query.filter_by(comment_id=comid).paginate(1, per_page=100, error_out = False).items

            num = 0
            for reply in replyss:
                num = num + 1
            contentss = {'id': comid, 'author': comauthor, 'avatar': comauthorface,
                         'content': comcontent, 'time': comtime, "number": num, "user_id": comauthorid}
            payload.append(contentss)
            contentss = {}
    data = {"id": id, "title": title, "authorid": authorid, "content": content, "time": time, "pageviews": pageviews,
            "author": author,
            "collection": collection, "follow": follow, "avatar ": face, "comments": payload}

    payload = json.dumps(data)
    return payload, 200


# 收藏博客接口
@app.route("/blog/collection", methods=["GET", "POST"])
def blogCollection():
    id = request.form.get('id')  # 博客的id
    user_id = request.form.get('userid')  # 用户的id

    com = Blog.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        blogcol = Blogcol(blog_id=id, user_id=user_id)
        db.session.add(blogcol)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200

    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 取消收藏博客接口
@app.route("/blog/deletecollection", methods=["GET", "POST"])
def deblogCollection():
    id = request.form.get('id')  # 博客的id
    user_id = request.form.get('userid')  # 用户的id

    com = Blog.query.get(id)
    user = User.query.get(user_id)
    if com == None or user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        blogcol = Blogcol.query.filter_by(blog_id=id, user_id=user_id).first()
        db.session.delete(blogcol)
        db.session.commit()
        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 获取回复
@app.route("/activity/reply", methods=["GET", "POST"])
@app.route("/reply", methods=["GET", "POST"])
def CommentReply():
    id = request.form.get('id')  # 获取要查看的id
    if id == None:
        pass
    else:
        payload = []
        contentss = {}
        replys = Reply.query.filter_by(comment_id=id).all()  # 获取当前评论id的回复者们
        for reply in replys:  # 从回复者们分别打印每个回复者的信息以及 回复者的回复被回复的次数
            replyid = reply.id  # 回复的表的id
            sender_id = reply.sender_id  # 发送者的id
            face = User.query.get(reply.sender_id).face  # 发送者的头像
            name = User.query.get(reply.sender_id).username  # 发送者的名字
            content = reply.content  # 内容
            replyids = reply.id  # 子节点的回复
            comtime = reply.addtime.strftime('%Y-%m-%d %H:%M:%S')  # 回复的时间
            getreplys = Reply.query.filter_by(comment_id=replyids).all()
            num = 0
            for getreply in getreplys:
                num = num + 1
            contentss = {'id': replyid, 'author': name, 'avatar': face,
                         'content': content, 'time': comtime, "number": num, "userid": sender_id}
            payload.append(contentss)
            contentss = {}
        data = {"comments": payload}
        payload = json.dumps(data)
        return payload, 200


# 评论及回复
@app.route("/blog/comment", methods=["GET", "POST"])
@app.route("/comment", methods=["GET", "POST"])
def blogComment():
    blogid = request.form.get('blogid')
    actid = request.form.get('activityid')
    comid = request.form.get('competeid')
    commentid = request.form.get('commentid')
    userid = request.form.get('userid')
    content = request.form.get("content")

    # 确保有用户
    if userid == None or User.query.get(userid) == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    # 确保有内容
    if content == None:
        data = {'msg': "请输入内容"}
        payload = json.dumps(data)
        return payload, 400
    # 如果是博客
    if blogid != None:
        blog = Blog.query.get(blogid)
        if blog != None:
            try:
                comment = Reply(sender_id=userid, content=content, type=1, blog_id=blogid)
                db.session.add(comment)
                db.session.commit()

                data = {'msg': "success"}
                payload = json.dumps(data)
                return payload, 200
            except:
                data = {'msg': "error"}
                payload = json.dumps(data)
                return payload, 400

    # 如果是活动
    if actid != None:
        act = Activity.query.get(actid)
        if act != None:
            try:
                comment = Reply(sender_id=userid, content=content, type=1, activity_id=actid)
                db.session.add(comment)
                db.session.commit()
                data = {'msg': "success"}
                payload = json.dumps(data)
                return payload, 200
            except:
                data = {'msg': "error"}
                payload = json.dumps(data)
                return payload, 400

    # 如果是竞赛
    if comid != None:
        com = Competition.query.get(comid)
        if com != None:
            try:
                comment = Reply(sender_id=userid, content=content, type=1, competition_id=comid)
                db.session.add(comment)
                db.session.commit()
                data = {'msg': "success"}
                payload = json.dumps(data)
                return payload, 200
            except:
                data = {'msg': "error"}
                payload = json.dumps(data)
                return payload, 400

    # 如果是回复
    if commentid != None:
        comm = Reply.query.get(commentid)
        if comm != None:
            try:
                comment = Reply(sender_id=userid, content=content, type=2, comment_id=commentid)
                db.session.add(comment)
                db.session.commit()

                data = {'msg': "success"}
                payload = json.dumps(data)
                return payload, 200
            except:
                data = {'msg': "error"}
                payload = json.dumps(data)
                return payload, 400
    # 如果什么都没有
    else:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 获取个人资料
@app.route("/user/data", methods=["GET", "POST"])
def UserData():
    id = request.form.get('id')  # 用户的id
    user = User.query.get(id)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    else:
        username = user.username
        nickname = user.nickname
        sex = user.sex
        school = user.school
        face = user.face
        data = {"username": username, "nickname": nickname, "sex": sex,
                "school": school, "avatar": face}
        data = {"user": data}
        payload = json.dumps(data)
        return payload, 200


# 修改个人资料
@app.route("/user/edit", methods=["GET", "POST"])
def UserEdit():
    id = request.form.get('id')
    sex = request.form.get('sex')
    nickname = request.form.get('nickname')

    img = request.files.get('pic')  # 修改头像

    edituser = User.query.get(id)
    if edituser == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    if sex == None and nickname == None:
        return "请输入"

    if img != None:
        try:
            path = basedir + "/static/photo/"
            img.filename = datetime.now().strftime("%Y%m%d%H%M%S") + img.filename
            file_path = path + img.filename
            img.save(file_path)
            pathfile = "/static/photo/" + img.filename
            edituser.face = pathfile
            db.session.add(edituser)
            db.session.commit()
        except:
            data = {'msg': "error"}
            payload = json.dumps(data)
            return payload, 400

    if nickname != None:
        try:
            edituser.nickname = nickname
            db.session.add(edituser)
            db.session.commit()
        except:
            data = {'msg': "error"}
            payload = json.dumps(data)
            return payload, 400

    if sex != None:
        try:
            edituser.sex = sex
            db.session.add(edituser)
            db.session.commit()
        except:
            data = {'msg': "error"}
            payload = json.dumps(data)
            return payload, 400
    # else:
    #     edituser.nickname = nickname
    #     edituser.sex = sex
    #     db.session.add(edituser)
    #     db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


# 关注
@app.route("/follow", methods=["GET", "POST"])
def follow():
    follpwer = request.form.get('follower')
    followed = request.form.get('followed')
    if follpwer == None or followed == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 200
    try:
        follow = Follow(follower_id=follpwer, followed_id=followed)
        db.session.add(follow)
        db.session.commit()
        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200

    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 取消关注
@app.route("/unfollow", methods=["GET", "POST"])
def unfollow():
    follower = request.form.get('follower')
    followed = request.form.get('followed')
    if follower == None:
        return "error"
    if followed == None:
        return "error"
    try:
        follow = Follow.query.filter_by(follower_id=follower, followed_id=followed).first()
        db.session.delete(follow)
        db.session.commit()
        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200

    except:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400


# 查看我的博客
@app.route("/user/myblog", methods=["POST", "GET"])
def myblogs():
    userid = request.form.get('userid')
    if userid == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    user = User.query.get(userid)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    payload = []
    content = {}
    mybs = user.myblog
    for b in mybs:
        title = b.title
        id = b.id
        pageviews = b.num_of_view
        time = b.create_time.strftime('%Y-%m-%d %H:%M:%S')
        content = {"title": title, "id": id, "pageviews": pageviews, "time": time}
        payload.append(content)
        content = {}
    data = {"myblogs": payload}
    payload = json.dumps(data)
    return payload, 200


# 查看我关注的人
@app.route("/user/following", methods=["POST", "GET"])
def myfollow():
    userid = request.form.get('userid')
    if userid == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    user = User.query.get(userid)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    following = user.followed
    payload = []
    content = {}
    for f in following:
        u = User.query.get(f.followed_id)
        name = u.username
        userid = u.id
        face = u.face
        content = {"username": name, "userid": userid, "avatar": face}
        payload.append(content)
        content = {}

    data = {"data": payload}
    payload = json.dumps(data)
    return payload, 200


# 查看我收藏的竞赛
@app.route("/user/colcompete", methods=["POST", "GET"])
def mycolcompete():
    userid = request.form.get('userid')
    if userid == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    user = User.query.get(userid)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    cpts = user.cptcol
    payload = []
    content = {}
    for c in cpts:
        a = Competition.query.get(c.competition_id)
        title = a.title
        id = a.id
        pageviews = a.num_of_view
        time = a.create_time.strftime('%Y-%m-%d %H:%M:%S')
        content = {"title": title, "id": id, "pageviews": pageviews, "time": time}
        payload.append(content)
        content = {}
    data = {"myblogs": payload}
    payload = json.dumps(data)
    return payload, 200


# 查看我收藏的活动
@app.route("/user/colactivity", methods=["POST", "GET"])
def mycolactivity():
    userid = request.form.get('userid')
    if userid == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    user = User.query.get(userid)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    acts = user.actcol
    payload = []
    content = {}
    for act in acts:
        a = Activity.query.get(act.activity_id)
        title = a.title
        id = a.id
        pageviews = a.num_of_view
        time = a.create_time.strftime('%Y-%m-%d %H:%M:%S')
        content = {"title": title, "id": id, "pageviews": pageviews, "time": time}
        payload.append(content)
        content = {}
    data = {"myblogs": payload}
    payload = json.dumps(data)
    return payload, 200


# 查看我收藏的博客
@app.route("/user/colblog", methods=["POST", "GET"])
def colblog():
    userid = request.form.get('userid')
    if userid == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400

    user = User.query.get(userid)
    if user == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    blogs = user.blogcol
    payload = []
    content = {}
    for bs in blogs:
        b = Blog.query.get(bs.blog_id)
        title = b.title
        id = b.id
        pageviews = b.num_of_view
        time = b.create_time.strftime('%Y-%m-%d %H:%M:%S')
        content = {"title": title, "id": id, "pageviews": pageviews, "time": time}
        payload.append(content)
        content = {}
    data = {"myblogs": payload}
    payload = json.dumps(data)
    return payload, 200


# 上传照片test接口
@app.route("/uploadpic", methods=["GET", "POST"])
def uploadpic():
    img = request.files.get('pic')
    path = basedir + "/static/photo/"
    img.filename = datetime.now().strftime("%Y%m%d%H%M%S") + img.filename
    file_path = path + img.filename
    img.save(file_path)
    pathfile = "/static/photo/" + img.filename
    return pathfile


if __name__ == "__main__":
    app.run(host="0.0.0.0")

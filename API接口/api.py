# coding: utf-8
from model import *
import json
from flask import request
import os
from sqlalchemy import and_

basedir = os.path.abspath(os.path.dirname(__file__))

"""
已经完成的功能
.获取竞赛推文/home/compete
.竞赛内容详情/compete/detail
.收藏竞赛接口/compete/collection
.取消收藏竞赛接口/compete/deletecollection
.发布组队信息接口/compete/team

.搜索功能/search

.获取活动推文/home/activity
.活动内容详情/activity/detail
.收藏活动接口/activity/collection
.取消收藏活动接口/activity/deletecollection

.获取回复/reply
.评论及回复/comment

.社区首页接口/community
.获取博客的详情/blog/detail
.收藏博客接口/blog/collection
.取消收藏博客接口/blog/deletecollection

.获取个人资料/user/data
.修改个人资料/user/edit
.关注/follow
.取消关注/unfollow
.上传照片（暂时不能智能保存）/uploadpic
"""


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

    '''team message　将组队的内容一个列表拼接起来'''
    payload = []
    contentss = {}
    teams = com.team
    for t in teams:
        teamid = t.id
        teamauthor = User.query.get(t.master_id).username
        teamauthorface = User.query.get(t.master_id).face
        teamcontent = t.info
        teamname = t.teamname
        teamcount = t.need
        teamtime = t.create_time.strftime('%Y-%m-%d %H:%M:%S')
        contentss = {'id': teamid, 'author': teamauthor, 'avatar': teamauthorface,
                     'content': teamcontent, 'name': teamname, 'count': teamcount, 'time': teamtime}
        payload.append(contentss)
        contentss = {}
    data = {"title": title, "content": content, "time": time, "pageviews": pageviews, "author": author,
            "collection": collection, "team": payload}

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
    comcol = Cptcol(competition_id=id, user_id=user_id)
    db.session.add(comcol)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


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
    comcol = Cptcol.query.filter_by(competition_id=id, user_id=user_id).first()
    db.session.delete(comcol)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200

# 发布组队信息
@app.route("/compete/team", methods=["GET", "POST"])
def competeteam():
    competeid = request.form.get('id')  # 竞赛的id
    userid = request.form.get('userid')  # 用户的id,没登录就传-1
    teamname = request.form.get('name')  # 队伍的名字
    neednum = request.form.get('number')  # 队伍需要的人数
    info = request.form.get('lam')  # 队伍的简介
    '''如果用户没登录或者没这个用户，不能发表组队信息'''
    user = User.query.get(userid)
    if user == None or userid == '-1':
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    '''如果竞赛id错误，就返回错误'''
    com = Competition.query.get(competeid)
    if com == None:
        data = {"msg": "error"}
        payload = json.dumps(data)
        return payload, 400
    try:
        team = Team(master_id=userid, teamname=teamname, need=neednum, info=info,competition_id=competeid)
        db.session.add(team)
        db.session.commit()

        data = {"msg": "success"}
        payload = json.dumps(data)
        return payload, 200
    except:
        data = {"msg":"error"}
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
    actcol = Actcol(activity_id=id, user_id=user_id)
    db.session.add(actcol)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


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
    Actcols = Actcol.query.filter_by(activity_id=id, user_id=user_id).first()
    db.session.delete(Actcols)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


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
    commentid = request.form.get('commentid')
    userid = request.form.get('userid')
    content = request.form.get("content")

    if blogid != None:
        blog = Blog.query.get(blogid)
    else:
        blog = None
    if userid != None:
        user = User.query.get(userid)
    else:
        user = None
    if actid != None:
        act = Activity.query.get(actid)
    else:
        act = None
    if commentid != None:
        comm = Reply.query.get(commentid)
    else:
        comm = None

    if user == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    if comm == None and blog == None:  # 如果是活动评论
        comment = Reply(sender_id=userid, content=content, type=1, activity_id=actid)
        db.session.add(comment)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    elif comm == None and act == None:  # 如果是博客评论
        comment = Reply(sender_id=userid, content=content, type=1, blog_id=blogid)
        db.session.add(comment)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200
    else:  # 回复评论
        comment = Reply(sender_id=userid, content=content, type=2, comment_id=commentid)
        db.session.add(comment)
        db.session.commit()

        data = {'msg': "success"}
        payload = json.dumps(data)
        return payload, 200


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
    blogcol = Blogcol(blog_id=id, user_id=user_id)
    db.session.add(blogcol)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


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
    blogcol = Blogcol.query.filter_by(blog_id=id, user_id=user_id).first()
    db.session.delete(blogcol)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


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
    username = request.form.get('username')
    edituser = User.query.get(id)
    if edituser == None:
        data = {'msg': "error"}
        payload = json.dumps(data)
        return payload, 400
    if sex == None and username == None:
        return "请输入"
    if sex == None:
        edituser.username = username
        db.session.add(edituser)
        db.session.commit()
    if username == None:
        edituser.sex = sex
        db.session.add(edituser)
        db.session.commit()
    else:
        edituser.username = username
        edituser.sex = sex
        db.session.add(edituser)
        db.session.commit()

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

    follow = Follow(follower_id=follpwer, followed_id=followed)
    db.session.add(follow)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


# 取消关注
@app.route("/unfollow", methods=["GET", "POST"])
def unfollow():
    follower = request.form.get('follower')
    followed = request.form.get('followed')
    if follower == None:
        return "error"
    if followed == None:
        return "error"
    follow = Follow.query.filter_by(follower_id=follower, followed_id=followed).first()
    db.session.delete(follow)
    db.session.commit()

    data = {'msg': "success"}
    payload = json.dumps(data)
    return payload, 200


# 上传照片test接口
@app.route("/uploadpic", methods=["GET", "POST"])
def uploadpic():
    img = request.files.get('pic')
    path = basedir + "/photo/"
    file_path = path + img.filename
    img.save(file_path)
    return "success"


if __name__ == "__main__":
    app.run(host="0.0.0.0")

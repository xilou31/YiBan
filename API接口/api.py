# coding: utf-8
from model import *
import json
from flask import request
import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 获取竞赛推文
@app.route("/home/compete", methods=['POST', 'GET'])
def HomeCpt():
    if request.method == 'POST' and request.form.get('sort') == '0':
        # 默认是时间顺序排列，直接ｇｅｔ和ｐｏｓｔ上来的不是０的时候，就时间排序，
        # 当ｐｏｓｔ上来的是０的时候就热度排序

        # json 格式的用这个方法获取信息加载
        # data = request.data
        # j_data = json.loads(data)
        # if j_data['sort'] == 1:
        #     pass
        # else:
        #     pass

        # form 表单格式的用这个来获取信息加载
        # sort = request.form.get('sort')
        # if sort == '0'

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


# 上传照片test接口
@app.route("/uploadpic", methods=["GET", "POST"])
def uploadpic():
    img = request.files.get('pic')
    path = basedir + "/photo/"
    file_path = path + img.filename
    img.save(file_path)
    return "success"


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
                         'content': comcontent, 'time': comtime, "number": num, "user_id": comauthorid}
            payload.append(contentss)
            contentss = {}
    data = {"title": title, "content": content, "time": time, "pageviews": pageviews, "author": author,
            "collection": collection, "comments": payload}

    payload = json.dumps(data)
    return payload, 200


# 获取回复
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
                         'content': content, 'time': comtime, "number": num, "user_id": sender_id}
            payload.append(contentss)
            contentss = {}
        data = {"comments": payload}
        payload = json.dumps(data)
        return payload, 200


# 社区首页接口
@app.route("/community", methods=["GET", "POST"])
def Community():
    if request.method == 'POST' and request.form.get('sort') == '0':
        # 默认是时间顺序排列，直接ｇｅｔ和ｐｏｓｔ上来的不是０的时候，就时间排序，
        A = Blog.query.order_by(Blog.num_of_view.desc()).all()  # desc()是从大到小，没有desc就是从小到大
        payload = []
        content = {}
        for AA in A:
            name = User.query.get(AA.user_id).username
            datetime = AA.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': AA.id, 'title': AA.title, 'author': AA.user_id, 'pageviews': AA.num_of_view,
                       'time': time, "name": name}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200

    else:
        # 新发布的文章时间比较大，就先出现用ｄｅｓｃ从大到小排序
        A = Blog.query.order_by(Blog.create_time.desc()).all()
        payload = []
        content = {}
        for AA in A:
            name = User.query.get(AA.user_id).username
            datetime = AA.create_time
            time = datetime.strftime('%Y-%m-%d %H:%M:%S')
            content = {'id': AA.id, 'title': AA.title, 'author': AA.user_id, 'pageviews': AA.num_of_view,
                       'time': time, "name": name}
            payload.append(content)
            content = {}
        data = {"data": payload}
        payload = json.dumps(data)
        return payload, 200


"""
用户的ｉｄ和博客的ｉｄ
用户的ｉｄ来查看是否与博客的作者关注
用户的ｉｄ来查看是否与博客收藏
博客的ｉｄ用来返回　文章内容　标题　作者头像　作者用户名　浏览次数　发布时间　评论的内容　　
"""


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
            follow = 1  # 则将收藏设置为1

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
                         'content': comcontent, 'time': comtime, "number": num, "user_id": comauthorid}
            payload.append(contentss)
            contentss = {}
    data = {"title": title, "content": content, "time": time, "pageviews": pageviews, "author": author,
            "collection": collection, "comments": payload}

    payload = json.dumps(data)
    return payload, 200


# 搜索
@app.route("/searchcp")
def HomeSearchcp():
    pass


# 收藏竞赛接口
@app.route("/compete/collection")
def CpCollection():
    pass


"""

# 获取个人资料
@app.route("/user/data")
def UserData():
    pass


# 修改个人资料
@app.route("/user/edit")
def UserEdit():
    pass

# 评论博客
@app.route("/blog/author/<int:id>")
def index1211121(id):
    pass


# 关注
@app.route("/follow")
def index121222():
    pass


# 取消关注
@app.route("/unfollow")
def index123():
    pass


# 收藏
@app.route("/collect")
def index321():
    pass


# 取消收藏
@app.route('/uncollect')
def index132():
    pass

"""

if __name__ == "__main__":
    app.run(host="0.0.0.0")

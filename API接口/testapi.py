# coding: utf-8
from model import *
import json
from flask import request


# 获取竞赛推文
@app.route("/home/compete/", methods=['POST', 'GET'])
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
        payload = json.dumps(payload)
        return payload

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
        payload = json.dumps(payload)
        return payload


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
        payload = json.dumps(payload)
        return payload

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
        payload = json.dumps(payload)
        return payload

# 竞赛搜索
@app.route("/home/searchcp")
def HomeSearchcp():
    pass


# 活动搜索
@app.route("/home/searchat")
def HomeSearchat():
    pass


# 竞赛内容详情
@app.route("/compete/detail")
def CptDetail():
    pass


# 收藏竞赛接口
@app.route("/compete/collection")
def CpCollection():
    pass


# 获取个人资料
@app.route("/user/data")
def UserData():
    pass


# 修改个人资料
@app.route("/user/edit")
def UserEdit():
    pass


"""


# 社区首页接口
@app.route("/community/<int:id>")
def index121(id):
    pass


# 获取博客的详情
@app.route("/blog/author/<int:id>")
def index1212(id):
    pass


# 获取品论
@app.route("/blog/author/<int:id>/comment")
def index2212(id):
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
    app.run()

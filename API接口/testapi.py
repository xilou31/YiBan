# coding: utf-8
from model import *
import json


# 获取竞赛推文
@app.route("/home/compete", methods=['POST', 'GET'])
def HomeCpt():
    c = Competition.query.all()
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
@app.route("/home/activity")
def HomeAct():
    pass


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
def index312():
    pass


# 修改个人资料
@app.route("/user/edit")
def index3121():
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

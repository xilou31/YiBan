# coding: utf-8
from . import app

# 获取竞赛推文
@app.route("/home/competition")
def index():
    pass


# 获取活动推文
@app.route("/home/activity")
def index():
    pass


# 竞赛搜索
@app.route("/home/searchcp")
def index():
    pass


# 活动搜索
@app.route("/home/searchat")
def index():
    pass


# 社区首页接口
@app.route("/community/<int:id>")
def index(id):
    pass


# 获取博客的详情
@app.route("/blog/author/<int:id>")
def index(id):
    pass


# 获取品论
@app.route("/blog/author/<int:id>/comment")
def index(id):
    pass

# 评论博客
@app.route("/blog/author/<int:id>")
def index(id):
    pass


# 关注
@app.route("/follow")
def index():
    pass


# 取消关注
@app.route("/unfollow")
def index():
    pass


# 收藏
@app.route("/collect")
def index():
    pass


# 取消收藏
@app.route('/uncollect')
def index():
    pass


# 获取个人资料
@app.route("/user/data")
def index():
    pass


# 修改个人资料
@app.route("/user/edit")
def index():
    pass



if __name__ == "__main__":
    app.run()


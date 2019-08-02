from model import *

"""
db.create_all()


user1 = User(name="lmp", pwd='123456', sex=1, email='382552192@qq.com', phone=123456789, school="hnnydx",
             level="大二", face="/root/face/123456.png")
user2 = User(name="lzk", pwd='12345622', sex=2, email='382552192s22@qq.com', phone=123, school="hnnydx222",
             level="大一", face="/root/face/123456222.png")
user3 = User(name="abc", pwd='123456', sex=1, email='3825521sdas92@qq.com', phone=123489, school="hnnsdsasydx",
             level="大二", face="/root/face/123456ss.png")
user4 = User(name="lhb", pwd='12345622', sex=2, email='3825521s9sdas222@qq.com', phone=1234522222, school="hnnydxss222",
             level="大一", face="/root/face/123456222d.png")
user5 = User(name="cyj", pwd='123456', sex=1, email='382552s1sdas92@qq.com', phone=1234829, school="hnnsdsasydx",
             level="大二", face="/root/face/123456ssss.png")
user6 = User(name="qxj", pwd='12345622', sex=2, email='38255219dsdas222@qq.com', phone=12345422222,
             school="hnnydxss222",
             level="大一", face="/root/face/123456222dsd.png")

cop1 = Competition(title="竞赛标题测试１", content="竞赛内容测试１", author="网站发布人1")
cop2 = Competition(title="竞赛标题测试２", content="竞赛内容测试2", author="网站发布人2")
cop3 = Competition(title="竞赛标题测试3", content="竞赛内容测试3", author="网站发布人3")
cop4 = Competition(title="竞赛标题测试4", content="竞赛内容测试4", author="网站发布人4")
cop5 = Competition(title="竞赛标题测试5", content="竞赛内容测试5", author="网站发布人5")
cop6 = Competition(title="竞赛标题测试6", content="竞赛内容测试6", author="网站发布人6")
team1 = Team(master_id=1, teamname="咸鱼队１", need=10, info="咸鱼１队简介，我们需要最帅的人来", competition_id=1)
team2 = Team(master_id=2, teamname="咸鱼队2", need=10, info="咸鱼２队简介，我们需要最帅的人来", competition_id=1)
team3 = Team(master_id=3, teamname="咸鱼队3", need=10, info="咸鱼３队简介，我们需要最帅的人来", competition_id=1)
team4 = Team(master_id=4, teamname="咸鱼队4", need=10, info="咸鱼４队简介，我们需要最帅的人来", competition_id=2)
team5 = Team(master_id=5, teamname="咸鱼队5", need=10, info="咸鱼５队简介，我们需要最帅的人来", competition_id=2)
team6 = Team(master_id=6, teamname="咸鱼队6", need=10, info="咸鱼６队简介，我们需要最帅的人来", competition_id=2)

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
c = Competition.query.get(1)
print(c)
teams = c.team
for team in teams:
    print(team.teamname, team.info, team.need, team.master_id)
    user = User.query.get(team.master_id)
    print("my name is " + user.name)
"""



第一步 创建虚拟环境
> python3 -m venv venv

第二步 激活虚拟环境
> source venv/bin/activate

第三步 安装依赖包
> pip install -r req.txt 

第四步 以后端形式运行
> nohup python api.py &


此时此刻就能正常使用了

说明：
> 这样子代码会自动运行在5000端口，可以在api.py代码里面的 app.run(host="0.0.0.0",port=xxx),加上端口port 
如果想不用flask的服务器 那么可以用 
gunicorn -b 0.0.0.0:5000 api:app --reload -t 500 -D --access-logfile log/gunicorn.log
来替换第四步的命令，想深刻理解（请自行百度 gunicorn部署命令）



如果想用自己的服务器和自己服务器的数据库
则在model文件里面修改对应的数据库的账号密码和端口号和数据库名字
并且单独运行一下model
命令如下：
>  python model.py

此时此刻如果没有报错，那么就是创建表成功，才能继续部署api文件

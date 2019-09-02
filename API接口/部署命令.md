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
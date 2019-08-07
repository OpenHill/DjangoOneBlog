# 部署文件
import multiprocessing

bind = "127.0.0.1:8000"  # 绑定的ip与端口
backlog = 1024  # 监听队列
workers = multiprocessing.cpu_count() * 2 + 1  # 核心数
threads = 4
timeout = 30  # 超时
chdir = '/home/DjangoOneBlog/DjangoOneBlog'  # gunicorn要切换到的目的工作目录
errorlog = '/home/DjangoOneBlog/gunicorn.error.log'  # 发生错误时log的路径
accesslog = '/home/DjangoOneBlog/gunicorn.access.log'  # 正常时的log路径
loglevel = 'info'  # 日志等级
proc_name = 'gunicorn_blog_project'  # 进程名

# 服务器选择 Ubuntu18.x or CentOS 7.5

> Ubuntu 部署流程 

#### 部署前操作
##### 非root用户注意使用
```
sudo -i #进入Root
sudo apt-get update # 更新软件
sudo apt-get install git # 有就不要安装了
```

##### 安装 Mysql 有数据库就跳过


```
sudo apt install mysql-server # 安装
sudo mysql_secure_installation # 初始化
n password n y n y

systemctl status mysql.service # test

mysql -uroot -p你的密码
CREATE DATABASE 数据库名字 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; # 与setting的数据库匹配
```



##### 安装Python 3.6.5 

```
# 安装python依赖
sudo apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat-dev libffi-dev python3-dev default-libmysqlclient-dev
# 下载 Python3.6.5 安装包
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
# 解压缩
tar -xvf Python-3.6.5.tgz 
#进入解压后的目录
cd Python-3.6.5/
# 配置 带SSL 避免 pip SSL Error
./configure --with-ssl
# 编译 路径可自定义
make && make –prefix=/usr/local/bin/python3.6.5 install
# 安装完成 更新 pip
python3 -m pip install --upgrade pip 
```
##### Python 安装完成 ，下载DjangoOneBlog ，安装项目依赖包

```
# 克隆项目
git clone https://github.com/OpenHill/DjangoOneBlog.git 

# 进入项目安装虚拟环境及依赖库
cd DjangoOneBlog/
pip install virtualenv # 虚拟环境管理包
virtualenv venv  # virtualenv 虚拟环境名
source venv/bin/activate # 启动虚拟环境  退出虚拟环境 deactivate
# 安装依赖库
pip install -r requirements.txt  # 自动安装 出错记得看 第一条
```

##### 环境安装好了配置项目 settings.py
```
cd DjangoOneBlog/DjangoOneBlog   # 当前目录为 ~/DjangoOneBlog/DjangoOneBlog/DjangoOneBlog/
# 数据库为 MySql
vim setting.py # 自己去改 数据库链接设置 和 网站作者名


cd ../  # 当前目录为 ~/DjangoOneBlog/DjangoOneBlog/

mkdir static  # 创建静态文件
python manage.py collectstatic # 整合静态文件
python manage.py makemigrations # 生成数据库
python manage.py migrate # 生效
python manage.py createcachetable # 生成缓存数据库
python manage.py createsuperuser # 生成SuperAdmin
python manage.py runserver 0:0 # 测试运行
```

##### nginx and gunicorn 安装与配置
```
apt-get install nginx # 安装nginx
pip install gunicorn # 安装gunicorn
```

配置 nginx
```
cd /etc/nginx/sites-available/  # 进入配置
vim default # 编辑默认配置 不用默认配置的话自己查资料
```
```
# ng配置
server {
    listen 80; #监听端口
    server_name 3io.cc; #名字
    server_name_in_redirect off;
    access_log /root/DjangoOneBlog/nginx.access.log; # 成功日志地址
    error_log /root/DjangoOneBlog/nginx.error.log; # 错误日志地址

    location / {
        proxy_pass http://127.0.0.1:8000; #代理地址
        proxy_pass_header       Authorization;
        proxy_pass_header       WWW-Authenticate;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /root/DjangoOneBlog/DjangoOneBlog/static; # 静态文件绝对地址
    }
}
```

`service nginx stop & service nginx statr`

在项目根目录创建部署文件
```
vim gunicron.conf.py
```



```python
import multiprocessing

bind = "127.0.0.1:8000"  # 绑定的ip与端口
workers = 3  # 核心数
errorlog = '/root/DjangoOneBlog/gunicorn.error.log'  # 发生错误时log的路径
accesslog = '/root/DjangoOneBlog/gunicorn.access.log'  # 正常时的log路径
# loglevel = 'debug'   #日志等级
proc_name = 'gunicorn_project'  # 进程名
```

修改配置
```python
INSTALLED_APPS = [
    ...
    ...
    'gunicorn',  # 部署用
]
```


在根目录启动程序 
```
# 在线测试
gunicorn DjangoOneBlog.wsgi:application -c /root/DjangoOneBlog/DjangoOneBlog/gunicorn.conf.py 

# 发布
nohup gunicorn DjangoOneBlog.wsgi:application -c /root/DjangoOneBlog/DjangoOneBlog/gunicorn.conf.py 
```
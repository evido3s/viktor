# [viktor](http://baike.baidu.com/link?url=ADJn0Xz2cwixAj4HlENrFCJlJaInfMC84YKpVN7rXGAlQVzEm_iDjjRW1YPavUeMddsIcaGLNlgsCQgixS6fmq)
自用的一个运维管理系统，名字取自机械先驱 -- 维克托

##说明
使用flask web框架开发，水平有限，持续学习中，数据库使用的是MySQL，利用了celery来跑批量任务。
消息中间件及结果后端使用的是Redis。


## 使用方式

先启动MySQL及redis服务，然后克隆代码到服务器，有两个配置文件需要配置，一个是**config.py**(这是主配置文件)，另一个是**gunicorn_config.py**（这是gunicorn的配置文件）

```bash
$ git clone https://github.com/Fize/viktor.git
```
装一些必备的依赖软件包

```
$ pip install -r requirements.txt
```
然后创建数据库viktor，并给予授权

```
> create database viktor;
> grant all privileges on viktor.* to viktor@'%' identified by 'viktor';
> flush privileges;
> \q
```
创建表，并创建一个admin用户

```
$ ./manage.py shell

进入python的交互环境

db.create_all()
User.set_admin('admin')    用户名：admin  密码：admin 参数为密码，可随意修改
```
如果需要测试数据，则可以使用如下命令来自动生成测试数据

```
$ ./manage.py shell

首先，依然要先进入python的交互环境

User.generate_fake()
IDC.generate_fake()
Groups.generate_fake()
Hosts.generate_fake()

generate_fake()函数会生成测试数据，可以指定生成的数据数量

```

以上搞定以后，如果是使用的centos 7以后的系统，直接运行 **install.sh** 文件即可，这个文件会自动安装配置**gunicorn**，**supervisor**和**nginx**,并启动。

```bash
$ sh -x install.sh
```

如果想测试下可以使用如下命令启动.

```
$ ./manage.py runserver yourip

默认使用5000端口
```

### 以上初始化服务的部分功能没测试过，也没有进行权限的划分，有时间再说


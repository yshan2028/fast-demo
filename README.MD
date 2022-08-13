# 一、简介

> FastAPI 的小demo

感谢 **冰可乐** 大佬 [传送门](https://gitee.com/binkuolo/fastapi.git)

[后端代码仓库](https://gitee.com/nhnhwsnh/fastapi_demo)

[前端代码仓库](https://gitee.com/nhnhwsnh/vben_admin_demo)

[演示站点](http://fastapi.rongli.vip)【 admin / a12345678 】

# 二、快速上手

## 1.下载代码

```shell
git clone https://gitee.com/nhnhwsnh/fastapi_demo.git
```

## 2。创建python虚拟环境

> 略

## 3. 安装依赖

```shell
cd fastapi_demo
pip install -r requirements.txt
```

## 4. 启动 mysql 等基础设施

> 如果不习惯使用 docker 也可以自己手动搞定这些

```shell
docker-compose -f docker-compose.local.yml up -d
```

## 5. 迁移数据库

> 见下面的 aerich 使用方法
>
> deploy/mysql 目录下有一些初始的数据，可能对你有帮助

## 6. 运行项目

```shell
python manage.py run server
```

# 三、manage管理命令

## 查看 manage 命令帮助

```shell
python manage.py --help
```

## run server

![run_server.png](./docs/images/run_server.png)

启动服务，默认 localhost:8000

```shell
python manage.py run server 
```

如需修改主机或端口

```shell
python manage.py run server --host 127.0.0.1 --port 8888
```

## user createroot

此命令**不会**对用户名密码的格式进行检验

```shell
python manage.py user createroot --help
```

# 四、aerich 使用方法

文档： [传送门](https://github.com/tortoise/aerich)

省流：[传送门](./docs/aerich.md)

# 继续开发

## 如果你修改了 `backend` 这个目录名，以下几处也要相应的修改

+ `manage.py`  ->  `from backend.commands import app`
+ `backend/commands/run.py`  -> `app='backend.main:app',`
+ 。。。

## 新建模型

+ 在 `backend/models` 目录下新增相应的文件，并将其加入到  `__init__.py` 中
+ 使用 aerich 迁移数据库

# manage管理命令

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

# aerich 使用方法

## 初始化项目

```shell
aerich init -t backend.config.tortoise_orm_config
```

## 初始化数据库

```shell
aerich init-db
```

## 生成迁移文件

```shell
aerich migrate
```

## 执行迁移

```shell
aerich upgrade
```

# 二次开发

## 如果你修改了 `backend` 这个目录名，以下几处也要相应的修改

+ `manage.py`  ->  `from backend.commands import app`
+ `backend/commands/run.py`  -> `app='backend.main:app',`

## 新建模型

+ 在 `backend/models` 目录下新增相应的文件，并将其加入到  `__init__.py` 中
+ 使用 aerich 迁移数据库

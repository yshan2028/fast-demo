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

## 如果出现迁移失败的情况

> 先 drop 再创建数据库
>
> 清空 migrations 目录
>
> 再执行 aerich init-db
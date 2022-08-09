FROM python:3.10

# 拷贝 requirements 并安装依赖
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置工作目录
WORKDIR /app
# 拷贝代码
COPY . /app

ENTRYPOINT ["python","manage.py","run","server"]
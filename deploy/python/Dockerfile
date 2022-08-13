FROM python:3.10

# 时区
ENV TZ Asia/Shanghai

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' >/etc/timezone

# 拷贝 requirements 并安装依赖
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置工作目录
WORKDIR /app
# 拷贝代码
COPY . /app

ENTRYPOINT ["python","manage.py","run","server"]
# 使用 Python 3.10 作为基础镜像（使用国内镜像源）
FROM docker.1ms.run/library/python:3.10-slim

# 设置工作目录
WORKDIR /app

# 更换为国内 apt 镜像源并安装系统依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y gcc && \
    rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt 并安装 Python 依赖（使用国内镜像源）
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制项目文件
COPY app.py .
COPY school.db .
COPY templates/ ./templates/
COPY logo/ ./logo/

# 创建数据目录（用于持久化数据库）
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

# 启动命令
CMD ["python", "app.py"]

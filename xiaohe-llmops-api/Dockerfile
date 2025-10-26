FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 使用腾讯云镜像源
RUN sed -i 's/deb.debian.org/mirrors.tencent.com/g' /etc/apt/sources.list.d/debian.sources || \
    echo "deb https://mirrors.tencent.com/debian/ bookworm main" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tencent.com/debian/ bookworm-updates main" >> /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 设置pip腾讯云镜像源并安装 uv
RUN pip config set global.index-url https://mirrors.tencent.com/pypi/simple/
RUN pip config set global.trusted-host mirrors.tencent.com
RUN pip install uv

# 复制项目文件
COPY pyproject.toml uv.lock* ./

# 创建虚拟环境并安装依赖
RUN uv sync --no-dev

# 复制应用代码
COPY . .

# 设置环境变量
ENV FLASK_APP=app.http.app:app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 5006

# 创建启动脚本
RUN echo '#!/bin/bash\n\
# 等待数据库就绪\n\
echo "等待数据库连接..."\n\
while ! pg_isready -h ${POSTGRES_HOST:-postgres} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-llmops}; do\n\
  echo "数据库未就绪，等待中..."\n\
  sleep 2\n\
done\n\
echo "数据库已就绪!"\n\
\n\
# 运行数据库迁移\n\
echo "执行数据库迁移..."\n\
uv run flask db upgrade -d internal/migration\n\
\n\
# 创建管理员账号（如果不存在）\n\
echo "检查并创建管理员账号..."\n\
uv run python create_admin_user.py\n\
\n\
# 启动应用\n\
echo "启动API服务..."\n\
uv run python -m app.http.app' > /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]

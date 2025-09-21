#!/bin/bash

# 设置项目根目录
PROJECT_ROOT="/home/breath/projects/llmops/xiaohe-llmops-api"
cd "$PROJECT_ROOT"

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "错误: 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 启动Celery Worker（后台运行）
echo "启动Celery Worker..."
celery -A app.http.app.celery worker --loglevel=info &
CELERY_PID=$!

# 启动Flask应用
echo "启动Flask应用..."
python -m app.http.app

# 当Flask应用停止时，清理Celery进程
trap "kill $CELERY_PID" EXIT



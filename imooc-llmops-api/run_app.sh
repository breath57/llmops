#!/bin/bash

# 设置项目根目录
PROJECT_ROOT="/home/breath/projects/llmops/imooc-llmops-api"
cd "$PROJECT_ROOT"

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "错误: 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 启动Flask应用
echo "启动Flask应用..."
python -m app.http.app



### 部署指南

#### 前端（Docker）
已提供 `imooc-llmops-ui/Dockerfile` 与 `docker/docker-compose.yaml`：
```
docker compose -f docker/docker-compose.yaml up --build -d
```
默认将容器端口 80 映射到宿主 5173。

#### 后端
方式一：直接运行（适合开发/内网环境）
```
python -m app.http.app
```

方式二：自行容器化
- 基于官方 `python:3.11-slim` 构建镜像
- 使用 `uv` 安装依赖并设置 `FLASK_ENV=production`
- 通过 `gunicorn` 或 `gevent.pywsgi` 启动，暴露 5000 端口

#### 依赖服务
- Redis：供会话、任务队列使用
- 数据库：开发可用 SQLite，生产建议 PostgreSQL/MySQL

#### 环境变量
参见 `docs/backend/config.md` 与 `docs/01-QuickStart.md` 中的 `.env` 示例。



### 快速开始（本地）

#### 先决条件
- Node（使用系统默认版本即可）
- Python 3.10+，并用 `uv` 管理虚拟环境与依赖
- Redis（本地或 Docker 均可）

#### 后端启动
1) 安装依赖并创建虚拟环境
```
cd xiaohe-llmops-api
uv sync
```

2) 启动 Redis（若本地无 Redis，可用 Docker）
```
docker run --name redis-llmops -p 6379:6379 -d redis:7
```

3) 启动postgre (若本地无， 使用Docker启动)
```
docker run --name postgres-llmops -e POSTGRES_DB=llmops -e POSTGRES_USER=llmops  -e POSTGRES_PASSWORD=llmops -p 5432:5432 -d postgres:15
```

4) 启用PostgreSQL UUID扩展（重要！）
```
# 安装PostgreSQL客户端工具
sudo apt update && sudo apt install -y postgresql-client-common postgresql-client

# 在数据库中启用uuid-ossp扩展
PGPASSWORD=llmops psql -h 127.0.0.1 -p 5432 -U llmops -d llmops -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

5) 启动 Weaviate
```
docker run -d --name weaviate -p 8080:8080 -p 50051:50051 -e WEAVIATE_HOSTNAME=0.0.0.0 semitechnologies/weaviate:latest
```


6) 创建 `.env`（位于 `xiaohe-llmops-api/`）
```
WTF_CSRF_ENABLED=False

# 使用 postgre
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://llmops:llmops@127.0.0.1:5432/llmops
SQLALCHEMY_POOL_SIZE=30
SQLALCHEMY_POOL_RECYCLE=3600
SQLALCHEMY_ECHO=True

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USERNAME=
REDIS_PASSWORD=
REDIS_DB=0
REDIS_USE_SSL=False

CELERY_BROKER_DB=1
CELERY_RESULT_BACKEND_DB=1
CELERY_TASK_IGNORE_RESULT=False
CELERY_RESULT_EXPIRES=3600
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True

# 示例：内置的辅助 Agent 应用 ID（可保持默认）
ASSISTANT_AGENT_ID=6774fcef-b594-8008-b30c-a05b8190afe6

# OpenAI 配置
OPENAI_API_KEY=sk-xxxx
OPENAI_API_BASE=https://api.siliconflow.cn/v1

## WEAVIATE
WEAVIATE_PORT=8080
WEAVIATE_HOST=127.0.0.1
```

7) 初始化数据库（迁移）
```
# 确保在 xiaohe-llmops-api 目录，并已激活虚拟环境
export FLASK_APP=app.http.app:app
flask db upgrade -d internal/migration
```

8) 运行后端
```
# 在项目根（xiaohe-llmops-api）内, 运行启动脚本
./run.sh
```

1)  API 冒烟测试
```
curl http://127.0.0.1:5006/ping
```

#### 前端启动
```
cd xiaohe-llmops-ui
yarn
yarn dev
# 访问 http://127.0.0.1:5173
```

#### 使用 Docker 运行前端
```
docker compose -f docker/docker-compose.yaml up --build -d
# 访问 http://127.0.0.1:5173
```

完成上述步骤即可在本地完成一次端到端联调。更多细节请参考 `02-Architecture.md` 与 `backend/`、`frontend/` 分册。


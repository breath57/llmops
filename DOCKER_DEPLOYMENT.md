# LLMOps 项目 Docker 一键部署指南

本指南将帮助您使用 Docker Compose 在任何具备 Docker 环境的机器上一键启动部署整个 LLMOps 项目。

## 🚀 快速开始

### 先决条件

确保您的系统已安装：
- [Docker](https://docs.docker.com/get-docker/) (版本 20.10 或更高)
- [Docker Compose](https://docs.docker.com/compose/install/) (版本 2.0 或更高)

### 🚀 镜像源优化

本项目已配置阿里云镜像源，确保在国内环境下快速构建：
- **前端**: 使用 `yarn` 和阿里npm镜像源
- **后端**: 使用 `uv` 和阿里pip镜像源
- **系统依赖**: 使用阿里云APT镜像源

### 一键部署步骤

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd llmops
   ```

2. **配置环境变量**
   ```bash
   # 复制环境变量模板
   cp env.template .env
   
   # 编辑配置文件，至少需要设置 OPENAI_API_KEY
   vim .env  # 或使用您喜欢的编辑器
   ```
   
   **重要**: 项目采用 dotenv 自动加载环境变量，Docker环境会自动覆盖容器内的服务主机名配置。

3. **一键启动**
   ```bash
   # 构建并启动所有服务
   docker-compose up --build -d
   ```

4. **验证部署**
   ```bash
   # 查看服务状态
   docker-compose ps
   
   # 查看日志
   docker-compose logs -f
   ```

## 🎯 访问应用

部署完成后，您可以通过以下地址访问：

- **前端界面**: http://localhost:5173
- **后端API**: http://localhost:5000
- **API文档**: http://localhost:5000/docs (如果有配置)

## 📋 服务架构

本部署包含以下服务：

| 服务名 | 容器名 | 端口 | 说明 |
|--------|--------|------|------|
| postgres | llmops-postgres | 5432 | PostgreSQL 数据库 |
| redis | llmops-redis | 6379 | Redis 缓存和消息队列 |
| weaviate | llmops-weaviate | 8080, 50051 | Weaviate 向量数据库 |
| api | llmops-api | 5000 | Flask 后端 API 服务 |
| celery-worker | llmops-celery-worker | - | Celery 异步任务处理 |
| ui | llmops-ui | 5173 | Vue.js 前端界面 |

## ⚙️ 配置说明

### 必需配置

在 `.env` 文件中，您必须设置：

```bash
# OpenAI API密钥（必填）
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**注意**: 项目使用 dotenv 自动加载所有环境变量到应用中，无需在 docker-compose.yml 中重复定义。Docker 环境仅覆盖服务主机名（如 postgres、redis、weaviate）。

### 可选配置

其他配置项都有合理的默认值，但您可以根据需要调整：

```bash
# OpenAI API基础URL（默认使用硅基流动）
OPENAI_API_BASE=https://api.siliconflow.cn/v1

# 应用密钥（生产环境请更改）
SECRET_KEY=your-secret-key-here
```

## 🗄️ 数据持久化

项目使用 Docker volumes 来持久化重要数据：

- `postgres_data`: PostgreSQL 数据库文件
- `redis_data`: Redis 数据文件  
- `weaviate_data`: Weaviate 向量数据库文件
- `./storage`: 应用存储目录（映射到宿主机）

## 🔧 常用命令

### 启动和停止

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart api

# 查看服务状态
docker-compose ps
```

### 日志管理

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api

# 查看最近100行日志
docker-compose logs --tail=100 api
```

### 数据库管理

```bash
# 连接到数据库
docker-compose exec postgres psql -U llmops -d llmops

# 查看数据库迁移状态
docker-compose exec api uv run flask db current -d internal/migration

# 手动运行数据库迁移（通常不需要，启动时自动执行）
docker-compose exec api uv run flask db upgrade -d internal/migration
```

### 维护操作

```bash
# 重新构建服务镜像
docker-compose build --no-cache

# 清理未使用的镜像和容器
docker system prune -f

# 重置所有数据（⚠️ 警告：会删除所有数据）
docker-compose down -v
docker-compose up --build -d
```

## 🔒 安全建议

### 生产环境部署

1. **更改默认密码和密钥**
   ```bash
   # 在 .env 文件中设置强密码
   SECRET_KEY=your-very-secure-random-key-here
   ```

2. **使用反向代理**
   建议在生产环境中使用 Nginx 或其他反向代理：
   ```bash
   # 仅暴露必要端口
   docker-compose up -d
   ```

3. **启用HTTPS**
   配置SSL证书和HTTPS重定向。

4. **定期备份**
   ```bash
   # 备份数据库
   docker-compose exec postgres pg_dump -U llmops llmops > backup.sql
   
   # 备份存储目录
   tar -czf storage_backup.tar.gz ./storage
   ```

## 🚨 故障排除

### 常见问题

**问题**: 数据库连接失败
```bash
# 解决方案：检查数据库是否就绪
docker-compose logs postgres
docker-compose restart api
```

**问题**: 前端无法访问API
```bash
# 解决方案：检查网络配置
docker-compose logs ui
# 确保 nginx.conf 中的代理配置正确
```

**问题**: Celery任务不执行
```bash
# 解决方案：检查Redis连接和Celery工作进程
docker-compose logs redis
docker-compose logs celery-worker
```

**问题**: 向量数据库连接失败
```bash
# 解决方案：等待Weaviate完全启动
docker-compose logs weaviate
# Weaviate启动较慢，请等待健康检查通过
```

### 调试模式

启用调试模式获取更详细的日志：

```bash
# 在 .env 文件中设置
DEBUG=true
LOG_LEVEL=DEBUG

# 重启服务
docker-compose restart api
```

### 清理和重置

如果遇到无法解决的问题，可以完全重置：

```bash
# ⚠️ 警告：这会删除所有数据
docker-compose down -v
docker system prune -f
docker-compose up --build -d
```

## 📊 性能优化

### 资源配置

根据您的硬件配置调整容器资源：

```yaml
# 在 docker-compose.yml 中添加资源限制
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          memory: 1G
```

### 监控建议

考虑添加监控服务：
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Docker自带的监控工具

## 📞 支持和帮助

如果在部署过程中遇到问题：

1. 检查本文档的故障排除部分
2. 查看服务日志：`docker-compose logs -f`
3. 确认所有环境变量配置正确
4. 验证Docker和Docker Compose版本兼容性

## 🎉 部署完成

恭喜！如果您看到所有服务都正常运行，说明 LLMOps 项目已成功部署。您现在可以开始使用这个强大的 LLMOps 平台了！

---

**提示**: 建议将此文档保存到项目根目录，方便团队成员参考使用。

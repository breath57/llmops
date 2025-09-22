# 数据库迁移管理脚本使用说明

`db_migrate.sh` 是一个用于管理 xiaohe-llmops-api 项目数据库迁移的便捷脚本。

## 🚀 快速开始

```bash
# 基本迁移（最常用）
./db_migrate.sh

# 查看帮助
./db_migrate.sh help
```

## 📋 功能列表

### 1. 数据库迁移
```bash
# 执行迁移（默认操作）
./db_migrate.sh
./db_migrate.sh upgrade
```

### 2. 创建新迁移
```bash
# 创建新的迁移版本
./db_migrate.sh create "添加用户表"
./db_migrate.sh create "修改应用字段"
```

### 3. 查看状态
```bash
# 查看当前迁移状态
./db_migrate.sh current

# 查看迁移历史
./db_migrate.sh history
```

### 4. 回滚操作
```bash
# 回滚到指定版本
./db_migrate.sh downgrade <版本号>

# 回滚到上一个版本
./db_migrate.sh downgrade head-1

# 回滚到最初状态
./db_migrate.sh downgrade base
```

### 5. 数据库管理
```bash
# 初始化数据库迁移
./db_migrate.sh init

# 重置数据库（危险操作）
./db_migrate.sh reset

# 仅检查服务状态
./db_migrate.sh check
```

## ⚙️ 自动化功能

脚本会自动处理以下内容：

### 环境变量设置
- `FLASK_APP=app.http.app:app`
- `WEAVIATE_HOST=127.0.0.1`
- `WEAVIATE_PORT=8080`
- `WEAVIATE_GRPC_PORT=50051`
- `SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://llmops:llmops@127.0.0.1:5432/llmops`

### 服务状态检查
- 检查 PostgreSQL 容器是否运行
- 检查 Weaviate 容器是否运行
- 自动启用 PostgreSQL UUID 扩展

### 安全措施
- 危险操作需要用户确认
- 错误时自动退出
- 彩色日志输出

## 🔧 前置要求

### 必需服务
1. **PostgreSQL 容器**
   ```bash
   docker run --name postgres-llmops \
     -e POSTGRES_DB=llmops \
     -e POSTGRES_USER=llmops \
     -e POSTGRES_PASSWORD=llmops \
     -p 5432:5432 -d postgres:15
   ```

2. **Weaviate 容器**（可选，但建议启动）
   ```bash
   docker run -d --name weaviate \
     -p 8080:8080 -p 50051:50051 \
     -e WEAVIATE_HOSTNAME=0.0.0.0 \
     semitechnologies/weaviate:latest
   ```

### Python 环境
- 确保已安装 `uv` 包管理器
- 项目虚拟环境已创建

## 📝 常见用法示例

### 开发流程
```bash
# 1. 修改模型文件后，创建迁移
./db_migrate.sh create "添加新字段到用户表"

# 2. 检查生成的迁移文件
ls internal/migration/versions/

# 3. 执行迁移
./db_migrate.sh

# 4. 验证迁移状态
./db_migrate.sh current
```

### 问题排查
```bash
# 检查服务状态
./db_migrate.sh check

# 查看迁移历史
./db_migrate.sh history

# 如果需要回滚
./db_migrate.sh downgrade head-1
```

### 重新开始
```bash
# 完全重置数据库（谨慎使用）
./db_migrate.sh reset
```

## ⚠️ 注意事项

1. **数据安全**：`reset` 命令会删除所有数据，请谨慎使用
2. **服务依赖**：确保 PostgreSQL 和 Weaviate 服务正在运行
3. **权限问题**：确保脚本有执行权限 (`chmod +x db_migrate.sh`)
4. **网络配置**：脚本默认连接到本地服务，如果使用不同配置需要修改脚本

## 🐛 故障排除

### 常见错误
1. **PostgreSQL 连接失败**
   - 检查容器是否运行：`docker ps | grep postgres`
   - 检查端口是否被占用：`lsof -i :5432`

2. **UUID 函数不存在**
   - 脚本会自动启用 UUID 扩展
   - 手动启用：`docker exec postgres-llmops psql -U llmops -d llmops -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"`

3. **Weaviate 连接问题**
   - 检查容器状态：`docker ps | grep weaviate`
   - Weaviate 不是必需的，可以跳过相关错误

### 获取帮助
```bash
./db_migrate.sh help
```

## 📈 进阶用法

### 自定义环境变量
如需修改默认配置，可以编辑脚本中的 `setup_env()` 函数。

### 集成到 CI/CD
脚本可以在自动化流程中使用：
```bash
# 在 CI 中执行迁移
./db_migrate.sh upgrade
```

### 备份和恢复
虽然脚本不直接提供备份功能，但可以配合 PostgreSQL 工具：
```bash
# 备份
docker exec postgres-llmops pg_dump -U llmops llmops > backup.sql

# 恢复
docker exec -i postgres-llmops psql -U llmops -d llmops < backup.sql
```

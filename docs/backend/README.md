### 后端总览（Flask）

目录概览（节选）：
- `app/http/app.py`: 运行入口，构建 `Http` 应用并注入扩展
- `internal/server/http.py`: 自定义 `Http(Flask)`，集中初始化扩展、CORS、路由与错误处理
- `internal/router/router.py`: 聚合并注册全部路由（基于 `Blueprint`）
- `internal/extension/*`: 扩展初始化（DB、Redis、Celery、Login、Migrate、Logging）
- `pkg/sqlalchemy/sqlalchemy.py`: 对 `SQLAlchemy` 进行封装，提供 `auto_commit()`
- `config/config.py` & `config/default_config.py`: 配置中心（环境变量优先）
- `internal/migration/`: Alembic 迁移目录

运行要点：
1) `.env` → `Config` → `Http.init_app`
2) `Router.register_router(app)` 将 Handler 方法绑定到多模块 API
3) 异步任务通过 `app.extensions["celery"]` 暴露 Celery 应用

下一步：阅读 `config.md`、`routing.md`、`db.md`、`celery.md`。



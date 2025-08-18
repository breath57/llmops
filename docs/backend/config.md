### 配置说明（Config）

配置由 `config/config.py` 从环境变量读取，`config/default_config.py` 提供默认值。常用项：

- `WTF_CSRF_ENABLED`: 是否开启 CSRF（默认 False）
- `SQLALCHEMY_DATABASE_URI`: 数据库连接串（开发建议用 SQLite：`sqlite:///storage/dev.sqlite3`）
- `SQLALCHEMY_POOL_SIZE`, `SQLALCHEMY_POOL_RECYCLE`, `SQLALCHEMY_ECHO`
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_USERNAME`, `REDIS_PASSWORD`, `REDIS_DB`, `REDIS_USE_SSL`
- `CELERY_*`: `broker_url`/`result_backend` 等由 `REDIS_*` 与 DB 编号拼装
- `ASSISTANT_AGENT_ID`: 内置 Agent 应用 ID（可保持默认值）

本地开发 `.env` 示例见 `../01-QuickStart.md`。



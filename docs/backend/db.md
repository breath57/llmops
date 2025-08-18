### 数据库与迁移

- 封装：`pkg/sqlalchemy/sqlalchemy.py` 提供 `SQLAlchemy.auto_commit()` 用于包裹写操作
- 初始化：`internal/extension/database_extension.py` 中实例化 `db = SQLAlchemy()`，在 `Http` 内 `db.init_app(app)`
- 迁移：`Flask-Migrate` 指向 `internal/migration` 目录；`alembic` 通过 `internal/migration/env.py` 读取 Flask app 上下文的数据库配置

开发常用命令（示例）：
```
flask db init -d internal/migration
flask db migrate -m "init" -d internal/migration
flask db upgrade -d internal/migration
```

注意：需要在应用上下文中执行，或设置 `FLASK_APP=app.http.app:app`。



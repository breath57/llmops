### 架构与运行机制

#### 高层视图
- 浏览器（Vue3 SPA）通过 `vue-router` 管理路由与权限守卫，`pinia` 管理状态，`services/` 统一封装后端 API 调用
- 后端 `Flask` 继承自自定义 `Http` 类，集中完成：配置加载、扩展初始化（DB/Redis/Celery/日志/登录）、跨域、异常处理、路由注册
- 数据持久化使用 `Flask-SQLAlchemy`，通过自定义 `SQLAlchemy.auto_commit()` 简化事务提交；`Flask-Migrate` + Alembic 进行迁移
- 异步任务通过 `Celery`，采用 `FlaskTask` 保证在 Flask 应用上下文中运行

#### 关键后端流程
1) 入口：`app/http/app.py`
   - 加载 `.env` → 构造 `Config` → 注入扩展实例（DB、Migrate、LoginManager、Middleware、Router）
   - 创建 `Http`（`internal/server/http.py`），并依次 `init_app` 各扩展、注册路由与错误处理
2) 路由：`internal/router/router.py`
   - 通过依赖注入装配各 `Handler`，集中绑定到 `Blueprint`，暴露 RESTful API（apps/datasets/documents/workflows 等）
3) 配置：`config/config.py` + `config/default_config.py`
   - 环境变量优先，默认值兜底；包含 SQLAlchemy、Redis、Celery、开关项等
4) 数据库：`pkg/sqlalchemy/sqlalchemy.py` + `internal/migration/`
   - 提供 `auto_commit` 语法糖；迁移目录通过 `Migrate.init_app(..., directory="internal/migration")` 指定
5) 任务队列：`internal/extension/celery_extension.py`
   - 注册 `celery` 到 `app.extensions["celery"]`，CLI 可用 `-A app.http.app.celery`

#### 关键前端流程
1) 入口：`src/main.ts`
   - 创建应用 → 注册 `pinia`、`router`、`Arco` 组件库 → 挂载
2) 路由：`src/router/index.ts`
   - 配置多层路由与布局（`DefaultLayout` / `BlankLayout`）
   - `beforeEach` 鉴权：未登录访问受限路由时跳转登录页
3) 组件与页面：
   - `views/space/*`、`views/store/*`、`views/openapi/*` 等分域页面

#### 本地开发端口
- 后端：`http://127.0.0.1:5000`
- 前端：`http://127.0.0.1:5173`

更多细节见 `backend/` 与 `frontend/` 分册。



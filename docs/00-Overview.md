### LLMOps 项目总览

本项目是一个面向大语言模型应用的工程化平台（LLMOps），提供从应用搭建、插件/工具管理、知识库管理、工作流编排、会话调试、Web 应用发布到开放 API 的端到端能力。

- **后端技术栈**: Flask, Flask-Login, Flask-Migrate, Flask-SQLAlchemy, Celery, Redis, Alembic, Injector 依赖注入
- **前端技术栈**: Vue 3 + Vite + TypeScript, Pinia, Vue Router, Arco Design, TailwindCSS, ECharts, Vue Flow
- **运行与部署**: 本地开发（Node + uv + Redis + SQLite/PG），前端 Dockerfile，UI 的 docker-compose 编排

#### 代码结构（顶层）
- `imooc-llmops-api/`: 后端服务（Flask + Celery + SQLAlchemy）
- `imooc-llmops-ui/`: 前端 SPA（Vue3 + Vite）
- `docker/`: 与前端相关的 docker-compose 编排
- `docs/`: 学习与实现文档（你正在读的内容）

#### 你将学到什么
1) 快速启动整套环境并完成一次端到端联调
2) 理解后端工程的配置、扩展初始化、路由注册、ORM 与迁移、任务队列
3) 理解前端工程的入口、路由守卫、状态管理与页面布局
4) 会根据已有模块，新增一个最小功能（如新增一个 API 并在前端调用）
5) 学会把该项目写入简历并能自信面试讲解

建议配合阅读：`01-QuickStart.md`、`02-Architecture.md`、`backend/` 与 `frontend/` 分册。



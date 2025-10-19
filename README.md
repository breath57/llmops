# LLMOps - 大语言模型应用工程化平台

[![Live Demo](https://img.shields.io/badge/🌐-Live%20Demo-brightgreen.svg)](http://llmops.hezhiwei.online/auth/login?user=root@root.com&pw=root123456)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Vue](https://img.shields.io/badge/vue-3.4+-green.svg)](https://vuejs.org)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://docker.com)

## 🎯 项目简介

LLMOps 是一个面向大语言模型应用的工程化平台，提供从应用搭建、插件/工具管理、知识库管理、工作流编排、会话调试、Web 应用发布到开放 API 的端到端能力。

> 🌟 **立即体验**: 项目已部署在线，[点击这里快速体验](http://llmops.hezhiwei.online/auth/login?user=root@root.com&pw=root123456) 所有功能！

### ✨ 核心功能

- **🤖 AI应用管理**: 创建、配置和发布AI应用
- **📚 知识库管理**: 文档上传、分片处理和向量检索
- **🔧 工具集成**: API工具提供者管理和工具调用
- **🔄 工作流编排**: 可视化工作流设计和执行
- **💬 会话调试**: 实时对话测试和调试
- **🌐 Web应用发布**: 一键发布为Web应用
- **🔑 开放API**: 完整的RESTful API接口
- **👤 用户管理**: 多用户支持和权限控制
- **🔓 匿名访问**: 支持匿名用户访问Web应用

## 🏗️ 技术架构

### 后端技术栈
- **框架**: Flask 3.1+ (Python 3.12+)
- **数据库**: PostgreSQL 15 + SQLAlchemy 2.0
- **缓存/队列**: Redis 7 + Celery 5.5
- **向量数据库**: Weaviate
- **认证**: Flask-Login + JWT
- **依赖注入**: Injector
- **文档处理**: LangChain + Unstructured
- **包管理**: uv

### 前端技术栈
- **框架**: Vue 3.4 + Vite 5.2
- **语言**: TypeScript 5.4
- **状态管理**: Pinia 2.1
- **路由**: Vue Router 4.3
- **UI组件**: Arco Design Vue 2.55
- **样式**: TailwindCSS 3.4
- **图表**: ECharts 5.6 + Vue-ECharts
- **流程图**: Vue Flow
- **包管理**: npm/yarn

### 基础设施
- **容器化**: Docker + Docker Compose
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **向量存储**: Weaviate
- **文件存储**: 本地存储 + 腾讯云COS

## 🌐 在线体验

**无需安装，立即体验！**

- 🔗 **测试账号登录**: [点击自动登录测试号](http://llmops.hezhiwei.online/auth/login?user=root@root.com&pw=root123456)
- 🔗 **GitHub授权登录**: [点击GitHub授权登录](https://github.com/login?client_id=Ov23liFFWNPXG4h62ylh&return_to=%2Flogin%2Foauth%2Fauthorize%3Fclient_id%3DOv23liFFWNPXG4h62ylh%26redirect_uri%3Dhttp%253A%252F%252Fllmops.hezhiwei.online%252Fauth%252Fauthorize%252Fgithub%26scope%3Duser%253Aemail)

> 💡 **提示**: 使用测试账号可以快速体验所有功能，包括AI应用创建、知识库管理、工作流编排等。

## 🚀 快速开始

### 环境要求

- **Docker**: 20.10+ (推荐使用阿里云镜像源)
- **Docker Compose**: 2.0+
- **Node.js**: 18+ (前端开发)
- **Python**: 3.12+ (后端开发)
- **uv**: Python包管理器

### 一键部署 (推荐)

1. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd llmops
   ```

2. **配置环境变量**
   ```bash
   # 复制环境变量模板
   cp .env.template .env
   
   # 编辑配置文件，设置必要的API密钥
   vim .env
   ```

3. **一键启动**
   ```bash
   # 构建并启动所有服务
   docker-compose up --build -d
   ```

4. **访问应用**
   - 前端界面: http://localhost:5173
   - 后端API: http://localhost:5006
   - 管理员账号: 查看 `.env` 文件中的 `ADMIN_USER_ACCOUNT` 和 `ADMIN_USER_PW`

### 本地开发

#### 后端开发
```bash
cd xiaohe-llmops-api

# 安装依赖
uv sync

# 启动开发服务器
uv run python -m app.http.app
```

#### 前端开发
```bash
cd xiaohe-llmops-ui

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 启动中间件服务
```bash
# 启动数据库和缓存服务
docker-compose up postgres redis weaviate -d
```

## 📁 项目结构

```
llmops/
├── xiaohe-llmops-api/          # 后端API服务
│   ├── app/                    # 应用主目录
│   ├── internal/               # 内部模块
│   │   ├── extension/          # 扩展初始化
│   │   ├── migration/          # 数据库迁移
│   │   └── router/             # 路由管理
│   ├── pkg/                    # 公共包
│   └── pyproject.toml          # Python依赖配置
├── xiaohe-llmops-ui/           # 前端UI应用
│   ├── src/                    # 源代码
│   │   ├── views/              # 页面组件
│   │   ├── components/         # 通用组件
│   │   ├── services/           # API服务
│   │   └── stores/             # 状态管理
│   └── package.json            # Node.js依赖配置
├── docker/                     # Docker相关配置
├── docs/                       # 项目文档
├── storage/                    # 文件存储目录
├── docker-compose.yml          # Docker编排配置
└── README.md                   # 项目说明文档
```

## 🔧 配置说明

### 环境变量配置

主要环境变量包括：

```bash
# 数据库配置
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=llmops
POSTGRES_PASSWORD=llmops
POSTGRES_DB=llmops

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# Weaviate配置
WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080

# 大模型配置 (硅基流动)
SILICONFLOW_API_KEY=your_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1

# LangSmith配置
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key

# 管理员账号
ADMIN_USER_ACCOUNT=admin
ADMIN_USER_PW=admin123
```

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端UI | 5173 | Vue开发服务器 |
| 后端API | 5006 | Flask API服务 |
| PostgreSQL | 5432 | 数据库服务 |
| Redis | 6379 | 缓存和消息队列 |
| Weaviate | 8080 | 向量数据库 |

## 📖 使用指南

### 创建AI应用

1. 登录系统后，进入"应用管理"
2. 点击"创建应用"，填写应用基本信息
3. 配置应用参数（模型、提示词等）
4. 关联知识库（可选）
5. 发布应用到Web版本

### 知识库管理

1. 进入"知识库管理"
2. 创建知识库并上传文档
3. 配置文档处理规则
4. 等待文档处理和向量化完成
5. 测试知识库检索效果

### 工作流编排

1. 进入"工作流管理"
2. 使用可视化编辑器设计工作流
3. 配置节点参数和连接关系
4. 测试工作流执行
5. 发布工作流供应用使用

## 🔍 API文档

后端提供完整的RESTful API接口，主要模块包括：

- **用户认证**: `/api/auth/*`
- **应用管理**: `/api/apps/*`
- **知识库**: `/api/datasets/*`
- **工作流**: `/api/workflows/*`
- **对话**: `/api/conversations/*`
- **工具**: `/api/tools/*`

详细的API文档请参考项目中的 `docs/` 目录。

## 🧪 测试

### 后端测试
```bash
cd xiaohe-llmops-api
uv run pytest
```

### 前端测试
```bash
cd xiaohe-llmops-ui
npm run test:unit
```

## 📚 文档

- [快速开始指南](docs/01-QuickStart.md)
- [架构设计](docs/02-Architecture.md)
- [简历指南](docs/03-Resume-Guide.md)
- [Docker部署指南](DOCKER_DEPLOYMENT.md)
- [匿名访问功能](ANONYMOUS_ACCESS_GUIDE.md)
- [管理员创建指南](CREATE_ADMIN_GUIDE.md)

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架
- [LangChain](https://langchain.com/) - LLM应用开发框架
- [Weaviate](https://weaviate.io/) - 向量数据库
- [Arco Design](https://arco.design/) - 企业级UI组件库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/your-repo/llmops/issues)
- 发送邮件至: 1498408920@qq.com

---

⭐ 如果这个项目对你有帮助，请给它一个星标！

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import dotenv
from flask_login import LoginManager
from flask_migrate import Migrate
from injector import Injector

from config import Config
from internal.middleware import Middleware
from internal.router import Router
from internal.server import Http
from pkg.sqlalchemy import SQLAlchemy
from .module import injector

# 1.将env加载到环境变量中
# 判断环境
if os.getenv("FLASK_ENV") == "production":
    dotenv.load_dotenv()
else:
    dotenv.load_dotenv(".env.local")

# 2.构建LLMOps项目配置
conf = Config()

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    login_manager=injector.get(LoginManager),
    middleware=injector.get(Middleware),
    router=injector.get(Router),
)

celery = app.extensions["celery"]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

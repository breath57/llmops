### 路由与 Handler

集中定义在 `internal/router/router.py`，通过依赖注入将各 `Handler`（位于 `internal/handler/*`）装配进来，再统一绑定到 `Blueprint`。

核心代码：
```8:35:/home/breath/projects/llmops/xiaohe-llmops-api/internal/router/router.py
@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler
    api_tool_handler: ApiToolHandler
    ...
```

绑定示例：
```62:76:/home/breath/projects/llmops/xiaohe-llmops-api/internal/router/router.py
def register_router(self, app: Flask):
    """注册路由"""
    bp = Blueprint("llmops", __name__, url_prefix="")
    openapi_bp = Blueprint("openapi", __name__, url_prefix="")

    bp.add_url_rule("/ping", view_func=self.app_handler.ping)
    bp.add_url_rule("/apps", view_func=self.app_handler.get_apps_with_page)
    ...
```

你可以新增一个最小 API：
1) 在 `internal/handler/` 新增 `hello_handler.py`，提供 `def hello(): return json(Response.ok({"msg": "hello"}))`
2) 在 `internal/handler/__init__.py` 导出 `HelloHandler`
3) 在 `internal/router/router.py` 注入并 `bp.add_url_rule("/hello", view_func=self.hello_handler.hello)`
4) 重启后端，访问 `GET /hello`



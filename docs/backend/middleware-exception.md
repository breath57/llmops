### 中间件与异常处理

#### 中间件（登录与鉴权）
`internal/middleware/middleware.py` 通过 `LoginManager.request_loader` 托管鉴权：

```19:33:/home/breath/projects/llmops/imooc-llmops-api/internal/middleware/middleware.py
@dataclass
class Middleware:
    ...
    def request_loader(self, request: Request) -> Optional[Account]:
        if request.blueprint == "llmops":
            access_token = self._validate_credential(request)
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
        elif request.blueprint == "openapi":
            api_key = self._validate_credential(request)
            api_key_record = self.api_key_service.get_api_by_by_credential(api_key)
            ...
```

`_validate_credential` 统一校验 `Authorization: Bearer <credential>` 格式。

#### 异常处理
自定义异常定义在 `internal/exception/exception.py`，`Http._register_error_handler` 捕获：

```73:93:/home/breath/projects/llmops/imooc-llmops-api/internal/server/http.py
def _register_error_handler(self, error: Exception):
    if isinstance(error, CustomException):
        return json(Response(code=error.code, message=error.message, data=error.data or {}))
    ...
```

在业务代码中抛出 `UnauthorizedException/ForbiddenException` 等即可得到统一错误响应体。



### 数据模型（Models）概览

模型位于 `internal/model/*`，通过 Flask-SQLAlchemy 定义，并配合 Alembic 进行迁移。示例（节选）：

```1:20:/home/breath/projects/llmops/xiaohe-llmops-api/internal/model/app.py
class App(db.Model):
    ...
```

统一响应封装位于 `pkg/response/`，包含：
```8:22:/home/breath/projects/llmops/xiaohe-llmops-api/pkg/response/__init__.py
from .http_code import HttpCode
from .response import (
    Response,
    json, success_json, fail_json, validate_error_json,
    message, success_message, fail_message, not_found_message, unauthorized_message, forbidden_message,
    compact_generate_response,
)
```

在 Handler 中建议返回 `success_json(data)` 或 `compact_generate_response(...)` 保持一致的返回体格式。



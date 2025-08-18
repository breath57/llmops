### Celery 异步任务

- 初始化：`internal/extension/celery_extension.py` 在 `init_app` 中创建 `Celery(app.name, task_cls=FlaskTask)` 并加载 `app.config["CELERY"]`
- 上下文：自定义 `FlaskTask` 保证任务在 Flask 上下文中运行
- 暴露：`app.extensions["celery"]`

运行 Worker：
```
celery -A app.http.app.celery worker -l INFO
```

新增任务示例：
```
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

然后在业务代码中调用 `add.delay(1, 2)`。



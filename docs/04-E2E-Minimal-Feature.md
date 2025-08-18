### 端到端最小功能实战（新增一个 Hello 接口并在前端调用）

目标：后端新增 `GET /hello` 返回固定 JSON，前端新增页面按钮调用并展示结果。

#### 后端改动
1) 新增 `internal/handler/hello_handler.py`
```
from pkg.response import success_json

class HelloHandler:
    def hello(self):
        return success_json({"msg": "hello"})
```

2) 修改 `internal/handler/__init__.py` 导出 `HelloHandler`
```
from .hello_handler import HelloHandler
__all__ = [..., "HelloHandler"]
```

3) 修改 `internal/router/router.py` 注入并绑定路由
```
@dataclass
class Router:
    ...
    hello_handler: HelloHandler

def register_router(self, app):
    ...
    bp.add_url_rule("/hello", view_func=self.hello_handler.hello)
```

重启后端，`curl http://127.0.0.1:5000/hello`

#### 前端改动
1) 新增一个页面（或在 `HomeView.vue`）添加按钮与请求逻辑
```
<template>
  <a-button @click="load">Call Hello</a-button>
  <div>{{ msg }}</div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
const msg = ref('')
const load = async () => {
  const res = await fetch('/hello')
  const data = await res.json()
  msg.value = data.data.msg
}
</script>
```

2) 若有统一服务封装，可在 `src/services` 增加 `hello.ts` 并在页面引入调用。

完成后即可实现从路由到前端页面的完整打通。



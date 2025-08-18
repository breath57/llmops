### 前端总览（Vue 3 + Vite）

目录概览：
- `src/main.ts`: 应用入口，注册 `pinia`、`router`、`Arco`
- `src/router/index.ts`: 路由表与登录守卫
- `src/stores/*`: Pinia 状态管理
- `src/services/*`: 后端 API 封装
- `src/views/*`: 页面与布局（`layouts/DefaultLayout.vue` 等）

开发命令：
```
yarn
yarn dev
```

路由守卫要点：未登录访问受限路由时重定向到 `/auth/login`。



# 构建阶段
FROM node:23-alpine AS builder

WORKDIR /app

# 设置阿里镜像源
# RUN npm config set registry https://registry.npmmirror.com
RUN npm config set registry https://mirrors.cloud.tencent.com/npm

# 安装yarn并设置阿里镜像源
# RUN npm install -g yarn
# RUN yarn config set registry https://registry.npmmirror.com
RUN yarn config set registry https://mirrors.cloud.tencent.com/npm

# 复制package文件
COPY package*.json yarn.lock* ./

# 安装依赖
RUN yarn install --frozen-lockfile

# 复制源代码
COPY . .

# 构建应用
RUN yarn build

# 生产阶段
FROM nginx:alpine

# 复制构建结果到nginx目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口（与nginx监听端口一致）
EXPOSE 5173

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]

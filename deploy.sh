# 清理未使用的镜像和容器
docker system prune -f

# 重置所有数据（⚠️ 警告：会删除所有数据）
# docker-compose down -v
docker-compose up --build -d
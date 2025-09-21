# 管理员账号创建指南

## 📖 概述

本指南说明如何使用 `create_admin_user.py` 脚本创建系统管理员账号。

## 🔧 使用方法

### 方法一：在容器内执行（推荐）

```bash
# 1. 进入API容器
docker-compose exec api bash

# 2. 在容器内执行脚本
python create_admin_user.py
```

### 方法二：本地环境执行

```bash
# 1. 进入后端项目目录
cd xiaohe-llmops-api

# 2. 确保虚拟环境激活
uv sync

# 3. 执行脚本
uv run python create_admin_user.py
```

## 👤 创建的账号信息

| 字段 | 值 |
|------|-----|
| **邮箱** |  `(.env文件自定义)ADMIN_USER_ACCOUNT` |
| **密码** |  `(.env文件自定义)ADMIN_USER_PW` |
| **名称** | Administrator |

## ⚠️ 重要提醒

1. **密码安全性**：创建的密码 `root` 不符合系统安全要求，仅用于初始化
2. **立即修改**：登录后请立即在系统中修改为符合安全要求的密码
3. **安全要求**：系统要求密码至少8位，包含字母和数字

## 🚨 故障排除

### 常见错误

**错误1：账号已存在**
```
❌ 账号 root@root.com 已存在！
```
**解决方案**：账号已创建，可直接使用现有账号登录

**错误2：数据库连接失败**
```
❌ 创建管理员账号失败: database connection error
```
**解决方案**：
- 确保数据库服务正在运行
- 检查环境变量配置是否正确
- 确保数据库迁移已完成

**错误3：权限不足**
```
permission denied: ./create_admin_user.py
```
**解决方案**：
```bash
chmod +x create_admin_user.py
```

## 🔄 脚本执行流程

1. ✅ 加载环境变量和配置
2. ✅ 创建Flask应用上下文
3. ✅ 检查账号是否已存在
4. ✅ 生成密码盐值和哈希
5. ✅ 创建账号记录
6. ✅ 保存到数据库

## 🎯 成功输出示例

```
🚀 开始创建管理员账号...
⚠️  密码 'root' 不符合系统安全要求，仅用于演示
✅ 管理员账号创建成功！
📧 邮箱: root@root.com
🔑 密码: root
👤 名称: Administrator
🆔 ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

⚠️  提醒：登录后请立即修改密码为符合安全要求的密码！
🎉 脚本执行完成！
```

## 🔐 后续安全措施

1. **登录系统**：使用.env文件中的 `ADMIN_USER_ACCOUNT` / `ADMIN_USER_PW` 登录
2. **修改密码**：进入个人设置页面，修改为安全密码
3. **删除脚本**：生产环境中可删除此脚本文件
4. **监控日志**：定期检查账号访问日志

---

**注意**：此脚本仅用于初始化管理员账号，请在生产环境中妥善保管和使用。

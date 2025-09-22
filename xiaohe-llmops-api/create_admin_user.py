#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
管理员账号创建脚本
创建账号：root@root.com，密码：root
"""
import os
import sys
import base64
import secrets
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
import dotenv
if os.getenv("FLASK_ENV") == "production":
    dotenv.load_dotenv()
else:
    dotenv.load_dotenv(".env.local")

from flask import Flask
from internal.model.account import Account
from internal.extension.database_extension import db
from pkg.password import hash_password, validate_password
from config import Config


def create_flask_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    config = Config()
    app.config.from_object(config)
    
    # 初始化数据库
    db.init_app(app)
    
    return app


def create_admin_user():
    """创建管理员账号"""
    app = create_flask_app()
    
    with app.app_context():
        email = os.getenv("ADMIN_USER_ACCOUNT")
        password = os.getenv("ADMIN_USER_PW")
        if not email or not password:
            print("❌ 环境变量未配置管理员账号，因此不创建管理员账号，若需要请检查环境变量 ADMIN_USER_ACCOUNT 和 ADMIN_USER_PW")
            return
        
        name = "Administrator"
        
        try:
            # 检查账号是否已存在
            existing_account = db.session.query(Account).filter(
                Account.email == email
            ).one_or_none()
            
            # 注意：这里的密码不符合系统默认的复杂度要求（至少8位包含字母和数字）
            # 但为了演示目的，我们跳过验证
            print(f"⚠️  密码 '{password}' 不符合系统安全要求，仅用于演示")
            
            # 生成密码盐值
            salt = secrets.token_bytes(16)
            base64_salt = base64.b64encode(salt).decode()
            
            # 加密密码
            password_hashed = hash_password(password, salt)
            base64_password_hashed = base64.b64encode(password_hashed).decode()

            if existing_account:
                # 直接更新密码即可
                existing_account.password = base64_password_hashed
                existing_account.password_salt = base64_salt
                print('更新密码成功')
            else:
                # 创建账号
                admin_account = Account(
                    name=name,
                    email=email,
                    password=base64_password_hashed,
                    password_salt=base64_salt,
                    avatar="",
                    last_login_at=datetime.now(),
                    last_login_ip="127.0.0.1"
                )
                db.session.add(admin_account)
            db.session.commit()
            
            print("✅ 管理员账号创建成功！")
            print(f"📧 邮箱: {email}")
            print(f"🔑 密码: {password}")
            print(f"👤 名称: {name}")
            print("\n⚠️  提醒：请不要将该账号信息泄露给他人！")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建管理员账号失败: {str(e)}")
            raise


if __name__ == "__main__":
    print("🚀 开始创建管理员账号...")
    create_admin_user()
    print("🎉 脚本执行完成！")

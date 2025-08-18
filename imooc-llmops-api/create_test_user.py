#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建测试用户的临时脚本
"""
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 加载环境变量
import dotenv
dotenv.load_dotenv()

from app.http.app import app
from app.http.module import injector
from internal.service import AccountService
from pkg.password import hash_password
from pkg.sqlalchemy import SQLAlchemy

def create_test_user():
    """创建一个测试用户"""
    with app.app_context():
        # 获取服务实例
        account_service = injector.get(AccountService)
        db = injector.get(SQLAlchemy)
        
        # 测试用户信息
        test_email = "test@example.com"
        test_password = "123456"
        test_name = "测试用户"
        
        # 检查用户是否已存在
        existing_user = account_service.get_account_by_email(test_email)
        if existing_user:
            print(f"用户 {test_email} 已存在，ID: {existing_user.id}")
            return existing_user
        
        # 生成密码哈希和盐
        password_salt = os.urandom(16).hex()
        password_hash = hash_password(test_password, password_salt)
        
        # 创建用户
        with db.auto_commit():
            user = account_service.create_account(
                name=test_name,
                email=test_email,
                password=password_hash,
                password_salt=password_salt,
                avatar="",
                last_login_at=datetime.now(),
                last_login_ip="127.0.0.1"
            )
        
        print(f"测试用户创建成功！")
        print(f"邮箱: {test_email}")
        print(f"密码: {test_password}")
        print(f"用户ID: {user.id}")
        
        return user

if __name__ == "__main__":
    create_test_user()

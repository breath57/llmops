#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接通过SQL创建测试用户的脚本
"""
import os
import hashlib
from datetime import datetime

def create_test_user_sql():
    """生成创建测试用户的SQL语句"""
    # 测试用户信息
    test_email = "test@example.com"
    test_password = "123456"
    test_name = "测试用户"
    
    # 生成密码哈希和盐
    password_salt = os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac('sha256', test_password.encode(), password_salt.encode(), 100000).hex()
    
    # 生成UUID（使用PostgreSQL的uuid_generate_v4()）
    sql = f"""
INSERT INTO account (id, name, email, password, password_salt, avatar, last_login_at, last_login_ip, updated_at, created_at)
VALUES (
    uuid_generate_v4(),
    '{test_name}',
    '{test_email}',
    '{password_hash}',
    '{password_salt}',
    '',
    CURRENT_TIMESTAMP,
    '127.0.0.1',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
"""
    
    print("测试用户信息:")
    print(f"邮箱: {test_email}")
    print(f"密码: {test_password}")
    print()
    print("执行以下SQL语句:")
    print(sql)
    
    return sql

if __name__ == "__main__":
    create_test_user_sql()

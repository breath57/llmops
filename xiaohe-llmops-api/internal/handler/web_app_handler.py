#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/10 22:04
@Author  : thezehui@gmail.com
@File    : web_app_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from flask import request, session
from flask_login import current_user
from injector import inject
import uuid

from internal.schema.web_app_schema import (
    GetWebAppResp,
    WebAppChatReq,
    GetConversationsReq,
    GetConversationsResp,
)
from internal.service import WebAppService
from pkg.response import success_json, validate_error_json, success_message, compact_generate_response


@inject
@dataclass
class WebAppHandler:
    """WebApp处理器"""
    web_app_service: WebAppService

    def get_web_app(self, token: str):
        """根据传递的token凭证标识获取WebApp基础信息"""
        # 1.调用服务根据传递的token获取应用信息
        app = self.web_app_service.get_web_app(token)
        
        # 2.检查是否需要登录
        is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
        if not app.allow_anonymous_access and not is_authenticated:
            return validate_error_json({"error": "此应用需要登录才能访问"})

        # 3.构建响应结构并返回
        resp = GetWebAppResp()

        return success_json(resp.dump(app))

    def web_app_chat(self, token: str):
        """根据传递的token+query等信息与WebApp进行对话"""
        # 1.获取应用信息并检查访问权限
        app = self.web_app_service.get_web_app(token)
        
        # 2.检查是否需要登录
        is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
        if not app.allow_anonymous_access and not is_authenticated:
            return validate_error_json({"error": "此应用需要登录才能访问"})
        
        # 3.提取请求并校验
        req = WebAppChatReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 4.获取用户信息（登录用户或匿名用户）
        user = self._get_user_for_webapp(app)

        # 5.调用服务获取对应响应内容
        response = self.web_app_service.web_app_chat(token, req, user)

        return compact_generate_response(response)

    def stop_web_app_chat(self, token: str, task_id: UUID):
        """根据传递的token+task_id停止与WebApp的对话"""
        # 1.获取应用信息并检查访问权限
        app = self.web_app_service.get_web_app(token)
        
        # 2.检查是否需要登录
        is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
        if not app.allow_anonymous_access and not is_authenticated:
            return validate_error_json({"error": "此应用需要登录才能访问"})
        
        # 3.获取用户信息（登录用户或匿名用户）
        user = self._get_user_for_webapp(app)
        
        self.web_app_service.stop_web_app_chat(token, task_id, user)
        return success_message("停止WebApp会话成功")

    def get_conversations(self, token: str):
        """根据传递的token+is_pinned获取指定WebApp下的所有会话列表信息"""
        # 1.获取应用信息并检查访问权限
        app = self.web_app_service.get_web_app(token)
        
        # 2.检查是否需要登录
        is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
        if not app.allow_anonymous_access and not is_authenticated:
            return validate_error_json({"error": "此应用需要登录才能访问"})
        
        # 3.提取请求并校验
        req = GetConversationsReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 4.获取用户信息（登录用户或匿名用户）
        user = self._get_user_for_webapp(app)

        # 5.调用服务获取会话列表
        conversations = self.web_app_service.get_conversations(token, req.is_pinned.data, user)

        # 6.构建响应并返回
        resp = GetConversationsResp(many=True)

        return success_json(resp.dump(conversations))
    
    def _get_user_for_webapp(self, app):
        """获取WebApp访问用户（登录用户或匿名用户）"""
        # 检查用户是否已登录
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            return current_user
        elif app.allow_anonymous_access:
            # 为匿名用户创建或获取临时用户标识
            return self._get_or_create_anonymous_user()
        else:
            return None
    
    def _get_or_create_anonymous_user(self):
        """获取或创建匿名用户"""
        # 从session中获取匿名用户ID，如果不存在则创建
        anonymous_user_id = session.get('anonymous_user_id')
        if not anonymous_user_id:
            # 生成标准UUID作为匿名用户ID
            anonymous_user_id = str(uuid.uuid4())
            session['anonymous_user_id'] = anonymous_user_id
        
        # 创建一个匿名用户对象（类似Account模型的简化版）
        class AnonymousUser:
            def __init__(self, user_id):
                # 确保ID是UUID格式
                self.id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
                self.email = f"anonymous_{str(self.id)[:8]}@temp.com"
                self.name = f"匿名用户_{str(self.id)[:8]}"
                self.is_anonymous = True
        
        return AnonymousUser(anonymous_user_id)

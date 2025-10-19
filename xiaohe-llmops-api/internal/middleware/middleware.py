#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/10/25 10:42
@Author  : thezehui@gmail.com
@File    : middleware.py
"""
from dataclasses import dataclass
from typing import Optional

from flask import Request, session
from injector import inject
import uuid

from internal.exception import UnauthorizedException
from internal.model import Account
from internal.service import JwtService, AccountService, ApiKeyService, WebAppService


@inject
@dataclass
class Middleware:
    """应用中间件，可以重写request_loader与unauthorized_handler"""
    jwt_service: JwtService
    api_key_service: ApiKeyService
    account_service: AccountService
    web_app_service: WebAppService

    def request_loader(self, request: Request) -> Optional[Account]:
        """登录管理器的请求加载器"""
        # 1.单独为llmops路由蓝图创建请求加载器
        if request.blueprint == "llmops":
            # 2.检查是否为WebApp接口，如果是则进行特殊处理
            if self._is_web_app_request(request):
                return self._handle_web_app_request(request)
            
            # 3.校验获取access_token
            access_token = self._validate_credential(request)

            # 4.解析token信息得到用户信息并返回
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
        elif request.blueprint == "openapi":
            # 4.校验获取api_key
            api_key = self._validate_credential(request)

            # 5.解析得到APi秘钥记录
            api_key_record = self.api_key_service.get_api_by_by_credential(api_key)

            # 6.判断Api秘钥记录是否存在，如果不存在则抛出错误
            if not api_key_record or not api_key_record.is_active:
                raise UnauthorizedException("该秘钥不存在或未激活")

            # 7.获取秘钥账号信息并返回
            return api_key_record.account
        else:
            return None

    @classmethod
    def _validate_credential(cls, request: Request) -> str:
        """校验请求头中的凭证信息，涵盖access_token和api_key"""
        # 1.提取请求头headers中的信息
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException("该接口需要授权才能访问，请登录后尝试")

        # 2.请求信息中没有空格分隔符，则验证失败，Authorization: Bearer access_token
        if " " not in auth_header:
            raise UnauthorizedException("该接口需要授权才能访问，验证格式失败")

        # 4.分割授权信息，必须符合Bearer access_token
        auth_schema, credential = auth_header.split(None, 1)
        if auth_schema.lower() != "bearer":
            raise UnauthorizedException("该接口需要授权才能访问，验证格式失败")

        return credential
    
    def _is_web_app_request(self, request: Request) -> bool:
        """检查是否为WebApp相关的请求"""
        # 1. 直接的WebApp接口
        if request.path.startswith('/web-apps/'):
            return True
        
        # 2. 排除 /apps/{app_id}/conversations/messages 这种格式，因为它不是WebApp请求
        # 该请求，对 debbug chat的窗口会使用
        if '/apps/' in request.path and '/conversations/messages' in request.path:
            return False
        
        # 3. 检查是否为会话相关的接口且session中有匿名用户ID
        try:
            if 'anonymous_user_id' in session and self._is_conversation_related_request(request):
                return True
        except Exception:
            # session可能未初始化，忽略错误
            pass
            
        return False
    
    def _handle_web_app_request(self, request: Request) -> Optional[Account]:
        """处理WebApp请求的认证逻辑"""
        # 1.确定token来源
        token = None
        
        # 如果是直接的WebApp接口，从URL中提取token
        if request.path.startswith('/web-apps/'):
            path_parts = request.path.split('/')
            if len(path_parts) >= 3:
                token = path_parts[2]  # /web-apps/<token>/...
        
        # 如果是基于session的间接请求，且有匿名用户ID
        elif 'anonymous_user_id' in session and self._is_conversation_related_request(request):
            # 对于会话相关的请求，需要检查会话对应的应用是否允许匿名访问
            return self._handle_conversation_request(request)
        
        if not token:
            return None
        
        try:
            # 2.获取WebApp应用信息
            app = self.web_app_service.get_web_app(token)
            
            # 3.如果应用允许匿名访问，返回匿名用户对象
            if app.allow_anonymous_access:
                return self._get_or_create_anonymous_user_account()
            
            # 4.如果不允许匿名访问，则进行正常的认证流程
            access_token = self._validate_credential(request)
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
            
        except Exception:
            # 5.如果获取应用信息失败，则要求认证
            access_token = self._validate_credential(request)
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
    
    def _get_or_create_anonymous_user_account(self):
        """获取或创建匿名用户Account对象"""
        # 从session中获取匿名用户ID，如果不存在则创建
        anonymous_user_id = session.get('anonymous_user_id')
        if not anonymous_user_id:
            # 生成标准UUID作为匿名用户ID
            anonymous_user_id = str(uuid.uuid4())
            session['anonymous_user_id'] = anonymous_user_id

        # 创建一个匿名用户Account对象（类似Account模型）
        class AnonymousAccount:
            def __init__(self, user_id):
                # 确保ID是UUID格式
                self.id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
                self.email = f"anonymous_{str(self.id)[:8]}@temp.com"
                self.name = f"匿名用户_{str(self.id)[:8]}"
                self.is_anonymous = True
                # 添加login_required装饰器需要的属性
                self.is_authenticated = True
                self.is_active = True

        return AnonymousAccount(anonymous_user_id)
    
    def _is_conversation_related_request(self, request: Request) -> bool:
        """检查是否为会话相关的请求"""
        # 检查路径是否匹配会话相关的接口
        return (request.path.startswith('/conversations/') or 
                '/conversations/' in request.path)
    
    def _handle_conversation_request(self, request: Request) -> Optional[Account]:
        """处理会话相关请求的认证逻辑"""
        # 从URL中提取conversation_id
        import re
        conversation_id_match = re.search(r'/conversations/([a-f0-9-]+)', request.path)
        if not conversation_id_match:
            return None
        
        conversation_id = conversation_id_match.group(1)
        
        try:
            # 查询会话对应的应用
            from internal.model.conversation import Conversation
            from internal.model.app import App
            
            conversation = Conversation.query.filter_by(id=conversation_id).first()
            if not conversation:
                return None
            
            app = App.query.filter_by(id=conversation.app_id).first()
            if not app:
                return None
            
            # 如果应用允许匿名访问，返回匿名用户对象
            if app.allow_anonymous_access:
                return self._get_or_create_anonymous_user_account()
            
            # 如果不允许匿名访问，要求正常认证
            access_token = self._validate_credential(request)
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
            
        except Exception:
            # 如果查询失败，要求正常认证
            access_token = self._validate_credential(request)
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)

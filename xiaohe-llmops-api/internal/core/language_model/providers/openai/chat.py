#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import get_buffer_string

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(ChatOpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    
    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        """
        重写token计算方法，提供fallback机制
        """
        try:
            # 先尝试调用父类的方法
            return super().get_num_tokens_from_messages(messages)
        except NotImplementedError:
            # 如果父类方法未实现，使用自定义计算方式
            return sum([self.get_num_tokens(get_buffer_string([m])) for m in messages])

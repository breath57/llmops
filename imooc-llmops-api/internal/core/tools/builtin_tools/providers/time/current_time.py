#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/7/19 20:46
@Author  : thezehui@gmail.com
@File    : current_time.py
"""
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from langchain_core.tools import BaseTool

from internal.lib.helper import add_attribute


class CurrentTimeInput(BaseModel):
    """获取当前时间工具的输入参数（无需参数）"""
    pass

class CurrentTimeTool(BaseTool):
    """一个用于获取当前时间的工具"""
    name: str = "current_time"
    description: str = "一个用于获取当前时间的工具，无需任何参数"

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """获取当前系统的时间并进行格式化后返回"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


@add_attribute("args_schema", CurrentTimeInput)
def current_time(**kwargs) -> BaseTool:
    """返回获取当前时间的LangChain工具"""
    return CurrentTimeTool()

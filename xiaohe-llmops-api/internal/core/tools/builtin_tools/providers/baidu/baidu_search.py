#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import requests

from internal.lib.helper import add_attribute


class BaiduSearchArgsSchema(BaseModel):
    query: str = Field(description="搜索查询内容，支持自然语言查询")


class BaiduSearchAPIWrapper(BaseModel):
    """百度AI搜索API包装器配置"""
    max_results: int = Field(description="最大搜索结果数", default=10)
    search_type: str = Field(description="搜索类型", default="web")
    edition: str = Field(description="搜索版本", default="standard")


class BaiduSearch(BaseTool):
    """百度AI搜索工具"""
    name: str = "baidusearch"
    description: str = "使用百度AI搜索获取实时网络信息，支持自然语言查询"
    api_wrapper: BaiduSearchAPIWrapper

    def _run(self, query: str) -> str:
        """执行百度AI搜索"""
        try:
            # 构建搜索请求
            search_url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
            headers = {
                "Content-Type": "application/json",
                "X-Appbuilder-Authorization": f"Bearer {os.getenv('BAIDU_BCE_API_KEY')}"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "user", 
                        "content": query
                    }
                ],
                "search_source": "baidusearch_v2",
                "resource_type_filter": [
                    {"type": self.api_wrapper.search_type, "top_k": self.api_wrapper.max_results}
                ],
                "edition": self.api_wrapper.edition
            }

            # 发送请求
            response = requests.post(search_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return self._format_search_result(result)
            else:
                error_info = response.json() if response.content else {"error": "未知错误"}
                return f"搜索失败：{error_info.get('message', '请求失败')} (状态码: {response.status_code})"
                
        except requests.exceptions.Timeout:
            return "搜索超时，请稍后重试"
        except requests.exceptions.RequestException as e:
            return f"网络请求错误：{str(e)}"
        except Exception as e:
            return f"搜索过程中发生错误：{str(e)}"

    def _format_search_result(self, result: Dict[str, Any]) -> str:
        """格式化搜索结果"""
        try:
            if "references" in result and len(result["references"]) > 0:
                references = result["references"]
                
                # 构建搜索结果摘要
                content = "**搜索结果：**\n\n"
                
                for i, ref in enumerate(references[:5], 1):  # 只显示前5个结果
                    title = ref.get("title", "无标题")
                    url = ref.get("url", "")
                    snippet = ref.get("content", "")
                    date = ref.get("date", "")
                    website = ref.get("website", "")
                    
                    content += f"{i}. **{title}**\n"
                    if snippet:
                        # 限制摘要长度
                        snippet = snippet[:200] + "..." if len(snippet) > 200 else snippet
                        content += f"   {snippet}\n"
                    if website:
                        content += f"   来源：{website}\n"
                    if url:
                        content += f"   链接：{url}\n"
                    if date:
                        content += f"   时间：{date}\n"
                    content += "\n"
                
                return content
            else:
                return "未找到相关搜索结果"
        except Exception as e:
            return f"格式化搜索结果时出错：{str(e)}"


@add_attribute("args_schema", BaiduSearchArgsSchema)
def baidusearch(**kwargs) -> BaseTool:
    """返回百度AI搜索的LangChain工具"""
    return BaiduSearch(api_wrapper=BaiduSearchAPIWrapper(**kwargs))

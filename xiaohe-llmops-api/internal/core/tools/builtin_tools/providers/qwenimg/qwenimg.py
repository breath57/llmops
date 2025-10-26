#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
import requests

from internal.lib.helper import add_attribute


class QwenImgArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示(prompt)")

class QwenImgAPIWrapper(BaseModel):
    size: str = Field(description="图片尺寸", default="1328x1328")
    seed: int = Field(description="随机种子", default=666)
    model: str = Field(description="模型名称", default="Qwen/Qwen-Image")

class QwenImg(BaseTool):
    name: str = "qwenimg"
    description: str = "一个用于生成图像的工具"
    api_wrapper: QwenImgAPIWrapper

    def _run(self, query: str) -> str:
        url = f'{os.getenv("OPENAI_API_BASE")}/images/generations'
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": query,
            **self.api_wrapper.model_dump()
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["images"][0]["url"]


@add_attribute("args_schema", QwenImgArgsSchema)
def qwenimg(**kwargs) -> BaseTool:
    """返回qwenimg绘图的LangChain工具"""
    return QwenImg(api_wrapper=QwenImgAPIWrapper(**kwargs))


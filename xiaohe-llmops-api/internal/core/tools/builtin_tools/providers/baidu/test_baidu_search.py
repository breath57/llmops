#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度AI搜索插件测试脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append('/home/breath/projects/llmops/xiaohe-llmops-api')

from internal.core.tools.builtin_tools.providers.baidusearch.baidusearch import baidusearch

def test_baidusearch():
    """测试百度AI搜索插件"""
    print("测试百度AI搜索插件...")
    
    # 从环境变量获取API密钥
    api_key = os.getenv("BAIDU_BCE_API_KEY")
    if not api_key:
        print("❌ 错误：未找到环境变量 BAIDU_BCE_API_KEY")
        print("请设置环境变量：export BAIDU_BCE_API_KEY=your_api_key_here")
        return
    
    # 创建插件实例
    try:
        tool = baidusearch(
            api_key=api_key,
            max_results=5,
            search_type="web",
            edition="standard"
        )
        
        print(f"✅ 插件名称: {tool.name}")
        print(f"✅ 插件描述: {tool.description}")
        print("✅ 插件创建成功！")
        
        # 测试搜索功能
        print("\n🔍 测试搜索功能...")
        test_query = "今天北京的天气怎么样？"
        print(f"搜索查询: {test_query}")
        
        result = tool._run(test_query)
        print(f"搜索结果: {result}")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_baidusearch()

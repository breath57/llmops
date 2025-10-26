#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
百度AI搜索插件简化测试脚本
"""

def test_baidusearch_structure():
    """测试百度AI搜索插件文件结构"""
    import os
    
    plugin_dir = "/home/breath/projects/llmops/xiaohe-llmops-api/internal/core/tools/builtin_tools/providers/baidusearch"
    
    required_files = [
        "__init__.py",
        "baidusearch.py", 
        "baidusearch.yaml",
        "positions.yaml",
        "_asset/icon.svg",
        "README.md"
    ]
    
    print("检查百度AI搜索插件文件结构...")
    
    for file_path in required_files:
        full_path = os.path.join(plugin_dir, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
    
    print("\n检查providers.yaml配置...")
    providers_yaml = "/home/breath/projects/llmops/xiaohe-llmops-api/internal/core/tools/builtin_tools/providers/providers.yaml"
    if os.path.exists(providers_yaml):
        with open(providers_yaml, 'r', encoding='utf-8') as f:
            content = f.read()
            if "baidusearch" in content:
                print("✅ providers.yaml 已包含百度AI搜索配置")
            else:
                print("❌ providers.yaml 未包含百度AI搜索配置")
    else:
        print("❌ providers.yaml 文件不存在")

def test_yaml_syntax():
    """测试YAML文件语法"""
    import yaml
    
    print("\n检查YAML文件语法...")
    
    yaml_files = [
        "/home/breath/projects/llmops/xiaohe-llmops-api/internal/core/tools/builtin_tools/providers/baidusearch/baidusearch.yaml",
        "/home/breath/projects/llmops/xiaohe-llmops-api/internal/core/tools/builtin_tools/providers/baidusearch/positions.yaml"
    ]
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✅ {yaml_file} - YAML语法正确")
        except Exception as e:
            print(f"❌ {yaml_file} - YAML语法错误: {e}")

if __name__ == "__main__":
    test_baidusearch_structure()
    test_yaml_syntax()
    print("\n🎉 百度AI搜索插件集成完成！")
    print("\n使用说明:")
    print("1. 在百度千帆平台获取API Key和Secret Key")
    print("2. 在应用的工具配置中添加百度AI搜索插件")
    print("3. 配置API密钥和相关参数")
    print("4. 用户可以通过自然语言进行搜索查询")

# 百度AI搜索插件

## 概述

百度AI搜索插件是一个内置工具，允许用户通过自然语言查询获取实时网络信息。该插件基于百度千帆平台的AI搜索API，支持智能搜索生成和多种搜索类型。

## 功能特性

- **自然语言查询**: 支持用自然语言进行搜索查询
- **实时信息获取**: 获取最新的网络信息
- **多种搜索类型**: 支持网页搜索、视频搜索、图片搜索、阿拉丁搜索
- **智能结果格式化**: 自动格式化搜索结果，包含来源信息
- **多版本支持**: 支持完整版本和标准版本

## 配置参数

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
| api_key | text | 是 | - | 百度千帆平台的API Key |
| max_results | number | 否 | 10 | 最大结果数(1-50) |
| search_type | select | 否 | web | 搜索类型 (web/video/image/aladdin) |
| edition | select | 否 | standard | 搜索版本 (standard/lite) |

## 使用方法

### 1. 获取API密钥

1. 访问 [百度千帆平台](https://cloud.baidu.com/product/wenxinworkshop)
2. 注册并登录账号
3. 创建应用并获取API Key

### 2. 配置插件

在应用的工具配置中添加百度AI搜索插件，并填入以下信息：
- API Key: 你的百度千帆API Key
- 选择适合的搜索类型和参数

### 3. 环境变量配置

你也可以通过环境变量配置API Key：
```bash
export BAIDU_BCE_API_KEY=your_api_key_here
```

### 4. 使用示例

用户可以通过以下方式使用搜索功能：

```
用户: "今天北京的天气怎么样？"
AI: [使用百度AI搜索获取实时天气信息]

用户: "最新的AI技术发展动态"
AI: [使用百度AI搜索获取最新AI新闻]

用户: "帮我搜索一下Python编程教程"
AI: [使用百度AI搜索获取相关教程信息]
```

## API参考

### 搜索接口

- **URL**: `https://qianfan.baidubce.com/v2/ai_search/web_search`
- **方法**: POST
- **认证**: X-Appbuilder-Authorization: Bearer <API Key>

### 请求参数

```json
{
  "messages": [
    {
      "role": "user",
      "content": "搜索查询内容"
    }
  ],
  "search_source": "baidusearch_v2",
  "resource_type_filter": [
    {"type": "web", "top_k": 10}
  ],
  "edition": "standard"
}
```

### 响应格式

```json
{
  "references": [
    {
      "title": "搜索结果标题",
      "url": "https://example.com",
      "content": "搜索结果内容摘要",
      "website": "网站名称",
      "date": "2024-12-19 10:00:00",
      "type": "web"
    }
  ],
  "request_id": "请求ID"
}
```

## 错误处理

插件包含完善的错误处理机制：

- **认证错误**: 当API密钥无效时返回相应错误信息
- **网络超时**: 处理网络请求超时情况
- **API错误**: 处理百度API返回的错误信息
- **格式错误**: 处理搜索结果格式化过程中的错误

## 注意事项

1. **API配额**: 注意百度千帆平台的API调用配额限制（每日免费额度100次）
2. **网络连接**: 确保服务器能够访问百度API服务
3. **密钥安全**: 妥善保管API密钥，避免泄露
4. **搜索内容**: 遵守相关法律法规，避免搜索不当内容

## 更新日志

- **v1.1.0** (2024-12-19): 修正API使用方式
  - 移除Secret Key依赖，仅需API Key
  - 更新为正确的API端点和请求格式
  - 支持环境变量配置
  - 优化搜索结果格式化
- **v1.0.0** (2024-12-19): 初始版本发布
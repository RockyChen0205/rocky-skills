# 工具使用指南

本指南详细介绍 DeepResearch 技能中使用的各个工具。

---

## 1. 网页搜索 - MiniMax MCP

### 工具信息
- **工具名**: `mcp__MiniMax__web_search`
- **用途**: 执行网络搜索，返回搜索结果摘要

### 使用方法

```bash
mcp__MiniMax__web_search --query "搜索查询内容"
```

### 参数说明
- `query`: 搜索查询字符串，支持中英文

### 返回结果
- 搜索结果列表，包含标题、链接、摘要等信息

### 示例

```bash
# 搜索 Python 机器学习教程
mcp__MiniMax__web_search --query "Python 机器学习教程"

# 搜索最新的 AI 研究论文
mcp__MiniMax__web_search --query "latest AI research papers 2025"
```

### 最佳实践
1. 搜索查询要具体明确
2. 可以使用引号进行精确匹配: `"exact phrase"`
3. 使用 site: 限定搜索范围: `site:github.com python`

---

## 2. 网页内容提取 - Jina Reader

### 工具信息
- **工具名**: WebFetch / 手动调用
- **用途**: 抓取任意网页内容，提取文本

### 使用方法

通过 WebFetch 工具访问：
```
URL: https://r.jina.ai/{目标URL}
```

例如，要提取 https://example.com 的内容：
```
URL: https://r.jina.ai/https://example.com
```

### 支持的功能
- 提取网页正文内容
- 去除广告和无关内容
- 支持 JavaScript 渲染的页面
- 返回 Markdown 格式

### 示例

```python
# 要提取的网页
url = "https://github.com/anthropics/claude-code"

# Jina Reader URL
jina_url = f"https://r.jina.ai/{url}"
```

### 注意事项
1. URL 需要完整编码
2. 某些网站可能阻止抓取
3. 大页面可能需要更长时间

---

## 3. 学术搜索 - Serper

### 工具信息
- **API**: Serper Scholar API
- **用途**: 搜索学术论文和研究资料

### 使用前提
需要配置 Serper API Key（免费开发额度）

### API 配置
参见 [API 配置说明](./api-setup.md#serper-学术搜索)

### 使用方法

配置完成后，可使用以下方式搜索：
1. 通过自定义工具调用 Serper API
2. 使用通用搜索并筛选学术结果

### 搜索技巧
- 使用关键词 + "paper" / "research" / "study"
- 使用 filetype:pdf 限定 PDF 文档
- 使用 site:arxiv.org 搜索预印本

---

## 4. 文件解析 - Dashscope

### 工具信息
- **API**: Dashscope 文件解析
- **用途**: 解析 PDF、Word、PPT 等文档

### 使用前提
需要注册 Dashscope 并获取 API Key（免费）

### 支持格式
- PDF
- Word (doc/docx)
- PowerPoint (ppt/pptx)
- Excel (xls/xlsx)
- 图片
- 音视频

### API 配置
参见 [API 配置说明](./api-setup.md#dashscope-文件解析)

### 使用方法

```python
from dashscope import FileParsing

# 解析文件
response = FileParsing.call(
    file_path='document.pdf',
    parsing_cfgs=[...]
)
```

---

## 5. 音视频分析 - Dashscope qwen-omni

### 工具信息
- **模型**: qwen-omni
- **用途**: 分析音视频内容，理解多模态信息

### 使用前提
需要 Dashscope API Key

### 功能
- 视频内容理解
- 音频转文字和分析
- 图片内容分析
- 多模态内容综合分析

### API 配置
参见 [API 配置说明](./api-setup.md#dashscope-音视频分析)

### 使用方法

```python
from dashscope import MultiModalConversation

# 分析图片
messages = [{
    'role': 'user',
    'content': [
        {'image': 'https://example.com/image.jpg'},
        {'text': '描述这张图片'}
    ]
}]

response = MultiModalConversation.call(
    model='qwen-omni',
    messages=messages
)
```

---

## 工具选择指南

| 场景 | 推荐工具 |
|------|----------|
| 快速信息检索 | MiniMax web_search |
| 深度内容分析 | Jina Reader + LLM |
| 学术论文搜索 | Serper / 通用搜索+筛选 |
| 文档内容提取 | Dashscope 文件解析 |
| 视频/音频分析 | Dashscope qwen-omni |

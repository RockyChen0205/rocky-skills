# API 配置说明

本文档详细介绍各 API 的申请和配置方法。

---

## 1. MiniMax MCP（已配置）

### 状态
✅ 已配置 - 可直接使用

### 使用方式
通过 MCP 服务器 `mcp__MiniMax__web_search` 直接使用

---

## 2. Jina Reader（无需配置）

### 状态
✅ 无需 API Key - 免费使用

### 使用方式
直接通过 URL 访问：`https://r.jina.ai/{目标URL}`

---

## 3. Serper 学术搜索

### 状态
✅ 已配置 - 可直接使用

### 免费额度
- 开发模式：$0/月
- 适合测试和开发

### 申请步骤

1. 访问 [Serper 官网](https://serper.dev)
2. 注册账户
3. 获取 API Key
4. 在环境中配置 `SERPER_KEY_ID`

### 配置方法

```bash
# 设置环境变量
export SERPER_KEY_ID="your-api-key"
```

### 使用示例

```python
import requests

url = "https://google.serper.dev/scholar"
payload = {"q": "machine learning"}
headers = {
    "X-API-KEY": "your-serper-api-key",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
```

---

## 4. Dashscope 文件解析

### 免费额度
- 免费注册
- 每月有一定免费调用额度

### 申请步骤

1. 访问 [Dashscope 官网](https://dashscope.aliyuncs.com)
2. 使用阿里云账号注册
3. 获取 API Key

### 配置方法

```bash
# 设置环境变量
export DASHSCOPE_API_KEY="your-api-key"
```

### Python 使用示例

```python
from dashscope import FileParsing

# 解析 PDF 文件
response = FileParsing.call(
    file_path='path/to/document.pdf'
)
print(response.output)
```

### 支持的功能
- 文档内容提取
- 结构化解析
- 表格提取
- 图片提取

---

## 5. Dashscope 音视频分析

### 免费额度
- 与文件解析共用免费额度

### 使用前提
需要 Dashscope API Key（见上文）

### Python 使用示例

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

# 分析视频
messages = [{
    'role': 'user',
    'content': [
        {'video': 'path/to/video.mp4'},
        {'text': '描述这个视频的内容'}
    ]
}]
```

### 可用模型
- `qwen-omni`: 多模态通才模型
- `qwen-vl-plus`: 视觉理解
- `qwen-audio`: 音频理解

---

## 环境变量配置汇总

将以下内容添加到 `.bashrc` 或 `.zshrc`:

```bash
# Serper（已配置）
export SERPER_KEY_ID="your-serper-api-key"

# Dashscope（如需要文件解析和音视频分析）
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

然后执行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

---

## API 状态检查

| API | 状态 | 配置方式 |
|-----|------|----------|
| MiniMax | ✅ 已配置 | MCP 服务器 |
| Jina Reader | ✅ 可用 | 无需配置 |
| Serper | ✅ 已配置 | 环境变量 |
| Dashscope | ⏳ 需申请 | 环境变量 |

---

## 常见问题

### Q: 这些 API 都是免费的吗？
A: Jina Reader 完全免费。MiniMax、Serper 开发模式免费。Dashscope 注册后有免费额度。

### Q: 需要全部配置吗？
A: 不需要。根据你的需求选择配置：
- 基础搜索：无需额外配置
- 学术搜索：配置 Serper
- 文件解析：配置 Dashscope
- 音视频分析：配置 Dashscope

### Q: API Key 安全吗？
A: 建议将 API Key 存储在环境变量中，不要硬编码在代码里。

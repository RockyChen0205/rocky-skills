---
name: fetch-skill
description: 统一的 URL 内容抓取工具。自动识别 URL 类型（普通网页 / X/Twitter / 微信公众号），路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。零依赖核心（Python stdlib），Camofox / WeSpy / wechat-article-exporter 为可选增强。使用场景：读取网页内容、提取推文、解析微信公众号文章、研究工作流。当用户说"抓取"、"fetch"、"读取URL"、"解析微信"、"获取推文"时使用此技能。
---

# fetch-skill

统一的 URL 内容抓取工具。自动识别 URL 类型，路由到最佳后端，输出干净的 Markdown / JSON / 纯文本。

## 能力矩阵

| URL 类型 | 后端 | 依赖 |
|---|---|---|
| 普通网页 | Jina Reader → defuddle.md → markdown.new → Raw | 无 |
| X/Twitter 单条推文 | FxTwitter API | 无（零依赖）|
| X/Twitter 回复 | Camofox + Nitter | Camofox（本地 9377）|
| X/Twitter 用户时间线 | Camofox + Nitter | Camofox |
| X Article（长文）| Camofox → Jina 兜底 | 推荐 Camofox |
| 微信公众号文章 | WeSpy → wechat-article-exporter → Jina → defuddle | 可选 WeSpy/API |

## 脚本位置

`~/.codex/skills/fetch-skill/fetch.py`

## 使用方法

```bash
# 抓取任意网页
python3 ~/.codex/skills/fetch-skill/fetch.py https://example.com

# 保存到文件
python3 ~/.codex/skills/fetch-skill/fetch.py https://example.com -o output.md

# 静默抓取
python3 ~/.codex/skills/fetch-skill/fetch.py https://example.com -q

# 纯文本输出
python3 ~/.codex/skills/fetch-skill/fetch.py https://example.com -t
```

### X / Twitter

```bash
# 单条推文（无需登录）
python3 ~/.codex/skills/fetch-skill/fetch.py https://x.com/OpenAI/status/123456 -t

# 推文 JSON
python3 ~/.codex/skills/fetch-skill/fetch.py https://x.com/OpenAI/status/123456 --pretty

# 推文 + 回复（需要 Camofox）
python3 ~/.codex/skills/fetch-skill/fetch.py https://x.com/OpenAI/status/123456 --replies -t
```

### 微信公众号

```bash
# 默认（Jina 兜底）
python3 ~/.codex/skills/fetch-skill/fetch.py "https://mp.weixin.qq.com/s/xxxx"

# 使用 wechat-article-exporter
python3 ~/.codex/skills/fetch-skill/fetch.py "https://mp.weixin.qq.com/s/xxxx" --wechat-api http://localhost:3000
```

## 命令行选项

```
python3 fetch.py [url] [选项]

通用:
  -o, --output FILE      保存到文件
  -m, --mode auto|web|twitter|wechat   强制模式（默认 auto）
  --timeout N            HTTP 超时秒数（默认 30）
  -q, --quiet            不输出进度

网页:
  --no-jina              跳过 Jina Reader

X/Twitter:
  -r, --replies          抓取回复（需 Camofox）
  --user USERNAME        抓取用户时间线（需 Camofox）
  --limit N              时间线最大条数（默认 50）
  --pretty               JSON 缩进输出
  -t, --text-only        人类可读输出
  --port PORT            Camofox 端口（默认 9377）

微信:
  --wechat-api URL       wechat-article-exporter API 地址
```

## 回退链

### 普通网页
```
Jina Reader → defuddle.md → markdown.new → Raw HTML
```

### 微信公众号
```
WeSpy → wechat-article-exporter → Jina → defuddle → Raw HTML
```

### 单条推文
```
FxTwitter /{user}/status/{id} → FxTwitter /status/{id} → Jina
```

进度和错误 → **stderr**，内容 → **stdout**。

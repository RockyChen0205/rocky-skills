---
name: paper-index-generator
description: 为指定目录生成/更新 paper-index.yaml 索引文件，自动从论文笔记中提取元信息并生成结构化索引
---

# Paper Index Generator

> 为指定目录生成/更新 paper-index.yaml 索引文件

## 触发条件

当用户提到：
- "生成 paper index"
- "更新 paper 索引"
- "为 xxx 目录生成索引"
- "/paper-index-generator"

## 使用方式

```bash
/paper-index-generator [目录路径]
```

例如：
- `/paper-index-generator 03-Papers/02-understanding&reasoning/understanding-video/`
- `/paper-index-generator 03-Papers/`

## 索引格式

每个条目包含 9 个字段：

```yaml
- id: video-thinker-2025
  title: "Video-Thinker: Sparking Thinking with Videos via RL"
  arxiv: "2510.23473"
  date: "2025.10"
  team: "Southeast University, Monash University, Xiaohongshu"
  year: 2025
  core_contribution: 提出Video-Thinker框架，通过SFT+GRPO训练使MLLMs能够自主利用内在的grounding和captioning能力生成推理线索，无需构建外部工具即可实现高效视频推理，在Video-Holmes等基准上达到SOTA
  task_type: [video_reasoning, chain_of_thought]
  method_type: [reinforcement_learning, grpo]
  tech_highlights: [grounding, captioning, intrinsic_tool]
```

### 字段说明

| 字段 | 说明 |
|------|------|
| id | 唯一标识，标题缩写 + 年份 |
| title | 论文标题（精简版） |
| arxiv | arXiv ID（可选） |
| date | 发表年月 |
| team | 团队（精简版，保留主要机构） |
| year | 年份数字 |
| core_contribution | **一句话详细描述**（50-80字）：方法名称 + 核心机制 + 创新点 + 效果/应用 |
| task_type | 任务类型列表（3-5个关键词） |
| method_type | 方法类型列表（3-5个关键词） |
| tech_highlights | 技术亮点列表（3-5个关键词） |

### core_contribution 写作规范

**必须是一句话，包含以下要素：**
1. **方法名称** - 提出的框架/模型名称
2. **核心机制** - 具体的技术手段
3. **创新点** - 相比前人工作的突破
4. **效果/应用** - 在什么场景下达到什么效果

**示例：**
```yaml
# 好例子
提出Video-Thinker框架，通过SFT+GRPO训练使MLLMs能够自主利用内在的grounding和captioning能力生成推理线索，无需构建外部工具即可实现高效视频推理，在Video-Holmes等基准上达到SOTA

# 坏例子（太短，没区分度）
内在整合grounding和captioning到思维链推理
```

### note_path 推断规则

**不存储 note_path**，通过目录结构推断：
- `paper-index.yaml` 所在目录 + `{id}.md`
- 例如：`understanding-video/paper-index.yaml` 中的 `video-thinker-2025`
- → 对应 `understanding-video/video-thinker-2025.md`

## 执行流程

### 1. 接收目录路径
- 将相对路径转换为绝对路径
- 验证目录存在

### 2. 发现论文文件
- 遍历目录中的 `.md` 文件
- 过滤掉包含 `summary`、`总结`、`_summary.md` 的文件

### 3. 并行提取信息（使用 Subagent）
- 启动多个 subagent 并行读取 md 文件
- 每个 subagent 提取：
  - frontmatter（发表年月、团队）
  - 从内容推断：core_contribution、task_type、method_type、tech_highlights
- 汇总结果

### 4. 生成索引
- 精简标题（去掉冗余信息）
- 生成 id（标题缩写 + 年份）
- **撰写详细的 core_contribution（一句话，50-80字）**
- 提取关键词到 task_type、method_type、tech_highlights
- 按年份降序排序

## Token 优化

| 字段 | 状态 | 原因 |
|------|------|------|
| id, title, arxiv, date, team, year | ✅ 保留 | 核心元信息 |
| core_contribution | ✅ 保留（详细版） | 区分度的关键 |
| task_type, method_type, tech_highlights | ✅ 保留（列表形式） | 便于分类和检索 |
| note_path | ❌ 去掉 | 通过目录推断 |
| benchmarks | ❌ 去掉 | 太占token |
| applicable_scenarios | ❌ 去掉 | 可从 core_contribution 推断 |

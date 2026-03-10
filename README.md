<p align="center">
  <img src="./assets/rocky-skills-banner.png" alt="rocky-skills banner" />
</p>

<h1 align="center">rocky-skills</h1>

<p align="center">This repository is a collection of skills I use in my regular workflow.</p>

## Structure

- `academic/`: skills for academic writing, paper analysis, citation grounding, and related research tasks.

## 如何安装

你可以直接给你的 AI agent (Claude Code / Codex / opencode / ...) 发送以下 prompt 来安装本项目中的所有 skills：

```
你好，我需要你帮我安装 rocky-skills 项目中的所有 skills。
项目地址：https://github.com/RockyChen0205/rocky-skills.git
请将项目中的每个 skill 复制到你的 skills 目录下（每个 skill 复制到对应的子目录），并确保它们可以被正确加载。
```

## Included Skills

### [paper-citation-grounder](./academic/paper-citation-grounder/)
在论文中查找、验证、放置并可选地写入可靠的引用，同时避免虚构引用和引用聚类。

**输入**: 论文草稿（Markdown/LaTeX）、待验证的引用声明  
**输出**: 经过验证的引用、引用位置建议、引用报告

### [Humanizer-zh](./academic/Humanizer-zh/) ([原始仓库](https://github.com/op7418/Humanizer-zh))
中文版 AI 写作去痕工具，基于维基百科 "Signs of AI writing" 指南，帮助将 AI 生成的内容改写得更自然、更像人类书写。

**输入**: AI 生成的中文文本  
**输出**: 去除 AI 痕迹后的自然中文文本

### [humanizer](./academic/humanizer/) ([原始仓库](https://github.com/blader/humanizer))
英文版 AI 写作去痕工具，基于维基百科 "Signs of AI writing" 指南，移除文本中的 AI 生成痕迹。

**输入**: AI 生成的英文文本  
**输出**: 去除 AI 痕迹后的自然英文文本

### [baoyu-translate](./academic/baoyu-translate/) ([原始仓库](https://github.com/JimLiu/baoyu-skills))
多模式翻译技能，支持快速/标准/精修三种模式，可自定义翻译风格（叙事/正式/技术/学术/商务等），支持长文分块翻译和术语表一致性。

**输入**: 源语言文本、目标语言、翻译模式（quick/normal/refined）、术语表（可选）  
**输出**: 翻译后的目标语言文本、术语一致性检查报告

### [arxiv-latex-to-knowledge-base](./academic/arxiv-latex-to-knowledge-base/)
将 arXiv 论文转换为完整的知识库文档集合，包含英文 Markdown（直接从 LaTeX 转换）和中文总结笔记（按模板生成结构化总结），自动下载源码、提取图片、生成可直接阅读的笔记。

**输入**: arXiv 论文 URL 或论文 ID  
**输出**: 
- 英文 Markdown（从 LaTeX 直接转换）
- 中文总结笔记（按模板结构化）
- 原始 PDF 文件
- 提取的图片

### [ml-paper-writing](./academic/ml-paper-writing/) ([原始仓库](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/20-ml-paper-writing))
为 NeurIPS、ICML、ICLR、ACL、AAAI、COLM 等顶级会议撰写 publication-ready 的 ML/AI 论文。包含 LaTeX 模板、引用验证工作流以及来自顶级研究者的写作最佳实践。

**输入**: 研究代码仓库、实验结果、初步草稿（可选）  
**输出**: 
- 完整的论文草稿（LaTeX/Markdown）
- 经过验证的引用列表（BibTeX）
- 符合会议格式的提交文件

### [ljg-xray-paper](./academic/ljg-xray-paper/) ([原始仓库](https://github.com/lijigang/ljg-skill-xray-paper)) ⚠️ 已修改
像 X 光机一样解构学术论文，穿透学术黑话，提取核心贡献、关键假设和"餐巾纸公式"级别的洞察。生成结构化分析报告和 ASCII 逻辑图。

**修改说明**: 对原始 skill 进行了以下修改：
- 文件名格式改为 `{论文完整标题}_xray-read.md`
- 保存路径由用户指定（不再固定到 ~/Documents/notes/）
- 移除了自动生成后自动打开文件的步骤

**输入**: 论文 PDF 路径、文本内容或论文链接
**输出**:
- Markdown 分析报告（文件名：`{论文标题}_xray-read.md`）
- 包含：核心痛点、解题机制、创新增量、批判性边界、ASCII 逻辑图、餐巾纸公式

### [peer-review](./academic/peer-review/)
系统性同行评审工具包。评估方法论、统计方法、研究设计、可复现性、伦理规范、图表完整性、报告标准。支持跨学科手稿和基金申请的评审。

**输入**: 待评审的论文手稿、基金申请或研究提案
**输出**: 结构化评审意见、改进建议、评分表

### [arxiv-search](./academic/arxiv-search/)
搜索 arXiv 预印本数据库，获取物理学、数学、计算机科学、量化生物学、量化金融、统计学等领域的最新研究成果。在论文正式发表前获取最新研究动态。

**输入**: 搜索关键词（如 "neural networks protein structure"、"single cell RNA-seq"）
**输出**: 相关论文列表，包含标题、摘要、作者、arXiv ID 等信息

## Attribution

- **Humanizer-zh**: [op7418](https://github.com/op7418)
- **humanizer**: [blader](https://github.com/blader)  
- **baoyu-translate**: [JimLiu](https://github.com/JimLiu)
- **ml-paper-writing**: [Orchestra Research](https://github.com/Orchestra-Research)
- **ljg-xray-paper**: [lijigang](https://github.com/lijigang) (modified by RockyChen0205)

Other skills are custom implementations.

## 使用说明

这些 skills（如 `/humanizer-zh`、`/baoyu-translate`、`/ljg-xray-paper` 等）只是给到一个思考框架，要做到对自己好用，需要你和 agent 一起打磨调教。每个 skill 的默认行为可能不完全符合你的个人工作流，建议：

1. 先试用几次，观察输出是否符合预期
2. 根据实际使用情况调整 prompt 和参数
3. 添加个人偏好的约束和风格要求
4. 逐步形成适合自己的定制化版本

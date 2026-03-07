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

- `academic/paper-citation-grounder`: find, verify, place, and optionally write back trustworthy citations into a paper while avoiding fabricated references and citation clustering.
- `academic/Humanizer-zh` (https://github.com/op7418/Humanizer-zh): 中文版 AI 写作去痕工具，基于维基百科 "Signs of AI writing" 指南，帮助将 AI 生成的内容改写得更自然、更像人类书写。
- `academic/humanizer` (https://github.com/blader/humanizer): 英文版 AI 写作去痕工具，基于维基百科 "Signs of AI writing" 指南，移除文本中的 AI 生成痕迹。
- `academic/baoyu-translate` (https://github.com/JimLiu/baoyu-skills): 多模式翻译技能，支持快速/标准/精修三种模式，可自定义翻译风格（叙事/正式/技术/学术/商务等），支持长文分块翻译和术语表一致性。
- `academic/arxiv-latex-to-knowledge-base`: 将 arXiv 论文转换为完整的知识库文档集合，包含英文 Markdown（直接从 LaTeX 转换）和中文总结笔记（按模板生成结构化总结），自动下载源码、提取图片、生成可直接阅读的笔记。

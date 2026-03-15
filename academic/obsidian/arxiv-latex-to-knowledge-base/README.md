# arXiv LaTeX 转知识库

将 arXiv 论文转换为完整的知识库文档集合，包含英文 Markdown 和中文总结笔记。

## 安装依赖

```bash
# 安装 poppler（PDF 转图片需要）
brew install poppler

# 安装 Python 库
pip3 install pdf2image pillow
```

## 使用方法

在 Claude Code 中，使用以下方式调用：

```
/arxiv-latex-to-knowledge-base
```

然后提供 arXiv ID 或链接，例如 `2506.10821` 或 `https://arxiv.org/abs/2506.10821`。

## 工作流程

1. **下载源码** - 从 arXiv 下载 LaTeX 源码
2. **下载 PDF** - 保存原始 PDF 文件
3. **图片处理** - PDF → 300 DPI PNG，裁剪白边
4. **生成英文 Markdown** - LaTeX 转英文 Markdown（不翻译）
5. **生成中文笔记** - 按模板生成结构化总结笔记

## 输出

```
Papers/
├── {论文标题}.md           # 英文原文 Markdown
├── {论文标题}_summary.md   # 中文总结笔记
└── {论文标题}.pdf          # 原始 PDF

图片集/
├── model.png
└── ...
```

## 示例

```
/arxiv-latex-to-knowledge-base
arXiv ID: 2506.10821
```

将生成：
- `Papers/Think_With_Videos_For_Agentic_Long-Video_Understanding.md`
- `Papers/Think_With_Videos_For_Agentic_Long-Video_Understanding_summary.md`
- `Papers/Think_With_Videos_For_Agentic_Long-Video_Understanding.pdf`
- `图片集/model.png`, `case_study.png` 等

## 总结笔记结构

按照 `Prompts/paper_summary.md` 模板生成，包含：
- Abstract 对齐阅读
- Intro 叙事主线与贡献地图
- Proposed Method 详细讲解
- Experiments 分析
- 复现指南与踩坑清单

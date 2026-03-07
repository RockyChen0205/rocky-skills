---
name: arxiv-latex-to-knowledge-base
description: 将 arXiv 论文转换为完整的知识库文档集合。生成三份文档：(1) LaTeX 转英文 Markdown，(2) 按指定模板生成中文总结笔记，(3) 原始 PDF 文件。
---

# arXiv LaTeX 转知识库

将 arXiv 论文转换为完整的知识库，包含**英文原文 Markdown**（直接转换自 LaTeX 源码）和中文总结笔记。

## ⚠️ 核心原则：原文转换，而非总结

**这是最关键的要求**：生成的英文 Markdown 必须是 **LaTeX 源码的直接转换**，每一句话、每一个公式、每一个表格数据都必须是原文搬运，**绝对不能是你总结或改写后的概要**。

- ❌ 禁止：用自己的话概括原文内容
- ❌ 禁止：省略细节或简化表述
- ✅ 必须：逐字逐句转换 LaTeX 源码为 Markdown
- ✅ 必须：保留所有公式、符号、编号
- ✅ 必须：保留所有表格的原始数据

## 使用场景

当用户提供 arXiv ID 或论文链接，需要生成完整的论文知识库文档时使用此技能。

## 输入

- arXiv ID（如 `2506.10821`）
- 或 arXiv URL（如 `https://arxiv.org/abs/2506.10821`）
- **输出目录**：由用户指定（笔记保存的目录，相对于 Obsidian Vault 根目录）
  - 例如：`Papers/arxiv`、`Research/Papers` 等（相对路径，相对于 Vault 根目录）

## 输出文档

| 文档 | 说明 | 保存位置 |
|-----|-----|---------|
| 英文 Markdown | LaTeX 源码转英文 Markdown，保留公式和图片 | `{用户指定目录}/{论文标题}.md` |
| 中文总结笔记 | 按 paper_summary.md 模板生成的分析笔记 | `{用户指定目录}/{论文标题}_summary.md` |
| 原始 PDF | 论文原始 PDF 文件 | `{用户指定目录}/{论文标题}.pdf` |

**图片存储**：所有图片存储在 Vault 根目录的 `assets/{论文标题}/` 目录中

## 核心工作流

### 1. 下载并解压 LaTeX 源码

```bash
curl -L -o {arxiv_id}.tar.gz "https://arxiv.org/e-print/{arxiv_id}"
tar -xzf {arxiv_id}.tar.gz
```

### 2. 下载原始 PDF

```bash
# 先下载到临时名称
curl -L -o {arxiv_id}.pdf "https://arxiv.org/pdf/{arxiv_id}.pdf"

# 从 LaTeX 源码或 arXiv 页面提取论文标题，然后重命名 PDF
mv {arxiv_id}.pdf "{论文标题}.pdf"
```

### 3. 图片处理（使用 2 个并行 subagent）

**⚠️ 必须执行的自检流程：**

启动 2 个并行 subagent 处理图片任务：

| Subagent | 任务 |
|----------|------|
| **图片提取 agent** | ① 扫描 LaTeX 源码中的 `\includegraphics{}` 引用<br>② 查找图片文件（常见目录：`Figs/`, `figures/`, `images/`, `./`）<br>③ 复制图片到 `assets/{论文标题}/` 目录 |
| **路径更新 agent** | ① 更新 Markdown 中的图片引用路径<br>② 将 `![[图片集/论文名/图片名.png]]` 转换为 `![[assets/论文名/图片名.png]]` |

**主 agent 只需下达指令**：
> "请并行启动 2 个 subagent：（1）图片提取 agent，负责扫描 LaTeX 源码查找图片引用，复制图片到 assets/{论文标题}/ 目录；（2）路径更新 agent，负责更新 Markdown 中的图片引用路径。"

---

### 3.1 矢量图（PDF）转换为 PNG

**为什么需要转换**：Obsidian 原生不支持直接嵌入 PDF 文件作为图片，需要将矢量图（PDF）转换为 PNG 格式才能在 Markdown 中正常显示。

#### 转换命令

```bash
# 安装依赖
brew install poppler

# PDF 转 PNG（300 DPI，推荐用于清晰显示）
pdftoppm -r 300 -png input.pdf output

# 批量转换时注意去除 -1 后缀
# 单页 PDF 转换后文件名会带 -1 后缀，需要重命名
# 例如：output-1.png -> output.png
```

#### 使用方法

1. 查找 LaTeX 源码中引用为 PDF 格式的图片（通常是矢量图）
2. 使用 `pdftoppm` 将 PDF 转换为 PNG
3. 如果转换后文件名带有 `-1` 后缀，需要重命名去除后缀
4. 将转换后的 PNG 图片复制到 `assets/{论文标题}/` 目录
5. 更新 Markdown 中的图片引用路径

#### 注意事项

- 推荐使用 300 DPI 以保证在 Obsidian 中显示清晰
- 如果是多页 PDF，每页会生成一个 PNG 文件，需要注意页码对应
- 转换后的 PNG 文件可能带有白边，可以使用图像处理工具裁剪

### 4. LaTeX 转英文 Markdown（关键步骤）

**必须严格按照原文转换**：
- 使用多个 subagent 并行处理（不翻译）：
  - 摘要和引言
  - 相关工作
  - 方法论
  - 实验部分
  - 附录

**每个 subagent 的任务指令必须明确强调**：
> "你是一个精确的 LaTeX 到 Markdown 转换器。你的任务是将 LaTeX 源码直接转换为 Markdown 格式，**每一句话都必须来自原文**，绝对不能添加自己的解释、总结或改写。保留所有公式、图表编号、脚注、引用。"

### 4.1 完整性检查（使用 5 个并行 subagent）

在完成 LaTeX 到 Markdown 的转换后，启动 **5 个并行 subagent** 逐一核对以下项目：

| Subagent | 检查内容 |
|----------|---------|
| **章节完整性检查** | 检查 `\section{}`、`\subsection{}`、`\appendix`、致谢部分是否完整 |
| **公式完整性检查** | 统计 equation 块数量，检查 `\tag{}`、行内公式 `$..$`、多行公式 |
| **表格完整性检查** | 统计 table/tabular 数量，检查表头、列对齐、跨列跨行 |
| **图片完整性检查** ⚠️ | 检查 `\includegraphics{}` 引用、图片文件存在、引用路径更新 |
| **引用与脚注检查** | 检查 `\cite{}`、`\footnote{}`、参考文献列表 |

**每个 subagent 的任务**：
- 接收：LaTeX 源码路径 + 已生成的 Markdown 路径
- 执行：按照检查清单核对
- 返回：「通过」或「缺失 XXX」

**主 agent 汇总结果后，如有缺失，统一补全。**

#### 4.1.1 章节完整性检查
- [ ] 检查 LaTeX 源码中所有的 `\section{}` 和 `\subsection{}`
- [ ] 检查是否所有章节都有对应的 Markdown 标题
- [ ] 检查是否有 `\appendix` 后的附录章节
- [ ] 检查是否有 `\acknowledgements` 或致谢部分

#### 4.1.2 公式完整性检查
- [ ] 统计 LaTeX 源码中 `\begin{equation}` 和 `\end{equation}` 的数量
- [ ] 统计 Markdown 中 equation 块的数量
- [ ] 检查所有编号的公式（如 `\tag{1}`）是否都保留
- [ ] 检查行内公式 `$...$` 是否都保留
- [ ] 检查多行公式 `align` 环境是否完整

#### 4.1.3 表格完整性检查
- [ ] 统计 LaTeX 源码中 `\begin{table}` 和 `\begin{tabular}` 的数量
- [ ] 检查每个表格的表头、列对齐、单元格内容是否完整
- [ ] 检查表格的 caption 和 label 是否保留
- [ ] 检查跨列/跨行命令 `\ multicolumn` / `\ multirow` 是否正确转换

#### 4.1.4 图片完整性检查 ⚠️
- [ ] **必须检查**：LaTeX 源码中 `\includegraphics{}` 引用的所有图片文件是否存在
- [ ] **必须执行**：将图片移动到 `assets/{论文标题}/` 目录
- [ ] **必须执行**：更新 Markdown 中的图片引用路径为 `![[assets/{论文标题}/xxx.png|说明]]`
- [ ] 检查每个 figure 的 caption 是否完整
- [ ] 检查子图（subfigures）是否都包含

#### 4.1.5 引用与脚注检查
- [ ] 检查所有 `\cite{}` 引用是否保留
- [ ] 检查脚注 `\footnote{}` 是否转换
- [ ] 检查参考文献列表是否完整

#### 4.1.6 算法与环境检查
- [ ] 检查 `\begin{algorithm}` 或 `algorithm2e` 环境
- [ ] 检查伪代码是否完整保留
- [ ] 检查代码块是否正确转换

### 5. Markdown 格式规范

#### 5.1 图片链接

Obsidian 使用 `[[]]` 语法嵌入图片（相对于 `assets/` 目录）：

```markdown
![[assets/论文名/图片名.png|说明]]
```

例如：`![[assets/OLMoE/overview.png|模型性能对比示意图]]`

**注意**：必须是 `[[]]`（感叹号 + 双方括号），单独的 `[[]]` 或 `![]()` 都无法正确显示图片。

#### 5.2 论文元信息（使用 YAML Frontmatter）

```yaml
---
title: OmniVideo-R1: Reinforcing Audio-visual Reasoning
date: 2026-02
authors: Zhangquan Chen, et al.
arXiv: 2602.05847
code: https://github.com/...
---
```

#### 5.3 表格格式
```markdown
| Model | Parameters | Accuracy |
|-------|-----------|----------|
| VideoExplorer | 7B | **55.4** |
```

### 6. 生成中文总结笔记

按照模板生成结构化总结：

#### 6.1 总结笔记结构
```yaml
---
发表年月: "2026.02"
团队: "..."
---
```

### 7. 输出文件结构

```
Obsidian Vault/
├── {用户指定目录}/
│   ├── {论文标题}.md           # 英文原文
│   ├── {论文标题}_summary.md   # 中文总结笔记
│   └── {论文标题}.pdf          # 原始 PDF
└── assets/
    └── {论文标题}/
        ├── model.png
        ├── data_generation.png
        └── ...
```

图片在 Markdown 中引用格式：`![[assets/{论文标题}/xxx.png|说明]]`

### 8. 清理临时文件

```bash
# 删除 arXiv 下载的压缩包
rm -rf {arxiv_id}.tar.gz

# 删除所有 LaTeX 源码相关文件
rm -rf *.tex *.sty *.bbl *.bst *.bib
rm -rf images/ Figs/ figures/ data/
rm -rf texmf/ latex/
rm -rf {arxiv_id}/  # 删除解压后的源码目录

# 删除 PDF 临时转换文件（如有）
rm -rf *.png  # 仅保留 assets 目录中的图片

# 注意：PDF 已重命名为论文标题，保存在目标目录中
```

### 9. 添加 DailyNote 引用

在 `DailyNote/{YYYY-MM-DD}.md` 中添加论文引用：

```markdown
## 论文阅读
- [[{用户指定目录}/{论文标题}.md]] - {论文标题}
```

## 关键依赖

| 工具 | 安装方式 |
|-----|---------|
| poppler | `brew install poppler` |
| pdf2image | `pip3 install pdf2image` |
| PIL (Pillow) | `pip3 install pillow` |

## 质量检查清单

### 英文 Markdown（原文转换验证）

⚠️ **在提交前，你必须对照原始 LaTeX 源码逐一核对以下所有项目**：

#### 章节完整性 对照 `\section
- [ ]{}` 列表，检查每个章节标题都存在
- [ ] 对照 `\subsection{}` 列表，检查每个子章节标题都存在
- [ ] 确认没有跳过任何小节
- [ ] 确认 appendix（附录）部分完整
- [ ] 确认 acknowledgements（致谢）部分完整

#### 公式完整性
- [ ] 统计 LaTeX 中 equation 环境数量 = Markdown 中 equation 块数量
- [ ] 检查所有带编号公式 `\tag{}` 保留
- [ ] 检查行内公式 `$...$` 保留
- [ ] 检查多行公式 align/eqnarray 完整

#### 表格完整性
- [ ] 统计 LaTeX 中 table/tabular 数量 = Markdown 中表格数量
- [ ] 确认每个表格的表头、分割线、数据行完整
- [ ] 确认跨列/跨行正确保留

#### 图片完整性 ⚠️ 必须检查
- [ ] **执行**：统计 LaTeX 中 `\includegraphics{}` 引用数量
- [ ] **执行**：确认所有引用的图片文件都已复制到 assets 目录
- [ ] **执行**：更新 Markdown 中图片引用路径
- [ ] 确认每个图片的 caption 完整
- [ ] 确认所有图片文件都已提取并转换
- [ ] **PDF 转 PNG 检查**：确认矢量图（PDF）已转换为 PNG 格式
- [ ] **PDF 转 PNG 检查**：确认转换后的 PNG 文件已移动到 assets 目录
- [ ] **PDF 转 PNG 检查**：确认去除了 -1 后缀（如有）
- [ ] **PDF 转 PNG 检查**：确认 PNG 分辨率为 300 DPI 或更高

#### 引用与脚注
- [ ] 确认所有 `\cite{}` 保留
- [ ] 确认脚注 `\footnote{}` 转换
- [ ] 确认参考文献列表完整

### 中文总结笔记
- [ ] YAML 元信息完整
- [ ] 摘要原文 + 翻译对齐
- [ ] 贡献地图表格完整
- [ ] 公式逐符号解释
- [ ] 至少 5 条实验 insight
- [ ] 至少 5 条踩坑点

### 整体
- [ ] PDF 文件下载成功
- [ ] 临时文件已清理
- [ ] PNG 文件无多余白边
- [ ] **图片已移动到 assets 目录**
- [ ] **图片引用路径已更新**
- [ ] **DailyNote 已添加引用**

## 执行顺序

1. 解析 arXiv ID
2. 下载 LaTeX 源码
3. 下载原始 PDF 并重命名为论文标题
4. 分析文件结构（列出所有 .tex 文件）
5. **【并行】图片处理**：启动 2 个 subagent 并行处理
   - 图片提取 agent：扫描引用、复制图片
   - 路径更新 agent：更新 Markdown 引用路径
5.1 **PDF 转 PNG**：将矢量图（PDF）转换为 PNG 格式
   - 查找 LaTeX 中引用的 PDF 图片
   - 使用 pdftoppm 转换为 PNG
   - 去除 -1 后缀并移动到 assets 目录
6. **【并行】LaTeX → Markdown**：启动 5 并行处理不同+ 个 subagent章节
7. **【并行】完整性检查**：启动 5 个 subagent 并行核对
   - 章节完整性检查
   - 公式完整性检查
   - 表格完整性检查
   - 图片完整性检查
   - 引用与脚注检查
8. 整合 Markdown 内容（如有缺失则补全）
9. 生成中文总结笔记
10. 移动所有文件到用户指定的目标目录
11. **添加 DailyNote 引用**
12. 清理临时文件

## ⚠️ 完整性检查执行指南

在执行顺序第 7 步中，使用 **5 个并行 subagent** 进行完整性检查：

### 并行检查流程

```
┌─────────────────────────────────────┐
│         主 Agent (汇总结果)           │
├─────────┬─────────┬─────────┬───────┤
│章节检查  │ 公式检查 │ 表格检查 │图片检查│ ← 并行执行
│ subagent│ subagent│ subagent│ sub...│
│         │         │         │引用检查│
└─────────┴─────────┴─────────┴───────┘
```

### 每个 subagent 的任务

1. **章节完整性检查 agent**
   - 统计 LaTeX 源码中 `\section{`、`\subsection{` 数量
   - 统计 Markdown 中 `## `、`### ` 数量
   - 检查 appendix、acknowledgements 是否存在

2. **公式完整性检查 agent**
   - 统计 LaTeX 中 `\begin{equation}` 数量
   - 统计 Markdown 中 `$$` 或 equation 块数量
   - 检查 `\tag{}`、行内公式 `$..$` 是否保留

3. **表格完整性检查 agent**
   - 统计 LaTeX 中 `\begin{table}`、`\begin{tabular}` 数量
   - 统计 Markdown 中表格数量
   - 检查跨列/跨行是否正确

4. **图片完整性检查 agent** ⚠️
   - 统计 LaTeX 中 `\includegraphics{}` 引用数量
   - 确认图片文件存在于 assets 目录
   - 确认 Markdown 中引用路径已更新

5. **引用与脚注检查 agent**
   - 统计 LaTeX 中 `\cite{` 数量
   - 统计 Markdown 中 `[@` 数量
   - 检查 `\footnote{}` 是否转换

### 执行步骤

1. **读取所有 .tex 文件**：在启动 subagent 前，先列出并浏览所有 LaTeX 源文件
2. **统计关键元素数量**：用 Grep 统计各类元素出现次数
3. **启动并行 subagent**：同时启动 5 个检查 agent
4. **汇总结果**：主 agent 收集所有检查结果
5. **查漏补缺**：如有缺失，统一补全

## ⚠️ 图片处理自检清单

**每次转换必须执行以下检查：**

- [ ] 使用 `grep -r "\\includegraphics" *.tex` 查找所有图片引用
- [ ] 确认引用的图片文件存在于本地目录
- [ ] 执行 `mkdir -p "assets/{论文标题}"` 创建目录
- [ ] 执行 `mv {图片文件} "assets/{论文标题}/"` 移动图片
- [ ] 使用替换更新所有图片引用路径（图片集 → assets）
- [ ] 验证 Markdown 文件中不再存在 "图片集" 字符串

---

## ⚠️ 最终清理：仅保留必要文件

**⚠️ 执行任何操作前，必须完成以下最终清理步骤**

### 保留文件清单

转换完成后，**仅保留以下文件**，其余全部删除：

| 类型 | 保留位置 | 说明 |
|-----|---------|------|
| 英文 Markdown | `{用户指定目录}/{论文标题}.md` | LaTeX 转换后的英文原文 |
| 中文总结笔记 | `{用户指定目录}/{论文标题}_summary.md` | 中文分析笔记 |
| 原始 PDF | `{用户指定目录}/{论文标题}.pdf` | 论文原始 PDF |
| 图片 | `assets/{论文标题}/*.png` | Markdown 中引用的图片 |

### 必须删除的中间文件

以下文件**必须全部删除**，不能保留在 Vault 中：

```bash
# 1. LaTeX 源码相关（全部删除）
rm -rf *.tex              # 所有 .tex 源文件
rm -rf *.sty              # 样式文件
rm -rf *.cls              # 文档类文件
rm -rf *.bbl              # BibTeX 输出
rm -rf *.bib              # 参考文献数据库
rm -rf *.bst              # BibTeX 样式
rm -rf *.blg              # BibTeX 日志

# 2. 源码目录（解压后的目录）
rm -rf {arxiv_id}/        # arXiv 源码解压目录
rm -rf texmf/             # TeX 宏包目录
rm -rf latex/             # LaTeX 辅助目录

# 3. 图片目录（仅删除源码中的图片目录，不删除 assets）
rm -rf Figs/              # 源码中的图片目录
rm -rf figures/           # 源码中的图片目录
rm -rf images/            # 源码中的图片目录
rm -rf img/               # 源码中的图片目录

# 4. 数据文件
rm -rf data/              # 源码中的数据目录
rm -rf *.dat              # 数据文件
rm -rf *.csv              # CSV 数据文件

# 5. 下载的临时文件
rm -rf {arxiv_id}.tar.gz  # 下载的压缩包
rm -rf {arxiv_id}.pdf     # 临时 PDF（已重命名的除外）

# 6. 其他临时文件
rm -rf *.log              # 编译日志
rm -rf *.aux              # 辅助文件
rm -rf *.toc              # 目录文件
rm -rf *.out              # 书签文件
```

### 清理验证清单

完成清理后，必须验证以下内容：

- [ ] **确认 Markdown 文件存在**：`{用户指定目录}/{论文标题}.md`
- [ ] **确认中文笔记存在**：`{用户指定目录}/{论文标题}_summary.md`
- [ ] **确认 PDF 存在**：`{用户指定目录}/{论文标题}.pdf`
- [ ] **确认图片存在**：`assets/{论文标题}/` 目录中有图片
- [ ] **确认 Markdown 中图片引用正确**：使用 `assets/{论文标题}/` 路径
- [ ] **确认无 .tex 文件残留**
- [ ] **确认无 .sty/.cls 文件残留**
- [ ] **确认无源码目录残留**（如 `{arxiv_id}/`）
- [ ] **确认无数据目录残留**（如 `data/`、`Figs/`）

### ⚠️ 绝对路径检查

**确保技能文件中不包含任何绝对路径**：
- 所有路径应使用相对路径或用户指定的变量（如 `{用户指定目录}`）
- 图片路径应使用 `assets/{论文标题}/`（相对于 Vault 根目录）
- 不应在任何命令或路径中硬编码绝对路径（如 `/Users/xxx/`）

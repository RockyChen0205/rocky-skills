---
name: vault-paper-survey
description: 在当前 Academic Vault 的 03-Papers 中执行 project 级论文调研。先读取 paper-index.yaml 做宽搜，再用多 agent 并行精读论文笔记，最后按用户目标生成 survey、solution research、research gap、proposal input 等产物。适用于“调研某个方向”“找某类方案”“从 03-Papers 中系统综述”“跨目录探索论文并沉淀结论”等场景。
---

# Vault Paper Survey

> 面向当前项目的论文调研 skill。核心不是固定模板，而是稳定执行 survey action。

## 触发条件

当用户提到：
- “调研 `03-Papers/...`”
- “做一个 survey”
- “找一下某类论文/方案”
- “从 vault 里系统看看这个方向”
- “跨目录梳理论文”
- “基于 paper-index 做综述”
- `/vault-paper-survey`

## 输入模式

支持三类输入：

1. **目录驱动**
   - 例：`/vault-paper-survey 03-Papers/03-agent/Gui-agent`
2. **问题驱动**
   - 例：`帮我调研长视频推理里降低 token 开销的方案`
3. **混合驱动**
   - 例：`在 03-Papers/02-understanding&reasoning 下调研 video reasoning 的 RL 方法`

## 强制工作流

### 1. 先创建工作文件

每次运行都在目标工作目录创建或更新：
- `plan.md`
- `notes.md`

如果用户没有指定最终产物，再默认生成一个主交付文件：
- `survey.md`

如果用户指定了最终产物，例如 `solution-landscape.md`、`proposal-input.md`、`research-gap.md`，则不要额外生成 `survey.md`。

### 2. 先宽搜，再深读

不要一开始就读正文。

先用 `scripts/discover_indexes.py` 和 `scripts/query_index.py`：
- 找到相关 `paper-index.yaml`
- 建立候选论文池
- 记录到 `plan.md` 和 `notes.md`

只有在完成候选池构建后，才进入正文精读。

### 3. 多 agent 是默认策略，不是可选装饰

出现以下任一情况时，必须显式采用多 agent 分工：
- 涉及多个目录
- 候选论文超过 12 篇
- 用户要求 “系统调研 / 全面梳理 / 尽量多看”
- 任务同时追求 wide 和 deep

推荐角色：
- `Scout agent`：只读 index，负责扩池、聚类、初筛
- `Analyst agent`：精读一组论文笔记，输出结构化分析卡
- `Synthesizer agent`：只汇总各 agent 结果，生成最终结论

### 4. 控制 context 的方式是“磁盘外存 + 分治”，不是少读

不要因为担心 context 就过早砍掉论文数量。

正确做法：
- 用 `notes.md` 存储中间发现
- 每个 subagent 只处理一个主题簇或一批论文
- 主 agent 只回收结构化结论，不重新吞下全部正文

## 输出策略

默认只保证三个层级：

1. **过程文件**
   - `plan.md`
   - `notes.md`
2. **主交付文件**
   - 用户没指定：`survey.md`
   - 用户指定了：按用户要求命名
3. **可选附加文件**
   - 仅在用户明确要求时创建比较表、shortlist、gap note、proposal input 等

## 执行阶段

简版协议如下，细节见：
- `references/workflow.md`
- `references/output-defaults.md`
- `references/index-schema.md`

1. 定义目标和边界
2. 扫描相关 index
3. 构建候选池并分主题
4. 多 agent 并行精读
5. 汇总成面向目标的结论
6. 写回用户要求的产物

## 脚本

### `scripts/discover_indexes.py`

扫描 `03-Papers` 下的 `paper-index.yaml`，输出目录地图。

示例：

```bash
python3 .claude/skills/vault-paper-survey/scripts/discover_indexes.py 03-Papers --format table
```

### `scripts/query_index.py`

按目录、关键词、标签、年份等条件检索候选论文。

示例：

```bash
python3 .claude/skills/vault-paper-survey/scripts/query_index.py \
  --root 03-Papers \
  --keyword video reasoning \
  --task video_reasoning \
  --method reinforcement_learning \
  --limit 30 \
  --format table
```

## 关键规则

- 优先复用已有 `paper-index.yaml`，不要把这个 skill 做成索引生成器。
- 精读阶段优先读论文笔记；只有笔记明显不够时才补原文。
- 输出必须围绕用户目标组织，而不是机械罗列论文。
- 默认追求 “尽量多读符合条件的论文”，再在综合阶段做筛选。
- 如果范围明显过大，先缩到若干主题簇，而不是直接缩到少量论文。

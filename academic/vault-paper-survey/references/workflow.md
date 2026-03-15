# Workflow

## 1. Scope

先在 `plan.md` 记录：
- 用户目标
- 范围类型：目录驱动 / 问题驱动 / 混合驱动
- 交付目标：survey / solution research / gap note / proposal input / other
- 用户是否指定了最终文件名

如果用户没有指定最终文件名：
- 默认最终文件为 `survey.md`

## 2. Discovery

运行 `discover_indexes.py`：
- 找出相关 `paper-index.yaml`
- 估计目录覆盖范围
- 判断是否需要多 agent

以下情形应直接切成多 agent：
- 命中 index 文件 >= 3
- 候选目录 >= 2
- 查询同时包含多个主题词

把结果写入 `notes.md`，不要只放在上下文里。

## 3. Candidate Expansion

运行 `query_index.py` 构建候选池。

这里的目标不是立刻压缩到很少的论文，而是：
- 尽量召回符合条件的论文
- 做初步聚类
- 标出明显的代表路线

推荐在 `notes.md` 里按以下结构记录：
- Topic cluster
- Candidate papers
- Why relevant
- Confidence / uncertainty

## 4. Deep Reading

把候选池按主题簇拆给多个 `Analyst agent`。

每个 analyst 只需要输出：
- 解决的问题
- 方法主线
- 与相邻工作的关键差异
- 优势 / 局限
- 是否值得进入最终综合

如果候选很多，优先保证每个主题簇都有足够覆盖，而不是把预算集中到单一路线。

## 5. Synthesis

主 agent 汇总 analyst 结果，形成：
- 分类法
- 代表路线
- 主要分歧
- 适用场景
- 空白点 / 机会点

写作时围绕用户目标组织，不要把笔记堆成 paper list。

## 6. Handoff

默认输出逻辑：
- 始终维护 `plan.md`
- 始终维护 `notes.md`
- 用户未指定最终文件时，生成 `survey.md`
- 用户指定最终文件时，只生成用户要求的目标文件

如果下一步明显是实验设计、proposal、review rebuttal 等，产物要直接服务下一步，而不是只停留在综述。

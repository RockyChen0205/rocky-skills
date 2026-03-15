# Index Schema

当前 Vault 中的 `paper-index.yaml` 至少常见这些字段：

- `id`
- `title`
- `arxiv`
- `date`
- `team`
- `year`
- `core_contribution`
- `task_type`
- `method_type`
- `tech_highlights`
- `note_path` 可选

## Compatibility rules

- `note_path` 可能不存在，此时优先尝试：
  - `index 所在目录 / {id}.md`
- 某些字段可能缺失或为空，不应因此丢弃整条记录
- 注释行和 YAML block string 需要保留兼容

## Retrieval fields

候选检索时优先使用：
- `title`
- `core_contribution`
- `task_type`
- `method_type`
- `tech_highlights`
- 所在目录路径

## Ranking heuristics

简单有效即可，不要过拟合：
- 明确标签命中权重大于自由文本模糊命中
- 多个查询维度同时命中的条目优先
- 同主题下优先保留年份较近且描述更具体的条目

---
name: handoff
description: Generate a project handoff document for the next AI agent and write it to `./{yymmdd}-handoff.md` using a fixed 7-section structure. Use when the user asks for handoff/交接, context is getting long, or work will continue in a new session.
---

# Handoff

## Overview

This skill creates a continuation-ready handoff for the next agent.
It writes a concrete, execution-oriented summary to `./{yymmdd}-handoff.md` and overwrites the same-day handoff file if it already exists.

## Trigger Conditions

Use this skill when any of the following appears:
- User asks for "handoff", "交接", "接手摘要", "新会话继续".
- User says current context is too long and wants continuity.
- User explicitly requests `./{yymmdd}-handoff.md` style output.

## Output Contract

- Target file: `./{yymmdd}-handoff.md` (use system date, e.g. `260325`).
- If the file already exists, overwrite it with the latest handoff.
- The document is for the next agent, not for end users.
- Use repository-relative paths.
- Integrate user-supplied extra context into the relevant sections (do not append as a detached appendix).

## Required Document Structure

Write exactly these sections in order:

## 1. 当前任务目标
说明当前要解决的问题、预期产出和完成标准。

## 2. 当前进展
说明目前已经完成了哪些分析、确认、修改、排查、讨论或产出。

## 3. 关键上下文
包括但不限于：
- 重要背景信息
- 用户的明确要求
- 已知约束
- 已做出的关键决定
- 重要假设
- 如果是文件，写清楚所有的文件路径

## 4. 关键发现
列出目前最重要的结论、规律、异常点、根因判断、设计判断或值得注意的信息。

## 5. 未完成事项
列出仍需要继续处理的内容，并按优先级排序。

## 6. 建议接手路径
告诉下一位 Agent：
- 应优先查看哪些文件、模块、数据、日志、命令、页面或线索
- 应先验证什么
- 推荐的下一步动作是什么

## 7. 风险与注意事项
说明哪些点容易误判、重复劳动或跑偏，哪些方向已经验证过且不建议继续。

最后补一段：`下一位 Agent 的第一步建议`

## Content Quality Bar

- Keep it specific and actionable; avoid vague statements.
- Prefer concrete artifacts: file paths, commands, interfaces, class/function names, logs, decisions.
- Distinguish facts vs assumptions.
- Prioritize continuation value over narration.

## Suggested Build Process

1. Collect current state from conversation + working tree + task docs.
2. Extract decisions, unresolved items, and verification status.
3. Draft the 7 sections with priority ordering.
4. Add the final "第一步建议" as an immediate executable next action.
5. Write/overwrite `./{yymmdd}-handoff.md`.

## Anti-Patterns

- Do not output only a user-facing summary.
- Do not omit concrete file paths.
- Do not mark unclear assumptions as confirmed facts.
- Do not skip risks and pending work.

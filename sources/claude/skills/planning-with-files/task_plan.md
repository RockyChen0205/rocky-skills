# Task Plan: OpenReview API 研究

## Goal
了解 OpenReview 是否有 API，以及如何查询会议论文

## Phases
- [ ] Phase 1: 研究 OpenReview API 文档
- [ ] Phase 2: 整理 API 使用方法和查询会议论文的方式

## Key Questions
1. OpenReview 是否有官方 API？
2. 如何通过 API 查询会议论文？
3. API 的认证和使用限制如何？

## Status
**Phase 1 Completed** - 已完成 OpenReview API 研究

## Research Summary
### OpenReview API 存在两种版本：
1. **API v1**: `https://api.openreview.net`
2. **API v2**: `https://api2.openreview.net` (新版，推荐使用)

### 认证方式：
- 使用邮箱和密码登录获取 `openreview.accessToken`
- 基于 cookie 的认证机制

### 查询会议论文的主要方式：
- `GET /notes` - 获取论文列表，支持多种过滤条件
- `GET /notes/search` - 搜索论文
- 关键参数：`invitation`, `content.venue`, `content.title`, `content.authorids` 等
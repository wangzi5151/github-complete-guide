# 练习 35：GitHub 团队协作

## 目标

学习如何使用 GitHub 进行高效的团队协作，包括分支策略、代码审查、项目管理等。

## 前置条件

- 有 GitHub 账号
- 有一个测试仓库
- 有团队成员（或使用多个账号模拟）

## 步骤

### 1. 理解团队协作流程

**标准工作流**：

```
1. 从 main 创建功能分支
2. 在功能分支上开发
3. 提交 PR
4. 代码审查
5. CI 检查通过
6. 合并到 main
7. 部署
```

**分支命名规范**：

```yaml
功能开发: feature/xxx
Bug 修复: bugfix/xxx
紧急修复: hotfix/xxx
文档更新: docs/xxx
实验功能: experiment/xxx
```

### 2. 创建团队

**创建组织**：

1. 访问 [GitHub](https://github.com/organizations/new)
2. 填写组织信息
3. 选择计划
4. 完成创建

**创建团队**：

1. 访问组织设置
2. 点击 "Teams"
3. 点击 "New team"
4. 填写团队信息
5. 设置权限

**团队权限**：

| 权限 | 说明 |
|------|------|
| Read | 只读访问 |
| Triage | Issue 和 PR 管理 |
| Write | 代码推送和分支管理 |
| Maintain | 仓库管理（不含危险操作） |
| Admin | 完全管理权限 |

### 3. 配置分支保护

**配置步骤**：

1. 访问仓库设置
2. 点击 "Branches"
3. 点击 "Add rule"
4. 配置保护规则

**推荐配置**：

```yaml
# 分支保护规则
required_pull_request_reviews:
  required_approving_review_count: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

required_status_checks:
  strict: true
  contexts:
    - "ci/build"
    - "ci/test"

enforce_admins: true

restrictions:
  users: ["admin-user"]
  teams: ["core-team"]
```

### 4. 使用 Pull Request

**创建 Pull Request**：

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 进行更改
# ...

# 提交更改
git add .
git commit -m "feat: add new feature"

# 推送分支
git push origin feature/new-feature

# 在 GitHub 上创建 PR
gh pr create --title "feat: add new feature" --body "Description of the feature"
```

**PR 模板**：

```markdown
# Pull Request

## 描述

简要描述这个 PR 的目的和更改内容。

## 更改类型

- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 测试
- [ ] 其他

## 测试

描述如何测试这些更改。

## 相关 Issue

关闭 #123

## 截图（如果适用）

添加截图来展示更改。

## 检查清单

- [ ] 代码遵循项目规范
- [ ] 已添加测试
- [ ] 已更新文档
- [ ] 已通过 CI 检查
```

### 5. 进行代码审查

**审查步骤**：

1. 打开 PR
2. 查看更改的文件
3. 添加评论
4. 提交审查

**审查最佳实践**：

```markdown
# 代码审查指南

## 审查要点

### 代码质量
- 代码是否清晰易懂？
- 是否有重复代码？
- 是否遵循项目规范？

### 功能正确性
- 功能是否按预期工作？
- 是否有边界情况？
- 是否有错误处理？

### 安全性
- 是否有安全漏洞？
- 是否有敏感信息泄露？
- 是否有输入验证？

### 性能
- 是否有性能问题？
- 是否有优化空间？
- 是否有资源泄露？

## 审查建议

### 建设性反馈
- 使用 "我建议..." 而不是 "你应该..."
- 解释为什么
- 提供替代方案

### 示例

❌ "这段代码很糟糕"
✅ "这段代码可以优化，建议使用 X 方法，因为 Y"

❌ "这里有个 bug"
✅ "这里可能有个问题，当 Z 情况下会..."
```

### 6. 使用项目管理

**使用 GitHub Projects**：

1. 访问仓库
2. 点击 "Projects"
3. 点击 "New project"
4. 选择模板
5. 配置项目

**项目视图**：

| 视图 | 用途 |
|------|------|
| Board | 看板视图，适合敏捷开发 |
| Table | 表格视图，适合数据分析 |
| Roadmap | 路线图视图，适合长期规划 |

**自动化配置**：

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, closed]
  pull_request:
    types: [opened, closed, ready_for_review]

jobs:
  auto-add:
    runs-on: ubuntu-latest
    steps:
    - name: Add to project
      uses: actions/add-to-project@v0.5.0
      with:
        project-url: https://github.com/orgs/your-org/projects/1
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 7. 使用 Issue 管理

**Issue 模板**：

```markdown
# Bug Report

## 描述

简要描述 bug。

## 复现步骤

1. 访问 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

## 预期行为

描述你期望发生什么。

## 实际行为

描述实际发生了什么。

## 截图

如果适用，添加截图来帮助解释问题。

## 环境

- 操作系统: [例如 iOS]
- 浏览器 [例如 chrome, safari]
- 版本 [例如 22]

## 其他信息

添加任何其他有关问题的信息。
```

**Issue 标签**：

| 标签 | 用途 |
|------|------|
| bug | Bug 报告 |
| enhancement | 功能增强 |
| documentation | 文档相关 |
| good first issue | 适合新手 |
| help wanted | 需要帮助 |
| wontfix | 不会修复 |
| duplicate | 重复问题 |
| invalid | 无效问题 |

### 8. 使用里程碑

**创建里程碑**：

1. 访问仓库
2. 点击 "Issues"
3. 点击 "Milestones"
4. 点击 "New milestone"
5. 填写信息

**里程碑最佳实践**：

```markdown
# 里程碑管理指南

## 设置里程碑

- 明确目标
- 设置截止日期
- 分配 Issue
- 追踪进度

## 里程碑命名

- v1.0.0 - 初始版本
- v1.1.0 - 功能更新
- v1.1.1 - Bug 修复
- 2024-Q1 - 季度目标

## 里程碑审查

- 定期审查进度
- 调整优先级
- 及时关闭完成的里程碑
- 总结经验教训
```

### 9. 使用团队协作工具

**使用 GitHub Discussions**：

1. 启用 Discussions
2. 创建分类
3. 鼓励团队使用

**Discussions 分类**：

| 分类 | 用途 |
|------|------|
| 📣 Announcements | 官方公告 |
| 💬 General | 一般讨论 |
| 💡 Ideas | 想法和建议 |
| 🙋 Q&A | 问答 |
| 📝 Show and tell | 展示和分享 |

**使用 GitHub Wiki**：

1. 启用 Wiki
2. 创建页面
3. 编写文档

**Wiki 最佳实践**：

```markdown
# Wiki 管理指南

## Wiki 结构

- 首页
- 快速开始
- 安装指南
- 使用指南
- API 文档
- 常见问题
- 贡献指南

## Wiki 维护

- 定期更新
- 保持简洁
- 使用图片
- 链接相关页面
```

### 10. 团队协作最佳实践

**沟通规范**：

```markdown
# 团队沟通规范

## 沟通渠道

- GitHub Issues：问题报告和功能请求
- GitHub Discussions：讨论和问答
- Slack/Teams：实时沟通
- 邮件列表：重要公告

## 沟通原则

- 及时响应
- 清晰表达
- 尊重他人
- 建设性反馈

## 沟通频率

- 每日站会：15 分钟
- 每周例会：1 小时
- 每月回顾：2 小时
```

**协作流程**：

```markdown
# 团队协作流程

## 开发流程

1. 需求分析
2. 任务分配
3. 开发实现
4. 代码审查
5. 测试验证
6. 部署上线
7. 监控反馈

## 分支策略

- main：生产分支
- develop：开发分支
- feature/*：功能分支
- bugfix/*：修复分支
- hotfix/*：紧急修复分支

## 发布流程

1. 创建发布分支
2. 测试验证
3. 修复问题
4. 合并到 main
5. 打标签
6. 部署
7. 发布公告
```

## 挑战

1. **挑战 1**：为你的团队配置完整的协作流程
2. **挑战 2**：创建团队协作规范文档
3. **挑战 3**：配置自动化工作流
4. **挑战 4**：进行代码审查实践
5. **挑战 5**：使用项目管理工具

## 思考

1. 团队协作中最重要的因素是什么？
2. 如何处理团队冲突？
3. 如何提高团队效率？
4. 如何平衡质量和速度？

## 相关资源

- [GitHub 团队协作文档](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations)
- [GitHub Projects 文档](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Discussions 文档](https://docs.github.com/en/discussions)
- [GitHub Pull Requests 文档](https://docs.github.com/en/pull-requests)
- [GitHub Issues 文档](https://docs.github.com/en/issues)

---

**上一篇：[练习 34：GitHub 安全最佳实践](exercise-34-github-security-best-practices.md) | 下一篇：[GitHub 高级功能](../docs/00-advanced-features-guide.md)**
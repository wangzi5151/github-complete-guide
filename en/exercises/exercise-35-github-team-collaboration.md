# Exercise 35: GitHub Team Collaboration

## Objective

Learn how to use GitHub for efficient team collaboration, including branching strategies, code reviews, project management, and more.

## Prerequisites

- A GitHub account
- A test repository
- Team members (or use multiple accounts to simulate)

## Steps

### 1. Understand the Team Collaboration Workflow

**Standard Workflow**:

```
1. Create a feature branch from main
2. Develop on the feature branch
3. Submit a PR
4. Code review
5. CI checks pass
6. Merge to main
7. Deploy
```

**Branch Naming Convention**:

```yaml
Feature development: feature/xxx
Bug fix: bugfix/xxx
Hotfix: hotfix/xxx
Documentation update: docs/xxx
Experimental feature: experiment/xxx
```

### 2. Create a Team

**Create an Organization**:

1. Visit [GitHub](https://github.com/organizations/new)
2. Fill in organization information
3. Choose a plan
4. Complete creation

**Create a Team**:

1. Visit organization settings
2. Click "Teams"
3. Click "New team"
4. Fill in team information
5. Set permissions

**Team Permissions**:

| Permission | Description |
|------|------|
| Read | Read-only access |
| Triage | Issue and PR management |
| Write | Code push and branch management |
| Maintain | Repository management (excluding dangerous operations) |
| Admin | Full administrative access |

### 3. Configure Branch Protection

**Configuration Steps**:

1. Visit repository settings
2. Click "Branches"
3. Click "Add rule"
4. Configure protection rules

**Recommended Configuration**:

```yaml
# Branch protection rules
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

### 4. Using Pull Requests

**Create a Pull Request**:

```bash
# Create a feature branch
git checkout -b feature/new-feature

# Make changes
# ...

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push the branch
git push origin feature/new-feature

# Create a PR on GitHub
gh pr create --title "feat: add new feature" --body "Description of the feature"
```

**PR Template**:

```markdown
# Pull Request

## Description

Briefly describe the purpose and changes of this PR.

## Change Type

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance optimization
- [ ] Testing
- [ ] Other

## Testing

Describe how to test these changes.

## Related Issue

Closes #123

## Screenshots (if applicable)

Add screenshots to show the changes.

## Checklist

- [ ] Code follows project conventions
- [ ] Tests have been added
- [ ] Documentation has been updated
- [ ] CI checks have passed
```

### 5. Conducting Code Reviews

**Review Steps**:

1. Open the PR
2. Review changed files
3. Add comments
4. Submit review

**Review Best Practices**:

```markdown
# Code Review Guide

## Review Focus

### Code Quality
- Is the code clear and easy to understand?
- Is there duplicated code?
- Does it follow project conventions?

### Functional Correctness
- Does the function work as expected?
- Are there edge cases?
- Is there error handling?

### Security
- Are there security vulnerabilities?
- Is there sensitive information exposure?
- Is there input validation?

### Performance
- Are there performance issues?
- Is there room for optimization?
- Are there resource leaks?

## Review Suggestions

### Constructive Feedback
- Use "I suggest..." instead of "You should..."
- Explain why
- Provide alternatives

### Examples

❌ "This code is terrible"
✅ "This code can be optimized, I suggest using method X because of Y"

❌ "There's a bug here"
✅ "There might be an issue here, when Z happens..."
```

### 6. Using Project Management

**Using GitHub Projects**:

1. Visit the repository
2. Click "Projects"
3. Click "New project"
4. Choose a template
5. Configure the project

**Project Views**:

| View | Purpose |
|------|------|
| Board | Kanban view, suitable for agile development |
| Table | Table view, suitable for data analysis |
| Roadmap | Roadmap view, suitable for long-term planning |

**Automation Configuration**:

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

### 7. Using Issue Management

**Issue Template**:

```markdown
# Bug Report

## Description

Briefly describe the bug.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See the error

## Expected Behavior

Describe what you expected to happen.

## Actual Behavior

Describe what actually happened.

## Screenshots

If applicable, add screenshots to help explain the issue.

## Environment

- Operating System: [e.g., iOS]
- Browser: [e.g., Chrome, Safari]
- Version: [e.g., 22]

## Additional Information

Add any other information about the issue.
```

**Issue Labels**:

| Label | Purpose |
|------|------|
| bug | Bug reports |
| enhancement | Feature enhancements |
| documentation | Documentation related |
| good first issue | Good for beginners |
| help wanted | Help needed |
| wontfix | Will not fix |
| duplicate | Duplicate issue |
| invalid | Invalid issue |

### 8. Using Milestones

**Create a Milestone**:

1. Visit the repository
2. Click "Issues"
3. Click "Milestones"
4. Click "New milestone"
5. Fill in the information

**Milestone Best Practices**:

```markdown
# Milestone Management Guide

## Setting Up Milestones

- Define clear goals
- Set deadlines
- Assign issues
- Track progress

## Milestone Naming

- v1.0.0 - Initial release
- v1.1.0 - Feature update
- v1.1.1 - Bug fix
- 2024-Q1 - Quarterly goal

## Milestone Review

- Regularly review progress
- Adjust priorities
- Close completed milestones promptly
- Summarize lessons learned
```

### 9. Using Team Collaboration Tools

**Using GitHub Discussions**:

1. Enable Discussions
2. Create categories
3. Encourage team usage

**Discussion Categories**:

| Category | Purpose |
|------|------|
| 📣 Announcements | Official announcements |
| 💬 General | General discussion |
| 💡 Ideas | Ideas and suggestions |
| 🙋 Q&A | Questions and answers |
| 📝 Show and tell | Showcase and share |

**Using GitHub Wiki**:

1. Enable Wiki
2. Create pages
3. Write documentation

**Wiki Best Practices**:

```markdown
# Wiki Management Guide

## Wiki Structure

- Home
- Getting Started
- Installation Guide
- Usage Guide
- API Documentation
- Frequently Asked Questions
- Contributing Guide

## Wiki Maintenance

- Update regularly
- Keep it concise
- Use images
- Link related pages
```

### 10. Team Collaboration Best Practices

**Communication Standards**:

```markdown
# Team Communication Standards

## Communication Channels

- GitHub Issues: Issue reports and feature requests
- GitHub Discussions: Discussions and Q&A
- Slack/Teams: Real-time communication
- Mailing list: Important announcements

## Communication Principles

- Respond promptly
- Express clearly
- Respect others
- Provide constructive feedback

## Communication Frequency

- Daily standup: 15 minutes
- Weekly meeting: 1 hour
- Monthly review: 2 hours
```

**Collaboration Workflow**:

```markdown
# Team Collaboration Workflow

## Development Process

1. Requirements analysis
2. Task assignment
3. Development implementation
4. Code review
5. Testing verification
6. Deployment
7. Monitoring and feedback

## Branching Strategy

- main: Production branch
- develop: Development branch
- feature/*: Feature branches
- bugfix/*: Fix branches
- hotfix/*: Hotfix branches

## Release Process

1. Create release branch
2. Testing verification
3. Fix issues
4. Merge to main
5. Tag the release
6. Deploy
7. Release announcement
```

## Challenges

1. **Challenge 1**: Configure a complete collaboration workflow for your team
2. **Challenge 2**: Create team collaboration standards documentation
3. **Challenge 3**: Configure automated workflows
4. **Challenge 4**: Practice code reviews
5. **Challenge 5**: Use project management tools

## Reflection

1. What is the most important factor in team collaboration?
2. How to handle team conflicts?
3. How to improve team efficiency?
4. How to balance quality and speed?

## Related Resources

- [GitHub Team Collaboration Documentation](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Discussions Documentation](https://docs.github.com/en/discussions)
- [GitHub Pull Requests Documentation](https://docs.github.com/en/pull-requests)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)

---

**Previous: [Exercise 34: GitHub Security Best Practices](exercise-34-github-security-best-practices.md) | Next: [Exercise 36: GitHub Advanced Features](exercise-36-github-advanced-features.md)**

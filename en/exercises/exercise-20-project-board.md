# Exercise 20: GitHub Projects Board Management

## Learning Objectives

- Create a GitHub Project
- Configure board views
- Use automation

## Steps

### Step 1: Create Project

```bash
# Create project
gh project create --title "My Project" --owner your-org
```

### Step 2: Add Issues to Project

```bash
# Add Issue
gh project item-add 1 --owner your-org --url https://github.com/your-org/your-repo/issues/1
```

### Step 3: Configure Automation

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

### Step 4: Create Views

```bash
# Use CLI to view projects
gh project list --owner your-org
gh project item-list 1 --owner your-org
```

## Hands-on Tasks

1. Create a GitHub Project
2. Add multiple Issues to the project
3. Configure automation workflows
4. Create different views (Board, Table, Roadmap)

## Verification Checklist

- [ ] Project created
- [ ] Issues added to the project
- [ ] Automation configured
- [ ] Views created

## Completion

Congratulations on completing all exercises! You have mastered:
- Git basics
- GitHub core features
- CI/CD pipelines
- Docker containerization
- Security scanning
- Release management
- Monorepo management
- China environment configuration
- Enterprise configuration
- Reusable workflows
- Project management

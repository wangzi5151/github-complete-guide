# GitHub Cheat Sheet

> This chapter provides a quick reference for common GitHub commands and operations.

---

## Table of Contents

1. [Git Basic Commands](#git-basic-commands)
2. [GitHub CLI Commands](#github-cli-commands)
3. [GitHub Actions Syntax](#github-actions-syntax)
4. [GitHub API Endpoints](#github-api-endpoints)
5. [GitHub Keyboard Shortcuts](#github-keyboard-shortcuts)
6. [GitHub Markdown Syntax](#github-markdown-syntax)
7. [GitHub Configuration Files](#github-configuration-files)
8. [GitHub Templates](#github-templates)

---

## Git Basic Commands

### Configuration

```bash
# Set user information
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# View configuration
git config --list

# Set default editor
git config --global core.editor "code --wait"

# Set default branch name
git config --global init.defaultBranch main
```

### Repository Operations

```bash
# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git

# Add remote repository
git remote add origin https://github.com/user/repo.git

# View remote repository
git remote -v

# Update remote repository
git remote update

# Remove remote repository
git remote remove origin
```

### Branch Operations

```bash
# View branches
git branch
git branch -a
git branch -r

# Create branch
git branch feature/new-feature

# Switch branch
git checkout feature/new-feature

# Create and switch branch
git checkout -b feature/new-feature

# Delete branch
git branch -d feature/new-feature
git branch -D feature/new-feature

# Rename branch
git branch -m old-name new-name

# Merge branch
git merge feature/new-feature

# Rebase branch
git rebase main
```

### Commit Operations

```bash
# View status
git status

# Add files
git add file.txt
git add .
git add *.js

# Commit
git commit -m "commit message"
git commit -am "commit message"

# Amend last commit
git commit --amend

# View commit history
git log
git log --oneline
git log --graph
git log --author="Author Name"
```

### Push and Pull

```bash
# Push
git push origin main
git push -u origin main
git push --force

# Pull
git pull origin main
git pull --rebase origin main

# Fetch
git fetch origin
git fetch --all
```

### Undo Operations

```bash
# Undo working directory changes
git checkout -- file.txt

# Undo staging
git reset HEAD file.txt

# Undo commit
git reset --soft HEAD~1
git reset --hard HEAD~1

# Undo remote commit
git revert commit-hash

# Clean untracked files
git clean -fd
```

### Tag Operations

```bash
# View tags
git tag

# Create tag
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags

# Delete tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### Stash Operations

```bash
# Stash changes
git stash
git stash push -m "stash message"

# View stashes
git stash list

# Restore stash
git stash pop
git stash apply stash@{0}

# Delete stash
git stash drop stash@{0}
git stash clear
```

## GitHub CLI Commands

### Authentication

```bash
# Login
gh auth login

# View authentication status
gh auth status

# Refresh token
gh auth refresh

# Logout
gh auth logout
```

### Repository Operations

```bash
# Clone repository
gh repo clone owner/repo

# Create repository
gh repo create repo-name

# View repository
gh repo view owner/repo

# Edit repository
gh repo edit owner/repo

# Delete repository
gh repo delete owner/repo

# Fork repository
gh repo fork owner/repo
```

### Issue Operations

```bash
# Create Issue
gh issue create

# View Issue
gh issue view 123

# List Issues
gh issue list

# Close Issue
gh issue close 123

# Reopen Issue
gh issue reopen 123

# Edit Issue
gh issue edit 123
```

### Pull Request Operations

```bash
# Create PR
gh pr create

# View PR
gh pr view 123

# List PRs
gh pr list

# Merge PR
gh pr merge 123

# Close PR
gh pr close 123

# Checkout PR
gh pr checkout 123

# Review PR
gh pr review 123
```

### Actions Operations

```bash
# View workflows
gh workflow list

# View workflow runs
gh run list

# View run details
gh run view 123

# View run logs
gh run view 123 --log

# Rerun
gh run rerun 123

# Trigger workflow manually
gh workflow run workflow-name
```

### Release Operations

```bash
# Create Release
gh release create v1.0.0

# View Release
gh release view v1.0.0

# List Releases
gh release list

# Delete Release
gh release delete v1.0.0

# Download Release assets
gh release download v1.0.0
```

### API Operations

```bash
# Call API
gh api repos/{owner}/{repo}

# Use GraphQL
gh api graphql -f query='{ viewer { login } }'

# Filter with jq
gh api repos/{owner}/{repo} --jq '.name'
```

## GitHub Actions Syntax

### Workflow Syntax

```yaml
# .github/workflows/workflow.yml
name: Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

env:
  GLOBAL_VAR: value

jobs:
  job-name:
    runs-on: ubuntu-latest
    needs: previous-job
    
    strategy:
      matrix:
        node-version: [14, 16, 18]
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Run commands
        run: |
          echo "Hello World"
          npm install
      
      - name: Use environment variables
        env:
          MY_VAR: value
        run: echo $MY_VAR
      
      - name: Use secrets
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: echo $API_KEY
```

### Common Actions

```yaml
# Checkout code
- uses: actions/checkout@v4

# Setup Node.js
- uses: actions/setup-node@v4
  with:
    node-version: '18'

# Setup Python
- uses: actions/setup-python@v4
  with:
    python-version: '3.9'

# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

# Upload artifacts
- uses: actions/upload-artifact@v3
  with:
    name: my-artifact
    path: path/to/artifact

# Download artifacts
- uses: actions/download-artifact@v3
  with:
    name: my-artifact

# Create Release
- uses: actions/create-release@v1
  with:
    tag_name: ${{ github.ref }}
    release_name: Release ${{ github.ref }}

# Deploy to GitHub Pages
- uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./public
```

## GitHub API Endpoints

### REST API

```bash
# User information
GET /users/{username}
GET /user

# Repository information
GET /repos/{owner}/{repo}
GET /user/repos

# Issue
GET /repos/{owner}/{repo}/issues
POST /repos/{owner}/{repo}/issues
PATCH /repos/{owner}/{repo}/issues/{issue_number}

# Pull Request
GET /repos/{owner}/{repo}/pulls
POST /repos/{owner}/{repo}/pulls
PATCH /repos/{owner}/{repo}/pulls/{pull_number}

# Actions
GET /repos/{owner}/{repo}/actions/runs
GET /repos/{owner}/{repo}/actions/workflows

# Release
GET /repos/{owner}/{repo}/releases
POST /repos/{owner}/{repo}/releases
```

### GraphQL API

```graphql
# Get user information
query {
  viewer {
    login
    name
    email
  }
}

# Get repository information
query {
  repository(owner: "owner", name: "repo") {
    name
    description
    stargazerCount
  }
}

# Get Issues
query {
  repository(owner: "owner", name: "repo") {
    issues(first: 10) {
      nodes {
        title
        body
      }
    }
  }
}
```

## GitHub Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Function |
|----------|----------|
| `s` or `/` | Focus search box |
| `g` then `n` | Notifications |
| `g` then `c` | Code |
| `g` then `i` | Issues |
| `g` then `p` | Pull Requests |
| `g` then `a` | Actions |
| `g` then `b` | Projects |

### Code View Shortcuts

| Shortcut | Function |
|----------|----------|
| `b` | View blame |
| `y` | Get permalink |
| `t` | File finder |
| `l` | Go to line |
| `w` | Switch branch |

### Issue and PR Shortcuts

| Shortcut | Function |
|----------|----------|
| `c` | Create comment |
| `ctrl+enter` | Submit comment |
| `r` | Reply to comment |
| `l` | Add label |
| `a` | Add assignee |
| `m` | Add milestone |

## GitHub Markdown Syntax

### Basic Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold**
*Italic*
~~Strikethrough~~

- Unordered list
1. Ordered list

[Link](https://example.com)
![Image](image.png)

> Blockquote

`Code`
```

Code block
```

### Task Lists

```markdown
- [x] Completed task
- [ ] Incomplete task
```

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Content 1 | Content 2 | Content 3 |
```

### Collapsible Content

```markdown
<details>
<summary>Click to expand</summary>

Hidden content

</details>
```

### Alert Boxes

```markdown
> [!NOTE]
> This is a note

> [!TIP]
> This is a tip

> [!IMPORTANT]
> This is important

> [!WARNING]
> This is a warning

> [!CAUTION]
> This is a warning
```

## GitHub Configuration Files

### .gitignore

```gitignore
# Environment variables
.env
.env.local

# Dependencies
node_modules/
vendor/

# Build artifacts
dist/
build/

# Logs
*.log

# IDE
.vscode/
.idea/
```

### .github/dependabot.yml

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
```

### .github/CODEOWNERS

```markdown
* @team-leads
/frontend/ @frontend-team
/backend/ @backend-team
```

### .github/PULL_REQUEST_TEMPLATE.md

```markdown
## Description

Briefly describe the purpose of this PR.

## Change Type

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Checklist

- [ ] Code follows project conventions
- [ ] Tests have been added
- [ ] Documentation has been updated
```

## GitHub Templates

### Issue Templates

**Bug Report**:

```markdown
---
name: Bug Report
about: Report a bug
title: '[BUG] '
labels: bug
assignees: ''
---

## Description

Briefly describe the bug.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior

Describe what you expected to happen.

## Actual Behavior

Describe what actually happened.

## Environment

- OS: [e.g. iOS]
- Browser: [e.g. chrome, safari]
- Version: [e.g. 22]
```

**Feature Request**:

```markdown
---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Description

Briefly describe the feature you want.

## Use Case

Describe the use case for this feature.

## Suggested Solution

Describe your suggested implementation.

## Additional Information

Add any other information about the feature.
```

### PR Template

```markdown
## Description

Briefly describe the purpose of this PR.

## Change Type

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Testing

## Testing

Describe how to test these changes.

## Related Issue

Closes #123

## Checklist

- [ ] Code follows project conventions
- [ ] Tests have been added
- [ ] Documentation has been updated
- [ ] CI checks have passed
```

---

**Previous: [Appendix F: GitHub Shortcuts Guide](F-shortcuts.md) | Next: [Appendix B: Git Alias Configuration](B-git-aliases.md)**

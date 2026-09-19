# Exercise 11: Advanced GitHub CLI Usage

## Learning Objectives

- Master advanced features of GitHub CLI
- Learn to use `gh` to manage repositories, issues, and PRs
- Understand `gh` extensions and aliases

## Prerequisites

Make sure GitHub CLI is installed and you are logged in:

```bash
# Install (macOS)
brew install gh

# Install (Windows)
winget install GitHub.cli

# Install (Linux)
sudo apt install gh

# Login
gh auth login
```

## Basic Operations

### Repository Management

```bash
# Create repository
gh repo create my-project --public --description "My project"

# Clone repository
gh repo clone owner/repo

# List repositories
gh repo list

# View repository information
gh repo view owner/repo

# Set repository default branch
gh repo edit owner/repo --default-branch main
```

### Issue Management

```bash
# Create issue
gh issue create --title "Feature request" --body "Describe your requirement"

# Create from template
gh issue create --template "bug_report.md"

# List issues
gh issue list

# View issue
gh issue view 123

# Add comment
gh issue comment 123 --body "Comment content"

# Close issue
gh issue close 123 --reason "completed"

# Reopen issue
gh issue reopen 123

# Assign issue
gh issue edit 123 --add-assignee username
```

### Pull Request Management

```bash
# Create PR
gh pr create --title "feat: New feature" --body "Description"

# List PRs
gh pr list

# View PR
gh pr view 456

# Checkout PR
gh pr checkout 456

# Merge PR
gh pr merge 456 --merge

# Squash merge
gh pr merge 456 --squash

# Rebase merge
gh pr merge 456 --rebase

# Review PR
gh pr review 456 --approve

# Request changes
gh pr review 456 --request-changes --body "Needs modifications..."

# Add label
gh pr edit 456 --add-label "enhancement"
```

## Advanced Features

### Using JSON Output

```bash
# Get issue list (JSON format)
gh issue list --json number,title,state

# Process with jq
gh issue list --json number,title | jq '.[] | "\(.number): \(.title)"'

# Get PR information
gh pr view 456 --json title,body,author
```

### Using the API

```bash
# Call API
gh api repos/owner/repo/issues

# Create issue
gh api repos/owner/repo/issues \
  --method POST \
  -f title="Issue title" \
  -f body="Issue content"

# Update issue
gh api repos/owner/repo/issues/123 \
  --method PATCH \
  -f state="closed"
```

### Alias Configuration

```bash
# Create alias
gh alias set prc 'pr create --fill'
gh alias set prl 'pr list --state all'
gh alias set iss 'issue list'

# View all aliases
gh alias list

# Delete alias
gh alias delete prc
```

## Hands-On Tasks

### Task 1: Manage a Repository

1. Create a new repository
2. Add a README file
3. Set repository description
4. Add topic tags

```bash
gh repo create practice-project --public
gh repo clone practice-project
echo "# Practice" > README.md
git add . && git commit -m "docs: Add README"
git push
gh repo edit practice-project --description "Practice project" --add-topic "git,github,practice"
```

### Task 2: Manage Issues

1. Create 3 issues
2. Add labels to issues
3. Assign issues
4. Close one issue

```bash
gh issue create --title "Feature 1" --label "enhancement"
gh issue create --title "Feature 2" --label "enhancement"
gh issue create --title "Bug 1" --label "bug"

gh issue close 1 --reason "completed"
```

### Task 3: Manage PRs

1. Create a new branch
2. Modify files and commit
3. Create a PR
4. Add a comment
5. Merge the PR

```bash
git checkout -b feature/new-feature
echo "New feature" > feature.txt
git add . && git commit -m "feat: Add new feature"
git push -u origin feature/new-feature

gh pr create --title "feat: Add new feature" --body "Implement new feature"
gh pr comment 1 --body "Looks good"
gh pr merge 1 --squash
```

### Task 4: Use Extensions

```bash
# Install extension
gh extension install dlvhdr/gh-dash

# View installed extensions
gh extension list

# Use dash
gh dash
```

## Advanced Scripts

### Batch Operation Script

```bash
#!/bin/bash
# Batch close all merged PRs
gh pr list --state merged --json number | \
  jq -r '.[].number' | \
  xargs -I {} gh pr close {}

# Batch add labels
for issue in $(gh issue list --label "needs-triage" --json number | jq -r '.[].number'); do
  gh issue edit $issue --add-label "triaged"
done
```

### Automation Workflow

```yaml
# .github/workflows/auto-label.yml
name: Auto Label

on:
  issues:
    types: [opened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/labeler@v4
      with:
        repo-token: ${{ secrets.GITHUB_TOKEN }}
```

## Verification Checklist

- [ ] Able to use `gh repo` commands
- [ ] Able to use `gh issue` commands
- [ ] Able to use `gh pr` commands
- [ ] Able to use JSON output
- [ ] Able to use `gh api` to call APIs
- [ ] Able to configure and use aliases
- [ ] Able to install and use extensions

## FAQ

### Q: How to update GitHub CLI?
A: Use `gh extension upgrade` to update extensions, and use the package manager to update `gh` itself.

### Q: How to configure a proxy?
A: Set environment variables:
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### Q: How to check API rate limits?
A: Use `gh api rate_limit` to check.

## Next Steps

After completing this exercise, you have mastered the advanced usage of GitHub CLI. You can continue exploring [GitHub Actions Automation](exercise-7-github-actions.md) or [Contributing to Open Source](exercise-6-open-source.md)

# GitHub CLI (gh) Complete Guide

## Overview

GitHub CLI (command line tool `gh`) is GitHub's official command line tool, allowing developers to perform almost all GitHub operations in the terminal. This chapter will comprehensively introduce GitHub CLI's installation, configuration and various practical features to help you improve development efficiency.

---

## 1. GitHub CLI Overview and Installation

### 1.1 What is GitHub CLI

GitHub CLI is GitHub's official command line interface tool, main features include:

- Manage Issues, Pull Requests, Releases in terminal
- Operate GitHub Actions workflows
- Manage GitHub Codespaces
- Directly call GitHub API
- Support custom aliases and extensions
- Seamlessly work with Git commands

### 1.2 Official Installation Methods

**macOS Installation:**

```bash
# Using Homebrew (recommended)
brew install gh

# Using MacPorts
sudo port install gh
```

**Windows Installation:**

```powershell
# Using winget (recommended)
winget install --id GitHub.cli

# Using Scoop
scoop install gh

# Using Chocolatey
choco install gh

# Using WinGet
winget install GitHub.cli
```

**Linux Installation:**

```bash
# Ubuntu/Debian (official source)
sudo apt update
sudo apt install gh

# CentOS/RHEL/Fedora
sudo dnf install gh

# Arch Linux
sudo pacman -S github-cli

# openSUSE
sudo zypper install gh
```

### 1.3 Domestic Installation Solutions

Due to network reasons, domestic users may not be able to directly access official sources. Here are several alternative solutions:

**Solution 1: Use domestic mirror source (Ubuntu/Debian)**

```bash
# Add GitHub CLI official repository
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# If above address is inaccessible, can use proxy or mirror
# Method 1: Use ghproxy proxy
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://ghproxy.com/https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

sudo apt update
sudo apt install gh
```

**Solution 2: Manually download deb/rpm packages**

```bash
# Visit GitHub Releases page to download
# https://github.com/cli/cli/releases

# Download using ghproxy proxy (example for 2.40.1)
wget https://ghproxy.com/https://github.com/cli/cli/releases/download/v2.40.1/gh_2.40.1_linux_amd64.deb

# Install
sudo dpkg -i gh_2.40.1_linux_amd64.deb

# If there are dependency issues
sudo apt-get install -f
```

**Solution 3: Install using Go**

```bash
# Ensure Go 1.21+ is installed
go version

# Set Go proxy (domestic acceleration)
go env -w GOPROXY=https://goproxy.cn,direct

# Install gh
go install github.com/cli/cli/v2/cmd/gh@latest

# Add to PATH
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

**Solution 4: Use pre-compiled binary files**

```bash
# Download binary file
wget https://ghproxy.com/https://github.com/cli/cli/releases/download/v2.40.1/gh_2.40.1_linux_amd64.tar.gz

# Extract
tar -xzf gh_2.40.1_linux_amd64.tar.gz

# Move to system path
sudo cp gh_2.40.1_linux_amd64/bin/gh /usr/local/bin/

# Verify installation
gh --version
```

### 1.4 Termux Installation Solution

```bash
# Install in Termux
pkg update
pkg install gh

# If official source unavailable, try
pkg install -y gh

# Or install using Go
pkg install golang
go env -w GOPROXY=https://goproxy.cn,direct
go install github.com/cli/cli/v2/cmd/gh@latest
```

### 1.5 Verify Installation

```bash
# Check version
gh --version
# Output example:
# gh version 2.40.1 (2023-12-01)
# https://github.com/cli/cli/releases/tag/v2.40.1

# View help
gh --help

# View all available commands
gh --help | grep -E "^  [a-z]"
```

---

## 2. gh Basic Commands

### 2.1 Authentication Management (gh auth)

```bash
# Interactive login (recommended)
gh auth login
# Follow prompts to select:
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate? Login with a web browser

# Login using Token
gh auth login --with-token < token.txt

# Set Token via environment variable
export GH_TOKEN=your_token_here
gh auth status

# View authentication status
gh auth status
# Output:
# github.com
#   ✓ Logged in to github.com account username
#   - Active account: true
#   - Git operations protocol: https
#   - Token: gho_****

# Refresh Token
gh auth refresh

# Refresh specific permissions
gh auth refresh -s admin:org -s delete_repo

# Logout
gh auth logout

# Open GitHub Token settings page in browser
gh auth login --web

# Set Token to configuration file
gh auth setup-git
```

### 2.2 Repository Operations (gh repo)

```bash
# Clone repository
gh repo clone owner/repo

# Clone to specified directory
gh repo clone owner/repo ~/projects/my-repo

# Create new repository (interactive)
gh repo create

# Create public repository
gh repo create my-project --public --description "My new project"

# Create private repository
gh repo create my-project --private

# Create repository from template
gh repo create my-project --template owner/template-repo

# Create and clone
gh repo create my-project --public --clone

# View repository info
gh repo view owner/repo

# Open repository in browser
gh repo view --web

# List your repositories
gh repo list

# List specified user's repositories
gh repo list username

# List organization repositories
gh repo list my-org --limit 50

# List only owned repositories
gh repo list --source

# List only forked repositories
gh repo list --fork

# View repository Topics
gh repo view owner/repo --json name,description,homepageUrl

# Edit repository settings
gh repo edit --description "New description"
gh repo edit --homepage "https://example.com"
gh repo edit --visibility private
gh repo edit --default-branch main

# Archive repository
gh repo archive owner/repo --yes

# Delete repository (use with caution)
gh repo delete owner/repo --yes

# Fork repository
gh repo fork owner/repo

# Fork and clone
gh repo fork owner/repo --clone

# Sync fork
gh repo sync owner/repo
```

### 2.3 Browser Operations (gh browse)

```bash
# Open current repository in browser
gh browse

# Open specified repository
gh browse owner/repo

# Open repository's Issues page
gh browse --issues

# Open repository's Pull Requests page
gh browse --pulls

# Open repository's Wiki
gh browse --wiki

# Open repository's Settings
gh browse --settings

# Open specified file
gh browse src/main.go

# Open specific line of file
gh browse src/main.go:42

# Open file in specified branch
gh browse src/main.go --branch develop

# Only output URL, don't open browser
gh browse --no-browser

# Open GitHub Actions page
gh browse --actions
```

---

## 3. Issue Management (gh issue)

### 3.1 View Issues

```bash
# List current repository's Issues
gh issue list

# List specified repository's Issues
gh issue list --repo owner/repo

# Filter by status
gh issue list --state open
gh issue list --state closed
gh issue list --state all

# Filter by label
gh issue list --label "bug"
gh issue list --label "bug,priority:high"

# Filter by author
gh issue list --author username

# Filter by assignee
gh issue list --assignee username

# Filter by milestone
gh issue list --milestone "v1.0"

# Limit quantity
gh issue list --limit 20

# Sort by creation time
gh issue list --sort created
gh issue list --sort updated
gh issue list --sort comments

# View specific Issue
gh issue view 123

# Open Issue in browser
gh issue view 123 --web

# View Issue comments
gh issue view 123 --comments

# View in JSON format
gh issue view 123 --json title,body,state,labels,assignees
```

### 3.2 Create Issues

```bash
# Create Issue interactively
gh issue create

# Quick create Issue
gh issue create --title "Fix login page bug" --body "Describe problem details..."

# Create with labels
gh issue create \
  --title "Fix login page bug" \
  --body "User cannot login normally" \
  --label "bug,priority:high"

# Create with assignee
gh issue create \
  --title "Fix login page bug" \
  --body "User cannot login normally" \
  --assignee username

# Read body from file
gh issue create \
  --title "Feature request" \
  --body-file issue-template.md

# Create using template
gh issue create \
  --title "Bug report" \
  --template bug_report.md
```

### 3.3 Manage Issues

```bash
# Close Issue
gh issue close 123

# Close and add comment
gh issue close 123 --comment "Fixed, please verify"

# Reopen Issue
gh issue reopen 123

# Reopen and add comment
gh issue reopen 123 --comment "Problem still exists"

# Add comment
gh issue comment 123 --body "Working on this issue..."

# Add labels
gh issue edit 123 --add-label "bug,priority:high"

# Remove labels
gh issue edit 123 --remove-label "priority:low"

# Add assignee
gh issue edit 123 --add-assignee username

# Remove assignee
gh issue edit 123 --remove-assignee username

# Modify title
gh issue edit 123 --title "New title"

# Modify milestone
gh issue edit 123 --milestone "v2.0"

# Transfer Issue to other repository
gh issue transfer 123 owner/other-repo

# Lock Issue
gh issue lock 123

# Unlock Issue
gh issue unlock 123

# Delete Issue (requires permission)
gh issue delete 123 --yes

# Batch operate Issues
gh issue list --label "stale" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Auto-closed: long-term inactivity"
```

### 3.4 Search Issues

```bash
# Search Issues
gh search issues "login bug"

# Search in specified repository
gh search issues "login bug" --repo owner/repo

# Search open Issues
gh search issues "login" --state open

# Search by label
gh search issues --label "bug"

# Search by author
gh search issues --author username

# Combined search
gh search issues "login" --label "bug" --state open --sort created
```

---

## 4. Pull Request Management (gh pr)

### 4.1 View PRs

```bash
# List current repository's PRs
gh pr list

# List specified repository's PRs
gh pr list --repo owner/repo

# Filter by status
gh pr list --state open
gh pr list --state closed
gh pr list --state merged
gh pr list --state all

# Filter by branch
gh pr list --head feature-branch
gh pr list --base main

# Filter by author
gh pr list --author username

# Filter by label
gh pr list --label "needs-review"

# View specific PR
gh pr view 456

# Open PR in browser
gh pr view 456 --web

# View PR comments
gh pr view 456 --comments

# View PR diff
gh pr diff 456

# View PR check status
gh pr checks 456

# View in JSON format
gh pr view 456 --json title,body,state,mergeable,reviews
```

### 4.2 Create PRs

```bash
# Create PR interactively
gh pr create

# Quick create PR
gh pr create \
  --title "feat: Add user login feature" \
  --body "## Changes\n\n- Implement user login\n- Add login page"

# Specify base branch
gh pr create --base main --head feature-branch

# Set as draft PR
gh pr create --draft

# Add reviewers
gh pr create --reviewer reviewer1,reviewer2

# Add assignee
gh pr create --assignee username

# Add labels
gh pr create --label "feature,needs-review"

# Add to project
gh pr create --project "My Project"

# Set milestone
gh pr create --milestone "v1.0"

# Auto-fill commit messages
gh pr create --fill

# Create PR from Issue (associate Issue)
gh pr create --body "Closes #123"

# Read body from file
gh pr create --body-file pr-template.md
```

### 4.3 Manage PRs

```bash
# Checkout PR locally
gh pr checkout 456

# Checkout PR to specified branch
gh pr checkout 456 --branch my-branch

# Merge PR
gh pr merge 456

# Merge using squash
gh pr merge 456 --squash

# Merge using merge commit
gh pr merge 456 --merge

# Merge using rebase
gh pr merge 456 --rebase

# Merge and delete branch
gh pr merge 456 --squash --delete-branch

# Merge and auto-fill merge message
gh pr merge 456 --squash --auto

# Close PR
gh pr close 456

# Close and add comment
gh pr close 456 --comment "Not merging for now"

# Reopen PR
gh pr reopen 456

# Edit PR
gh pr edit 456 --title "New title"
gh pr edit 456 --body "New description"
gh pr edit 456 --add-reviewer reviewer1
gh pr edit 456 --remove-label "wip"
gh pr edit 456 --add-assignee username

# Mark PR as ready
gh pr ready 456

# Mark PR as draft
gh pr ready 456 --undo

# Lock PR
gh pr lock 456

# Unlock PR
gh pr unlock 456

# Add review comment
gh pr review 456 --approve
gh pr review 456 --request-changes --body "Please fix the following issues..."
gh pr review 456 --comment --body "Looks good"
```

### 4.4 PR Status and Checks

```bash
# View PR status
gh pr status

# View all PR statuses
gh pr status --repo owner/repo

# View PR check results
gh pr checks 456

# Wait for checks to complete
gh pr checks 456 --watch

# View PR merge status
gh pr view 456 --json mergeable,mergeStateStatus

# View PR review status
gh pr view 456 --json reviews
```

### 4.5 Search PRs

```bash
# Search PRs
gh search prs "login feature"

# Search in specified repository
gh search prs "login" --repo owner/repo

# Search open PRs
gh search prs "login" --state open

# Search by author
gh search prs --author username

# Search by reviewer
gh search prs --reviewer username

# Search by label
gh search prs --label "needs-review"
```

---

## 5. Release Management (gh release)

### 5.1 View Releases

```bash
# List all Releases
gh release list

# List specified repository's Releases
gh release list --repo owner/repo

# Limit quantity
gh release list --limit 10

# View latest Release
gh release view

# View specified Release
gh release view v1.0.0

# Open Release in browser
gh release view v1.0.0 --web

# View in JSON format
gh release view v1.0.0 --json tagName,name,body,assets

# View only tag name
gh release view v1.0.0 --json tagName --jq '.tagName'

# View Release Assets
gh release view v1.0.0 --json assets
```

### 5.2 Create Releases

```bash
# Create simple Release
gh release create v1.0.0

# Create Release with title and notes
gh release create v1.0.0 \
  --title "v1.0.0 Official Version" \
  --notes "First official release version"

# Read notes from file
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes-file RELEASE_NOTES.md

# Auto-generate Release Notes
gh release create v1.0.0 --generate-notes

# Create Draft Release
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "Ready to release" \
  --draft

# Create Pre-release
gh release create v1.0.0-beta.1 \
  --title "v1.0.0 Beta 1" \
  --notes "Test version, do not use in production" \
  --prerelease

# Create Release and upload files
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "Official release" \
  ./dist/app-linux \
  ./dist/app-macos \
  ./dist/app-windows.exe

# Upload files using wildcard
gh release create v1.0.0 ./dist/*

# Specify target branch
gh release create v1.0.0 --target main

# Create discussion for Release
gh release create v1.0.0 --discussion-category "Announcements"

# Use notes template
gh release create v1.0.0 \
  --notes "**🚀 New Features**\n\n- Feature 1\n- Feature 2\n\n**🐛 Fixes**\n\n- Bug 1"
```

### 5.3 Manage Releases

```bash
# Edit Release
gh release edit v1.0.0 --title "v1.0.0 - Official Version"
gh release edit v1.0.0 --notes "Updated notes"
gh release edit v1.0.0 --notes-file NEW_NOTES.md

# Publish draft as official
gh release edit v1.0.0 --draft=false

# Mark as pre-release
gh release edit v1.0.0 --prerelease

# Remove pre-release mark
gh release edit v1.0.0 --prerelease=false

# Add files to Release
gh release upload v1.0.0 ./new-asset.zip

# Upload multiple files
gh release upload v1.0.0 ./file1.zip ./file2.tar.gz

# Replace existing file
gh release upload v1.0.0 ./app-linux --clobber

# Delete Release file
gh release delete-asset v1.0.0 old-file.zip --yes

# Download Release files
gh release download v1.0.0

# Download to specified directory
gh release download v1.0.0 --dir ./downloads

# Download specific files
gh release download v1.0.0 --pattern "*.zip"

# Download platform-specific files
gh release download v1.0.0 --pattern "*linux*"

# Delete Release
gh release delete v1.0.0 --yes
```

### 5.4 Download Latest Release

```bash
# Download latest Release
gh release download --pattern "*.tar.gz"

# Download latest Release to specified directory
gh release download --dir ./latest --pattern "app-*"

# Download only checksum file
gh release download --pattern "checksums*"
```

---

## 6. GitHub Actions Management

### 6.1 View Workflows (gh workflow)

```bash
# List all workflows
gh workflow list

# View workflow details
gh workflow view deploy.yml

# View workflow runs
gh workflow view deploy.yml --yaml

# Enable workflow
gh workflow enable deploy.yml

# Disable workflow
gh workflow disable deploy.yml

# Manually trigger workflow
gh workflow run deploy.yml

# Manually trigger with parameters
gh workflow run deploy.yml --ref main -f environment=production -f version=1.0.0

# Open workflow in browser
gh workflow view deploy.yml --web
```

### 6.2 View Run Records (gh run)

```bash
# List recent runs
gh run list

# List specified workflow's runs
gh run list --workflow=deploy.yml

# Filter by status
gh run list --status=completed
gh run list --status=failure
gh run list --status=in_progress

# Limit quantity
gh run list --limit 20

# View specific run
gh run view 1234567890

# View run's jobs
gh run view 1234567890 --json jobs

# View run logs
gh run view 1234567890 --log

# View specific job logs
gh run view 1234567890 --job=job-id --log

# Open run in browser
gh run view 1234567890 --web

# View run status
gh run status 1234567890

# Wait for run to complete
gh run watch 1234567890

# Re-run failed jobs
gh run rerun 1234567890 --failed

# Re-run entire workflow
gh run rerun 1234567890

# Cancel running workflow
gh run cancel 1234567890

# Download run artifacts
gh run download 1234567890

# Download specific artifact
gh run download 1234567890 --name my-artifact

# Download to specified directory
gh run download 1234567890 --dir ./artifacts
```

### 6.3 View Secrets and Variables

```bash
# List repository Secrets
gh secret list

# List environment Secrets
gh secret list --env production

# List organization Secrets
gh secret list --org my-org

# Set repository Secret
gh secret set MY_SECRET --body "secret-value"

# Set Secret from file
gh secret set MY_SECRET --body-file secret.txt

# Set environment Secret
gh secret set MY_SECRET --env production --body "value"

# Delete Secret
gh secret delete MY_SECRET

# List Variables
gh variable list

# Set Variable
gh variable set MY_VAR --body "variable-value"

# Delete Variable
gh variable delete MY_VAR
```

---

## 7. GitHub Codespaces Management (gh codespace)

### 7.1 Basic Operations

```bash
# List Codespaces
gh codespace list

# Create Codespace
gh codespace create --repo owner/repo

# Create with specified machine type
gh codespace create --repo owner/repo --machine largePremiumLinux

# Create with specified branch
gh codespace create --repo owner/repo --branch develop

# View Codespace info
gh codespace view codespace-name

# Open Codespace in browser
gh codespace codespace codespace-name

# Delete Codespace
gh codespace delete codespace-name --yes

# Stop Codespace
gh codespace stop codespace-name
```

### 7.2 Remote Connection

```bash
# Connect to Codespace via SSH
gh codespace ssh codespace-name

# Connect using VS Code
gh codespace code codespace-name

# Connect using Jupyter Notebook
gh codespace jupyter codespace-name

# Forward port
gh codespace ports forward 8080:80 codespace-name

# View port list
gh codespace ports list codespace-name

# Set port visibility
gh codespace ports visibility 8080:public codespace-name
```

### 7.3 File Operations

```bash
# Copy file from Codespace to local
gh codespace cp codespace-name:/path/to/file ./local-file

# Copy file from local to Codespace
gh codespace cp ./local-file codespace-name:/path/to/file
```

---

## 8. gh api Advanced Usage

### 8.1 Basic API Calls

```bash
# GET request
gh api repos/owner/repo

# POST request
gh api repos/owner/repo/issues -f title="Bug" -f body="Problem description"

# PATCH request
gh api repos/owner/repo/issues/123 -f state="closed"

# DELETE request
gh api repos/owner/repo/issues/123 -X DELETE

# Specify API version
gh api --method GET repos/owner/repo
```

### 8.2 Request Parameters

```bash
# Add query parameters
gh api "repos/owner/repo/issues?state=open&per_page=10"

# Add request body fields
gh api repos/owner/repo/issues \
  -f title="Issue Title" \
  -f body="Issue Body" \
  -f "labels[]=bug" \
  -f "labels[]=priority:high"

# Add request headers
gh api repos/owner/repo \
  -H "Accept: application/vnd.github.v3+json"

# Read request body from file
gh api repos/owner/repo/issues --input issue.json

# Use JSON format
gh api repos/owner/repo/issues \
  --method POST \
  --input - <<EOF
{
  "title": "Bug Report",
  "body": "Describe problem",
  "labels": ["bug"]
}
EOF
```

### 8.3 Response Processing

```bash
# Output in JSON format
gh api repos/owner/repo --jq '.name'

# Extract specific fields
gh api repos/owner/repo --jq '.full_name, .description'

# Format output
gh api repos/owner/repo --jq '{name: .name, desc: .description}'

# List processing
gh api repos/owner/repo/issues --jq '.[].title'

# Get paginated data
gh api --paginate repos/owner/repo/issues

# Limit pagination quantity
gh api --paginate repos/owner/repo/issues --per-page 5

# Get all pages (auto-handle pagination)
gh api --paginate "repos/owner/repo/contributors" --jq '.[].login'
```

### 8.4 GraphQL Queries

```bash
# GraphQL query
gh api graphql -f query='
{
  repository(owner: "owner", name: "repo") {
    name
    description
    stargazerCount
  }
}
'

# GraphQL with variables
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    name
    pullRequests(first: 10, states: OPEN) {
      nodes {
        title
        author {
          login
        }
      }
    }
  }
}
' -f owner="owner" -f repo="repo"

# Get current user info
gh api graphql -f query='{ viewer { login name email } }'

# Get repository's Issues (using GraphQL)
gh api graphql -f query='
{
  repository(owner: "owner", name: "repo") {
    issues(first: 10, states: OPEN) {
      nodes {
        number
        title
        createdAt
      }
    }
  }
}
'
```

### 8.5 Common API Endpoints

```bash
# Get current user
gh api user

# Get user's repositories
gh api users/username/repos

# Get repository's Issues
gh api repos/owner/repo/issues

# Get repository's PRs
gh api repos/owner/repo/pulls

# Get repository's Releases
gh api repos/owner/repo/releases

# Get repository's Tags
gh api repos/owner/repo/tags

# Get repository's Contributors
gh api repos/owner/repo/contributors

# Get repository's Languages
gh api repos/owner/repo/languages

# Get repository's Workflows
gh api repos/owner/repo/actions/workflows

# Get Workflow's Runs
gh api repos/owner/repo/actions/workflows/deploy.yml/runs

# Get user's Notifications
gh api notifications

# Get user's Organizations
gh api user/orgs

# Get Organization's Members
gh api orgs/my-org/members

# Get team info
gh api orgs/my-org/teams
```

---

## 9. gh Alias Custom Aliases

### 9.1 Create Aliases

```bash
# Create simple command alias
gh alias set pv 'pr view'

# Use alias
gh pv 123  # Equivalent to gh pr view 123

# Create alias with parameters
gh alias set prs 'pr list --state=open --author=@me'

# Use alias
gh prs  # List your own open PRs

# Create complex alias (using shell commands)
gh alias set my-repos 'api user/repos --jq ".[].full_name"'

# Create multi-line alias
gh alias set my-status '!gh pr status && echo "---" && gh issue list --assignee=@me'

# Create alias with parameter substitution
gh alias set pr-info '!f() { gh pr view $1 --json title,body,state; }; f'

# Use environment variables
gh alias set whoami 'api user --jq ".login"'
```

### 9.2 Manage Aliases

```bash
# List all aliases
gh alias list

# Delete alias
gh alias delete pv

# Edit alias configuration file
gh alias edit

# Export aliases
gh alias list > aliases.txt

# Import aliases (from configuration file)
# Edit ~/.config/gh/config.yml
```

### 9.3 Practical Alias Examples

```bash
# Quick view your PRs
gh alias set my-prs 'pr list --author=@me --state=open'

# Quick view PRs needing review
gh alias set review-prs 'pr list --reviewer=@me --state=open'

# Quick view Issues assigned to you
gh alias set my-issues 'issue list --assignee=@me --state=open'

# Quick merge PR (squash)
gh alias set pr-merge-squash '!f() { gh pr merge $1 --squash --delete-branch; }; f'

# Quick create Issue
gh alias set bug '!f() { gh issue create --title "$1" --body "$2" --label bug; }; f'

# Quick view repository info
gh alias set repo-info 'api repos/{owner}/{repo} --jq "{name: .name, stars: .stargazers_count, forks: .forks_count}"'

# Batch close Issues
gh alias set close-all '!gh issue list --state=open --json number --jq ".[].number" | xargs -I {} gh issue close {}'

# Quick view workflow status
gh alias set wf-status 'run list --limit=5 --json name,status,conclusion --jq ".[] | \"\(.name): \(.status) - \(.conclusion)\""'

# Quick fork and clone
gh alias set fork-clone '!f() { gh repo fork $1 --clone; }; f'

# View repository contributors
gh alias set contributors 'api repos/{owner}/{repo}/contributors --jq ".[] | \"\(.login): \(.contributions) commits\""'
```

---

## 10. gh Extension System

### 10.1 What are gh Extensions

gh Extensions are command line tools written in any programming language that can seamlessly integrate into gh. Extension naming format is `gh-<name>`.

### 10.2 Manage Extensions

```bash
# Browse available extensions
gh extension list

# Install extension
gh extension install owner/gh-extension-name

# Install from specific branch
gh extension install owner/gh-extension-name --branch main

# Upgrade extension
gh extension upgrade gh-extension-name

# Upgrade all extensions
gh extension upgrade --all

# Uninstall extension
gh extension remove gh-extension-name

# View extension info
gh extension browse gh-extension-name
```

### 10.3 Recommended Extensions

```bash
# gh-dash - Terminal dashboard
gh extension install dlvhdr/gh-dash

# gh-copilot - AI assistant
gh extension install github/gh-copilot

# gh-poi - Clean merged branches
gh extension install seachicken/gh-poi

# gh-notify - Notification management
gh extension install meiji163/gh-notify

# gh-stars - Starred repository management
gh extension install gaowei2/gh-stars

# gh-user-status - User status
gh extension install vilmibm/gh-user-status

# gh-repo-explore - Repository browsing
gh extension install samcoe/gh-repo-explore

# gh-actions-cache - Actions cache management
gh extension install actions/gh-actions-cache

# gh-eco - Ecosystem browsing
gh extension install github/gh-eco
```

### 10.4 Create Your Own Extension

```bash
# Create bash extension
cat > gh-hello << 'EOF'
#!/bin/bash
# gh hello - Greeting extension
echo "Hello from gh extension!"
echo "Arguments: $@"
EOF
chmod +x gh-hello

# Install local extension
gh extension install .

# Test extension
gh hello world

# Create Go extension (using gh library)
# Reference: https://github.com/cli/go-gh

# Publish extension
# 1. Create public repository named gh-<name>
# 2. Push code
# 3. Other users can install via gh extension install owner/gh-<name>
```

---

## 11. gh and Git Command Coordination

### 11.1 Repository Clone and Initialization

```bash
# Clone using gh (supports shorthand)
gh clone owner/repo  # Equivalent to git clone https://github.com/owner/repo.git

# Fork and clone
gh repo fork owner/repo --clone

# Sync fork
gh repo sync

# Create repository and push
gh repo create my-project --public --source=. --push
```

### 11.2 Branch Management Coordination

```bash
# Create branch and push
git checkout -b feature/new-feature
git push -u origin feature/new-feature
gh pr create  # Directly create PR

# Checkout PR branch
gh pr checkout 123
# This automatically creates local branch and switches

# Cleanup after PR merge
gh pr merge 123 --squash --delete-branch
# Automatically deletes remote and local branches
```

### 11.3 Commit and PR Association

```bash
# Reference Issue in commit message
git commit -m "fix: Fix login issue

Closes #123"

# Push and create PR
git push origin feature/fix-login
gh pr create --body "Closes #123"

# Use gh auto-association
gh pr create --fill-first  # Use first commit as PR title
```

### 11.4 Workflow Example

```bash
# Complete feature branch workflow

# 1. Sync main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-auth

# 3. Develop and commit
git add .
git commit -m "feat: Implement user authentication module"

# 4. Push branch
git push -u origin feature/user-auth

# 5. Create PR
gh pr create \
  --title "feat: User authentication feature" \
  --body "## Changes\n\n- Implement login/registration\n- Add JWT verification\n\nCloses #45" \
  --reviewer team-lead \
  --label "feature,needs-review"

# 6. View PR status
gh pr status

# 7. Wait for review and CI
gh pr checks 456 --watch

# 8. Merge PR
gh pr merge 456 --squash --delete-branch

# 9. Update local
git checkout main
git pull origin main
git branch -d feature/user-auth
```

---

## 12. Practical Scenarios and Tips

### 12.1 Quick Create Issue Template

```bash
# Create Issue template
gh alias set bug-report '!f() {
  gh issue create \
    --title "Bug: $1" \
    --body "## Problem Description\n\n$1\n\n## Steps to Reproduce\n\n1. \n2. \n3. \n\n## Expected Behavior\n\n\n\n## Actual Behavior\n\n\n\n## Environment Info\n\n- OS: \n- Browser: \n- Version: " \
    --label "bug"
}; f'

# Use
gh bug-report "Login page cannot load"
```

### 12.2 Batch Operations

```bash
# Batch close expired Issues (no activity for 30+ days)
gh issue list --state=open --json number,updatedAt --jq '
  .[] | select((now - (.updatedAt | fromdate)) > 2592000) | .number
' | xargs -I {} gh issue close {} --comment "Auto-closed: no activity for 30+ days"

# Batch add labels
gh issue list --state=open --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "triage"

# Batch download Release Assets
gh release list --json tagName --jq '.[].tagName' | \
  xargs -I {} gh release download {} --pattern "*.zip" --dir ./downloads/{}
```

### 12.3 Monitoring and Notifications

```bash
# Create PR status check script
#!/bin/bash
echo "=== My PR Status ==="
gh pr list --author=@me --json number,title,statusCheckRollup --jq '
  .[] | "\(.number) \(.title) - \(if .statusCheckRollup | length > 0 then .statusCheckRollup[0].conclusion else "pending" end)"
'

echo ""
echo "=== PRs Needing Review ==="
gh pr list --reviewer=@me --json number,title --jq '.[] | "\(.number) \(.title)"'

echo ""
echo "=== My Issues ==="
gh issue list --assignee=@me --json number,title --jq '.[] | "\(.number) \(.title)"'
```

### 12.4 Automation Scripts

```bash
# Daily report script
#!/bin/bash
DATE=$(date +%Y-%m-%d)
REPORT="daily-report-$DATE.md"

{
  echo "# Daily Development Report - $DATE"
  echo ""
  echo "## Today's Merged PRs"
  gh search prs --merged=$(date +%Y-%m-%d) --author=@me --json number,title --jq '.[] | "- #\(.number) \(.title)"'
  echo ""
  echo "## Today's Created Issues"
  gh search issues --created=$(date +%Y-%m-%d) --author=@me --json number,title --jq '.[] | "- #\(.number) \(.title)"'
  echo ""
  echo "## Pending PRs"
  gh pr list --reviewer=@me --state=open --json number,title --jq '.[] | "- #\(.number) \(.title)"'
} > $REPORT

echo "Report generated: $REPORT"
```

### 12.5 Configuration Files

```bash
# View configuration
gh config list

# Set default editor
gh config set editor vim
gh config set editor code  # VS Code

# Set default browser
gh config set browser firefox

# Set default protocol
gh config set git_protocol https

# Set default prompt
gh config set prompt enabled

# Set default alias
gh config set aliases.my-alias 'pr list --author=@me'

# Configuration file locations
# ~/.config/gh/config.yml
# ~/.config/gh/hosts.yml
```

---

## 13. Domestic Usage Notes

### 13.1 Network Problem Solutions

**Solution 1: Use proxy**

```bash
# Set HTTP proxy
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# Set gh proxy
gh config set http_proxy http://127.0.0.1:7890
gh config set https_proxy http://127.0.0.1:7890

# Or set in configuration file
# ~/.config/gh/config.yml
# http_proxy: http://127.0.0.1:7890
# https_proxy: http://127.0.0.1:7890
```

**Solution 2: Use ghproxy**

```bash
# Use ghproxy when cloning
gh repo clone owner/repo -- --config url."https://ghproxy.com/https://github.com/".insteadOf="https://github.com/"

# Or global configuration
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"
```

**Solution 3: Configure Git to use mirror**

```bash
# Use gitee mirror (if repository is mirrored)
git config --global url."https://gitee.com/".insteadOf "https://github.com/"

# Only configure for specific domain
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"
```

### 13.2 Token Configuration Tips

```bash
# Manually configure Token (avoid network issues)
# 1. Create Personal Access Token on GitHub website
#    Settings → Developer settings → Personal access tokens → Tokens (classic)
#    Permissions: repo, read:org, workflow

# 2. Login using Token
echo "ghp_your_token_here" | gh auth login --with-token

# 3. Or set environment variable
echo 'export GH_TOKEN=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc

# 4. Verify login status
gh auth status
```

### 13.3 Common Problem Troubleshooting

```bash
# Problem 1: Network connection timeout
# Solution: Use proxy or ghproxy

# Problem 2: Insufficient permissions
# Solution: Refresh Token permissions
gh auth refresh -s admin:org,repo,workflow

# Problem 3: API rate limit
# Solution: Use authenticated Token (higher limit for authenticated users)
gh api rate_limit

# Problem 4: SSH connection issues
# Solution: Use HTTPS protocol
gh config set git_protocol https

# Problem 5: Certificate issues
# Solution: Configure Git to skip SSL verification (not recommended for production)
git config --global http.sslVerify false
```

### 13.4 Domestic Alternatives

If gh really cannot be used, consider:

```bash
# 1. Use GitHub API directly
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo

# 2. Use GitLab CLI (glab)
# GitLab is relatively stable domestically
brew install glab

# 3. Use Gitee API
# If project is hosted on Gitee
curl https://gitee.com/api/v5/repos/owner/repo

# 4. Use FastGit mirror
# https://hub.fastgit.xyz/
```

### 13.5 Best Practices

```bash
# 1. Always use Token authentication (more secure than password)
gh auth login --with-token < token.txt

# 2. Regularly refresh Token
gh auth refresh

# 3. Use ghproxy for acceleration
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"

# 4. Configure proxy
export HTTPS_PROXY=http://127.0.0.1:7890

# 5. Use SSH protocol (if SSH is available)
gh config set git_protocol ssh

# 6. Cache authentication info
gh auth setup-git

# 7. Use gh's --json output to reduce API calls
gh pr list --json number,title,state

# 8. Use cache to reduce API calls
gh api repos/owner/repo --cache 1h
```

---

## Summary

This chapter comprehensively introduces GitHub CLI (gh) usage methods:

1. **Installation Configuration**: Official and domestic multiple installation solutions
2. **Basic Commands**: Authentication, repository, browser operations
3. **Issue Management**: Create, view, update, search Issues
4. **PR Management**: Complete Pull Request workflow
5. **Release Management**: Create and manage release versions
6. **Actions Management**: Workflow and run monitoring
7. **Codespaces Management**: Cloud development environment operations
8. **API Advanced Usage**: REST and GraphQL calls
9. **Custom Aliases**: Efficiency-boosting commands
10. **Extension System**: Install and create extensions
11. **Git Coordination**: Collaboration with Git commands
12. **Practical Tips**: Batch operations, automation scripts
13. **Domestic Notes**: Network problems and alternatives

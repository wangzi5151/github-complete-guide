# Git Workflow Complete Guide

> This chapter provides a detailed introduction to various Git workflow patterns, helping teams choose the most suitable collaboration method.

## Table of Contents

- [What is Git Workflow](#what-is-git-workflow)
- [Centralized Workflow](#centralized-workflow)
- [Feature Branch Workflow](#feature-branch-workflow)
- [Git Flow Workflow Details](#git-flow-workflow-details)
- [GitHub Flow Workflow Details](#github-flow-workflow-details)
- [GitLab Flow Workflow Details](#gitlab-flow-workflow-details)
- [Trunk-Based Development](#trunk-based-development)
- [Forking Workflow](#forking-workflow)
- [Workflow Comparison and Selection Guide](#workflow-comparison-and-selection-guide)
- [Branch Naming Standards](#branch-naming-standards)
- [Commit Message Standards](#commit-message-standards)
- [Version Number Standards](#version-number-standards)
- [Release Management Strategy](#release-management-strategy)
- [Multi-person Collaboration Conflict Prevention](#multi-person-collaboration-conflict-prevention)
- [Chinese Internet Company Git Workflow Practices](#chinese-internet-company-git-workflow-practices)
- [Workflow Decision Flowcharts](#workflow-decision-flowcharts)

---

## What is Git Workflow

Git Workflow is a set of collaboration standards and best practices based on Git version control system. It defines standard processes for how team members create branches, merge code, release versions, and handle emergency fixes.

### Why Git Workflow is Needed

In multi-person collaborative development, without unified workflow standards, will cause the following problems:

1. **Frequent code conflicts**: Multiple people simultaneously modifying same file, conflicts difficult to resolve
2. **Version confusion**: Cannot clearly distinguish development versions, test versions and production versions
3. **Release difficulty**: Don't know which version can be released, which version is being tested
4. **Rollback difficulty**: Difficult to quickly locate and rollback when problems occur
5. **Low collaboration efficiency**: Team members work in silos, collaboration cost high

### Core Elements of Git Workflow

A complete Git workflow usually includes following elements:

| Element | Description |
|---------|-------------|
| Branch Strategy | How to create, name and manage branches |
| Merge Strategy | How to merge branch code to main branch |
| Release Strategy | How to manage version releases |
| Conflict Resolution | How to prevent and resolve code conflicts |
| Code Review | How to conduct code review |
| Continuous Integration | How to integrate with CI/CD tools |

### Evolution History of Git Workflow

Git workflow has evolved from simple to complex:

```
2005 ─── Git born
    │
2008 ─── GitHub launched, Fork workflow appears
    │
2010 ─── Git Flow released (Vincent Driessen)
    │
2011 ─── GitHub Flow proposed (Scott Chacon)
    │
2014 ─── GitLab Flow proposed
    │
2016 ─── Trunk-Based Development becomes popular
    │
2020 ─── Mainstream workflows mature and stabilize
```

---

## Centralized Workflow

Centralized Workflow is the simplest Git workflow, suitable for small teams or teams migrating from SVN.

### Working Principle

All developers work on the same branch (usually `main` or `master`), directly commit and pull code.

```
Developer A ──→ ┌─────────┐ ──→ Developer A
                 │  main   │
Developer B ──→ │  branch │ ──→ Developer B
                 └─────────┘
Developer C ──→              ──→ Developer C
```

### Basic Operation Flow

```bash
# 1. Clone repository
git clone https://github.com/team/project.git

# 2. Before starting work, pull latest code first
git pull origin main

# 3. Modify files
# ... Edit code ...

# 4. Commit changes
git add .
git commit -m "feat: Add user login feature"

# 5. Push to remote repository
git push origin main

# 6. If push fails (others have new commits), pull first then push
git pull --rebase origin main
git push origin main
```

### Advantages and Disadvantages Analysis

**Advantages:**
- Simple and easy to understand, low learning cost
- Suitable for small teams (2-3 people)
- Similar to SVN work style, low migration cost
- No need for complex branch management

**Disadvantages:**
- Cannot parallel develop multiple features
- Directly commit on main branch, easy to introduce bugs
- Cannot conduct code review
- Not suitable for continuous deployment

### Applicable Scenarios

- Personal projects
- Small teams of 2-3 people
- Initial stage of migrating from SVN to Git
- Simple internal tool development

### Common Problems and Solutions

#### Problem 1: Push Rejected

When multiple people simultaneously pushing code, may encounter push rejection:

```bash
# Error message
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'origin'

# Solution: Pull first then push
git pull --rebase origin main
git push origin main
```

#### Problem 2: Accidentally Committed Large File

If accidentally committed large file, need to remove from history:

```bash
# Find large files
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sed -n 's/^blob //p' | sort -rnk2 | head -10

# Clean large files using BFG
java -jar bfg.jar --strip-blobs-bigger-than 10M repo.git
```

#### Problem 3: Committed Sensitive Information

If committed passwords, keys and other sensitive information:

```bash
# Remove file from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch PATH-TO-FILE' \
  --prune-empty --tag-name-filter cat -- --all

# Use git-filter-repo (Recommended)
git-filter-repo --path PATH-TO-FILE --invert-paths
```

### Centralized Workflow Migration Strategy

When migrating from SVN to Git, can adopt gradual migration strategy:

```
Phase 1: Parallel Run (1-2 weeks)
    │
    ├─ Git repository creation completed
    ├─ Team members learn Git basic operations
    └─ SVN and Git used in parallel

Phase 2: Main Branch Switch (1 week)
    │
    ├─ Stop SVN commits
    ├─ All new code committed to Git
    └─ Retain SVN read-only access

Phase 3: Complete Migration (After 1 week)
    │
    ├─ SVN repository set to read-only
    ├─ Git becomes the only version control system
    └─ Establish Git workflow standards
```

---

## Feature Branch Workflow

Feature Branch Workflow is an improved version of centralized workflow, each new feature developed on independent branch.

### Working Principle

All new features, bug fixes are developed on independent feature branches, after completion merged back to main branch through Pull Request.

```
main ─────●───────●───────●───────●────→
           \     /         \     /
feature-1   ●───●           ●───●  feature-2
            Feature development   Feature development
```

### Branch Naming Standards

```bash
# Feature branches
feature/user-login
feature/user-login
feature/20240101-user-login

# Bug fix branches
bugfix/fix-login-error
bugfix/fix-login-error

# Hotfix branches
hotfix/urgent-fix-payment-vulnerability
```

### Complete Workflow

```bash
# 1. Create feature branch from main branch
git checkout main
git pull origin main
git checkout -b feature/user-login

# 2. Develop on feature branch
# ... Write code ...
git add .
git commit -m "feat: Implement user login feature"

# 3. Push feature branch to remote
git push origin feature/user-login

# 4. Create Pull Request (PR)
# Create PR on GitHub/GitLab, request code review

# 5. Merge after code review passes
# Can merge through GitHub/GitLab interface, or command line:
git checkout main
git pull origin main
git merge --no-ff feature/user-login
git push origin main

# 6. Delete feature branch
git branch -d feature/user-login
git push origin --delete feature/user-login
```

### Pull Request Workflow

Pull Request (PR) is the core of feature branch workflow, it enables:

1. **Code Review**: Team members can review code quality
2. **Discussion**: Discuss and improve code
3. **Automated Testing**: Integrate CI/CD for automated testing
4. **Documentation**: PR records the feature implementation process

### PR Template Example

```markdown
## Feature Description
Implement user login feature, support username/email login.

## Implementation
- Use JWT for authentication
- Password encrypted with bcrypt
- Support remember login status

## Testing
- [x] Unit tests passed
- [x] Integration tests passed
- [x] Manual tests passed

## Related Issues
Closes #123
```

### Advantages and Disadvantages Analysis

**Advantages:**
- Each feature developed independently, without affecting each other
- Supports code review, improves code quality
- Supports parallel development of multiple features
- Facilitates continuous integration and deployment

**Disadvantages:**
- Branch management relatively complex
- If feature branch lifecycle too long, many conflicts when merging
- Need team members to follow branch standards

### Applicable Scenarios

- Small to medium teams (3-10 people)
- Projects needing code review
- Continuous integration/continuous deployment projects
- Most Web application development

### Feature Branch Workflow Best Practices

#### 1. Keep Branch Short Lifecycle

Feature branches should complete within 1-3 days, avoid long-existing branches:

```bash
# Bad practice: Branch exists for weeks
git checkout -b feature/massive-refactor
# ... Develop for weeks ...

# Good practice: Split into multiple small features
git checkout -b feature/user-login      # 1-2 days to complete
git checkout -b feature/user-profile    # 1-2 days to complete
git checkout -b feature/user-settings   # 1-2 days to complete
```

#### 2. Frequently Sync Main Branch

Regularly merge main branch's latest code to feature branch, reduce final merge conflicts:

```bash
# Regularly sync main branch on feature branch
git checkout feature/my-feature
git fetch origin
git rebase origin/main

# Or use merge
git merge origin/main
```

#### 3. Use Draft Pull Request

For unfinished features, can create Draft PR for early feedback:

```bash
# Create Draft PR on GitHub
# 1. Push feature branch
git push origin feature/my-feature

# 2. Create PR on GitHub, select "Create draft pull request"

# 3. Mark as Ready for review after completion
```

#### 4. Automated Branch Cleanup

Use scripts to automatically clean merged branches:

```bash
#!/bin/bash
# clean-merged-branches.sh

# Delete merged local branches
git branch --merged main | grep -v "main" | xargs -n 1 git branch -d

# Delete merged remote branches
git branch -r --merged main | grep -v "main" | sed 's/origin\///' | xargs -n 1 git push origin --delete
```

### Feature Branch Workflow Common Pitfalls

| Pitfall | Problem Description | Solution |
|---------|---------------------|----------|
| Branch lifecycle too long | Many conflicts when merging, difficult code review | Split features, short cycle development |
| Not syncing main branch | Massive conflicts when finally merging | Regularly rebase or merge main branch |
| Lack of code review | Code quality cannot be guaranteed | Enforce PR review process |
| Branch naming chaotic | Difficult to identify branch purpose | Unified naming standards |
| Not deleting merged branches | Branch list chaotic | Delete branch immediately after merge

---

## Git Flow Workflow Details

Git Flow is a branch management model proposed by Vincent Driessen in 2010, one of the most classic Git workflows.

### Branch Types

Git Flow defines five branch types:

| Branch Type | Naming Rule | Lifecycle | Usage |
|-------------|-------------|-----------|-------|
| master | master | Permanent | Production environment code |
| develop | develop | Permanent | Main development branch |
| feature/* | feature/xxx | Temporary | New feature development |
| release/* | release/x.x.x | Temporary | Version release preparation |
| hotfix/* | hotfix/xxx | Temporary | Emergency fix |

### Branch Structure Diagram

```
master    ──●───────────────●───────────────●──→
              \             ↑               ↑
               \           /               /
hotfix          \         /               /
                 \       /               /
release           ●─────●               /
                  ↑     \             /
                  │      \           /
develop    ───────●───────●─────●────●──────→
                  ↑       ↑     ↑
                  │       │     │
feature-1         ●───────●     │
                                 │
feature-2                ●───────●
```

### Detailed Workflow

#### 1. Initialize Git Flow

```bash
# Install git-flow tool
# macOS
brew install git-flow

# Linux (Ubuntu/Debian)
sudo apt-get install git-flow

# Initialize Git Flow
git flow init

# Set branch names according to prompts:
# Production branch: master
# Development branch: develop
# Feature branches: feature/
# Release branches: release/
# Hotfix branches: hotfix/
# Support branches: support/
# Version tag prefix: v
```

#### 2. Feature Development Flow

```bash
# Start new feature
git flow feature start user-login

# This will automatically create and switch to feature/user-login branch

# Develop on feature branch
# ... Write code ...
git add .
git commit -m "feat: Implement user login feature"

# Complete feature, merge to develop
git flow feature finish user-login

# This will automatically:
# 1. Merge feature/user-login to develop
# 2. Delete feature/user-login branch
# 3. Switch back to develop branch

# If need collaboration, can publish feature branch
git flow feature publish user-login

# Or pull remote feature branch
git flow feature pull origin user-login
```

#### 3. Version Release Flow

```bash
# Start version release
git flow release start 1.0.0

# This will automatically create release/1.0.0 branch

# Make final fixes and adjustments on release branch
# ... Fix bugs ...
git add .
git commit -m "fix: Fix login page style issue"

# Update version number
echo "1.0.0" > VERSION

# Complete version release
git flow release finish 1.0.0

# This will automatically:
# 1. Merge release/1.0.0 to master
# 2. Create tag v1.0.0 on master
# 3. Merge release/1.0.0 to develop
# 4. Delete release/1.0.0 branch
```

#### 4. Emergency Fix Flow

```bash
# Start emergency fix
git flow hotfix start fix-payment-bug

# This will automatically create hotfix/fix-payment-bug branch from master

# Fix bug
# ... Fix code ...
git add .
git commit -m "fix: Fix payment verification vulnerability"

# Complete emergency fix
git flow hotfix finish fix-payment-bug

# This will automatically:
# 1. Merge hotfix/fix-payment-bug to master
# 2. Create tag on master (e.g., v1.0.1)
# 3. Merge hotfix/fix-payment-bug to develop
# 4. Delete hotfix/fix-payment-bug branch
```

### Git Flow Advantages and Disadvantages

**Advantages:**
- Clear branch roles, clear responsibilities
- Suitable for projects with clear release cycles
- Supports multi-version parallel maintenance
- Detailed documentation and tool support

**Disadvantages:**
- Large number of branches, complex management
- Cumbersome merge process
- Not suitable for continuous deployment
- May be overly complex for small projects

### Applicable Scenarios

- Software products with fixed release cycles
- Enterprise applications needing to maintain multiple versions
- Large team collaborative development
- Traditional software development model

### Git Flow Practical Application Cases

#### Case 1: Enterprise ERP System

An enterprise ERP system adopts Git Flow workflow, version release cycle is 2 weeks:

```
Timeline:
Week 1-2: Feature development
    │
    ├─ feature/user-management development
    ├─ feature/report-export development
    └─ feature/data-visualization development

Week 3: Version release preparation
    │
    ├─ Create release/2.1.0 branch
    ├─ Testing and bug fixing
    └─ Documentation update

Week 4: Official release
    │
    ├─ Merge to master
    ├─ Create tag v2.1.0
    ├─ Deploy to production environment
    └─ Merge back to develop
```

#### Case 2: Mobile Application Development

A mobile application adopts Git Flow, each version corresponds to an app store version:

```bash
# Version release flow
git flow release start 3.2.0

# Fix issues found in testing
git commit -am "fix: Fix iOS 16 compatibility issue"

# Update version number
echo "3.2.0" > VERSION
git commit -am "chore: Update version number to 3.2.0"

# Complete release
git flow release finish 3.2.0

# Push to remote
git push origin master --tags
git push origin develop
```

### Git Flow Tool Recommendations

#### 1. git-flow Tool

```bash
# Install git-flow
# macOS
brew install git-flow

# Linux
apt-get install git-flow

# Windows (via Chocolatey)
choco install gitflow

# Initialize
git flow init

# Common commands
git flow feature start <name>
git flow feature finish <name>
git flow release start <version>
git flow release finish <version>
git flow hotfix start <name>
git flow hotfix finish <name>
```

#### 2. GitKraken

GitKraken is a graphical Git client with built-in Git Flow support:

- Visual branch structure
- One-click creation of Git Flow branches
- Drag and drop merge branches
- Visual conflict resolution

#### 3. SourceTree

SourceTree is a Git client produced by Atlassian:

- Built-in Git Flow support
- Visual branch management
- Jira integration
- Supports Windows and macOS

### Git Flow Variants

#### 1. Simplified Git Flow

For small teams, can simplify Git Flow:

```
main    ──●───────●───────●──→
           \     /         \
develop     ●───●───────●───●──→
             ↑       ↑       ↑
             │       │       │
            feat    feat    feat
```

#### 2. Git Flow with Support Branches

For projects needing long-term support of multiple versions:

```
main    ──●───────●───────●───────●──→
           \               ↑       ↑
support-1   ●───────●──────●       │
            ↑       ↑               │
            │       │               │
hotfix     fix     fix             │
                                    │
main    ────────────────────────────●──→
                                    ↑
support-2   ●───────●───────●──────●
            ↑       ↑       ↑
            │       │       │
           feat    feat    feat
```

---

## GitHub Flow Workflow Details

GitHub Flow is a lightweight workflow proposed by GitHub, emphasizing simplicity and continuous deployment.

### Core Principles

1. **Main branch always deployable**: Code on `main` branch can be released to production at any time
2. **All work on feature branches**: New features, bug fixes on independent branches
3. **Merge through PR**: All code changes merged through Pull Request
4. **Deploy immediately after merge**: Should deploy to production as soon as possible after PR merge

### Workflow Diagram

```
main    ──●───────●───────●───────●───────●──→
           \     /         \     /         \
feature-1   ●───●           │               │
                            │               │
feature-2           ●───────●               │
                                            │
bugfix                              ●───────●
```

### Complete Workflow

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-search

# 2. Develop and commit
# ... Write code ...
git add .
git commit -m "feat: Add search feature"

# 3. Push to remote
git push origin feature/add-search

# 4. Create Pull Request
# Create PR on GitHub, fill in description

# 5. Code review and discussion
# Team members review code, propose modification suggestions

# 6. Fix review comments
# ... Modify code ...
git add .
git commit -m "fix: Modify search logic according to review comments"
git push origin feature/add-search

# 7. Merge after review passes
# Click "Merge pull request" on GitHub

# 8. Deploy to production
# Auto or manual deployment after merge

# 9. Delete feature branch
git branch -d feature/add-search
git push origin --delete feature/add-search
```

### GitHub Flow Features

**Continuous Deployment Friendly:**
- Deploy immediately after merge
- Small batch releases, reduce risk
- Quick feedback, quick iteration

**Code Review as Core:**
- All changes go through PR
- Supports line-level comments
- Supports suggested modifications
- Automated check integration

### Advantages and Disadvantages Analysis

**Advantages:**
- Simple and easy to understand, low learning cost
- Suitable for continuous deployment
- Code quality guaranteed
- Quick iteration

**Disadvantages:**
- Not suitable for projects needing multi-version maintenance
- High requirements for main branch stability
- Needs complete automated testing support

### Applicable Scenarios

- SaaS products
- Continuously deployed Web applications
- Small to medium teams
- Agile development projects

### GitHub Flow Automation Configuration

#### 1. GitHub Actions Configuration

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Run linting
        run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Deploy script
```

#### 2. Automated Deployment Script

```bash
#!/bin/bash
# deploy.sh

set -e

echo "Starting deployment..."

# Pull latest code
git pull origin main

# Install dependencies
npm ci

# Run tests
npm test

# Build project
npm run build

# Deploy to server
rsync -avz --delete dist/ user@server:/var/www/app/

# Restart service
ssh user@server "sudo systemctl restart nginx"

echo "Deployment completed!"
```

#### 3. Branch Protection Configuration

```yaml
# .github/settings.yml
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - ci/test
          - ci/build
      enforce_admins: true
      restrictions:
        users: []
        teams:
          - maintainers
```

### GitHub Flow Team Collaboration Tips

#### 1. Use Issue Tracking Tasks

```markdown
## Issue Template

### Problem Description
Briefly describe problem or requirement.

### Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

### Expected Behavior
Describe expected behavior.

### Actual Behavior
Describe actual behavior.

### Environment Information
- Operating System:
- Browser:
- Version:
```

#### 2. Use Project Management Tasks

GitHub Projects can help team manage tasks:

- Board view: To Do → In Progress → Done
- Automation: Auto-move tasks after PR merge
- Filter and sort: Filter by priority, assignee

#### 3. Use CODEOWNERS

```bash
# .github/CODEOWNERS

# Default owners
*       @team-lead

# Frontend code
/src/frontend/    @frontend-team

# Backend code
/src/backend/     @backend-team

# Documentation
/docs/            @doc-team

# CI/CD configuration
/.github/         @devops-team
```

### GitHub Flow Integration with GitHub Features

| GitHub Feature | Usage | Configuration Location |
|----------------|-------|------------------------|
| Issues | Task tracking | Repository → Issues |
| Pull Requests | Code review | Repository → Pull Requests |
| Projects | Project management | Repository → Projects |
| Actions | CI/CD | Repository → Actions |
| Discussions | Team discussion | Repository → Discussions |
| Wiki | Documentation management | Repository → Wiki |
| Security | Security scanning | Repository → Security |

---

## GitLab Flow Workflow Details

GitLab Flow is a workflow proposed by GitLab, combining GitHub Flow's simplicity and Git Flow's version management capabilities.

### Core Concept

GitLab Flow's core concept is "Upstream First": Code can only flow from upstream to downstream, cannot flow in reverse.

```
feature → main → pre-production → production
  ↑         ↑           ↑             ↑
  │         │           │             │
 Feature   Development  Pre-release   Production
 Branch    Branch       Branch        Branch
```

### Environment Branch Patterns

#### 1. Production Environment Branch Pattern

Suitable for projects with only one production environment:

```bash
# Create feature branch
git checkout -b feature/add-user-profile main

# Merge to main after development
git checkout main
git merge feature/add-user-profile

# When deploying to production, create tag
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

#### 2. Multi-environment Branch Pattern

Suitable for projects with multiple environments (development, testing, production):

```
main ──────●───────●───────●───────●───────●──→
            \               \               \
staging       ●───────●───────●               │
              \               \               \
production             ●───────●───────●──────●──→
```

```bash
# 1. Feature development
git checkout -b feature/new-feature main
# ... Develop ...
git checkout main
git merge feature/new-feature

# 2. Deploy to test environment
git checkout staging
git merge main
git push origin staging

# 3. Deploy to production after testing passes
git checkout production
git merge staging
git push origin production

# 4. Create version tag
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

#### 3. Release Branch Pattern

Suitable for projects needing to maintain multiple versions simultaneously:

```
main ──────●───────●───────●───────●───────●──→
            \               \
release-1.0  ●───────●───────●───────●───────●──→
              \               \               \
release-2.0           ●───────●───────●───────●──→
```

```bash
# Create release branch from main
git checkout -b release-2.0 main

# Fix bugs on release branch
git checkout release-2.0
# ... Fix ...
git commit -am "fix: Fix release version bug"

# Merge fix back to main
git checkout main
git cherry-pick <commit-hash>

# Create version tag
git checkout release-2.0
git tag -a v2.0.0 -m "Release 2.0.0"
```

### Issue Tracking Integration

GitLab Flow emphasizes integration with Issue tracking systems:

```bash
# Reference Issue in commit message
git commit -m "feat: Implement user search feature

Closes #123"

# Reference Issue when creating branch
git checkout -b 123-user-search main
```

### Advantages and Disadvantages Analysis

**Advantages:**
- Flexible adaptation to different project needs
- Deep integration with CI/CD
- Supports multi-environment deployment
- Complete Issue tracking integration

**Disadvantages:**
- Need to choose appropriate pattern based on project
- Multi-environment pattern branch management complex
- Need team to understand upstream first principle

### Applicable Scenarios

- Teams using GitLab
- Projects needing multi-environment deployment
- Projects needing version management
- DevOps practice teams

### GitLab CI/CD Configuration Examples

#### 1. Basic Configuration

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  NODE_ENV: production

# Build stage
build:
  stage: build
  image: node:18
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

# Test stage
test:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm test
  coverage: '/All files\s*\|\s*([\d\.]+)/'

# Deploy to test environment
deploy_staging:
  stage: deploy
  image: ruby:latest
  script:
    - apt-get update -qy
    - apt-get install -y ruby-dev
    - gem install dpl
    - dpl --provider=heroku --app=$HEROKU_APP_STAGING --api-key=$HEROKU_API_KEY
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Deploy to production environment
deploy_production:
  stage: deploy
  image: ruby:latest
  script:
    - apt-get update -qy
    - apt-get install -y ruby-dev
    - gem install dpl
    - dpl --provider=heroku --app=$HEROKU_APP_PRODUCTION --api-key=$HEROKU_API_KEY
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

#### 2. Multi-environment Deployment Configuration

```yaml
# .gitlab-ci.yml (Multi-environment version)
stages:
  - build
  - test
  - deploy_staging
  - deploy_pre_production
  - deploy_production

# Build
build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

# Test
test:
  stage: test
  script:
    - npm ci
    - npm test

# Deploy to test environment
deploy_staging:
  stage: deploy_staging
  script:
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Deploy to pre-production environment
deploy_pre_production:
  stage: deploy_pre_production
  script:
    - ./deploy.sh pre-production
  environment:
    name: pre-production
    url: https://pre-prod.example.com
  only:
    - /^release-.*$/

# Deploy to production environment
deploy_production:
  stage: deploy_production
  script:
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

### GitLab Flow Environment Management

#### Environment Branch Strategy

```
main ──────●───────●───────●───────●───────●──→
            \               \               \
staging       ●───────●───────●               │
              \               \               \
pre-production  ●───────●───────●───────●──────●──→
                                \               \
production                               ●──────●──→
```

#### Environment Variable Management

```yaml
# GitLab CI/CD environment variable configuration
# Settings → CI/CD → Variables

# Database configuration
DATABASE_URL: postgresql://user:pass@host:5432/db

# API keys
API_KEY: your-api-key
API_SECRET: your-api-secret

# Deployment configuration
DEPLOY_SERVER: production-server.com
DEPLOY_USER: deploy
DEPLOY_KEY: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
```

### GitLab Flow Advanced Features

#### 1. Merge Request Template

```markdown
<!-- .gitlab/merge_request_templates/default.md -->

## Description

Briefly describe the purpose of this MR.

## Related Issues

Closes #

## Change Type

- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation update
- [ ] Other

## Testing

- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Manual tests passed

## Screenshots (if applicable)

## Review Checklist

- [ ] Code style conforms to standards
- [ ] No security risks
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

#### 2. Automated Code Quality Check

```yaml
# .gitlab-ci.yml (Code quality check)
code_quality:
  stage: test
  image: docker:stable
  variables:
    DOCKER_DRIVER: overlay2
  services:
    - docker:dind
  script:
    - docker run
      --env SOURCE_CODE="$PWD"
      --volume "$PWD":/code
      --volume /var/run/docker.sock:/var/run/docker.sock
      "registry.gitlab.com/gitlab-org/ci-codescan:latest" /code
  artifacts:
    reports:
      codequality: gl-code-quality-report.json
```

#### 3. Security Scanning

```yaml
# .gitlab-ci.yml (Security scanning)
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
```

---

## Trunk-Based Development

Trunk-Based Development (TBD, Mainline Development) is a development model emphasizing frequent integration on main branch.

### Core Principles

1. **Everyone works on main branch**: Developers frequently merge small batches of code to main branch
2. **Short lifecycle branches**: Feature branches survive no more than 1-2 days
3. **Feature Flags**: Use feature flags to control visibility of unfinished features
4. **Continuous Integration**: Frequent integration, quick feedback

### Working Modes

#### 1. Directly Commit on Main Branch

```
main ──●──●──●──●──●──●──●──●──●──●──→
       ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
      All developers' commits
```

```bash
# Work directly on main branch
git checkout main
git pull origin main

# Small batch modifications
# ... Modify code ...
git add .
git commit -m "feat: Add user name field"
git push origin main
```

#### 2. Short Lifecycle Feature Branches

```
main ──●─────●─────●─────●─────●──→
        \   /       \   /
feat-1   ●─●         │
                      │
feat-2          ●─────●
           (1-2 days)
```

```bash
# Create short lifecycle branch
git checkout main
git pull origin main
git checkout -b feature/quick-fix

# Quick development (complete within 1-2 days)
# ... Write code ...
git add .
git commit -m "feat: Quickly implement some feature"

# Immediately merge back to main branch
git checkout main
git pull origin main
git merge feature/quick-fix
git push origin main

# Delete branch
git branch -d feature/quick-fix
```

### Feature Flags

Feature flags are key practice of TBD, used to control visibility of unfinished features:

```javascript
// Feature flag example
function renderNewFeature() {
  if (featureFlags.isEnabled('new-search')) {
    return <NewSearchComponent />;
  }
  return <OldSearchComponent />;
}
```

```yaml
# Feature flag configuration
feature_flags:
  new-search:
    enabled: true
    rollout_percentage: 10%
    allowed_users:
      - user1
      - user2
```

### Advantages and Disadvantages Analysis

**Advantages:**
- Reduce merge conflicts
- Continuous integration, quick feedback
- Simplify branch management
- Suitable for continuous deployment

**Disadvantages:**
- Needs strong automated testing support
- Needs feature flag mechanism
- High requirements for team discipline
- Main branch instability risk

### Applicable Scenarios

- High-performance DevOps teams
- Continuously deployed SaaS products
- Projects with complete automated testing
- Large internet companies

### Trunk-Based Development Practice Key Points

#### 1. Establish Complete Automated Testing

TBD requires high-coverage automated testing:

```javascript
// Unit test example
describe('UserService', () => {
  describe('login', () => {
    it('Should successfully login valid user', async () => {
      const user = await userService.login('test@example.com', 'password');
      expect(user).toBeDefined();
      expect(user.email).toBe('test@example.com');
    });

    it('Should reject invalid password', async () => {
      await expect(
        userService.login('test@example.com', 'wrong-password')
      ).rejects.toThrow('Invalid credentials');
    });

    it('Should handle non-existent user', async () => {
      await expect(
        userService.login('nonexistent@example.com', 'password')
      ).rejects.toThrow('User not found');
    });
  });
});
```

```javascript
// Integration test example
describe('User API', () => {
  describe('POST /api/login', () => {
    it('Should return JWT token', async () => {
      const response = await request(app)
        .post('/api/login')
        .send({ email: 'test@example.com', password: 'password' })
        .expect(200);

      expect(response.body.token).toBeDefined();
    });

    it('Should return 401 for invalid credentials', async () => {
      await request(app)
        .post('/api/login')
        .send({ email: 'test@example.com', password: 'wrong' })
        .expect(401);
    });
  });
});
```

#### 2. Implement Feature Flag System

```javascript
// Feature flag service
class FeatureFlagService {
  constructor() {
    this.flags = {};
  }

  async loadFlags() {
    // Load feature flags from configuration center
    this.flags = await configCenter.getFeatureFlags();
  }

  isEnabled(flagName, userId = null) {
    const flag = this.flags[flagName];
    if (!flag) return false;

    // Check if globally enabled
    if (!flag.enabled) return false;

    // Check grayscale ratio
    if (flag.rolloutPercentage < 100) {
      const hash = this.hashUserId(userId);
      if (hash > flag.rolloutPercentage) return false;
    }

    // Check whitelist
    if (flag.whitelist && flag.whitelist.includes(userId)) {
      return true;
    }

    return true;
  }

  hashUserId(userId) {
    // Simple hash function, ensures same user always enters same group
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = ((hash << 5) - hash) + userId.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash) % 100;
  }
}

// Usage example
const featureFlags = new FeatureFlagService();

function renderSearchComponent(userId) {
  if (featureFlags.isEnabled('new-search', userId)) {
    return <NewSearchComponent />;
  }
  return <OldSearchComponent />;
}
```

#### 3. Establish Quick Rollback Mechanism

```bash
#!/bin/bash
# rollback.sh - Quick rollback script

set -e

echo "Starting rollback..."

# Get previous successful deployment version
PREVIOUS_VERSION=$(git describe --tags --abbrev=0 HEAD~1)

# Rollback code
git checkout $PREVIOUS_VERSION

# Redeploy
./deploy.sh

echo "Rollback completed, current version: $PREVIOUS_VERSION"
```

### TBD Team Collaboration Standards

#### 1. Commit Frequency

```
Ideal commit frequency:
    │
    ├─ At least 1-2 commits per day
    ├─ Each commit only does one thing
    ├─ Commit size controlled at 100-200 lines of code
    └─ Push immediately after commit

Behaviors to avoid:
    │
    ├─ Only commit once a week
    ├─ Commit thousands of lines of code at once
    ├─ Commit half-finished code
    └─ Not pushing for a long time
```

#### 2. Code Review Process

```markdown
## TBD Code Review Standards

### Review Timing
- Complete review within 1 hour after commit
- Emergency fixes within 30 minutes

### Review Key Points
- Code quality
- Test coverage
- Performance impact
- Security risks

### Review Process
1. Submit PR/MR
2. Automated checks run
3. At least 1 person review passes
4. Merge to main branch
5. Auto-deploy to test environment
```

#### 3. Main Branch Protection Strategy

```yaml
# Main branch protection configuration
branch_protection:
  main:
    required_reviews: 1
    dismiss_stale_reviews: true
    require_status_checks: true
    required_checks:
      - ci/test
      - ci/build
      - security/scan
    enforce_admins: false
    allow_force_pushes: false
```

### TBD Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Main branch unstable | Complete automated testing, quick rollback mechanism |
| Merge unfinished features | Feature flags, feature markers |
| High team discipline requirements | Code review, automated checks |
| Needs powerful CI/CD | Invest in CI/CD infrastructure |
| Frequent collaboration conflicts | Small batch commits, frequent integration |

---

## Forking Workflow

Forking Workflow is the most commonly used workflow in open source projects, also applicable to cross-team collaboration within enterprises.

### Working Principle

Each developer has their own remote repository copy (Fork), develops on their own copy, then contributes code through Pull Request.

```
┌─────────────────┐     Fork     ┌─────────────────┐
│   Original Repo  │ ──────────→ │   Developer A's Fork │
│   (upstream)    │             │   (origin)       │
└─────────────────┘             └─────────────────┘
         ↑                              │
         │         Pull Request         │
         └──────────────────────────────┘
```

### Complete Workflow

#### 1. Fork Repository

Click "Fork" button on GitHub/GitLab to create your own copy.

#### 2. Clone and Configure

```bash
# Clone your Fork
git clone https://github.com/your-username/project.git
cd project

# Add original repository as upstream
git remote add upstream https://github.com/original-owner/project.git

# View remote repository configuration
git remote -v
# origin    https://github.com/your-username/project.git (fetch)
# origin    https://github.com/your-username/project.git (push)
# upstream  https://github.com/original-owner/project.git (fetch)
# upstream  https://github.com/original-owner/project.git (push)
```

#### 3. Keep Synced

```bash
# Get upstream latest code
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream code
git merge upstream/main

# Push to your Fork
git push origin main
```

#### 4. Develop New Feature

```bash
# Create feature branch from latest main
git checkout main
git pull origin main
git checkout -b feature/new-feature

# Develop and commit
# ... Write code ...
git add .
git commit -m "feat: Implement new feature"

# Push to your Fork
git push origin feature/new-feature
```

#### 5. Create Pull Request

Create PR on GitHub/GitLab, from your Fork's feature branch pointing to original repository's main branch.

#### 6. Handle Review Comments

```bash
# Modify code according to review comments
# ... Modify code ...
git add .
git commit -m "fix: Modify according to review comments"
git push origin feature/new-feature

# PR will automatically update
```

### Fork Workflow Advantages

1. **Permission Isolation**: Contributors don't need write permissions to original repository
2. **Free Experimentation**: Can freely experiment on your own Fork
3. **Code Quality**: Code review through PR
4. **Suitable for Open Source**: Standard collaboration method for open source projects

### Enterprise Internal Fork Workflow

Within enterprises, Fork workflow can be used for cross-team collaboration:

```bash
# Team A member
git clone https://github.com/company/project.git
git checkout -b feature/team-a-feature
# ... Develop ...
git push origin feature/team-a-feature
# Create PR to main repository

# Team B member
git clone https://github.com/company/project.git
git checkout -b feature/team-b-feature
# ... Develop ...
git push origin feature/team-b-feature
# Create PR to main repository
```

### Advantages and Disadvantages Analysis

**Advantages:**
- Suitable for open source projects
- Flexible permission management
- Supports cross-team collaboration
- Code quality guaranteed

**Disadvantages:**
- Workflow relatively complex
- Need to manage multiple remote repositories
- Frequent sync operations
- Not friendly enough for beginners

### Applicable Scenarios

- Open source projects
- Cross-team collaboration
- Projects needing strict permission control
- Projects with external contributor participation

### Forking Workflow Detailed Operation Guide

#### 1. First-time Setup

```bash
# 1. Fork repository (operate on GitHub/GitLab interface)

# 2. Clone your Fork
git clone https://github.com/your-username/project.git
cd project

# 3. Add original repository as upstream
git remote add upstream https://github.com/original-owner/project.git

# 4. Verify remote repository configuration
git remote -v
# origin    https://github.com/your-username/project.git (fetch)
# origin    https://github.com/your-username/project.git (push)
# upstream  https://github.com/original-owner/project.git (fetch)
# upstream  https://github.com/original-owner/project.git (push)

# 5. Configure Git user info
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

#### 2. Daily Workflow

```bash
# 1. Sync upstream latest code
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 2. Create feature branch
git checkout -b feature/my-feature

# 3. Develop and commit
# ... Write code ...
git add .
git commit -m "feat: Implement new feature"

# 4. Push to your Fork
git push origin feature/my-feature

# 5. Create Pull Request

# 6. Handle review comments
# ... Modify code ...
git add .
git commit -m "fix: Modify according to review comments"
git push origin feature/my-feature

# 7. After PR merge, clean up branches
git checkout main
git pull origin main
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

#### 3. Handle Upstream Conflicts

```bash
# 1. Get upstream latest code
git fetch upstream

# 2. Switch to feature branch
git checkout feature/my-feature

# 3. Rebase to upstream main branch
git rebase upstream/main

# 4. Resolve conflicts (if any)
# ... Edit conflict files ...
git add .
git rebase --continue

# 5. Force push to your Fork
git push origin feature/my-feature --force-with-lease
```

### Open Source Project Contribution Process

#### 1. Find Projects to Contribute

```markdown
## Ways to Find Open Source Projects

### GitHub
- Good First Issues: https://github.com/topics/good-first-issue
- Help Wanted: https://github.com/topics/help-wanted
- Up For Grabs: https://up-for-grabs.net

### Platforms
- GitHub Explore: https://github.com/explore
- GitLab Explore: https://gitlab.com/explore
- Gitee Explore: https://gitee.com/explore

### Selection Criteria
- Project activity
- Community friendliness
- Documentation completeness
- Tech stack match
```

#### 2. Preparation Before Contribution

```markdown
## Pre-contribution Checklist

### Understand Project
- [ ] Read README.md
- [ ] Read CONTRIBUTING.md
- [ ] Read CODE_OF_CONDUCT.md
- [ ] Understand project architecture

### Environment Preparation
- [ ] Fork project
- [ ] Clone to local
- [ ] Configure development environment
- [ ] Run tests passed

### Communication
- [ ] View existing Issues
- [ ] View existing PRs
- [ ] Express willingness to contribute in Issue
- [ ] Confirm contribution direction
```

#### 3. Submit High-quality PR

```markdown
## Elements of High-quality PR

### Title
- Concise and clear
- Use Conventional Commits format
- Example: "feat: add user authentication"

### Description
- Explain what was done
- Why it was done this way
- How to test
- Related Issues

### Code
- Conforms to project code style
- Includes necessary tests
- Documentation updated
- No lint errors

### Example
## Description
Implement user authentication feature, support JWT token authentication.

## Changes
- Add JWT authentication middleware
- Implement login endpoint
- Add authentication tests

## Testing
- [x] Unit tests passed
- [x] Integration tests passed
- [x] Manual tests passed

Closes #123
```

### Forking Workflow Permission Management

#### 1. Repository Permission Settings

```yaml
# GitHub repository permission configuration
permissions:
  # Read permission
  read:
    - External contributors
    - Observers

  # Write permission
  write:
    - Core developers
    - Maintainers

  # Admin permission
  admin:
    - Project leads
    - Architects

  # Prohibited operations
  restrictions:
    - force push to main
    - delete main branch
    - modify protected branches
```

#### 2. Branch Protection Rules

```yaml
# Branch protection configuration
branch_protection:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
    required_status_checks:
      strict: true
      contexts:
        - ci/test
        - ci/build
        - security/scan
    enforce_admins: true
    restrictions:
      users: []
      teams:
        - core-team
        - maintainers
```

### Forking Workflow Automation

#### 1. Auto Sync Upstream

```yaml
# .github/workflows/sync-upstream.yml
name: Sync Upstream

on:
  schedule:
    - cron: '0 0 * * *'  # Execute once daily
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Sync upstream
        run: |
          git remote add upstream https://github.com/original-owner/project.git
          git fetch upstream
          git checkout main
          git merge upstream/main
          git push origin main
```

#### 2. Automated PR Check

```yaml
# .github/workflows/pr-check.yml
name: PR Check

on:
  pull_request:
    branches: [ main ]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check PR title
        uses: actions/github-script@v6
        with:
          script: |
            const title = context.payload.pull_request.title;
            const regex = /^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,50}/;
            if (!regex.test(title)) {
              core.setFailed('PR title does not follow Conventional Commits format');
            }

      - name: Run tests
        run: |
          npm ci
          npm test

      - name: Run linting
        run: |
          npm run lint
```

---

## Workflow Comparison and Selection Guide

### Comparison Table

| Workflow | Complexity | Branch Count | Suitable Team Size | Continuous Deployment | Version Maintenance | Learning Cost |
|----------|------------|--------------|-------------------|----------------------|--------------------|--------------|
| Centralized | Low | 1 | 1-3 people | ✓ | ✗ | Low |
| Feature Branch | Medium-Low | Medium | 3-10 people | ✓ | ✗ | Low |
| Git Flow | High | Many | 10+ people | ✗ | ✓ | High |
| GitHub Flow | Low | Few | 3-10 people | ✓ | ✗ | Low |
| GitLab Flow | Medium | Medium | 5-20 people | ✓ | ✓ | Medium |
| TBD | Medium | Very few | 5-20 people | ✓ | ✗ | Medium |
| Forking | Medium-High | Many | Any | ✓ | ✗ | Medium-High |

### Selection Decision Tree

```
Start selecting workflow
    │
    ├─ Is it an open source project?
    │   ├─ Yes → Forking Workflow
    │   └─ No ↓
    │
    ├─ Team size?
    │   ├─ 1-3 people → Centralized Workflow
    │   ├─ 3-10 people ↓
    │   └─ 10+ people → Git Flow
    │
    ├─ Need continuous deployment?
    │   ├─ Yes ↓
    │   └─ No → Git Flow
    │
    ├─ Need multi-version maintenance?
    │   ├─ Yes → GitLab Flow (Release branch pattern)
    │   └─ No ↓
    │
    ├─ Have complete automated testing?
    │   ├─ Yes → Trunk-Based Development
    │   └─ No → GitHub Flow
    │
    └─ Use GitLab platform?
        ├─ Yes → GitLab Flow
        └─ No → GitHub Flow
```

### Recommendations for Different Scenarios

#### Scenario 1: Startup Web Application

- **Recommended**: GitHub Flow
- **Reason**: Simple, suitable for continuous deployment, low learning cost
- **Team size**: 3-8 people
- **Release frequency**: Multiple times daily

#### Scenario 2: Enterprise ERP System

- **Recommended**: Git Flow
- **Reason**: Needs multi-version maintenance, has fixed release cycle
- **Team size**: 10-50 people
- **Release frequency**: Monthly or quarterly

#### Scenario 3: Large Internet Company

- **Recommended**: Trunk-Based Development
- **Reason**: Fast iteration, continuous deployment, strong automated testing support
- **Team size**: 50+ people
- **Release frequency**: Multiple times daily

#### Scenario 4: Open Source Project

- **Recommended**: Forking Workflow
- **Reason**: Permission isolation, supports external contributors
- **Team size**: Any
- **Release frequency**: Based on project

#### Scenario 5: Team Using GitLab

- **Recommended**: GitLab Flow
- **Reason**: Deep integration with GitLab platform
- **Team size**: 5-20 people
- **Release frequency**: Weekly or daily

### Workflow Migration Guide

#### Migrate from Centralized to Feature Branch Workflow

```bash
# 1. Create develop branch
git checkout main
git pull origin main
git checkout -b develop
git push origin develop

# 2. Set branch protection
# Set main branch protection on GitHub/GitLab

# 3. Train team
# Organize training, explain feature branch workflow

# 4. Establish standards
# Establish branch naming standards, commit message standards

# 5. Gradual migration
# New features use feature branches, old code gradually migrated
```

#### Migrate from Git Flow to GitHub Flow

```bash
# 1. Simplify branch structure
# Delete unnecessary branches
git branch -d feature/old-feature
git branch -d release/old-release

# 2. Merge develop to main
git checkout main
git merge develop

# 3. Delete develop branch
git branch -d develop

# 4. Update workflow
# All features create branches from main
# After completion merge back to main through PR

# 5. Establish continuous deployment
# Configure CI/CD, auto-deploy after merge
```

### Common Misconceptions in Workflow Selection

| Misconception | Correct Approach |
|---------------|------------------|
| Blindly choose complex workflow | Choose based on team size and project needs |
| Don't consider team experience | Choose workflow team can understand and execute |
| Ignore automated testing | First establish automated testing, then choose workflow |
| Never change | Adjust workflow as project develops |
| Lack of standards | Establish clear branch, commit, review standards

---

## Branch Naming Standards

### Common Naming Standards

#### 1. Feature Branches

```bash
# Format: feature/short-description
feature/user-login
feature/search-function
feature/payment-integration

# Format: feature/Issue-number-short-description
feature/123-user-login
feature/456-search-function
```

#### 2. Bug Fix Branches

```bash
# Format: bugfix/short-description
bugfix/fix-login-error
bugfix/fix-search-pagination

# Format: bugfix/Issue-number-short-description
bugfix/789-fix-login-error
```

#### 3. Hotfix Branches

```bash
# Format: hotfix/short-description
hotfix/fix-security-vulnerability
hotfix/fix-payment-error
```

#### 4. Release Branches

```bash
# Format: release/version-number
release/1.0.0
release/2.1.0
```

#### 5. Other Branches

```bash
# Documentation branches
docs/update-readme
docs/add-api-documentation

# Test branches
test/add-unit-tests
test/integration-tests

# Refactoring branches
refactor/user-module
refactor/database-layer
```

### Naming Best Practices

1. **Use lowercase letters and hyphens**: `feature/user-login` not `feature/UserLogin`
2. **Concise and clear**: Branch name should clearly express purpose
3. **Include Issue number**: Convenient for tracking and association
4. **Avoid special characters**: Don't use spaces, Chinese characters, or other special characters
5. **Maintain consistency**: Team unified naming standards

### Branch Naming Organization Strategy

#### 1. Organize by Team/Module

```bash
# User team
user/feature-login
user/bugfix-auth
user/refactor-profile

# Order team
order/feature-checkout
order/bugfix-payment
order/refactor-cart

# Payment team
payment/feature-alipay
payment/bugfix-refund
payment/refactor-wechat
```

#### 2. Organize by Priority

```bash
# Emergency fixes
hotfix/critical-security-fix
hotfix/payment-error

# Regular features
feature/user-login
feature/search-function

# Low priority
chore/update-dependencies
docs/readme-update
```

#### 3. Organize by Version

```bash
# Version related
release/v1.0.0
release/v1.1.0
release/v2.0.0

# Version fixes
hotfix/v1.0.1
hotfix/v1.0.2
```

### Branch Naming Automation Tools

#### 1. Git Alias Configuration

```bash
# Configure Git aliases
git config --global alias.feature-start '!f() { git checkout main && git pull && git checkout -b "feature/$1"; }; f'
git config --global alias.bugfix-start '!f() { git checkout main && git pull && git checkout -b "bugfix/$1"; }; f'
git config --global alias.hotfix-start '!f() { git checkout main && git pull && git checkout -b "hotfix/$1"; }; f'

# Usage examples
git feature-start user-login    # Create feature/user-login
git bugfix-start fix-auth       # Create bugfix/fix-auth
git hotfix-start security-fix   # Create hotfix/security-fix
```

#### 2. Branch Naming Check Script

```bash
#!/bin/bash
# check-branch-name.sh

BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

# Check branch naming standards
if [[ ! $BRANCH_NAME =~ ^(main|develop|(feature|bugfix|hotfix|release|docs|test|refactor)/[a-z0-9-]+)$ ]]; then
  echo "Error: Branch name does not conform to standards"
  echo "Standard format: feature/xxx, bugfix/xxx, hotfix/xxx, release/xxx"
  echo "Current branch: $BRANCH_NAME"
  exit 1
fi

echo "Branch name conforms to standards: $BRANCH_NAME"
```

#### 3. Husky Hook Configuration

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-push": "bash check-branch-name.sh"
    }
  }
}
```

### Branch Naming Common Problems

| Problem | Example | Correct Approach |
|---------|---------|------------------|
| Use uppercase letters | `Feature/User-Login` | `feature/user-login` |
| Use Chinese | `feature/用户登录` | `feature/user-login` |
| Use spaces | `feature user login` | `feature/user-login` |
| Too short | `feature/fix` | `feature/fix-login-error` |
| Too long | `feature/fix-the-login-error-that-occurs-when-user-enter-wrong-password` | `feature/fix-login-validation` |

---

## Commit Message Standards

### Conventional Commits Standard

Conventional Commits is a standard for standardizing commit messages, widely adopted.

#### Basic Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type Types

| Type | Description | Example |
|------|-------------|---------|
| feat | New feature | feat: Add user login feature |
| fix | Bug fix | fix: Fix login validation error |
| docs | Documentation update | docs: Update API documentation |
| style | Code format (no functionality impact) | style: Format code |
| refactor | Refactoring (neither new feature nor fix) | refactor: Refactor user module |
| perf | Performance optimization | perf: Optimize query performance |
| test | Test related | test: Add unit tests |
| build | Build system or external dependencies | build: Update webpack configuration |
| ci | CI configuration | ci: Add GitHub Actions |
| chore | Other miscellaneous | chore: Update dependency version |
| revert | Rollback | revert: Rollback last commit |

#### Examples

```bash
# Simple format
git commit -m "feat: Add user login feature"

# With scope
git commit -m "feat(auth): Add JWT authentication"

# With detailed description
git commit -m "feat(auth): Add user login feature

Implement username/email login, support remember login status.

Closes #123"

# Breaking change
git commit -m "feat(api)!: Change user interface

BREAKING CHANGE: User interface return format changed"
```

### Angular Commit Standard

Angular project's commit standard, an implementation of Conventional Commits:

```
<type>(<scope>): <short summary>
│       │             │
│       │             └─> Short description, no more than 50 characters
│       │
│       └─> Impact scope (optional)
│
└─> Type: feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert
```

#### Angular Commit Examples

```bash
# Feature
git commit -m "feat(user): add user registration"

# Fix
git commit -m "fix(auth): fix token expiration issue"

# Documentation
git commit -m "docs(readme): update installation guide"

# Refactoring
git commit -m "refactor(api): simplify error handling"

# Breaking change
git commit -m "feat(api)!: change response format

BREAKING CHANGE: The response format has changed from XML to JSON."
```

### Commit Message Validation Tools

#### 1. commitlint

```bash
# Install
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Configure commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat', 'fix', 'docs', 'style', 'refactor',
        'perf', 'test', 'build', 'ci', 'chore', 'revert'
      ]
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100]
  }
};
```

#### 2. Husky Git Hooks

```bash
# Install husky
npm install --save-dev husky

# Initialize husky
npx husky install

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

### Commit Message Best Practices

1. **Use imperative mood**: `feat: add feature` not `feat: added feature`
2. **First line no more than 50 characters**: Concise and clear
3. **Add detailed description after blank line**: Explain why this change was made
4. **Reference related Issues**: Use `Closes #123` or `Fixes #123`
5. **One commit does one thing**: Maintain atomicity

### Commit Message Advanced Tips

#### 1. Multi-line Commit Message

```bash
# Multi-line commit message example
git commit -m "feat(auth): implement JWT authentication

- Add JWT token generation and validation
- Implement login endpoint with email/password
- Add middleware for protected routes
- Include refresh token mechanism

Closes #123
Fixes #456"
```

#### 2. Use Scripts for Automation

```bash
#!/bin/bash
# commit.sh - Automated commit script

# Get commit type
echo "Select commit type:"
echo "1. feat - New feature"
echo "2. fix - Bug fix"
echo "3. docs - Documentation update"
echo "4. style - Code format"
echo "5. refactor - Refactoring"
echo "6. perf - Performance optimization"
echo "7. test - Test related"
echo "8. build - Build system"
echo "9. ci - CI configuration"
echo "10. chore - Other miscellaneous"
read -p "Enter number: " type_num

case $type_num in
  1) type="feat" ;;
  2) type="fix" ;;
  3) type="docs" ;;
  4) type="style" ;;
  5) type="refactor" ;;
  6) type="perf" ;;
  7) type="test" ;;
  8) type="build" ;;
  9) type="ci" ;;
  10) type="chore" ;;
  *) echo "Invalid selection"; exit 1 ;;
esac

# Get scope
read -p "Enter scope (optional): " scope

# Get description
read -p "Enter commit description: " description

# Build commit message
if [ -z "$scope" ]; then
  commit_msg="$type: $description"
else
  commit_msg="$type($scope): $description"
fi

# Execute commit
git add .
git commit -m "$commit_msg"
```

#### 3. Use Commitizen

```bash
# Install Commitizen
npm install -g commitizen cz-conventional-changelog

# Initialize
echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc

# Use cz command instead of git commit
cz
```

### Commit Message Error Examples and Corrections

| Error Example | Problem | Correct Example |
|---------------|---------|-----------------|
| `fixed bug` | Missing type, too vague | `fix: resolve user login validation error` |
| `update code` | Too vague | `refactor: simplify authentication logic` |
| `add feature` | Missing specific description | `feat: add user profile editing feature` |
| `修复bug` | Using Chinese | `fix: resolve user authentication issue` |
| `feat: 添加功能` | Using Chinese | `feat: add user registration feature` |
| `FEAT: ADD FEATURE` | Using uppercase | `feat: add user login feature` |
| `feat:add feature` | Missing space | `feat: add user login feature` |

### Commit Message and Automation

#### 1. Auto-generate CHANGELOG

```bash
# Use conventional-changelog
npm install -g conventional-changelog-cli

# Generate CHANGELOG
conventional-changelog -p angular -i CHANGELOG.md -s

# Configure package.json
{
  "scripts": {
    "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s",
    "release": "standard-version"
  }
}
```

#### 2. Auto-determine Version Number

```bash
# Use standard-version
npm install -g standard-version

# Auto-determine version number and generate CHANGELOG
npm run release

# Auto-determine version number based on commit messages
# feat: Minor +1
# fix: Patch +1
# BREAKING CHANGE: Major +1
```

#### 3. Commit Message Validation Tool Comparison

| Tool | Features | Applicable Scenarios |
|------|----------|---------------------|
| commitlint | Flexible, configurable | All projects |
| Husky | Git Hooks management | Used with commitlint |
| Commitizen | Interactive commits | Beginner-friendly teams |
| semantic-release | Automated release | Continuous deployment projects |
| standard-version | Version management | Projects needing version management |

---

## Version Number Standards

### Semantic Versioning

Semantic Versioning (SemVer) is the most popular version number standard, format: `MAJOR.MINOR.PATCH`

#### Version Number Format

```
v1.2.3
│ │ │
│ │ └── Patch: Backward compatible bug fixes
│ └──── Minor: Backward compatible new features
└────── Major: Incompatible API changes
```

#### Version Number Rules

| Change Type | Version Number Change | Example |
|-------------|----------------------|---------|
| Bug fix | Patch +1 | 1.0.0 → 1.0.1 |
| New feature | Minor +1 | 1.0.0 → 1.1.0 |
| Breaking change | Major +1 | 1.0.0 → 2.0.0 |

#### Pre-release Versions

```bash
# Alpha version (internal testing)
v1.0.0-alpha.1
v1.0.0-alpha.2

# Beta version (external testing)
v1.0.0-beta.1
v1.0.0-beta.2

# Release Candidate
v1.0.0-rc.1
v1.0.0-rc.2
```

#### Version Number Examples

```bash
# Initial version
v0.1.0

# Development stage
v0.1.0 → v0.2.0 → v0.3.0

# First official version
v1.0.0

# Bug fixes
v1.0.0 → v1.0.1 → v1.0.2

# New features
v1.0.2 → v1.1.0

# Breaking changes
v1.1.0 → v2.0.0
```

### Other Version Number Standards

#### 1. CalVer (Calendar Versioning)

Date-based version number, commonly used in Ubuntu, Python and other projects:

```
# Format: YY.MM.PATCH
Ubuntu: 22.04, 23.10

# Format: YYYY.MM.DD
Python: 2024.1.15
```

#### 2. Custom Version Numbers

Some projects use custom version number formats:

```
# Semantic + Build number
v1.2.3-build.456

# Date + Sequence
release-20240115-001
```

### Git Tag Management

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to remote
git push origin v1.0.0

# Push all tags
git push origin --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0

# View all tags
git tag

# View specific tag info
git show v1.0.0
```

### Automated Version Number Management

#### Using standard-version

```bash
# Install
npm install --save-dev standard-version

# Add to package.json scripts
{
  "scripts": {
    "release": "standard-version"
  }
}

# Run automated version release
npm run release

# Auto-determine version number based on commit messages
# feat: Minor +1
# fix: Patch +1
# BREAKING CHANGE: Major +1
```

#### Using semantic-release

```bash
# Install
npm install --save-dev semantic-release

# Configure .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github"
  ]
}
```

### Version Number Management Best Practices

#### 1. Version Number and Release Process

```markdown
## Version Release Process

### 1. Preparation Phase
- Determine version number type (Major/Minor/Patch)
- Update CHANGELOG
- Update version number file

### 2. Testing Phase
- Run complete test suite
- Performance testing
- Security scanning

### 3. Release Phase
- Create Git tag
- Push to remote repository
- Deploy to production environment

### 4. Verification Phase
- Verify production environment
- Monitor error logs
- Notify team members
```

#### 2. Version Number File Management

```json
// package.json
{
  "name": "my-app",
  "version": "1.2.3",
  "scripts": {
    "version": "npm version"
  }
}
```

```yaml
# VERSION file
1.2.3
```

```python
# Python: __init__.py
__version__ = "1.2.3"
```

```java
// Java: pom.xml
<project>
  <version>1.2.3</version>
</project>
```

#### 3. Version Number and Dependency Management

```json
// package.json (Semantic version range)
{
  "dependencies": {
    "lodash": "^4.17.21",    // Compatible with 4.x.x
    "react": "^18.2.0",      // Compatible with 18.x.x
    "express": "~4.18.2",    // Compatible with 4.18.x
    "axios": "1.6.0"         // Exact version
  }
}
```

### Version Number Management Common Problems

| Problem | Cause | Solution |
|---------|-------|----------|
| Version number conflict | Multiple people simultaneously updating version number | Use automated tools |
| Version number rollback | Need to revert release | Use npm unpublish or Git tags |
| Version number inconsistency | Different files have different version numbers | Use unified version number management script |
| Pre-release version management | Alpha/Beta/RC versions | Use pre-release version identifiers |

### Version Number Management Tool Comparison

| Tool | Features | Applicable Scenarios |
|------|----------|---------------------|
| npm version | Node.js built-in | Node.js projects |
| standard-version | Automated version management | Projects needing CHANGELOG |
| semantic-release | Fully automated release | Continuous deployment projects |
| lerna | Multi-package management | Monorepo projects |
| changesets | Change set management | Multi-package collaboration projects |

---

## Release Management Strategy

### Standardize Release Process

#### 1. Release Checklist

```markdown
## Release Checklist v1.2.0

### Code Preparation
- [ ] All feature branches merged
- [ ] All tests passed
- [ ] Code review completed
- [ ] No unresolved critical bugs

### Documentation Update
- [ ] CHANGELOG updated
- [ ] API documentation updated
- [ ] User manual updated

### Test Verification
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Performance tests passed
- [ ] Security tests passed

### Deployment Preparation
- [ ] Database migration scripts prepared
- [ ] Configuration files updated
- [ ] Rollback plan prepared

### Release Execution
- [ ] Create release branch
- [ ] Update version number
- [ ] Create Git tag
- [ ] Deploy to test environment
- [ ] Test verification
- [ ] Deploy to production environment
- [ ] Monitor verification
```

#### 2. Release Process Diagram

```
┌─────────────┐
│ Feature development completed │
└──────┬──────┘
       ↓
┌─────────────┐
│ Code review │
└──────┬──────┘
       ↓
┌─────────────┐
│ Automated testing │
└──────┬──────┘
       ↓
┌─────────────┐
│ Create release branch │
└──────┬──────┘
       ↓
┌─────────────┐
│ Test environment verification │
└──────┬──────┘
       ↓
┌─────────────┐
│ Production environment deployment │
└──────┬──────┘
       ↓
┌─────────────┐
│ Monitoring and verification │
└──────┬──────┘
       ↓
┌─────────────┐
│ Release completed │
└─────────────┘
```

### CHANGELOG Management

#### CHANGELOG Format

```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- Add user search feature (#123)
- Add data export feature (#124)

### Changed
- Optimize query performance (#125)
- Update user interface (#126)

### Fixed
- Fix login validation error (#127)
- Fix pagination display issue (#128)

### Security
- Update dependency versions to fix security vulnerabilities (#129)

## [1.1.0] - 2024-01-01

### Added
- Add user registration feature (#120)
...
```

#### Auto-generate CHANGELOG

```bash
# Use conventional-changelog
npm install --save-dev conventional-changelog-cli

# Generate CHANGELOG
conventional-changelog -p angular -i CHANGELOG.md -s

# Configure package.json
{
  "scripts": {
    "changelog": "conventional-changelog -p angular -i CHANGELOG.md -s"
  }
}
```

### Hotfix Process

```bash
# 1. Create hotfix branch from production version
git checkout v1.0.0
git checkout -b hotfix/fix-critical-bug

# 2. Fix bug
# ... Fix code ...
git add .
git commit -m "fix: Fix payment verification vulnerability"

# 3. Update version number
npm version patch  # 1.0.0 → 1.0.1

# 4. Merge to main branch
git checkout main
git merge hotfix/fix-critical-bug

# 5. Create tag
git tag -a v1.0.1 -m "Hotfix: Fix payment verification vulnerability"

# 6. Deploy to production
git push origin main --tags

# 7. Clean up branch
git branch -d hotfix/fix-critical-bug
```

### Release Management Best Practices

#### 1. Automated Release Process

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            ## Changes
            - See CHANGELOG.md for details
          draft: false
          prerelease: false
      
      - name: Deploy to Production
        run: |
          echo "Deploying to production..."
          # Deploy script
```

#### 2. Blue-Green Deployment Strategy

```bash
#!/bin/bash
# blue-green-deploy.sh

set -e

CURRENT_ENV=$(curl -s http://localhost/current-env)
NEW_ENV=""

if [ "$CURRENT_ENV" = "blue" ]; then
  NEW_ENV="green"
else
  NEW_ENV="blue"
fi

echo "Current environment: $CURRENT_ENV"
echo "Deploying to: $NEW_ENV"

# Deploy to new environment
./deploy.sh $NEW_ENV

# Run health check
./health-check.sh $NEW_ENV

# Switch traffic
./switch-traffic.sh $NEW_ENV

echo "Deployment completed! Current environment: $NEW_ENV"
```

#### 3. Canary Release Strategy

```yaml
# Canary release configuration
canary_release:
  stages:
    - name: Internal testing
      percentage: 1%
      duration: 1h
    
    - name: Small-scale canary
      percentage: 5%
      duration: 2h
    
    - name: Medium-scale canary
      percentage: 20%
      duration: 4h
    
    - name: Large-scale canary
      percentage: 50%
      duration: 8h
    
    - name: Full release
      percentage: 100%
      duration: 0
  
  rollback:
    error_rate_threshold: 1%
    latency_threshold: 500ms
```

### Release Management Tool Comparison

| Tool | Features | Applicable Scenarios |
|------|----------|---------------------|
| GitHub Releases | Simple and easy to use | GitHub projects |
| GitLab Releases | Feature-rich | GitLab projects |
| semantic-release | Fully automated | Continuous deployment projects |
| release-it | Flexible configuration | Various projects |
| lerna | Multi-package management | Monorepo projects |

---

## Multi-person Collaboration Conflict Prevention

### Causes of Conflicts

1. **Same position in same file modified by multiple people**
2. **File deleted but someone modified it**
3. **Binary file conflicts**
4. **Divergence caused by not merging for a long time**

### Prevention Strategies

#### 1. Frequently Pull and Merge

```bash
# Pull latest code before starting work
git checkout main
git pull origin main

# Regularly merge main branch to feature branch
git checkout feature/my-feature
git merge main

# Or use rebase
git checkout feature/my-feature
git rebase main
```

#### 2. Small Batch Commits

```bash
# Bad practice: Commit a large number of changes at once
git add .
git commit -m "Complete all features"

# Good practice: Small batch, frequent commits
git add src/user/login.js
git commit -m "feat: Implement user login"

git add src/user/register.js
git commit -m "feat: Implement user registration"
```

#### 3. Modular Code Organization

```
project/
├── src/
│   ├── user/          # User module
│   │   ├── login.js
│   │   └── register.js
│   ├── order/         # Order module
│   │   ├── create.js
│   │   └── query.js
│   └── payment/       # Payment module
│       ├── alipay.js
│       └── wechat.js
```

#### 4. Use .gitignore

```gitignore
# IDE configuration
.idea/
.vscode/
*.swp
*.swo

# System files
.DS_Store
Thumbs.db

# Dependency directories
node_modules/
vendor/

# Build artifacts
dist/
build/

# Environment configuration
.env
.env.local
```

### Conflict Resolution Methods

#### 1. Manually Resolve Conflicts

```bash
# Conflict during merge
git merge feature-branch
# CONFLICT (content): Merge conflict in src/app.js

# View conflict files
git status

# Edit conflict file
<<<<<<< HEAD
// Current branch code
const url = 'https://api.example.com';
=======
// Merging branch code
const url = 'https://api.new.com';
>>>>>>> feature-branch

# Manually select or merge code
const url = 'https://api.new.com';

# Mark conflict resolved
git add src/app.js

# Complete merge
git commit -m "merge: Merge feature-branch, resolve conflicts"
```

#### 2. Use Merge Tools

```bash
# Configure merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait --merge $REMOTE $LOCAL $BASE $MERGED'

# Use merge tool to resolve conflicts
git mergetool
```

#### 3. Use Rebase

```bash
# Use rebase instead of merge
git checkout feature/my-feature
git rebase main

# Resolve conflicts and continue rebase
git add .
git rebase --continue

# Or abandon rebase
git rebase --abort
```

### Team Collaboration Standards

#### 1. Code Ownership File (CODEOWNERS)

```bash
# .github/CODEOWNERS or docs/CODEOWNERS

# Default owners
*       @team-lead

# User module
/src/user/    @user-team

# Order module
/src/order/   @order-team

# Documentation
/docs/        @doc-team
```

#### 2. Branch Protection Rules

```yaml
# GitHub branch protection configuration example
branches:
  main:
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
      required_status_checks:
        strict: true
        contexts:
          - ci/build
          - ci/test
      enforce_admins: true
      restrictions:
        users: []
        teams:
          - core-team
```

#### 3. Code Review Checklist

```markdown
## Code Review Checklist

### Code Quality
- [ ] Code style conforms to standards
- [ ] Naming clear and meaningful
- [ ] No duplicate code
- [ ] Appropriate comments

### Feature Implementation
- [ ] Feature implemented correctly
- [ ] Boundary conditions handled
- [ ] Error handling complete
- [ ] Performance considerations

### Test Coverage
- [ ] Unit tests complete
- [ ] Test cases cover boundary situations
- [ ] Tests passed

### Security Considerations
- [ ] Input validation
- [ ] Permission checks
- [ ] Sensitive information handling

### Documentation Update
- [ ] API documentation updated
- [ ] README updated
- [ ] CHANGELOG updated
```

### Advanced Conflict Resolution Tips

#### 1. Use rerere (Reuse Recorded Resolution)

Git's rerere feature can remember conflict resolution methods, automatically apply when same conflict encountered next time:

```bash
# Enable rerere
git config --global rerere.enabled true

# View rerere records
git rerere status

# Clear rerere records
git rerere forget <path>
```

#### 2. Use Interactive Rebase

```bash
# Interactive rebase, merge multiple commits
git rebase -i HEAD~3

# Editor will show:
# pick abc1234 First commit
# pick def5678 Second commit
# pick ghi9012 Third commit

# Modify to:
# pick abc1234 First commit
# squash def5678 Second commit
# squash ghi9012 Third commit
```

#### 3. Use Cherry-pick

```bash
# Select specific commit from other branch
git cherry-pick <commit-hash>

# Select multiple commits
git cherry-pick <commit1> <commit2>

# Select commit range
git cherry-pick <start-commit>..<end-commit>
```

### Conflict Prevention Team Collaboration Standards

```markdown
## Team Collaboration Standards

### Communication Standards
- Daily standup to sync progress
- Communicate large features in advance
- Complete code review in a timely manner
- Report problems in a timely manner

### Code Standards
- Unified code style
- Use ESLint/Prettier
- Follow project architecture
- Modular development

### Commit Standards
- Small batch commits
- Frequent integration
- Use feature flags
- Keep main branch stable

### Review Standards
- At least 2 people review
- Complete within 24 hours
- Focus on code quality
- Provide constructive feedback
```

---

## Chinese Internet Company Git Workflow Practices

### Alibaba

Alibaba mainly adopts **Aone Flow** workflow, which is an improved version based on Trunk-Based Development:

#### Core Features

1. **Mainline development**: All development on mainline (master)
2. **Short lifecycle feature branches**: Feature branches no more than 1-2 days
3. **Release branches**: Pull release branches from mainline to production
4. **Environment branches**: Separate test, pre-release, production environments

#### Workflow

```
master    ──●──●──●──●──●──●──●──●──●──→
              \         \         \
release-test   ●───●     │         │
                \         \         \
release-pre      ●─────●   │         │
                  \         \         \
release-prod       ●───────●───●──────●──→
```

```bash
# 1. Create feature branch from master
git checkout master
git pull origin master
git checkout -b feature/user-login

# 2. Development completed, merge back to master
git checkout master
git merge feature/user-login

# 3. Create test branch from master
git checkout -b release-test master

# 4. After testing passes, create pre-release branch
git checkout -b release-pre release-test

# 5. After pre-release verification passes, create production branch
git checkout -b release-prod release-pre
```

### Tencent

Tencent internally uses **Gitea (Gitea Git)** platform, mainly adopting **Git Flow** variant:

#### Core Features

1. **Main branch protection**: master branch needs code review to merge
2. **Feature branches**: Each feature developed on independent branch
3. **Integration branch**: Use develop branch for feature integration
4. **Release branches**: Create release branches from develop

#### Branch Strategy

```
master    ──●───────────────●───────────────●──→
              ↑               ↑               ↑
              │               │               │
release-1.0   ●───────●───────●               │
              ↑               ↑               │
              │               │               │
develop  ─────●───────●───────●───────●───────●──→
              ↑       ↑       ↑       ↑
              │       │     │       │
feature-1     ●───────●     │       │
                              │       │
feature-2             ●───────●       │
                                      │
feature-3                     ●───────●
```

### ByteDance

ByteDance adopts **Trunk-Based Development** primarily:

#### Core Features

1. **Mainline development**: All code committed to main branch
2. **Short lifecycle branches**: Feature branches no more than 24 hours
3. **Feature flags**: Use feature flags to control visibility of unfinished features
4. **Automated testing**: Complete automated testing system

#### Practice Key Points

```javascript
// Feature flag configuration
const featureFlags = {
  'new-search': {
    enabled: true,
    rollout: 10,  // Canary 10%
    whitelist: ['user1', 'user2']
  },
  'new-payment': {
    enabled: false,
    rollout: 0
  }
};

// Use feature flags
if (featureFlags.isEnabled('new-search')) {
  // New search feature
} else {
  // Old search feature
}
```

### Meituan

Meituan adopts **Git Flow** combined with **GitHub Flow**:

#### Core Features

1. **Main branch protection**: master branch needs CR (Code Review) to merge
2. **Feature branches**: Each feature developed on independent branch
3. **Release branches**: Create release branches from master
4. **Hotfix branches**: Emergency fixes from release branches

#### Workflow

```bash
# 1. Create feature branch
git checkout master
git pull origin master
git checkout -b feature/new-feature

# 2. Develop and commit
git add .
git commit -m "feat: Implement new feature"

# 3. Create MR (Merge Request)
# Create MR on GitLab, request code review

# 4. Merge after CR passes
git checkout master
git merge feature/new-feature

# 5. Deploy to test environment
git checkout test
git merge master

# 6. Deploy to production after testing passes
git checkout production
git merge test
```

### Huawei

Huawei adopts **DevOps + Git Flow** workflow:

#### Core Features

1. **Code gate**: Must pass automated checks before commit
2. **Code review**: Mandatory code review system
3. **Branch management**: Strict branch management strategy
4. **Security scanning**: Integrated security scanning tools

#### Code Gate Configuration

```yaml
# Code gate check items
code_gate:
  checks:
    - name: unit_test
      command: "npm test"
      threshold: 80%  # Test coverage requirement

    - name: lint
      command: "npm run lint"
      threshold: 0  # No lint errors

    - name: security_scan
      command: "npm audit"
      threshold: 0  # No high-risk vulnerabilities

    - name: code_review
      required: true
      min_reviewers: 2

  blocking: true  # Block commit if gate check fails
```

### Chinese Internet Company Common Practices

#### 1. Code Review System

```markdown
## Code Review Process

1. Developer submits MR/PR
2. Automated checks (CI/CD)
3. At least 2 people review passes
4. Must resolve all review comments
5. Merge to main branch

## Review Key Points

- Code quality
- Performance impact
- Security risks
- Test coverage
- Documentation update
```

#### 2. Branch Protection Strategy

```yaml
# Common branch protection configuration
branch_protection:
  master:
    required_reviews: 2
    dismiss_stale_reviews: true
    require_status_checks: true
    required_checks:
      - ci/build
      - ci/test
      - security/scan
    restrict_pushes: true
    allowed_pushers:
      - @team-lead
      - @devops
```

#### 3. Release Process

```bash
# Common release process
# 1. Code freeze
git checkout master
git tag -a code-freeze-v1.2.0 -m "Code freeze v1.2.0"

# 2. Create release branch
git checkout -b release-v1.2.0

# 3. Testing and fixing
# ... Fix bugs ...
git commit -am "fix: Fix release version bug"

# 4. Deploy to pre-release environment
git checkout pre-release
git merge release-v1.2.0

# 5. After pre-release verification passes, deploy to production
git checkout production
git merge pre-release
git tag -a v1.2.0 -m "Release v1.2.0"

# 6. Merge back to main branch
git checkout master
git merge release-v1.2.0
```

### Chinese Internet Company Tool Ecosystem

#### 1. Code Hosting Platforms

| Platform | Features | Applicable Scenarios |
|----------|----------|---------------------|
| Gitee (码云) | Fast domestic access, Chinese interface | Domestic teams, open source projects |
| CODING | Tencent Cloud, DevOps tool chain | Enterprise development |
| Alibaba Cloud Codeup | Alibaba Cloud, integrates with Alibaba Cloud | Alibaba Cloud users |
| GitLab China版 | Private deployment, complete features | Large enterprises |

#### 2. CI/CD Tools

| Tool | Features | Applicable Scenarios |
|------|----------|---------------------|
| Jenkins | Open source, rich plugins | Various projects |
| Yunxiao | Alibaba Cloud, one-stop DevOps | Alibaba Cloud users |
| CODING CI | Tencent Cloud, simple and easy to use | Tencent Cloud users |
| GitLab CI | Integrates with GitLab | GitLab users |
| GitHub Actions | Integrates with GitHub | GitHub users |

#### 3. Code Quality Tools

```yaml
# Code quality check configuration
code_quality:
  tools:
    - name: ESLint
      purpose: JavaScript/TypeScript code checking
    
    - name: Prettier
      purpose: Code formatting
    
    - name: SonarQube
      purpose: Code quality analysis
    
    - name: CodeQL
      purpose: Security vulnerability scanning
  
  integration:
    - Integrate with CI/CD
    - Automated checking
    - Quality gates
```

### Chinese Internet Company Best Practices Summary

#### 1. Branch Management Strategy

```markdown
## Branch Management Best Practices

### Main Branch Protection
- Mandatory code review
- Automated tests passed
- Prohibit direct push

### Feature Branch Standards
- Short lifecycle (1-3 days)
- Frequently sync main branch
- Timely clean up merged branches

### Release Branch Management
- Create from main branch
- Only fix bugs
- Merge after testing passes
```

#### 2. Code Review Process

```markdown
## Code Review Best Practices

### Review Timing
- Complete within 24 hours after commit
- Emergency fixes within 2 hours

### Review Key Points
- Code quality
- Performance impact
- Security risks
- Test coverage

### Review Feedback
- Specific, actionable
- Constructive suggestions
- Timely response to modifications
```

#### 3. Continuous Integration Practice

```yaml
# Continuous integration best practices
ci_cd:
  pipeline:
    - stage: Code check
      tools:
        - ESLint
        - Prettier
        - TypeScript
    
    - stage: Unit test
      coverage_threshold: 80%
    
    - stage: Integration test
      environment: test
    
    - stage: Security scan
      tools:
        - npm audit
        - Snyk
    
    - stage: Build
      artifacts:
        - dist/
        - build/
    
    - stage: Deploy
      environments:
        - staging
        - production
```

---

## Workflow Decision Flowcharts

### Workflow Selection Decision Chart

```
                    Start selecting workflow
                          │
                          ▼
              ┌─────────────────────┐
              │ Is it an open source project? │
              └─────────────────────┘
                    │           │
                   Yes           No
                    │           │
                    ▼           ▼
          ┌─────────────┐  ┌─────────────────────┐
          │ Forking      │  │ What is team size?  │
          │ Workflow     │  └─────────────────────┘
          └─────────────┘        │         │         │
                              1-3 people 3-10 people 10+ people
                                │         │         │
                                ▼         ▼         ▼
                      ┌───────────┐ ┌───────────┐ ┌───────────┐
                      │ Centralized│ │ Feature   │ │ Git Flow  │
                      │ Workflow  │ │ Branch    │ │ Workflow  │
                      └───────────┘ │ Workflow  │ └───────────┘
                                    └───────────┘
```

### Continuous Deployment Decision Chart

```
                    Need continuous deployment?
                          │
                    ┌─────┴─────┐
                   Yes           No
                    │           │
                    ▼           ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Is automated    │  │ Need multi-version│
          │ testing complete?│  │ maintenance?     │
          └─────────────────┘  └─────────────────┘
                │       │           │       │
               Yes       No         Yes       No
                │       │           │       │
                ▼       ▼           ▼       ▼
      ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
      │ Trunk-    │ │ GitHub    │ │ GitLab    │ │ Git Flow  │
      │ Based     │ │ Flow      │ │ Flow      │ │ Workflow  │
      │ Dev       │ │           │ │           │ │           │
      └───────────┘ └───────────┘ └───────────┘ └───────────┘
```

### Branch Strategy Decision Chart

```
                    How to select branch strategy?
                          │
                          ▼
              ┌─────────────────────┐
              │ Need release branches? │
              └─────────────────────┘
                    │           │
                   Yes           No
                    │           │
                    ▼           ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Need to maintain│  │ Need feature     │
          │ multiple versions?│  │ flags?          │
          └─────────────────┘  └─────────────────┘
                │       │           │       │
               Yes       No         Yes       No
                │       │           │       │
                ▼       ▼           ▼       ▼
      ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
      │ GitLab    │ │ Git Flow  │ │ Trunk-    │ │ GitHub    │
      │ Flow      │ │           │ │ Based     │ │ Flow      │
      │ (Release) │ │           │ │ Dev       │ │           │
      └───────────┘ └───────────┘ └───────────┘ └───────────┘
```

### Conflict Resolution Decision Chart

```
                    Encounter code conflict
                          │
                          ▼
              ┌─────────────────────┐
              │ What is conflict type? │
              └─────────────────────┘
                    │       │       │
                 Content  Delete  Binary
                 Conflict Conflict Conflict
                    │       │       │
                    ▼       ▼       ▼
          ┌─────────────────────────────────────┐
          │ Conflict complexity?                 │
          └─────────────────────────────────────┘
                    │               │
                 Simple           Complex
                 Conflict         Conflict
                    │               │
                    ▼               ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Manual edit     │  │ Use merge tool  │
          │ git add .       │  │ git mergetool   │
          │ git commit      │  │                 │
          └─────────────────┘  └─────────────────┘
```

### Code Review Decision Chart

```
                    Code review process
                          │
                          ▼
              ┌─────────────────────┐
              │ Submit PR/MR        │
              └─────────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │ Automated checks pass? │
              └─────────────────────┘
                    │           │
                   Yes           No
                    │           │
                    ▼           ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Manual code     │  │ Fix automated   │
          │ review          │  │ check issues    │
          └─────────────────┘  └─────────────────┘
                    │
                    ▼
              ┌─────────────────────┐
              │ Review passes?      │
              └─────────────────────┘
                    │           │
                   Yes           No
                    │           │
                    ▼           ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Merge to main   │  │ Modify code     │
          │ branch          │  │ according to    │
          │                 │  │ review comments │
          └─────────────────┘  └─────────────────┘
```

---

## Summary

### Key Factors for Choosing Workflow

1. **Team size**: Small teams choose simple workflows, large teams choose standardized workflows
2. **Release frequency**: Continuous deployment chooses GitHub Flow, fixed cycle chooses Git Flow
3. **Platform choice**: Using GitLab chooses GitLab Flow, using GitHub chooses GitHub Flow
4. **Project type**: Open source projects choose Forking Workflow, internal projects choose other workflows
5. **Team experience**: Beginner teams choose simple workflows, experienced teams can choose complex workflows

### Best Practices Summary

1. **Unified standards**: Team uses same branch naming, commit message standards
2. **Code review**: All code changes should go through code review
3. **Automated testing**: Establish complete automated testing system
4. **Continuous integration**: Integrate CI/CD tools, automate build and deployment
5. **Documentation**: Document workflow standards and best practices
6. **Regular review**: Regularly review and optimize workflow

### Recommended Learning Path

```
Beginner Stage
    │
    ├─ Learn Git basic operations
    ├─ Understand branch concepts
    └─ Try centralized workflow
        │
        ▼
Advanced Stage
    │
    ├─ Learn feature branch workflow
    ├─ Master Pull Request
    └─ Understand code review process
        │
        ▼
Expert Stage
    │
    ├─ Learn Git Flow
    ├─ Understand GitHub Flow / GitLab Flow
    └─ Master version management and release process
        │
        ▼
Master Stage
    │
    ├─ Practice Trunk-Based Development
    ├─ Establish complete CI/CD process
    └─ Optimize team collaboration efficiency
```

---

## Appendix

### Common Git Command Quick Reference

```bash
# Branch operations
git branch                    # View local branches
git branch -a                 # View all branches
git branch -d <branch>        # Delete local branch
git checkout -b <branch>      # Create and switch branch
git switch -c <branch>        # Create and switch branch (new syntax)

# Merge operations
git merge <branch>            # Merge branch
git rebase <branch>           # Rebase
git cherry-pick <commit>      # Cherry-pick commit

# Tag operations
git tag                       # View tags
git tag -a v1.0.0 -m "msg"   # Create tag
git push origin --tags        # Push tags

# Remote operations
git remote -v                 # View remote repositories
git remote add <name> <url>   # Add remote repository
git fetch <remote>            # Fetch remote updates
git pull <remote> <branch>    # Pull and merge
git push <remote> <branch>    # Push

# Stash operations
git stash                     # Stash current work
git stash pop                 # Restore stashed work
git stash list                # View stash list

# Log operations
git log                       # View commit log
git log --oneline             # Concise log
git log --graph               # Graphical log
git log --author=<name>       # View by author
```

### Recommended Tools

| Tool | Purpose | Website |
|------|---------|---------|
| Git | Version control | https://git-scm.com |
| GitHub | Code hosting | https://github.com |
| GitLab | Code hosting | https://gitlab.com |
| SourceTree | Git GUI | https://www.sourcetreeapp.com |
| GitKraken | Git GUI | https://www.gitkraken.com |
| VS Code | Code editor | https://code.visualstudio.com |
| Husky | Git Hooks | https://typicode.github.io/husky |
| commitlint | Commit check | https://commitlint.js.org |
| standard-version | Version management | https://github.com/conventional-changelog/standard-version |

### Reference Materials

1. [Git Official Documentation](https://git-scm.com/doc)
2. [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
3. [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)
4. [A Successful Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
5. [Conventional Commits](https://www.conventionalcommits.org/)
6. [Semantic Versioning](https://semver.org/)
7. [Trunk-Based Development](https://trunkbaseddevelopment.com/)

---

> This document last updated: January 2024
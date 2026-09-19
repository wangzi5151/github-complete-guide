# GitHub Team Collaboration Complete Guide

> This guide is targeted at Chinese development teams, systematically explains GitHub team collaboration models, processes, tools and best practices, helping teams build efficient, standardized and secure collaboration systems.

---

## Table of Contents

- [1. GitHub Team Collaboration Models](#1-github-team-collaboration-models)
- [2. Branch Strategy and Naming Standards](#2-branch-strategy-and-naming-standards)
- [3. Pull Request Workflow Best Practices](#3-pull-request-workflow-best-practices)
- [4. Code Review Standards and Process](#4-code-review-standards-and-process)
- [5. CODEOWNERS File Configuration](#5-codeowners-file-configuration)
- [6. Branch Protection Rules](#6-branch-protection-rules)
- [7. GitHub Rulesets Details](#7-github-rulesets-details)
- [8. Team Permission Management (Roles and Permissions)](#8-team-permission-management-roles-and-permissions)
- [9. Issue and Project Management Standards](#9-issue-and-project-management-standards)
- [10. Team Communication Best Practices](#10-team-communication-best-practices)
- [11. Multi-repo Collaboration](#11-multi-repo-collaboration)
- [12. Team CI/CD Standards](#12-team-cicd-standards)
- [13. Knowledge Management and Documentation Collaboration](#13-knowledge-management-and-documentation-collaboration)
- [14. Remote Team Collaboration Experience](#14-remote-team-collaboration-experience)
- [15. Best Practices for Chinese Development Teams Using GitHub](#15-best-practices-for-chinese-development-teams-using-github)

---

## 1. GitHub Team Collaboration Models

Choosing the right collaboration model is the foundation for efficient team development. Here is a detailed comparison of five mainstream models.

### 1.1 Centralized Workflow

This is the simplest collaboration method, everyone works directly on `main` branch, suitable for very small teams or personal learning projects.

```
Developer A ──push──→ main
Developer B ──push──→ main
Developer C ──push──→ main
```

**Advantages**: Simple process, low learning cost.

**Disadvantages**: Easy to generate conflicts, cannot parallel develop, not suitable for formal projects.

### 1.2 Feature Branch Workflow

Each new feature is developed on an independent branch, after completion merged back to main branch through Pull Request. This is currently the most widely used workflow.

```
main ─────●─────────────●─────────────●──→
           \           /             /
feature-A   ●────●────●             /
                                   /
main ─────●──────────────●────────●──→
           \            /
feature-B   ●────●────●
```

**Workflow**:

```bash
# 1. Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/user-login

# 2. Develop and commit
git add .
git commit -m "feat(auth): Implement user login feature"

# 3. Push and create PR
git push origin feature/user-login
# Create Pull Request on GitHub

# 4. Merge after Code Review passes
# Click "Merge pull request" on GitHub
```

**Applicable Scenarios**: Small to medium teams, daily feature development.

### 1.3 Git Flow Workflow

Git Flow is a strict branch management model, proposed by Vincent Driessen, suitable for projects with clear version release cycles.

```
main ─────●─────────────────────●──────────────────→ (Production branch)
           \                   ↑
            \                 / merge
             \               /
hotfix/*       ●────●───────●
             ↑
release/*  ●────●────●──→ (Release preparation branch)
             ↑        ↑
develop ────●────●────●────●────●────●──→ (Development branch)
              \      ↑  \      ↑
feature/*      ●──●──●   ●──●──●
```

**Branch Description**:

| Branch | Usage | Lifecycle |
|--------|-------|-----------|
| `main` | Production environment code, only accepts release and hotfix merges | Permanent |
| `develop` | Main development branch, integrates all features | Permanent |
| `feature/*` | New feature development | Temporary |
| `release/*` | Version release preparation | Temporary |
| `hotfix/*` | Production environment emergency fix | Temporary |

**Typical Flow**:

```bash
# Start new feature
git checkout develop
git checkout -b feature/payment

# Merge back to develop after feature completion
git checkout develop
git merge --no-ff feature/payment

# Prepare for release
git checkout develop
git checkout -b release/v2.0.0
# Fix release related issues...

# Merge to main and develop after release
git checkout main
git merge --no-ff release/v2.0.0
git tag -a v2.0.0 -m "Release v2.0.0"
git checkout develop
git merge --no-ff release/v2.0.0

# Emergency fix
git checkout main
git checkout -b hotfix/fix-security
# Merge back to main and develop after fix
```

**Applicable Scenarios**: Enterprise projects with fixed release cycles, products that need to maintain multiple versions simultaneously.

### 1.4 GitHub Flow Workflow

GitHub Flow is a lightweight workflow officially recommended by GitHub, much simpler than Git Flow, emphasizing continuous deployment.

```
main ─────●────●────●────●────●────●──→ (Always deployable)
           \   ↑  \   ↑  \   ↑
            PR     PR     PR
           /      /      /
feature  ●──●  ●──●  ●──●
```

**Core Principles**:

1. Code on `main` branch is always deployable
2. All changes through feature branches + PR
3. PR must pass CI checks and Code Review
4. Deploy immediately after merge

**Applicable Scenarios**: SaaS products, continuous deployment projects, small to medium teams.

### 1.5 Trunk-Based Development

Trunk-based development emphasizes that all developers frequently submit small batches of changes to the trunk branch (usually `main`), a model adopted by companies like Google and Facebook.

```
main ──●──●──●──●──●──●──●──●──●──●──→
        ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
       Short-lived branches (lifespan < 1 day)
```

**Core Principles**:

- Branch lifespan extremely short (usually not exceeding one day)
- Frequent integration, reduce merge conflicts
- Depend on Feature Flags to control unfinished features
- Highly depend on automated testing

```bash
# Typical flow
git checkout main
git pull
git checkout -b quick-fix-123
# Small change...
git commit -m "fix: Fix order calculation precision issue"
git push origin quick-fix-123
# Create PR, quick review, merge
```

**Applicable Scenarios**: Mature DevOps teams, projects with complete automated testing.

### 1.6 Model Selection Decision Table

| Factor | Centralized | Feature Branch | Git Flow | GitHub Flow | Trunk-Based |
|--------|------------|----------------|----------|-------------|-------------|
| Team Size | 1-2 people | 3-10 people | 5-20 people | 3-15 people | 5-50+ people |
| Release Frequency | Not fixed | On demand | Regular | Continuous | Continuous |
| Learning Cost | Very low | Low | Medium | Low | Medium |
| Parallel Development | Not supported | Supported | Supported | Supported | Supported |
| Version Maintenance | None | Single version | Multiple versions | Single version | Single version |
| Automation Requirement | Low | Medium | Medium | Medium | High |

---

## 2. Branch Strategy and Naming Standards

### 2.1 Branch Naming Standards

Unified branch naming standards can help team members quickly understand branch purposes. Recommend using following format:

```
<type>/<ticket-id>-<short-description>
```

**Common Type Prefixes**:

| Prefix | Usage | Example |
|--------|-------|---------|
| `feature/` | New feature | `feature/PROJ-123-user-login` |
| `fix/` | Bug fix | `fix/PROJ-456-null-pointer` |
| `hotfix/` | Production emergency fix | `hotfix/PROJ-789-payment-error` |
| `release/` | Release preparation | `release/v2.1.0` |
| `docs/` | Documentation update | `docs/PROJ-100-api-docs` |
| `refactor/` | Code refactoring | `refactor/PROJ-200-auth-module` |
| `test/` | Test related | `test/PROJ-300-e2e-tests` |
| `chore/` | Build/tool | `chore/PROJ-400-update-deps` |

**Naming Rules**:

- Use lowercase letters and hyphens (kebab-case)
- Avoid special characters and spaces
- Include Issue/Task number for tracking
- Description concise and clear

```bash
# Good naming
feature/SHOP-123-add-cart
fix/SHOP-456-fix-login-error
hotfix/SHOP-789-payment-timeout

# Bad naming
feature/NewFeature          # No ticket number
fix/bug                     # Description too vague
FEATURE/SHOP-123            # Don't use uppercase
feature_add_cart            # Use underscores instead of hyphens
```

### 2.2 Commit Message Standards (Conventional Commits)

Commit messages are an important part of code history. Adopting Conventional Commits specification can make commit history clear and readable.

**Format Template**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type Description**:

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): Add WeChat login` |
| `fix` | Bug fix | `fix(api): Fix pagination parameter parsing error` |
| `docs` | Documentation change | `docs(readme): Update deployment instructions` |
| `style` | Code format (no logic impact) | `style: Unify indentation to 4 spaces` |
| `refactor` | Refactoring (neither new feature nor fix) | `refactor(db): Optimize query performance` |
| `perf` | Performance optimization | `perf(render): Reduce initial load time` |
| `test` | Test related | `test(auth): Add login unit tests` |
| `build` | Build system or external dependencies | `build: Upgrade webpack to v5` |
| `ci` | CI configuration change | `ci: Add GitHub Actions workflow` |
| `chore` | Other miscellaneous | `chore: Clean unused files` |
| `revert` | Rollback | `revert: Rollback feat(auth) changes` |

**Actual Examples**:

```
feat(user): Implement user registration feature

- Add email verification
- Implement password strength check
- Integrate SMS verification code service

Closes #123
Refs #124
```

```
fix(payment): Fix WeChat payment callback signature verification failure

WeChat payment V3 version's signature verification logic has case sensitivity issue,
causing some callback requests to be incorrectly rejected.

Fixes #456
```

**Recommended Tools**:

```bash
# Use commitizen to assist commits
npm install -g commitizen cz-conventional-changelog
echo '{ "path": "cz-conventional-changelog" }' > ~/.czrc

# Then use git cz instead of git commit
git cz
```

---

## 3. Pull Request Workflow Best Practices

### 3.1 Create High-quality Pull Request

A good PR description can significantly improve Code Review efficiency.

**PR Template Example** (`.github/pull_request_template.md`):

```markdown
## Change Description

Briefly describe the content and purpose of this change.

## Change Type

- [ ] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Documentation update (docs)
- [ ] Code refactoring (refactor)
- [ ] Performance optimization (perf)
- [ ] Test related (test)
- [ ] Other (chore)

## Related Issues

Closes #123
Refs #456

## Change Details

- Change point 1
- Change point 2
- Change point 3

## Testing Instructions

Describe how to test this change:

1. Step 1
2. Step 2
3. Expected result

## Screenshots/Screen Recording

(If there are UI changes, please attach screenshots or screen recordings)

## Self-check List

- [ ] Code conforms to team coding standards
- [ ] Unit tests added/updated
- [ ] Related documentation updated
- [ ] No new lint warnings or errors
- [ ] Local tests passed
```

### 3.2 PR Size Control

Keeping PRs small and focused is key to improving Review efficiency.

| PR Size | Code Lines | Review Time | Suggestion |
|---------|------------|-------------|------------|
| Micro | < 50 lines | < 15 minutes | Ideal size |
| Small | 50-200 lines | 15-30 minutes | Recommended |
| Medium | 200-500 lines | 30-60 minutes | Acceptable |
| Large | 500-1000 lines | 1-2 hours | Consider splitting |
| Very Large | > 1000 lines | > 2 hours | Must split |

**Split Strategy**:

```
Large feature PR → Split into multiple small PRs:

PR 1: Database model and migration
PR 2: API interface implementation
PR 3: Frontend component development
PR 4: Integration tests
PR 5: Documentation update
```

### 3.3 PR Workflow

```
Create Branch → Develop → Self-test → Push → Create PR
                                              ↓
                                       CI Auto Check
                                              ↓
                                    ┌── Pass ←─┤
                                    ↓          │
                                Code Review   Fail
                                    ↓          ↓
                             ┌── Approve ←─┤  Fix Issues
                             ↓          │      ↓
                           Merge        Request Changes ──→ Modify Code
                             ↓                          ↓
                          Deploy/Release              Resubmit
```

**Specific Operations**:

```bash
# 1. Ensure branch is up to date
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main

# 2. Run local checks
npm run lint
npm run test
npm run build

# 3. Push and create PR
git push origin feature/my-feature

# 4. Modify according to Review comments
git add .
git commit -m "fix: Modify according to review comments"
git push origin feature/my-feature

# 5. Cleanup after merge
git checkout main
git pull origin main
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

---

## 4. Code Review Standards and Process

### 4.1 Value of Code Review

Code Review is not just about finding bugs, but also a core means of knowledge sharing, team growth and code quality assurance.

**Core Goals of Code Review**:

- Discover potential logic errors and security vulnerabilities
- Ensure code conforms to team standards
- Promote knowledge dissemination in team
- Improve code maintainability
- Help junior developers grow

### 4.2 Reviewer Guide

**Key Review Items**:

```
□ Functional Correctness
  - Does code implement requirements
  - Are boundary conditions handled
  - Is error handling complete

□ Code Quality
  - Is naming clear
  - Are functions single responsibility
  - Is there duplicate code
  - Are there magic numbers/strings

□ Performance Considerations
  - Are there N+1 queries
  - Are there unnecessary loops
  - Memory leak risks

□ Security
  - Is input validated
  - Are there injection risks
  - Is sensitive information exposed

□ Test Coverage
  - Are there unit tests
  - Are test cases sufficient
  - Are boundary conditions covered

□ Maintainability
  - Is code easy to understand
  - Are there sufficient comments
  - Does documentation need updating
```

**Review Comment Standards**:

```markdown
# Comment Prefix Conventions

[Must Fix] Has bugs or serious issues, must fix
[Suggest Fix] Can be improved, strongly suggest fix
[Question] Need author explanation or clarification
[Praise] Code written well, worth learning
[Non-blocking] Small suggestion, doesn't block merge
```

**Example Comments**:

```markdown
[Must Fix] There's SQL injection risk here, user input directly concatenated into SQL statement.
Suggest using parameterized query:
```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

[Suggest Fix] This function has 200 lines, suggest splitting into smaller functions for readability.

[Question] Why choose double-checked locking instead of synchronized here?

[Praise] This error handling logic is elegantly written!
```

### 4.3 Author Guide

**Self-check Before Submitting Review**:

1. Review code yourself first
2. Ensure all CI checks pass
3. Provide clear PR description
4. Mark areas needing special attention
5. Control PR size within reasonable range

**Attitude Towards Review Comments**:

- Maintain open mind, focus on matter not person
- Comments you don't understand, communicate first, don't directly ignore
- Handle agreed modifications promptly
- Give reasonable explanations for disagreed comments

### 4.4 Code Review Process

```
1. Author submits PR
       ↓
2. CI Auto Check (lint, test, build)
       ↓
   ┌── Pass ←──┐
   ↓           │
3. Assign Reviewer  Fail → Author fixes
   ↓
4. Reviewer reviews code
   ↓
   ┌── Approve ──────────┐
   │                     │
   ├── Request Changes ──→ Author fixes → Back to step 3
   │                     │
   └── Comment Discuss ──→ Reach consensus
   ↓
5. Get sufficient approvals (usually 1-2 people)
   ↓
6. Merge PR
```

---

## 5. CODEOWNERS File Configuration

CODEOWNERS file is used to automatically designate code owners, when this code is modified, system will automatically request corresponding owners to Review.

### 5.1 Basic Configuration

Create `CODEOWNERS` file in repository root or `.github/` directory:

```bash
# CODEOWNERS file location (by priority):
# 1. Root directory /CODEOWNERS
# 2. docs/CODEOWNERS
# 3. .github/CODEOWNERS
```

### 5.2 Configuration Syntax

```bash
# Global owners - applies to all files
*                       @team-lead @senior-dev

# Frontend code is responsible for frontend team
/src/frontend/          @org/frontend-team
*.css                   @org/frontend-team
*.html                  @org/frontend-team
*.js                    @org/frontend-team
*.tsx                   @org/frontend-team
*.ts                    @org/frontend-team

# Backend code is responsible for backend team
/src/backend/           @org/backend-team
*.py                    @org/backend-team
*.java                  @org/backend-team

# Database related is responsible for DBA team
*.sql                   @org/dba-team
/db/migrations/         @org/dba-team

# API documentation is jointly responsible for backend and docs teams
/docs/api/              @org/backend-team @org/docs-team

# CI/CD configuration is responsible for DevOps team
/.github/               @org/devops-team
/Dockerfile             @org/devops-team
/docker-compose.yml     @org/devops-team
/Jenkinsfile            @org/devops-team

# Security related files need security team approval
/src/auth/              @org/security-team
/src/crypto/            @org/security-team
*.pem                   @org/security-team

# Dependency file changes need architect approval
/package.json           @org/architect
/requirements.txt       @org/architect
/pom.xml                @org/architect

# Files specifically owned by individuals
/README.md              @zhangsan
/CONTRIBUTING.md        @zhangsan
/LICENSE                @zhangsan
```

### 5.3 CODEOWNERS Best Practices

1. **Keep Updated**: Update CODEOWNERS promptly when code responsibilities change
2. **Avoid Too Many Global Approvers**: Each file only needs 1-2 approvers
3. **Use Teams Instead of Individuals**: Easier to manage batch changes and personnel changes
4. **Combine with Branch Protection Rules**: Require CODEOWNERS approval before merge

---

## 6. Branch Protection Rules

Branch protection rules can enforce specific workflow standards, ensuring code quality.

### 6.1 Configuration Path

```
Settings → Branches → Add rule
```

### 6.2 Core Protection Options

**Recommended Configuration for `main` Branch**:

```yaml
Branch name pattern: main

# Pull Request Requirements
☑ Require a pull request before merging
  ☑ Require approvals: 2
  ☑ Dismiss stale pull request approvals when new commits are pushed
  ☑ Require review from Code Owners

# Status Check Requirements
☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  Required check items:
    - ci/build
    - ci/test
    - ci/lint
    - security/scan

# Merge Requirements
☑ Require conversation resolution before merging
☑ Require linear history (prohibit merge commits)

# Push Restrictions
☑ Restrict pushes that create files
☐ Allow force pushes (Prohibited)
☐ Allow deletions (Prohibited)

# Administrators
☐ Include administrators (Recommend checking, let administrators also follow rules)
```

### 6.3 Protection Strategies for Different Branches

```
main (Production branch)
├── Strictest protection
├── Require 2 Reviewer approvals
├── Require all CI checks pass
├── Require CODEOWNERS approval
├── Prohibit force push
└── Prohibit direct push

develop (Development branch)
├── Medium protection
├── Require 1 Reviewer approval
├── Require CI checks pass
└── Allow administrators to bypass

release/* (Release branches)
├── Relatively strict protection
├── Require 1 Reviewer approval
├── Require all CI checks pass
└── Only allow specific personnel to push
```

---

## 7. GitHub Rulesets Details

GitHub Rulesets is a next-generation branch management rule system provided by GitHub, more flexible and powerful than traditional Branch Protection Rules.

### 7.1 Rulesets vs Traditional Branch Protection

| Feature | Traditional Branch Protection | Rulesets |
|---------|------------------------------|----------|
| Rule Granularity | One set of rules per branch pattern | Can combine multiple rule sets |
| Target Scope | Branches only | Branches + Tags |
| Inheritance | None | Supports rule inheritance and override |
| Execution Mode | Always blocking | Supports bypass |
| Flexibility | Relatively low | Highly flexible |

### 7.2 Create Ruleset

**Path**: `Settings → Rules → Rulesets → New ruleset`

**Create Branch Rule Set**:

```json
{
  "name": "Main Branch Protection Rules",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main", "refs/heads/release/*"]
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 2,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "require_last_push_approval": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          { "context": "ci/build" },
          { "context": "ci/test" },
          { "context": "ci/lint" }
        ],
        "strict_required_status_checks_policy": true
      }
    },
    {
      "type": "required_signatures",
      "parameters": {}
    },
    {
      "type": "non_fast_forward",
      "parameters": {}
    },
    {
      "type": "deletion",
      "parameters": {}
    }
  ],
  "bypass_actors": [
    {
      "actor_id": 1,
      "actor_type": "OrganizationAdmin",
      "bypass_mode": "always"
    }
  ]
}
```

### 7.3 Create Tag Rule Set

```json
{
  "name": "Release Tag Protection",
  "target": "tag",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/tags/v*"]
    }
  },
  "rules": [
    {
      "type": "creation",
      "parameters": {}
    },
    {
      "type": "update",
      "parameters": {}
    },
    {
      "type": "required_signatures",
      "parameters": {}
    }
  ]
}
```

### 7.4 Rulesets Hierarchy

```
Organization Rulesets (Organization level)
    ↓ Inheritance and override
Repository Rulesets (Repository level)
    ↓ Inheritance and override
Specific Branch Rules

Priority: Repository level > Organization level
```

### 7.5 Rulesets Best Practices

1. **Organization-level defines base rules**: Ensure basic protection for all repositories
2. **Repository-level extends as needed**: For specific repository special needs
3. **Use bypass roles**: Allow administrators to bypass rules in emergencies
4. **Regular review**: Adjust rules according to team needs

---

## 8. Team Permission Management (Roles and Permissions)

### 8.1 GitHub Permission Model Overview

GitHub permissions are divided into two levels: organization level and repository level.

**Organization Level Roles**:

| Role | Permission Scope |
|------|------------------|
| Owner | Full control of organization, including deleting organization |
| Member | Can view organization info, access authorized repositories |

**Repository Level Permissions**:

| Permission Level | Description |
|------------------|-------------|
| Read | Can view and clone code |
| Triage | Can manage Issues and PRs (cannot push code) |
| Write | Can push code, merge PRs |
| Maintain | Includes Write permissions, plus manage repository settings |
| Admin | Full control of repository |

### 8.2 Team Structure Design

```
Organization (Company/Organization)
├── @company/admins        → Admin permissions (Infrastructure team)
├── @company/maintainers   → Maintain permissions (Technical leads)
│
├── @frontend-team         → Write permissions
│   ├── @frontend-team/senior
│   └── @frontend-team/junior
│
├── @backend-team          → Write permissions
│   ├── @backend-team/senior
│   └── @backend-team/junior
│
├── @qa-team               → Triage permissions
├── @design-team           → Read permissions
└── @contractors           → Read permissions (Outsourced team)
```

### 8.3 Permission Configuration Practice

**Create Teams and Assign Permissions**:

```bash
# Use GitHub CLI to manage teams
gh api -X POST orgs/{org}/teams \
  -f name='frontend-team' \
  -f description='Frontend development team' \
  -f privacy='closed'

# Add repository access permissions for team
gh api -X PUT orgs/{org}/teams/{team_slug}/repos/{owner}/{repo} \
  -f permission='push'
```

**Fine-grained Personal Access Tokens**:

```yaml
# Create dedicated Token for CI/CD
Token Name: ci-deploy-bot
Repository Access: Only specific repositories
Permissions:
  - Contents: Read
  - Actions: Write
  - Deployments: Write
  - Packages: Read
Expiration: 90 days
```

### 8.4 Permission Management Best Practices

1. **Principle of Least Privilege**: Only grant minimum permissions needed to complete work
2. **Use Teams Instead of Individuals**: Easier for batch management and personnel changes
3. **Regular Audit**: Review permission assignments quarterly
4. **Timely Revoke**: Immediately remove permissions when members leave
5. **Enable SSO**: Enterprise users enable SAML SSO
6. **PAT Management**: Regularly check and rotate Personal Access Tokens

---

## 9. Issue and Project Management Standards

### 9.1 Issue Management Standards

**Issue Template Configuration** (`.github/ISSUE_TEMPLATE/bug_report.md`):

```markdown
---
name: Bug Report
about: Submit bug report
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

Briefly describe the bug's behavior.

## Steps to Reproduce

1. Open '...'
2. Click '...'
3. Scroll to '...'
4. See error

## Expected Behavior

Describe the behavior you expect.

## Actual Behavior

Describe the behavior that actually occurred.

## Environment Information

- Operating System: [e.g., Windows 11]
- Browser: [e.g., Chrome 120]
- Node.js Version: [e.g., v18.17.0]

## Screenshots/Logs

(Attach relevant screenshots or error logs)

## Additional Information

(Other relevant information)
```

**Feature Request Template** (`.github/ISSUE_TEMPLATE/feature_request.md`):

```markdown
---
name: Feature Request
about: Propose new feature suggestion
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Feature Description

Briefly describe the feature you hope to add.

## Use Case

Describe the use case and value of this feature.

## Expected Solution

Describe the implementation approach you expect.

## Alternative Solutions

Describe other alternative solutions you've considered.

## Additional Information

(Other relevant information)
```

### 9.2 Issue Label System

Establishing a complete label system helps Issue classification and priority management.

**Recommended Label Categories**:

```yaml
# Type Labels
type/bug: Bug fix
type/feature: New feature
type/docs: Documentation
type/refactor: Refactoring
type/test: Testing
type/chore: Miscellaneous

# Priority Labels
priority/critical: Urgent, handle immediately
priority/high: High priority
priority/medium: Medium priority
priority/low: Low priority

# Status Labels
status/needs-triage: Awaiting classification
status/accepted: Accepted
status/in-progress: In progress
status/blocked: Blocked
status/wontfix: Won't fix
status/duplicate: Duplicate

# Module Labels
module/auth: Authentication module
module/payment: Payment module
module/user: User module
module/api: API module

# Difficulty Labels
difficulty/easy: Easy
difficulty/medium: Medium
difficulty/hard: Hard

# Other Labels
good-first-issue: Suitable for beginners
help-needed: Needs help
breaking-change: Breaking change
security: Security related
```

### 9.3 GitHub Projects Management

GitHub Projects provides Kanban-like project management functionality.

**Board Column Design**:

```
Backlog → To Do → In Progress → In Review → Done
(Pending) (Plan)  (In Progress) (Reviewing) (Complete)
```

**Sprint Management Example**:

```yaml
Sprint Cycle: 2 weeks
Sprint Planning: Select Issues from Backlog at Sprint start
Daily Stand-up: Review board, update status
Sprint Review: Summarize completion, improve process

Custom Fields:
  - Sprint: Sprint 1, Sprint 2, Sprint 3...
  - Story Points: 1, 2, 3, 5, 8, 13
  - Priority: P0, P1, P2, P3
  - Due Date: Date
  - Owner: Assignee
```

### 9.4 Issue and PR Association

```markdown
# Associate Issue in PR description
Closes #123      # Auto-close Issue after PR merge
Fixes #456       # Same as above
Resolves #789    # Same as above
Refs #100        # Only reference, don't auto-close

# Associate in Commit message
git commit -m "fix(auth): Fix login timeout issue

Fixes #123"
```

---

## 10. Team Communication Best Practices

### 10.1 GitHub Discussions

GitHub Discussions is a discussion area within repository, suitable for non-code related technical discussions.

**Enable Discussions**: `Settings → General → Features → Discussions`

**Recommended Categories**:

| Category | Usage |
|----------|-------|
| 💬 General | General discussion |
| 🙏 Q&A | Q&A (supports accepting answers) |
| 💡 Ideas | Ideas and suggestions |
| 📢 Announcements | Announcements (only maintainers can post) |
| 📖 Show and Tell | Showcase works |
| 🗳️ Polls | Voting |

### 10.2 PR and Issue Comment Standards

```markdown
# Good comment examples

## Provide context
"Regarding this implementation, I encountered similar scenario in project X,
at that time adopted solution B, because..."

## Give specific suggestions
"Suggest splitting this function into two:
1. `validateInput()` responsible for input validation
2. `processData()` responsible for data processing
This can improve testability."

## Express gratitude
"Thank you for fixing this issue! Test cases are very comprehensive."

# Bad comment examples

"This code is wrong"              # Too vague, didn't say what's wrong
"LGTM"                            # Too simple for complex changes
"Why did you do it this way?"     # With questioning tone, suggest changing to
                                  # "What's the consideration for this implementation?"
```

### 10.3 Communication Tool Integration

```yaml
# Notification channel configuration

Slack/Microsoft Teams:
  - New PR creation notifications
  - CI status change notifications
  - Issue assignment notifications
  - Release notifications

Email Notifications:
  - @mention mentions
  - Review requests
  - Issue assignments
  - Important announcements

GitHub Mobile:
  - Real-time push notifications
  - Quick reply to comments
  - Approve PRs
```

### 10.4 Asynchronous Communication Principles

1. **Write Clearly**: Provide sufficient context information
2. **Use Documentation Instead of Verbal**: Record important decisions in Issues or Wikis
3. **Set Reasonable Response Time**: Reply within 24 hours for non-urgent issues
4. **Use Emoji Responses**: Use 👀 to indicate seen, 👍 to indicate agreed
5. **Use Quotes Well**: Quote specific content to respond

---

## 11. Multi-repo Collaboration

### 11.1 Git Submodules

Git Submodules allow referencing a specific version of another repository within a repository.

```bash
# Add submodule
git submodule add https://github.com/org/shared-lib.git libs/shared-lib

# Clone repository with submodules
git clone --recurse-submodules https://github.com/org/main-project.git

# Or step by step
git clone https://github.com/org/main-project.git
git submodule init
git submodule update

# Update submodule to latest version
cd libs/shared-lib
git pull origin main
cd ../..
git add libs/shared-lib
git commit -m "chore: Update shared-lib to latest version"

# Batch update all submodules
git submodule update --remote --merge
```

**`.gitmodules` File Example**:

```ini
[submodule "libs/shared-lib"]
    path = libs/shared-lib
    url = https://github.com/org/shared-lib.git
    branch = main
[submodule "libs/ui-components"]
    path = libs/ui-components
    url = https://github.com/org/ui-components.git
    branch = main
```

**Submodules Advantages and Disadvantages**:

| Advantages | Disadvantages |
|------------|---------------|
| Precise version locking | Complex operations, error-prone |
| Clear code isolation | High learning cost for newcomers |
| Supports different permission controls | Complex CI/CD configuration |

### 11.2 Git Subtree

Git Subtree is an alternative to Submodules, directly merging sub-repository code into main repository.

```bash
# Add subtree
git subtree add --prefix=libs/shared-lib https://github.com/org/shared-lib.git main --squash

# Update subtree
git subtree pull --prefix=libs/shared-lib https://github.com/org/shared-lib.git main --squash

# Push modifications back to sub-repository
git subtree push --prefix=libs/shared-lib https://github.com/org/shared-lib.git main
```

**Subtree vs Submodules Comparison**:

| Feature | Submodule | Subtree |
|---------|-----------|---------|
| Code Storage | Only stores reference | Stores complete code |
| Clone Speed | Slower (needs additional pull) | Faster |
| Operation Complexity | High | Medium |
| History Record | Separate | Merged |
| Learning Cost | High | Medium |

### 11.3 GitHub Package Registry

GitHub Packages can publish shared libraries as packages, referenced through package managers.

```yaml
# Publish npm package to GitHub Packages
# package.json
{
  "name": "@myorg/shared-lib",
  "version": "1.0.0",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}

# .npmrc
@myorg:registry=https://npm.pkg.github.com

# Use package
npm install @myorg/shared-lib
```

**Publish Workflow** (`.github/workflows/publish.yml`):

```yaml
name: Publish Package

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          registry-url: 'https://npm.pkg.github.com'
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 12. Team CI/CD Standards

### 12.1 CI/CD Workflow Design

```
Code Commit → Lint Check → Unit Test → Build → Integration Test → Deploy Staging → E2E Test → Deploy Production
```

### 12.2 Standard CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Code Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    name: Unit Test
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm run test -- --coverage
      - uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    name: Build Verification
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/

  e2e:
    name: E2E Test
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/
      - run: npm ci
      - run: npm run test:e2e
```

### 12.3 CD Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    name: Deploy Staging Environment
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        run: |
          # Deploy script
          echo "Deploying to staging..."
      - name: Run Smoke Tests
        run: |
          # Smoke tests
          echo "Running smoke tests..."

  deploy-production:
    name: Deploy Production Environment
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://www.example.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        run: |
          # Deploy script
          echo "Deploying to production..."
```

### 12.4 CI/CD Best Practices

1. **Cache Dependencies**: Use `actions/cache` or package manager built-in cache
2. **Parallel Execution**: Run independent tasks in parallel to save time
3. **Matrix Testing**: Test on multiple environments/versions
4. **Security Scanning**: Integrate CodeQL, Dependabot and other security tools
5. **Environment Separation**: Use Environments to manage different environment deployments
6. **Secret Management**: Use GitHub Secrets to store sensitive information
7. **Status Checks**: Set CI results as PR merge requirements

---

## 13. Knowledge Management and Documentation Collaboration

### 13.1 Essential Project Documentation

```markdown
# Project Documentation Checklist

## Basic Documentation
├── README.md              # Project introduction, quick start
├── CONTRIBUTING.md        # Contribution guide
├── CODE_OF_CONDUCT.md     # Code of conduct
├── LICENSE                # Open source license
├── CHANGELOG.md           # Changelog
└── SECURITY.md            # Security policy

## Development Documentation
├── docs/
│   ├── architecture.md    # Architecture design
│   ├── api/               # API documentation
│   ├── guides/            # Usage guides
│   ├── development.md     # Development environment setup
│   ├── deployment.md      # Deployment guide
│   └── troubleshooting.md # Common issues
```

### 13.2 README.md Structure

```markdown
# Project Name

Short project description.

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Requirements

- Node.js >= 18
- npm >= 9

### Installation

```bash
git clone https://github.com/org/project.git
cd project
npm install
```

### Run

```bash
npm run dev
```

## Documentation

- [Architecture Design](docs/architecture.md)
- [API Documentation](docs/api/README.md)
- [Deployment Guide](docs/deployment.md)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
```

### 13.3 CHANGELOG Standards

Adopt [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

This project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description

## [1.2.0] - 2024-01-15

### Added
- Add user export feature
- Support WeChat login

### Fixed
- Fix pagination calculation error
- Fix file upload timeout issue

## [1.1.0] - 2024-01-01

### Added
- Add data statistics feature

### Changed
- Optimize homepage load speed
```

### 13.4 Wiki Usage Scenarios

GitHub Wiki is suitable for maintaining long-term, multi-person collaborative knowledge documentation:

```yaml
Wiki Applicable Scenarios:
  - Project Architecture Decision Records (ADR)
  - Development specification documentation
  - Operations manual
  - Meeting minutes
  - Team knowledge base

Wiki Not Applicable Scenarios:
  - Documentation needing version management (store in repository)
  - API documentation (use auto-generation tools)
  - Temporary notes (use Issues or Discussions)
```

---

## 14. Remote Team Collaboration Experience

### 14.1 Asynchronous Collaboration Principles

The core of remote teams is asynchronous collaboration, reducing dependence on real-time communication.

```yaml
Asynchronous Collaboration Key Points:
  1. Write Clearly:
     - Issue/PR descriptions should be detailed
     - Comments should provide sufficient context
     - Decisions should record reasons

  2. Use Documentation Instead of Verbal:
     - Important discussions in Issues/Discussions
     - Technical solutions written as RFC documents
     - Meeting conclusions recorded in Wiki

  3. Set Reasonable Response Time:
     - Non-urgent: Reply within 24 hours
     - Normal: Reply within 4 hours
     - Urgent: Use instant messaging tools

  4. Use GitHub Features Well:
     - @mention relevant personnel
      - Use 👀 to indicate seen
      - Use 👍 to indicate agreed
     - Draft PR for early feedback
```

### 14.2 Time Zone Difference Management

```
Typical Scenario: Chinese team collaborating with overseas team

Chinese Team (UTC+8)          Overseas Team (UTC-8)
09:00 - 18:00              17:00 - 02:00 (Next day)
     ↑                          ↑
     └──── Overlap Time ────────┘
           (17:00 - 18:00)
```

**Coping Strategies**:

1. **Handover Documents**: Update work progress and to-do items at end of each day
2. **Asynchronous Code Review**: Use PR comments for asynchronous Review
3. **Screen Recording Explanations**: Record video explanations for complex issues
4. **Overlap Time Utilization**: Concentrate issues needing real-time discussion in overlap time period
5. **Rotate Meeting Times**: Rotate meeting times across different time zones

### 14.3 Team Collaboration Tool Chain

```yaml
Code Collaboration:
  - GitHub (Code hosting, PR, Issue)
  - VS Code + Live Share (Remote pair programming)

Instant Messaging:
  - Slack / Microsoft Teams / Feishu / DingTalk
  - For daily communication and quick questions

Documentation Collaboration:
  - GitHub Wiki / Notion / Feishu Docs
  - For knowledge management and documentation collaboration

Project Management:
  - GitHub Projects / Jira / Linear
  - For task management and progress tracking

Video Conferencing:
  - Tencent Meeting / Zoom / Google Meet
  - For weekly meetings and important discussions
```

---

## 15. Best Practices for Chinese Development Teams Using GitHub

### 15.1 Network Access Optimization

China has unstable network access to GitHub, here are several optimization solutions:

**Solution 1: SSH Protocol**

```bash
# Configure SSH (more stable than HTTPS)
git config --global url."git@github.com:".insteadOf "https://github.com/"

# SSH configuration optimization (~/.ssh/config)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    TCPKeepAlive yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Solution 2: GitHub Mirror Acceleration**

```bash
# Use ghproxy and other mirrors for acceleration
git config --global url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"

# Or use Gitee mirror
# 1. Fork repository to Gitee
# 2. Clone from Gitee
# 3. Add GitHub as upstream
git remote add upstream https://github.com/original/repo.git
```

**Solution 3: Use Proxy**

```bash
# Configure Git proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# Only use proxy for GitHub
git config --global http.https://github.com.proxy http://127.0.0.1:7890
```

### 15.2 Bilingual Collaboration Standards

For projects with international collaborators, recommend adopting bilingual standards:

```markdown
# Issue template supports bilingual

## Bug Description / Bug Description

Chinese description...

English description...

## Steps to Reproduce / Steps to Reproduce

1. Step 1 / Step 1
2. Step 2 / Step 2
```

**Bilingual Commit Messages**:

```
feat(auth): Add WeChat Login / Add WeChat Login

Implement WeChat login based on OAuth 2.0.
Implement WeChat login based on OAuth 2.0.

Closes #123
```

### 15.3 Domestic Alternative Solutions Comparison

| Feature | GitHub | Gitee | Gitea | GitLab |
|---------|--------|-------|-------|--------|
| Hosting | ✅ | ✅ | Self-hosted | Self-hosted/SaaS |
| Access Speed | Slow | Fast | Fast | Fast |
| CI/CD | Actions | Pipeline | Actions | CI |
| Ecosystem | Rich | Medium | Medium | Rich |
| Private Repos | Free | Free | Free | Free |
| Internationalization | Good | Average | Good | Good |

**Mixed Usage Strategy**:

```
International Open Source Projects → GitHub
Domestic Private Projects → Gitee / GitLab Self-hosted
Need Fast Access → Gitee Mirror + GitHub Source
Enterprise Projects → GitLab Self-hosted (Data Security)
```

### 15.4 Compliance and Security Considerations

```yaml
Data Compliance:
  - Don't put sensitive data in GitHub public repositories
  - Use .gitignore to exclude configuration files
  - Regularly scan repositories for sensitive information
  - Use GitHub Secret Scanning

Intellectual Property:
  - Choose appropriate open source license
  - Note third-party library license compatibility
  - Separate enterprise code from personal code

Security Practices:
  - Enable Two-Factor Authentication (2FA)
  - Use Fine-grained PAT
  - Regularly rotate keys
  - Enable Dependabot security updates
```

### 15.5 Team Collaboration Tool Recommendations

```yaml
Code Hosting and Collaboration:
  - GitHub (preferred for international projects)
  - Gitee (Fast domestic access)
  - Coding (Tencent subsidiary)

Instant Messaging:
  - Feishu (Comprehensive features, integrated docs)
  - DingTalk (Many enterprise users)
  - Enterprise WeChat (Interoperable with WeChat)

Documentation Collaboration:
  - Feishu Docs (Good collaboration experience)
  - Yuque (Knowledge management)
  - Notion (Powerful features)

Project Management:
  - GitHub Projects (Integrates with code)
  - Feishu Projects (Integrates with Feishu)
  - TAPD (Tencent Agile Development)

CI/CD:
  - GitHub Actions (Integrates with GitHub)
  - Yunxiao (Alibaba Cloud)
  - Tencent Cloud CODING
```

---

## Summary

Efficient GitHub team collaboration needs to establish standards at the following levels:

```
                    ┌─────────────┐
                    │   Culture   │
                    │  Open, Trust│
                    │  Knowledge  │
                    │  Sharing    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Process   │
                    │  Branch     │
                    │  Strategy   │
                    │  PR Process │
                    │  Code Review│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Tools     │
                    │  Branch     │
                    │  Protection │
                    │  CI/CD      │
                    │  Automation │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Standards  │
                    │  Naming     │
                    │  Commit     │
                    │  Document   │
                    └─────────────┘
```

**Key Points Review**:

1. **Choose collaboration model suitable for team**, don't blindly pursue complexity
2. **Establish unified branch naming and commit standards**, keep code history clear
3. **PRs should be small and focused**, reduce Review cost
4. **Code Review is learning opportunity**, not fault-finding competition
5. **Use CODEOWNERS and branch protection well**, automate standard enforcement
6. **Documentation is team's common wealth**, continuously maintain and update
7. **Asynchronous first**, reduce unnecessary meetings
8. **Focus on network and compliance**, Chinese characteristic practical experience
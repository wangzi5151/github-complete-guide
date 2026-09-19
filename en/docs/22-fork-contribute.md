# Fork and Open Source Contribution Complete Guide

> Open source has changed the way software is developed, and Fork is the core mechanism for participating in open source. This chapter will take you from zero to master the Fork workflow, and learn how to submit your first Pull Request to an open source project.

---

## Table of Contents

- [1. Fork Concept Details](#1-fork-concept-details)
- [2. Fork Workflow Details](#2-fork-workflow-details)
- [3. Keep Fork Sync with Upstream](#3-keep-fork-sync-with-upstream)
- [4. Submit First Pull Request to Open Source Project](#4-submit-first-pull-request-to-open-source-project)
- [5. Fork Best Practices](#5-fork-best-practices)
- [6. Open Source Contribution Etiquette and Standards](#6-open-source-contribution-etiquette-and-standards)
- [7. How to Find Suitable Open Source Projects to Contribute](#7-how-to-find-suitable-open-source-projects-to-contribute)
- [8. Tips for Reading and Understanding Others' Code](#8-tips-for-reading-and-understanding-others-code)
- [9. Common Contribution Types](#9-common-contribution-types)
- [10. Code Standards and Testing Requirements of Open Source Projects](#10-code-standards-and-testing-requirements-of-open-source-projects)
- [11. Handling PR Rejection or Modification Requests](#11-handling-pr-rejection-or-modification-requests)
- [12. Path to Becoming Project Maintainer/Core Member](#12-path-to-becoming-project-maintainercore-member)
- [13. Using GitHub Star, Watch, Sponsor](#13-using-github-star-watch-sponsor)
- [14. Notes for Chinese Developers Participating in International Open Source Projects](#14-notes-for-chinese-developers-participating-in-international-open-source-projects)
- [15. Practical Case: Contributing Code to a Famous Project](#15-practical-case-contributing-code-to-a-famous-project)

---

## 1. Fork Concept Details

### 1.1 What is Fork

**Fork** is a collaboration mechanism provided by GitHub, allowing you to create a complete copy of others' repository under your own account. This copy is independent of the original repository, you can freely modify, experiment and develop in it without affecting the original project.

Use a plain metaphor to understand: Suppose the original project is a book manuscript, Fork is equivalent to you getting a copy of this manuscript, you can freely annotate and modify on the copy, while the original manuscript remains intact. When you think your modifications are valuable, you can suggest to the original author (Pull Request), the original author decides whether to adopt your modifications after review.

```
┌─────────────────────────────────────────────────────────────┐
│                      How Fork Works                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Original Repository (upstream)    Your Fork (origin)      │
│   ┌─────────────────┐         ┌─────────────────┐          │
│   │  owner/repo     │  Fork   │  you/repo       │          │
│   │                 │ ──────> │                 │          │
│   │  main branch    │         │  main branch    │          │
│   │  issues         │         │  Your changes   │          │
│   │  pull requests  │         │  Your branches  │          │
│   └─────────────────┘         └─────────────────┘          │
│           │                           │                     │
│           │      Pull Request         │                     │
│           │ <─────────────────────────┘                     │
│           │                                                 │
│           ▼                                                 │
│   ┌─────────────────┐                                      │
│   │  Merged code    │                                      │
│   └─────────────────┘                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Why Fork

Fork mechanism exists for the following core reasons:

**Permission Isolation and Security Protection**

Original repository owners don't need to grant you direct write permissions. You can freely modify in your own copy after Forking, only when your contribution is reviewed and approved will it be merged into the original project. This design protects the original project's code security.

**Sandbox Environment for Free Experimentation**

Fork provides you with an independent development environment. You can try new features, refactor code, fix bugs in it without worrying about affecting the original project's stability. Even if your modifications have problems, they only affect your own Fork.

**Foundation of Open Source Collaboration**

Fork is the core mechanism of open source community collaboration. Any developer worldwide can Fork an open source project, make improvements and submit Pull Request. This model allows open source projects to gather wisdom and contributions from around the world.

**Project Fork and Independent Development**

Sometimes, when a project's development direction doesn't match some users' needs, Fork can also be used to create an independent branch version. For example, the famous LibreSSL was Forked from OpenSSL.

### 1.3 Difference between Fork and Clone

Many beginners confuse Fork and Clone, they have essential differences:

| Feature | Fork | Clone |
|---------|------|-------|
| Location | Create copy on GitHub server | Download to local computer |
| Permissions | Need GitHub account | Anyone can Clone public repository |
| Relationship | Maintain traceable relationship with original repository | Don't automatically associate with original repository |
| Usage | Open source contribution, independent development | Local development, learning research |
| Network | Happens on GitHub platform | Happens on Git command line |

Usually, Fork and Clone are used together: first Fork to your own account, then Clone to local for development.

---

## 2. Fork Workflow Details

Complete Fork workflow includes six steps, forming a closed development loop:

```
Fork → Clone → Branch → Commit → Push → Pull Request
  │       │       │        │       │         │
  │       │       │        │       │         └── Submit contribution to original project
  │       │       │        │       └── Push to your remote repository
  │       │       │        └── Save your changes
  │       │       └── Create independent feature branch
  │       └── Download to local computer
  └── Create copy on GitHub
```

### 2.1 Step 1: Fork Repository

1. Open the GitHub repository page you want to contribute to
2. Click **Fork** button in top right corner of page
3. Select your account as Fork target
4. Wait for GitHub to complete Fork operation

After Fork is complete, a repository with the same name as the original repository will appear under your account, GitHub will automatically display "This repository was forked from original-owner/repo" prompt.

### 2.2 Step 2: Clone to Local

Clone your Forked repository to local computer:

```bash
# Clone using SSH (Recommended, need to configure SSH Key)
git clone git@github.com:your-username/repo-name.git

# Or clone using HTTPS
git clone https://github.com/your-username/repo-name.git

# Enter project directory
cd repo-name
```

### 2.3 Step 3: Add Upstream Repository

This is a critical step, allowing your local repository to get updates from the original project:

```bash
# Add original repository as upstream
git remote add upstream git@github.com:original-owner/repo-name.git

# Verify remote repository configuration
git remote -v
```

After executing `git remote -v`, you should see output similar to:

```
origin    git@github.com:your-username/repo-name.git (fetch)
origin    git@github.com:your-username/repo-name.git (push)
upstream  git@github.com:original-owner/repo-name.git (fetch)
upstream  git@github.com:original-owner/repo-name.git (push)
```

### 2.4 Step 4: Create Feature Branch

Before starting modifications, create a new feature branch from the latest main branch:

```bash
# Ensure you are on main branch
git checkout main

# Create and switch to new feature branch
git checkout -b feature/your-feature-name
```

Branch naming should use meaningful names, common naming conventions:

```bash
# Feature branches
feature/add-login-page
feature/improve-performance

# Bug fix branches
fix/fix-login-error
fix/correct-typo-in-readme

# Documentation branches
docs/update-api-documentation
docs/add-chinese-translation
```

### 2.5 Step 5: Modify and Commit

Make your code changes, then commit:

```bash
# View which files you modified
git status

# View specific changes
git diff

# Add modified files to staging area
git add modified-file

# Create commit with clear commit message
git commit -m "feat: Add user login feature

- Implemented JWT-based authentication
- Added login form component
- Wrote related unit tests

Closes #42"
```

**Standard commit message format:**

```
<type>(<scope>): <short description>

<detailed description>

<associated Issue>
```

Common types include:

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation update |
| `style` | Code format adjustment (no functionality change) |
| `refactor` | Code refactoring |
| `test` | Add or modify tests |
| `chore` | Build process or auxiliary tool changes |

### 2.6 Step 6: Push and Create Pull Request

```bash
# Push your feature branch to your Fork
git push origin feature/your-feature-name
```

After push is complete, visit your Fork page, GitHub will display a yellow prompt bar, click **Compare & pull request** button, fill in PR description and submit.

---

## 3. Keep Fork Sync with Upstream

Over time, the original repository will have new updates. Keeping your Fork synced with upstream is very important, this can avoid a large number of conflicts during later merges.

### 3.1 Configure Upstream Repository

If you haven't added upstream repository yet, first execute:

```bash
git remote add upstream git@github.com:original-owner/repo-name.git
```

### 3.2 Fetch Upstream Updates

```bash
# Fetch all branches and commits from upstream repository
git fetch upstream
```

### 3.3 Merge Upstream Updates to Your Fork

**Method 1: Use merge (Recommended for beginners)**

```bash
# Switch to main branch
git checkout main

# Merge upstream's main branch
git merge upstream/main

# Push update to your Fork
git push origin main
```

**Method 2: Use rebase (Keep commit history clean)**

```bash
# Switch to main branch
git checkout main

# Rebase your commits onto latest upstream commits
git rebase upstream/main

# Push update to your Fork (need force push after rebase)
git push origin main --force-with-lease
```

### 3.4 Choosing between merge and rebase

```
Use merge when:
├── You are a Git beginner
├── Others are developing based on your Fork
├── You want to preserve complete history
└── You are unsure which method to use

Use rebase when:
├── You are familiar with Git operations
├── You want to maintain linear commit history
├── Your Fork is only used by yourself
└── Your feature branch needs to sync upstream updates
```

### 3.5 Sync Feature Branch

If your feature branch also needs to sync latest upstream changes:

```bash
# Switch to your feature branch
git checkout feature/your-feature-name

# Method 1: merge
git merge upstream/main

# Method 2: rebase (Recommended, can make feature branch based on latest upstream code)
git rebase upstream/main
```

### 3.6 Set Regular Sync Habit

Recommend syncing upstream repository at the following times:

- Before starting new development work
- Before preparing to submit Pull Request
- When upstream repository has major updates
- Regularly (e.g., once a week)

---

## 4. Submit First Pull Request to Open Source Project

### 4.1 Preparation Before Submitting PR

Before submitting PR, please ensure completing the following checks:

```markdown
Pre-submission checklist:
□ Read project's CONTRIBUTING.md file
□ Read project's CODE_OF_CONDUCT.md file
□ Understood project's code style and standards
□ Run tests locally and passed
□ Added necessary test cases
□ Updated related documentation
□ Commit message conforms to project standards
□ Code synced with upstream
```

### 4.2 Write High-quality PR Description

A good PR description should include the following content:

```markdown
## Description

Briefly explain what this PR does, and why this modification is needed.

## Changes

- List your changes in detail
- Use list format for easy reading
- Each change point on a separate line

## Related Issues

Closes #123
Fixes #456
Related to #789

## Testing

Explain how you tested your changes:
- Which tests run locally
- Which scenarios manually tested
- Whether new test cases added

## Screenshots (if applicable)

If changes involve UI changes, please provide screenshots or GIFs.

## Other Notes

Any matters needing reviewer's attention.
```

### 4.3 Steps to Create PR

```bash
# 1. Ensure your code is up to date
git fetch upstream
git rebase upstream/main

# 2. Run tests
npm test  # Or other test commands

# 3. Push to your Fork
git push origin feature/your-feature-name

# 4. Visit GitHub to create PR
# GitHub will automatically display PR creation prompt
```

### 4.4 Process After PR Creation

```
Create PR
   │
   ▼
Auto Check (CI/CD)
   │
   ├── Pass ──> Maintainer Review
   │              │
   │              ├── Approve ──> Merge
   │              │
   │              └── Request Changes ──> Modify Code ──> Resubmit
   │
   └── Fail ──> Fix Issues ──> Repush
```

---

## 5. Fork Best Practices

### 5.1 Atomic Commit Principle

Each commit should only do one thing, maintain commit atomicity:

```bash
# ✅ Good practice: each commit only does one thing
git commit -m "fix: Fix login page form validation issue"
git commit -m "feat: Add remember password feature"
git commit -m "docs: Update login feature documentation"

# ❌ Bad practice: one commit contains multiple unrelated changes
git commit -m "Fix login issue, add new feature, update documentation"
```

### 5.2 Keep PR Small and Focused

One PR should only solve one problem or add one feature:

```
PR size suggestions:
├── Small PR: < 100 line changes (Best)
├── Medium PR: 100-300 line changes (Acceptable)
└── Large PR: > 300 line changes (Should be split)
```

If a PR is too large, consider splitting it into multiple small, independent PRs:

```bash
# Split one large PR into multiple small PRs
# PR 1: Add base structure
git checkout -b feature/base-structure
# ... Only add base code
git push origin feature/base-structure

# PR 2: Add core functionality
git checkout -b feature/core-functionality
# ... Add core functionality based on PR 1
git push origin feature/core-functionality

# PR 3: Add tests and documentation
git checkout -b feature/tests-docs
# ... Add tests and documentation
git push origin feature/tests-docs
```

### 5.3 Associate Issues

Associate related Issues in PR description, so that when PR is merged, Issue will automatically close:

```markdown
## Related Issues

Closes #123        # Auto-close #123 after PR merge
Fixes #456         # Auto-close #456 after PR merge
Related to #789    # Associate but don't auto-close
```

### 5.4 Keep Fork Clean

```bash
# Regularly delete merged feature branches
git branch -d feature/merged-feature

# Delete remote branch
git push origin --delete feature/merged-feature

# Regularly sync upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 5.5 Write Meaningful Commit Messages

```bash
# ✅ Good commit message
git commit -m "fix(auth): Fix JWT token expiration refresh issue

When JWT token expires, refresh token request fails because of
missing correct Authorization header.

Fix method: Use old token for authentication when refreshing token.

Fixes #234"

# ❌ Bad commit message
git commit -m "fix bug"
git commit -m "update"
git commit -m "WIP"
```

---

## 6. Open Source Contribution Etiquette and Standards

### 6.1 Basic Etiquette Guidelines

**Respect Maintainer's Time and Energy**

Open source project maintainers are usually volunteers working in their spare time. Before asking questions or submitting contributions, please:

- Read project documentation carefully
- Search existing Issues and PRs
- Ensure your question or contribution is valuable

**Stay Friendly and Professional**

In Issue and PR communications, always maintain politeness and respect:

```markdown
# ✅ Friendly communication
"Thank you for taking the time to maintain this project! I noticed an issue and would like to submit a PR to fix it."

# ❌ Unfriendly communication
"This project has bugs, why haven't you fixed it yet?"
```

**Wait Patiently for Reply**

Maintainers may need several days or even weeks to reply to your Issue or PR. Don't frequently urge, wait patiently.

### 6.2 Issue Etiquette

Before creating Issue:

1. Search existing Issues, avoid duplicates
2. Use Issue template (if project provides)
3. Provide enough context information
4. Include reproducible steps (for Bug reports)

```markdown
## Bug Report Template

### Environment Information
- Operating System: macOS 14.0
- Node.js Version: 18.17.0
- Project Version: 2.1.0

### Problem Description
Briefly describe the problem you encountered.

### Steps to Reproduce
1. Execute `npm start`
2. Click login button
3. Enter username and password
4. Observe error

### Expected Behavior
Describe the correct behavior you expect.

### Actual Behavior
Describe the actual behavior that occurred.

### Error Logs
```
Paste relevant error logs
```

### Screenshots
If applicable, provide screenshots.
```

### 6.3 Pull Request Etiquette

- Before starting large work, open Issue to discuss first
- Ensure your PR conforms to project's contribution guidelines
- Respond to reviewer's feedback, maintain open mind
- If you cannot continue work, promptly notify maintainer

### 6.4 Communication Skills

**Communicate in English**

Most international open source projects use English for communication. If your English is not fluent enough, can:

- Use simple and direct sentences
- Use translation tools for assistance
- Code and commit messages use English

**Provide Context**

```markdown
# ✅ Provide sufficient context
"When running `npm test` on macOS 14.0 with Node.js 18.17.0,
the test case at line 42 failed. Error message as follows:..."

# ❌ Lack context
"Test failed, help me look at it."
```

---

## 7. How to Find Suitable Open Source Projects to Contribute

### 7.1 Use GitHub Label Search

GitHub provides some special labels to help beginners find suitable contribution opportunities:

```
Labels suitable for beginners:
├── good first issue        → Issues suitable for first contribution
├── help wanted             → Issues where project needs help
├── easy                    → Simple Issues
├── beginner-friendly       → Issues friendly to beginners
└── documentation           → Documentation related Issues
```

**Search Methods:**

```
# GitHub search URL
https://github.com/search?q=label%3A%22good+first+issue%22+language%3AJavaScript&type=issues

# Or enter in GitHub search box
label:"good first issue" language:Python state:open
```

### 7.2 Explore Platforms and Websites

| Platform | URL | Description |
|----------|-----|-------------|
| GitHub Explore | github.com/explore | Discover popular projects and trends |
| GitHub Trending | github.com/trending | View trending projects |
| First Timers Only | firsttimersonly.com | Specifically prepared for first-time contributors |
| Up For Grabs | up-for-grabs.net | Lists projects needing help |
| Good First Issue | goodfirstissue.dev | Aggregates good first issues on GitHub |
| CodeTriage | codetriage.com | Subscribe to open source project Issues |

### 7.3 Criteria for Choosing Projects

```
Factors to consider when choosing projects:
├── Projects you use daily (Most motivated)
├── Programming languages you are familiar with
├── Active maintenance (Recent updates)
├── Friendly community atmosphere
├── Clear contribution guidelines
├── Has good first issue label
└── Complete documentation
```

### 7.4 Start from Projects You Use

The best contribution starting point is tools and libraries you use daily:

```bash
# View installed npm packages
npm list -g --depth=0

# View used Python packages
pip list

# View projects you Starred
# Visit https://github.com/stars
```

### 7.5 Recommended Open Source Projects for Chinese Developers

The following are some open source projects friendly to Chinese developers:

```
├── Vue.js          → Created by Chinese developer, has Chinese documentation
├── Ant Design      → Ant Financial's UI library
├── Element UI      → Ele.me's UI library
├── WeChat Mini Program → WeChat mini program related tools
├── Node.js         → Large project, mature contribution process
├── VS Code         → Microsoft's editor, complete documentation
└── freeCodeCamp    → Learning platform, friendly to beginners
```

---

## 8. Tips for Reading and Understanding Others' Code

### 8.1 Code Reading Strategies

**Top-down Approach**

```
1. Read README → Understand what the project is
2. View directory structure → Understand code organization
3. View package.json / setup.py → Understand dependencies and scripts
4. View entry file → Understand how program starts
5. Trace core flow → Understand how main features are implemented
```

**Bottom-up Approach**

```
1. Start from the code you want to modify
2. Understand the function/class's purpose
3. View which other functions it calls
4. Understand these functions' purposes
5. Gradually build understanding of the entire module
```

### 8.2 Use Tools to Assist Understanding

```bash
# Use grep to search key functions
grep -r "functionName" --include="*.js"

# Use git log to view file's modification history
git log --follow -p path/to/file

# Use git blame to view each line's author
git blame path/to/file

# Use GitHub's search function
# Press 't' key on repository page to open file search
```

### 8.3 Understand Project Structure

Typical project structure:

```
project/
├── src/                # Source code directory
│   ├── index.js        # Entry file
│   ├── components/     # Components (frontend projects)
│   ├── services/       # Service layer
│   ├── utils/          # Utility functions
│   └── types/          # Type definitions
├── tests/              # Test files
├── docs/               # Documentation
├── .github/            # GitHub configuration
│   ├── workflows/      # GitHub Actions
│   ├── ISSUE_TEMPLATE/ # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── README.md           # Project description
├── CONTRIBUTING.md     # Contribution guide
├── LICENSE             # License
├── package.json        # Project configuration (Node.js)
└── .eslintrc.js        # Code style configuration
```

### 8.4 Debugging and Experimentation

```bash
# Clone project to local
git clone git@github.com:owner/repo.git
cd repo

# Install dependencies
npm install

# Run tests, ensure environment is normal
npm test

# Add console.log to understand code flow
# Or use debugger to step through

# View project's example code
ls examples/
```

### 8.5 Document Your Understanding

When reading code, recommend taking notes:

```markdown
## Code Reading Notes

### Core Modules
- `src/auth/` → Authentication module
  - `login.js` → Handle login logic
  - `token.js` → JWT token management

### Data Flow
User Request → Middleware Verification → Route Handling → Database Operation → Response

### Key Functions
- `authenticateUser()` → Verify user credentials
- `generateToken()` → Generate JWT token
- `validateToken()` → Verify token validity
```

---

## 9. Common Contribution Types

### 9.1 Code Contributions

Code contributions are the most common contribution type, including:

```
Code contribution types:
├── Fix Bugs
│   ├── Fix known Issues
│   ├── Fix problems you discover
│   └── Fix security vulnerabilities
│
├── Add New Features
│   ├── Implement features discussed by community
│   ├── Add new API endpoints
│   └── Add new configuration options
│
├── Performance Optimization
│   ├── Optimize algorithm complexity
│   ├── Reduce memory usage
│   └── Optimize database queries
│
└── Code Refactoring
    ├── Improve code structure
    ├── Improve code readability
    └── Eliminate technical debt
```

### 9.2 Documentation Contributions

Documentation contributions are equally important to projects:

```markdown
Documentation contribution types:
├── Fix spelling errors
├── Improve documentation structure
├── Add usage examples
├── Update outdated documentation
├── Add API documentation
├── Write tutorials and guides
└── Translate documentation
```

### 9.3 Translation Contributions

Translation is an important contribution for internationalizing projects:

```markdown
Steps for translation contributions:
1. Check if project needs translation contributions
2. View existing translation files
3. Choose a language to translate
4. Maintain translation accuracy and naturalness
5. Follow project's translation standards
```

### 9.4 Testing Contributions

Testing is key to ensuring code quality:

```bash
# Testing contribution types:
├── Add unit tests
│   └── Add tests for uncovered functions
├── Add integration tests
│   └── Test interactions between modules
├── Add end-to-end tests
│   └── Test complete user flows
├── Fix failing tests
│   └── Make CI green
└── Improve test coverage
    └── Find uncovered code paths
```

### 9.5 Issue Reports

High-quality Issue reports are also valuable contributions:

```markdown
# Excellent Bug Report Example

## Bug Description
When using `login()` function, when password contains special characters `@` and `#`,
returns 401 error, but password is correct.

## Steps to Reproduce
1. Call `login("user", "pass@word#123")`
2. Observe return result

## Expected Behavior
Should return successful token.

## Actual Behavior
Returns 401 Unauthorized error.

## Environment Information
- Project Version: 2.1.0
- Node.js Version: 18.17.0
- Operating System: macOS 14.0

## Additional Information
Possibly related to URL encoding, special characters not properly escaped.
```

### 9.6 Other Contribution Types

```
Other contributions:
├── Design Contributions
│   ├── UI/UX Design
│   ├── Logo Design
│   └── Icon Design
│
├── Community Contributions
│   ├── Answer questions in Issues
│   ├── Review Pull Requests
│   ├── Help newcomers
│   └── Organize community events
│
└── Infrastructure Contributions
    ├── CI/CD Configuration
    ├── Automation Scripts
    └── Project Management
```

---

## 10. Code Standards and Testing Requirements of Open Source Projects

### 10.1 Code Style Standards

Most open source projects have strict code style standards:

```javascript
// ESLint configuration example (.eslintrc.js)
module.exports = {
  extends: ['eslint:recommended'],
  rules: {
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'no-unused-vars': 'error',
    'no-console': 'warn'
  }
};
```

```python
# Python code style (PEP 8)
# Use 4 spaces for indentation
# Line length not exceeding 79 characters
# Function names use snake_case
# Class names use CamelCase

def calculate_total(items):
    """Calculate order total."""
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
```

### 10.2 Commit Message Standards

**Conventional Commits Specification**

```
<type>(<scope>): <subject>

<body>

<footer>
```

```bash
# Example
git commit -m "fix(auth): Fix JWT token expiration issue

When token expires, system doesn't properly handle refresh logic,
causing users to need to re-login.

Fix method: Auto-refresh token 5 minutes before expiration.

Fixes #123
Co-authored-by: John <john@example.com>"
```

### 10.3 Testing Requirements

```bash
# Run tests
npm test

# Run tests and generate coverage report
npm test -- --coverage

# Run specific test file
npm test -- tests/auth.test.js

# Run lint check
npm run lint

# Run type check (TypeScript projects)
npm run typecheck
```

### 10.4 CI/CD Checks

Most projects use GitHub Actions for automated checks:

```yaml
# .github/workflows/ci.yml example
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### 10.5 Pre-submission Checklist

```bash
# Pre-submission check script (pre-commit hook)
#!/bin/bash

echo "Running code style check..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Code style check failed"
  exit 1
fi

echo "Running tests..."
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ All checks passed"
```

---

## 11. Handling PR Rejection or Modification Requests

### 11.1 Understanding Reasons for Rejection

PR may be rejected for multiple reasons:

```
Common rejection reasons:
├── Doesn't conform to project direction
│   └── Maintainer has specific vision
│
├── Code quality issues
│   ├── Doesn't conform to code standards
│   ├── Missing tests
│   └── Has bugs
│
├── Duplicate work
│   └── Someone already working on similar feature
│
├── Maintenance burden
│   └── Maintainer doesn't want to increase maintenance cost
│
└── Communication issues
    └── Started work without prior discussion
```

### 11.2 How to Respond to Review Feedback

**Maintain Professional and Open Attitude**

```markdown
# ✅ Positive response
"Thank you for your feedback! I will modify according to suggestions. Regarding the second point,
I have a question: how would you like to handle boundary cases?"

# ❌ Negative response
"I think my code is fine, why should I change it?"
```

**Steps to Respond to Review**

```bash
# 1. Carefully read all feedback
# 2. Understand each feedback's reason
# 3. For unclear parts, politely ask questions
# 4. Modify code according to feedback
# 5. Push modified code
# 6. Reply to reviewer, explaining what modifications you made

# Push after code modification
git add .
git commit -m "fix: Modify code based on review feedback

- Fixed function naming issue
- Added boundary condition tests
- Improved error handling"

git push origin feature/your-feature-name
```

### 11.3 Handling Conflicts

If your PR has conflicts with main branch:

```bash
# 1. Get latest upstream code
git fetch upstream

# 2. Rebase your branch onto latest main
git rebase upstream/main

# 3. Resolve conflicts
# Edit conflicted files, remove conflict markers
git add conflicted-files

# 4. Continue rebase
git rebase --continue

# 5. Force push updated branch
git push origin feature/your-feature-name --force-with-lease
```

### 11.4 When PR is Closed

If your PR is closed:

1. **Don't be discouraged** — This is a normal part of open source contribution
2. **Understand the reason** — Carefully read maintainer's explanation
3. **Learn from experience** — Learn from this experience
4. **Continue contributing** — Look for other contribution opportunities

```markdown
# If you disagree with reason for closing, can politely discuss:

"Thank you for your reply. I understand your concerns, but I believe this feature
would be helpful to many users. Could it be considered as an optional feature?
I'm happy to adjust according to your suggestions."
```

---

## 12. Path to Becoming Project Maintainer/Core Member

### 12.1 Contributor Growth Path

```
Beginner Contributor
    │
    ▼
Regular Contributor
    │
    ▼
Recognized Contributor
    │
    ▼
Code Reviewer
    │
    ▼
Core Maintainer
    │
    ▼
Project Lead
```

### 12.2 Steps from Contributor to Maintainer

**Phase 1: Build Trust**

```markdown
- Continuously contribute high-quality code
- Actively participate in community discussions
- Help answer other users' questions
- Follow project standards and processes
```

**Phase 2: Take on More Responsibility**

```markdown
- Review other contributors' PRs
- Participate in Issue classification and discussion
- Help maintain documentation
- Participate in version release process
```

**Phase 3: Gain Recognition**

```markdown
- Maintainer notices your contributions
- Invited to join core team
- Gain repository write permissions
- Participate in project decisions
```

### 12.3 Maintainer Responsibilities

After becoming maintainer, you will shoulder the following responsibilities:

```markdown
Maintainer's daily work:
├── Review and merge Pull Requests
├── Answer questions in Issues
├── Release new versions
├── Maintain CI/CD processes
├── Update documentation
├── Participate in community management
└── Define project development direction
```

### 12.4 How to Showcase Your Contributions

```bash
# View your contribution statistics
# Visit https://github.com/your-username

# Your contribution calendar will show daily activity
# Your profile will show projects you participated in

# Showcase your open source contributions in resume
# - Project name and link
# - Your contribution content
# - Impact of contribution
```

---

## 13. Using GitHub Star, Watch, Sponsor

### 13.1 GitHub Star

Star is the simplest way to express love and support for a project:

```
Star's role:
├── Save project, convenient to find later
├── Express recognition of project
├── Help project increase visibility
└── Affect GitHub's recommendation algorithm
```

```bash
# How to use Star
# 1. Visit project page
# 2. Click ⭐ Star button in top right corner
# 3. You can view all Starred projects at https://github.com/stars

# Star classification
# Create lists to organize your Starred projects
# Example: Learning resources, commonly used tools, open source contributions
```

### 13.2 GitHub Watch

Watch allows you to stay informed about project dynamics in a timely manner:

```
Watch options:
├── Participating and @mentions
│   └── Only receive notifications when mentioned or participating in discussions
│
├── Activity
│   └── Receive all activity notifications (Issues, PRs, comments, etc.)
│
├── Ignore
│   └── Don't receive any notifications
│
└── Custom
    └── Customize notification types
```

### 13.3 GitHub Sponsor

Sponsor is an economic way to support open source maintainers:

```markdown
# How to become Sponsor

1. Visit project's Sponsor page
   - Example: https://github.com/sponsors/username

2. Select sponsorship amount
   - Usually multiple tiers available
   - Can choose monthly sponsorship or one-time sponsorship

3. Select payment method
   - Credit card
   - PayPal
   - Other supported methods

# Why should consider sponsoring

- Support continuous development of open source projects
- Help maintainers obtain economic return
- Get priority support (some projects)
- Become part of project community
```

### 13.4 How to Set Up Your Own Sponsor

```markdown
# Conditions for enabling GitHub Sponsor

1. Have an active open source project
2. Have certain contribution history
3. Apply and pass GitHub's review

# Setup steps

1. Visit https://github.com/sponsors
2. Click "Get sponsored"
3. Fill in your profile and sponsorship tiers
4. Connect Stripe or other payment methods
5. Wait for review approval
```

---

## 14. Notes for Chinese Developers Participating in International Open Source Projects

### 14.1 Overcoming Language Barriers

**English Communication Skills**

```markdown
# Common Issue and PR communication phrases

## Creating Issue
"I'd like to report a bug / suggest a feature..."
"Is there a way to...?"
"Would it be possible to...?"

## Responding to Review
"Thank you for the feedback!"
"Good point, I'll update the code."
"Could you clarify what you mean by...?"

## Expressing Gratitude
"Thank you for your time and effort!"
"Great work on this project!"
"I appreciate your help!"
```

**Using Translation Tools for Assistance**

```bash
# Recommended translation tools
├── DeepL        → High translation quality
├── Google Translate → Covers many languages
├── ChatGPT      → Can polish English
└── Grammarly    → Check English grammar
```

### 14.2 Handling Time Zone Differences

```
Impact of time zone differences:
├── Maintainers may be active when you're sleeping
├── Meetings may be held at inconvenient times
├── Responses may need to wait 12-24 hours
└── Need to reasonably arrange your contribution time

Coping strategies:
├── Don't expect immediate reply
├── State your time zone in Issues
├── Use asynchronous communication methods
└── Reasonably arrange your contribution time
```

### 14.3 Network Access Challenges

```bash
# Solutions for slow GitHub repository cloning

# Method 1: Use mirrors
# Some domestic platforms provide GitHub mirrors
# Example: gitee.com can import GitHub repositories

# Method 2: Use proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# Method 3: Use GitHub Actions
# Use GitHub Actions for building and testing in CI/CD
```

### 14.4 Understanding Cultural Differences

```markdown
# Differences in communication styles between Chinese and Western

## Western Style (Common in open source communities)
- Directly express opinions
- Focus on matter, not personal
- Encourage proposing different viewpoints
- Value logic and evidence

## Adaptation Suggestions
- Don't treat code review criticism as personal attack
- Directly state your problems and needs
- Support your viewpoints with facts and data
- Respect project's existing standards and processes
```

### 14.5 Participating in Chinese Open Source Communities

```markdown
# Open source communities suitable for Chinese developers

## Domestic Open Source Platforms
├── Gitee (码云)     → Domestic GitHub
├── Coding           → Tencent's development platform
├── Alibaba Cloud Open Source → Alibaba's open source projects
└── Huawei Open Source → Huawei's open source projects

## Chinese Open Source Communities
├── Open Source China (oschina.net)
├── CSDN Open Source
├── Juejin
└── V2EX

## Recommended Chinese Open Source Projects to Participate
├── Vue.js           → Frontend framework
├── Ant Design       → UI component library
├── Element UI       → UI component library
├── Taro             → Cross-platform framework
├── Nacos            → Service discovery
└── Dubbo            → RPC framework
```

---

## 15. Practical Case: Contributing Code to a Famous Project

### 15.1 Case Background

Let's take contributing code to **freeCodeCamp** project as an example, this is an open source project very suitable for beginners.

freeCodeCamp is a free programming learning platform, its code repository is hosted on GitHub, very friendly to beginner contributors.

### 15.2 Preparation

```bash
# Step 1: Fork project
# Visit https://github.com/freeCodeCamp/freeCodeCamp
# Click Fork button

# Step 2: Clone your Fork
git clone git@github.com:your-username/freeCodeCamp.git
cd freeCodeCamp

# Step 3: Add upstream repository
git remote add upstream git@github.com:freeCodeCamp/freeCodeCamp.git

# Step 4: Install dependencies
npm install

# Step 5: Read contribution guide
# Carefully read CONTRIBUTING.md file
# Understand project's development process and standards
```

### 15.3 Finding Contribution Opportunities

```bash
# Visit Issues page
# https://github.com/freeCodeCamp/freeCodeCamp/issues

# Filter using labels
label:"first timers only"    # Only for first-time contributors
label:"good first issue"     # Suitable for beginners
label:"help wanted"          # Needs help

# Select an Issue
# Example: Fix a spelling error
```

### 15.4 Implementing Changes

```bash
# Step 1: Sync upstream code
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Step 2: Create feature branch
git checkout -b fix/typo-in-challenge-description

# Step 3: Find file to modify
# According to Issue description, find corresponding file
# Example: curriculum/challenges/english/01-responsive-web-design/basic-css/change-the-color-of-text.md

# Step 4: Modify file
# Fix spelling error or add content

# Step 5: Commit changes
git add .
git commit -m "fix(curriculum): correct typo in CSS challenge description

Fixed a spelling error in the 'Change the Color of Text' challenge.
Changed 'colour' to 'color' to match American English convention.

Closes #12345"

# Step 6: Push and create PR
git push origin fix/typo-in-challenge-description
```

### 15.5 Creating Pull Request

```markdown
## PR Description Template

### Description
Corrected spelling error in CSS challenge description.

### Changes
- Changed 'colour' to 'color', conforming to American English standards

### Related Issues
Closes #12345

### Checklist
- [x] I have read CONTRIBUTING.md
- [x] My code conforms to project's code standards
- [x] I have tested my changes locally
- [x] My commit message conforms to standards
```

### 15.6 Handling Review Feedback

```markdown
# Reviewer may ask you to:
1. Modify code style
2. Add tests
3. Update documentation
4. Explain your changes

# Response example:
"Thank you for your feedback! I have modified the code according to suggestions.
Now 'color' spelling is unified to American English."
```

### 15.7 PR is Merged

```bash
# After your PR is merged:
# 1. Delete your feature branch
git checkout main
git branch -d fix/typo-in-challenge-description
git push origin --delete fix/typo-in-challenge-description

# 2. Sync upstream code
git fetch upstream
git merge upstream/main
git push origin main

# 3. Celebrate your first contribution!
```

### 15.8 Continue Contributing

```markdown
# After first successful contribution, you can:

1. Look for more good first issues
2. Try to fix more complex problems
3. Participate in code review
4. Help answer other newcomers' questions
5. Gradually become an active contributor to the project
```

---

## Summary

### Core Points of Open Source Contribution

```
Successful open source contributors need:

1. Understand Fork mechanism
   └── Master every step of Fork workflow

2. Maintain patience and persistence
   └── First contribution may take long time

3. Respect community standards
   └── Follow project's contribution guidelines and etiquette

4. Continuously learn and improve
   └── Learn experience from each contribution

5. Actively participate in community
   └── Not just submit code, also participate in discussions
```

### Quick Reference Commands

```bash
# Fork workflow quick reference

# 1. Clone your Fork
git clone git@github.com:your-username/repo-name.git

# 2. Add upstream repository
git remote add upstream git@github.com:original-owner/repo-name.git

# 3. Sync upstream code
git fetch upstream
git checkout main
git merge upstream/main

# 4. Create feature branch
git checkout -b feature/your-feature

# 5. Modify and commit
git add .
git commit -m "feat: Your change description"

# 6. Push and create PR
git push origin feature/your-feature
```

### Recommended Resources

```markdown
# Learning Resources

## Official Documentation
- GitHub Documentation: docs.github.com
- Git Documentation: git-scm.com/doc

## Books
- "GitHub入门与实践"
- "Pro Git" Chinese version

## Online Courses
- freeCodeCamp
- GitHub Skills

## Communities
- GitHub Community Forum
- Stack Overflow
```

---

## Next Step

Now that you have mastered complete knowledge of Fork and open source contribution, it's time to start your first contribution!

Choose an open source project you're interested in, find a `good first issue`, and start your open source journey!

# Chapter 6: Team Collaboration and Open Source Contribution

## 6.1 Team Collaboration Basics

### Team Collaboration Workflow

```
1. Clone repository
   ↓
2. Create feature branch
   ↓
3. Develop and test
   ↓
4. Push branch
   ↓
5. Create Pull Request
   ↓
6. Code review
   ↓
7. Merge to main branch
   ↓
8. Deploy
```

### Branching Strategy

**Git Flow:**
```
main (production branch)
├── develop (development branch)
│   ├── feature/xxx (feature branch)
│   └── release/xxx (release branch)
└── hotfix/xxx (hotfix)
```

**GitHub Flow:**
```
main (main branch)
└── feature/xxx (feature branch)
```

**Trunk-Based Development:**
```
main (main branch, frequent commits)
```

### Commit Message Convention

**Format:**
```
type(scope): description

Detailed description (optional)

Related Issue (optional)
```

**Type Descriptions:**

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add user login feature` |
| `fix` | Bug fix | `fix: fix login page style issue` |
| `docs` | Documentation update | `docs: update README installation instructions` |
| `style` | Code formatting | `style: format code` |
| `refactor` | Refactoring | `refactor: refactor user service` |
| `test` | Tests | `test: add unit tests` |
| `chore` | Build/tools | `chore: update dependencies` |
| `perf` | Performance optimization | `perf: optimize query performance` |

**Examples:**
```bash
git commit -m "feat: add user login feature"
git commit -m "fix: fix login page style issue"
git commit -m "docs: update README installation instructions"
```

## 6.2 Code Review

### Review Process

**Step 1:** Open the PR's **Files changed** page

**Step 2:** Review code changes

**Step 3:** Add inline comments

**Step 4:** Submit review

### Review Checklist

| Category | Items to Check |
|----------|----------------|
| **Functionality** | Is the logic correct, edge cases |
| **Design** | Is the architecture sound |
| **Readability** | Naming, comments, structure |
| **Performance** | Any performance issues |
| **Security** | Any security vulnerabilities |
| **Testing** | Is testing sufficient |
| **Documentation** | Does documentation need updating |

### Providing Good Feedback

**Good feedback:**
- Point out the specific location of the problem
- Explain why it is a problem
- Provide improvement suggestions
- Use code suggestions

**Example:**
```
The class name "new" here is not descriptive enough, suggest changing it to "primary"
to indicate this is a primary button.

```suggestion
className="primary"
```
```

### Review Outcomes

| Option | Description | When to Use |
|--------|-------------|-------------|
| **Comment** | Comment only | Don't oppose merging, just providing suggestions |
| **Approve** | Approved | Code quality is good, can be merged |
| **Request changes** | Request changes | Issues need to be fixed |

## 6.3 Fork and Open Source Contribution

### What is a Fork?

A Fork is copying someone else's repository to your GitHub account so you can freely modify it without affecting the original repository.

### Fork Workflow

```
1. Fork repository (web UI)
   ↓
2. Clone the Forked repository (command line)
   ↓
3. Add upstream repository (command line)
   ↓
4. Create feature branch (command line)
   ↓
5. Develop and commit (command line)
   ↓
6. Push to your Fork (command line)
   ↓
7. Create Pull Request (web UI)
```

### Fork a Repository

**Step 1:** Open the source repository page

**Step 2:** Click the **Fork** button in the top right corner

```
┌─────────────────────────────────────────────┐
│  owner/repo                                  │
│                                             │
│  [Fork]  ← click this button                │
│  ⭐ 1.2k  👁 345                             │
└─────────────────────────────────────────────┘
```

**Step 3:** Select the Fork destination (usually your account)

**Step 4:** Wait for the Fork to complete

### Clone the Forked Repository

```bash
# Clone your Forked repository
git clone https://github.com/your-username/repo.git

# Enter repository directory
cd repo
```

### Add Upstream Repository

```bash
# Add the original repository as upstream
git remote add upstream https://github.com/owner/repo.git

# View remote repositories
git remote -v
```

**Output Example:**
```
origin    https://github.com/your-username/repo.git (fetch)
origin    https://github.com/your-username/repo.git (push)
upstream  https://github.com/owner/repo.git (fetch)
upstream  https://github.com/owner/repo.git (push)
```

### Syncing Fork

```bash
# Fetch upstream updates
git fetch upstream

# Merge upstream main branch
git checkout main
git merge upstream/main

# Push to your Fork
git push origin main
```

### Create Feature Branch

```bash
# Create feature branch
git checkout -b feature-your-feature
```

### Develop and Commit

```bash
# Modify files...
git add .
git commit -m "feat: add new feature"
```

### Push to Fork

```bash
git push origin feature-your-feature
```

### Create Pull Request

**Step 1:** Open your Fork page

**Step 2:** Click **Compare & pull request**

**Step 3:** Confirm PR information

```
┌─────────────────────────────────────────────┐
│  Open a pull request                         │
│                                             │
│  base: owner:main  ← compare: your:feature  │
│                                             │
│  Title: [feat: add new feature            ]  │
│                                             │
│  Description:                                │
│  ┌─────────────────────────────────────┐    │
│  │ ## Change Description              │    │
│  │ Added a new feature                │    │
│  │                                     │    │
│  │ ## Testing                         │    │
│  │ - [x] All tests passed            │    │
│  └─────────────────────────────────────┘    │
│                                             │
│        [Create pull request]                │
└─────────────────────────────────────────────┘
```

**Step 4:** Click **Create pull request**

### Keeping Fork in Sync

```bash
# Fetch upstream updates
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream updates
git merge upstream/main

# Push to your Fork
git push origin main
```

## 6.4 Open Source Project Management

### Creating an Open Source Project

**Preparation:**
- [ ] Write README
- [ ] Add LICENSE
- [ ] Create CONTRIBUTING.md
- [ ] Create CODE_OF_CONDUCT.md
- [ ] Set up Issue templates
- [ ] Set up PR templates
- [ ] Configure CI/CD

### README Template

```markdown
# Project Name

> Short description

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Installation

```bash
npm install your-package
```

### Usage

```javascript
import { yourFunction } from 'your-package';

yourFunction();
```

## Documentation

- [Documentation link](docs/)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
```

### CONTRIBUTING.md Template

```markdown
# Contributing Guide

Thank you for your interest in the project!

## How to Contribute

### Reporting Bugs

1. Search existing Issues
2. Create a new Issue
3. Use the Bug Report template

### Submitting Code

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your Fork
5. Create a Pull Request

### Code Standards

- Follow the existing code style
- Add necessary comments
- Ensure tests pass

### Commit Message Convention

Follow the Conventional Commits specification:

```
type(scope): description

Detailed description (optional)
```
```

### Community Building

**Channels:**
- GitHub Issues: Issue tracking
- GitHub Discussions: Community discussions
- Discord/Slack: Instant messaging
- Twitter: Project updates

**Activities:**
- Regular release updates
- Respond to Issues and PRs
- Organize online events
- Write blog posts

### Project Promotion

**Methods:**
- Share on social media
- Write blog introductions
- Participate in open source events
- Collaborate with other projects
- Submit to awesome lists

## 6.5 Open Source Licenses

### Common Licenses

| License | Description | Restrictions |
|---------|-------------|--------------|
| **MIT** | Most permissive, allows any use | Must retain copyright notice |
| **Apache 2.0** | Permissive, requires noting modifications | Must retain copyright notice |
| **GPL** | Requires derivative works to be open source | Derivative works must be open source |
| **LGPL** | Allows libraries to be used in closed source | Library itself must be open source |
| **BSD** | Similar to MIT, with additional restrictions | Must retain copyright notice |

### Choosing a License

**Recommendations:**
- Personal projects: MIT
- Enterprise projects: Apache 2.0
- Want derivative works to be open source: GPL

### Adding a License

**Method 1: Add via Web UI**

1. Go to repository page
2. Click **Add file** → **Create new file**
3. Enter filename `LICENSE`
4. Select template
5. Click **Commit changes**

**Method 2: Add via Command Line**

```bash
# Using GitHub CLI
gh api repos/{owner}/{repo}/license \
  --method PUT \
  -f license='mit'
```

## 6.6 Best Practices

### Team Collaboration Best Practices

1. **Use clear branch naming**
   - `feature/user-login`
   - `bugfix/fix-crash`
   - `hotfix/security-patch`

2. **Write good commit messages**
   - Follow the Conventional Commits specification
   - Be clear and describe what was done

3. **Keep PRs small and focused**
   - One PR should do one thing
   - Easier to review and understand

4. **Respond to reviews promptly**
   - Don't leave PRs sitting for too long
   - Consider each piece of feedback carefully

### Open Source Contribution Best Practices

1. **Start with simple tasks**
   - Look for `good first issue` labels
   - Fix documentation errors

2. **Read the contributing guide**
   - Understand project conventions
   - Follow code style

3. **Maintain communication**
   - Discuss ideas in Issues
   - Respond to feedback promptly

4. **Be patient**
   - Reviews take time
   - Don't be discouraged by rejections

## 6.7 Chapter Summary

This chapter provided a detailed introduction to team collaboration and open source contribution, including:

- Team collaboration workflow
- Code review methods
- Fork and open source contribution
- Open source project management
- Open source licenses

**Key Takeaways:**
- Good collaboration habits are the foundation of team success
- Participating in open source can improve technical skills
- Respect others and maintain friendliness

**Next:**
[Security and DevOps →](28-security-permissions.md)

# Complete Guide to Issue and PR Templates

## 1. Purpose and Value of Issue Templates

### 1.1 Why Issue Templates Are Needed

In open-source projects or team collaboration, Issues are one of the most commonly used communication tools. However, Issues without template constraints often have the following problems:

- **Incomplete information:** Reporters forget to provide key information such as OS version, reproduction steps, etc., causing maintainers to repeatedly ask follow-up questions
- **Inconsistent formatting:** Everyone submits Issues in a different style, making it difficult to quickly locate key information
- **Ambiguous classification:** It's unclear whether to report a Bug or request a new feature, leading to Issues being misclassified
- **Low efficiency:** Maintainers need to spend a lot of time organizing and supplementing information instead of focusing on solving problems

Issue templates fundamentally solve these problems through predefined structures and required fields. A good Issue template should be like a well-designed form that guides reporters to provide complete, accurate, and useful information.

### 1.2 Core Value of Issue Templates

| Value Dimension | Specific Manifestation |
|----------|----------|
| **Standardization** | Unify the format of all Issues for batch processing and filtering |
| **Efficiency Improvement** | Reduce back-and-forth communication between maintainers and reporters, speeding up problem resolution |
| **Information Completeness** | Ensure key information is not missed through required fields |
| **Automation** | Work with GitHub Actions for automatic label assignment, auto-assignment, etc. |
| **Newcomer-Friendly** | Provide clear submission guidelines for first-time contributors |

### 1.3 Types of Issue Templates

GitHub supports two formats of Issue templates:

- **Markdown templates (.md):** Traditional Markdown format where users can freely edit the auto-filled template content upon submission
- **YAML form templates (.yml):** Next-generation form-style templates that provide dropdown menus, checkboxes, input boxes, and other form elements for a better user experience and more standardized information collection

**YAML form templates are recommended** because they provide a better structured data collection experience.

---

## 2. Creating Issue Templates (YAML Format)

### 2.1 Directory Structure

Issue templates are stored in the `.github/ISSUE_TEMPLATE/` folder at the repository root:

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.yml          # Bug report template
    ├── feature_request.yml     # Feature request template
    ├── documentation.yml       # Documentation improvement suggestion template
    ├── security_issue.yml      # Security issue report template
    ├── config.yml              # Template selector configuration
    └── PULL_REQUEST_TEMPLATE.md # PR template (can also be placed here)
```

### 2.2 YAML Form Template Fields Explained

YAML form templates support the following field types:

| Field Type | Description | Use Case |
|----------|------|----------|
| `markdown` | Plain text description, not used as input | Adding hints, dividers |
| `input` | Single-line text input box | Collecting brief information such as version numbers, URLs |
| `textarea` | Multi-line text input box | Collecting detailed descriptions, reproduction steps |
| `dropdown` | Dropdown menu | Selecting a single option, such as OS, priority |
| `checkboxes` | Checkbox group | Selecting multiple options, such as confirmation items |
| `number` | Number input box | Collecting numerical information |

### 2.3 Complete Bug Report Template

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug to help us improve the project
title: "[Bug]: "
labels: ["bug", "needs-triage"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Thank you for reporting a bug!
        Please fill out the following information as detailed as possible, which will help us locate and fix the issue faster.
        
        **Before submitting, please:**
        - Search existing Issues to confirm the problem hasn't been reported yet
        - Make sure you are using the latest version
        - Check the [troubleshooting documentation](https://docs.example.com/troubleshooting)

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Describe the bug clearly and concisely
      placeholder: "e.g.: After clicking the login button, the page is unresponsive, and the console shows 'TypeError: Cannot read property...'"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Provide detailed reproduction steps
      placeholder: |
        1. Open the application homepage
        2. Click the 'Login' button in the upper right corner
        3. Enter username and password
        4. Click the 'Submit' button
        5. Observe the error
      value: |
        1. 
        2. 
        3. 
        4. 
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: Clearly describe what you expected to happen
      placeholder: "e.g.: After clicking the submit button, it should navigate to the homepage and display the user avatar"
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: Clearly describe what actually happened
      placeholder: "e.g.: The page didn't navigate, and the console shows a TypeError"
    validations:
      required: true

  - type: dropdown
    id: version
    attributes:
      label: Version
      description: The software version you are using
      options:
        - Latest version (main branch)
        - v2.0.0
        - v1.9.0
        - v1.8.0
        - Other (please specify below)
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      multiple: true
      options:
        - Windows 11
        - Windows 10
        - macOS 14 (Sonoma)
        - macOS 13 (Ventura)
        - Ubuntu 22.04
        - Ubuntu 20.04
        - Other Linux distributions
    validations:
      required: true

  - type: dropdown
    id: browser
    attributes:
      label: Browser
      multiple: true
      options:
        - Chrome 120+
        - Firefox 120+
        - Safari 17+
        - Edge 120+
        - N/A
    validations:
      required: false

  - type: input
    id: node-version
    attributes:
      label: Node.js Version
      description: Run `node --version` to get this
      placeholder: "v20.10.0"
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: Logs/Error Messages
      description: Paste relevant log output or error stack traces
      render: shell
    validations:
      required: false

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots to help explain the issue (you can drag and drop images here)
    validations:
      required: false

  - type: textarea
    id: environment
    attributes:
      label: Runtime Environment Details
      description: Provide any other relevant environment information
      placeholder: |
        - Database version: PostgreSQL 15
        - Memory: 16GB
        - Network environment: Corporate intranet
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Confirmation Items
      options:
        - label: I have searched existing Issues and confirmed this problem hasn't been reported
          required: true
        - label: I am using the latest version
          required: false
        - label: I am willing to submit a PR to fix this issue
          required: false
```

### 2.4 Complete Feature Request Template

```yaml
# .github/ISSUE_TEMPLATE/feature_request.yml
name: Feature Request
description: Suggest a new feature or improvement
title: "[Feature]: "
labels: ["enhancement", "needs-review"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Thank you for your feature suggestion!
        Please describe your needs in detail, which will help us evaluate and plan this feature.

  - type: textarea
    id: problem
    attributes:
      label: Problem Description
      description: Clearly describe the problem or pain point you're experiencing
      placeholder: "e.g.: When I'm processing large amounts of data, the current search function is very slow, taking an average of more than 5 seconds to respond"
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: Describe how you'd like this problem to be solved
      placeholder: "e.g.: It's suggested to add index support and paginated queries, splitting large datasets into smaller batches for processing"
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: Describe other solutions you've considered
      placeholder: "e.g.: I tried using Redis caching, but it increased system complexity"
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How urgent do you think this feature is
      options:
        - High - Severely impacts workflow
        - Medium - Has some impact but can be worked around
        - Low - Nice-to-have improvement
    validations:
      required: true

  - type: dropdown
    id: scope
    attributes:
      label: Impact Scope
      description: Which users would this feature affect
      options:
        - All users
        - Power users
        - Administrators
        - Developers
        - Specific use case users
    validations:
      required: false

  - type: textarea
    id: additional
    attributes:
      label: Additional Information
      description: Any other information that helps understand the need, such as reference links, design drafts, competitor screenshots, etc.
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Confirmation Items
      options:
        - label: I have searched existing Issues and confirmed this feature hasn't been requested
          required: true
        - label: I am willing to participate in the discussion and design of this feature
          required: false
        - label: I am willing to submit a PR to implement this feature
          required: false
```

---

## 3. Issue Forms

### 3.1 Advantages of Issue Forms

Issue Forms (YAML form templates) have the following advantages over traditional Markdown templates:

| Feature | Markdown Templates | YAML Form Templates |
|------|--------------|--------------|
| User Experience | Free editing, easy to break formatting | Form-style filling, clear structure |
| Data Validation | No validation mechanism | Supports required field validation |
| Dropdown Menus | Not supported | Supports single and multiple selection |
| Checkboxes | Uses Markdown syntax | Native support |
| Post-Submission Format | Format may be inconsistent | Uniform and standardized format |
| Automation Processing | Difficult to parse | Easy to automate |

### 3.2 Form Elements Explained

**markdown element - Adding descriptive text:**

```yaml
- type: markdown
  attributes:
    value: |
      ## Title
      You can write descriptive text in **Markdown** format here.
      Supports links, images, code blocks, etc.
```

**input element - Single-line input:**

```yaml
- type: input
  id: email
  attributes:
    label: Email Address
    description: Used to notify you of issue resolution progress
    placeholder: "your@email.com"
    value: "default value"
  validations:
    required: true
    regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    regex_error: "Please enter a valid email address"
```

**textarea element - Multi-line input:**

```yaml
- type: textarea
  id: description
  attributes:
    label: Description
    description: Describe your issue in detail
    placeholder: "Please enter..."
    render: shell  # Automatically adds code block formatting
  validations:
    required: true
```

**dropdown element - Dropdown selection:**

```yaml
# Single selection
- type: dropdown
  id: priority
  attributes:
    label: Priority
    options:
      - High
      - Medium
      - Low
  validations:
    required: true

# Multiple selection
- type: dropdown
  id: platforms
  attributes:
    label: Affected Platforms
    multiple: true
    options:
      - Windows
      - macOS
      - Linux
      - iOS
      - Android
  validations:
    required: true
```

**checkboxes element - Checkboxes:**

```yaml
- type: checkboxes
  id: checklist
  attributes:
    label: Pre-Submission Checklist
    options:
      - label: I have read the contribution guidelines
        required: true
      - label: I have searched existing Issues
        required: true
      - label: I have tried the latest version
        required: false
```

**number element - Number input:**

```yaml
- type: number
  id: users
  attributes:
    label: Number of Affected Users
    description: Approximately how many users would be affected by this issue
    placeholder: "100"
  validations:
    required: false
    min: 0
    max: 1000000
```

### 3.3 Form Validation Rules

YAML form templates support the following validation rules:

```yaml
validations:
  required: true                    # Required field
  regex: "^[a-zA-Z0-9]+$"         # Regex validation
  regex_error: "Can only contain letters and numbers"  # Validation failure message
  min: 0                            # Minimum value (number fields)
  max: 100                          # Maximum value (number fields)
```

---

## 4. PR Template Creation and Configuration

### 4.1 Purpose of PR Templates

Pull Request templates provide a standardized information framework for code reviews, ensuring submitters provide enough context information to help reviewers quickly understand the changes and their purpose.

### 4.2 PR Template File Locations

PR templates can be placed in the following locations:

```
# Location 1: Root directory (most common)
.github/PULL_REQUEST_TEMPLATE.md

# Location 2: GitHub directory
PULL_REQUEST_TEMPLATE.md

# Location 3: Multiple template mode
.github/PULL_REQUEST_TEMPLATE/
├── bug_fix.md
├── feature.md
├── docs.md
└── refactor.md
```

### 4.3 Complete PR Template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->

## Change Overview

<!-- Describe what this PR does in one sentence -->

## Change Type

<!-- Please check the applicable type -->

- [ ] 🐛 Bug fix (changes that don't break existing functionality)
- [ ] ✨ New feature (new functionality that doesn't break existing features)
- [ ] 💥 Breaking changes (fixes or features that would cause existing functionality to stop working properly)
- [ ] 📝 Documentation update (documentation-only changes)
- [ ] ♻️ Code refactoring (code changes that neither fix a bug nor add a feature)
- [ ] ⚡ Performance optimization (code changes that improve performance)
- [ ] ✅ Tests (adding missing tests or correcting existing tests)
- [ ] 🔧 Build/CI (changes affecting the build system or external dependencies)
- [ ] 🔙 Rollback (reverting previous changes)

## Change Details

<!-- Describe your changes in detail, including implementation approach, design decisions, etc. -->

### Key Changes

- 

### Technical Implementation

- 

## Related Issues

<!-- Use keywords to auto-close Issues -->
<!-- Reference: https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue -->

Closes #
Fixes #
Resolves #

## Testing Instructions

<!-- Describe how you tested these changes -->

### Test Environment

- OS: 
- Node.js: 
- Browser: 

### Test Cases

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing passes

### Testing Steps

1. 
2. 
3. 

## Screenshots/Recordings

<!-- If this is a UI change, please provide screenshots or recordings -->

| Before | After |
|--------|--------|
| ![before](url) | ![after](url) |

## Self-Check List

<!-- Please complete the following checks before submitting -->

### Code Quality

- [ ] Code follows the project's coding standards
- [ ] Self code review has been performed
- [ ] Code has adequate comments, especially in hard-to-understand areas
- [ ] Relevant tests have been added (if applicable)
- [ ] Both new and existing tests pass

### Documentation Update

- [ ] Related documentation has been updated (e.g., README, API docs, etc.)
- [ ] CHANGELOG has been updated (if applicable)
- [ ] Changes don't affect the accuracy of existing documentation

### Security

- [ ] No hardcoded keys or sensitive information
- [ ] No new security vulnerabilities introduced
- [ ] Dependencies have been checked for security vulnerabilities

### Compatibility

- [ ] Changes are backward-compatible
- [ ] If there are breaking changes, they are documented in the description
- [ ] Cross-browser/device compatibility has been considered

## Additional Notes

<!-- Any additional information reviewers need to know -->
```

### 4.4 Type-Specific PR Templates

**Bug Fix Template:**

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE/bug_fix.md -->
## Bug Fix

### Problem Description

<!-- Describe the bug being fixed -->

### Root Cause

<!-- Explain the root cause of the bug -->

### Fix Approach

<!-- Describe your fix approach -->

### Before/After Comparison

```typescript
// Before fix
const result = data.filter(item => item.id == id);

// After fix
const result = data.filter(item => item.id === id);
```

### Test Coverage

- [ ] Test cases reproducing the bug have been added
- [ ] Test cases fail before the fix
- [ ] Test cases pass after the fix

Closes #
```

---

## 5. Multiple Template Configuration

### 5.1 Configuring the Template Selector

Through the `config.yml` file, you can customize the template selector on the Issue creation page:

```yaml
# .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false  # Disable blank Issue creation
contact_links:
  - name: 💬 Questions & Discussions
    url: https://github.com/your-org/your-repo/discussions
    about: If you have usage questions or want to discuss a topic, please post in Discussions
  - name: 📖 View Documentation
    url: https://docs.example.com
    about: Before submitting an Issue, please check the documentation first
  - name: 🔒 Security Vulnerability Report
    url: https://github.com/your-org/your-repo/security/advisories/new
    about: If you've found a security vulnerability, please report it through security advisories, not as a public Issue
  - name: 💰 Sponsorship
    url: https://github.com/sponsors/your-org
    about: If this project has been helpful to you, sponsorship is welcome
```

### 5.2 Multiple PR Template Configuration

```yaml
# .github/PULL_REQUEST_TEMPLATE/bug_fix.md
---
name: Bug Fix
about: Fix a known bug
labels: ["bug", "fix"]
---

## Bug Fix PR

### Issue Fixed

Closes #

### Problem Description

### Fix Approach

### Testing
```

```yaml
# .github/PULL_REQUEST_TEMPLATE/feature.md
---
name: New Feature
about: Add a new feature
labels: ["enhancement", "feature"]
---

## New Feature PR

### Feature Description

### Implementation Plan

### Test Coverage

### Documentation Update
```

### 5.3 Using URL Parameters to Select Templates

When creating an Issue or PR, you can specify the template directly via URL parameters:

```
# Using an Issue template
https://github.com/owner/repo/issues/new?template=bug_report.yml

# Using a PR template
https://github.com/owner/repo/compare/main...feature-branch?template=feature.md

# Pre-filling fields
https://github.com/owner/repo/issues/new?title=[Bug]:&labels=bug&body=## Description
```

---

## 6. Template Best Practices

### 6.1 Template Design Principles

**Simplicity Principle:**

- Only request necessary information, avoid over-engineering
- Use clear, concise language
- Provide useful default values and examples

**Guidance Principle:**

- Use the placeholder attribute to provide filling examples
- Add instructions and links through markdown elements
- Use required fields to ensure key information is not missed

**Consistency Principle:**

- All templates use unified naming conventions
- Maintain similar structure and formatting
- Use consistent labels and categories

### 6.2 Label Strategy

```yaml
# Bug report labels
labels: ["bug", "needs-triage"]

# Feature request labels
labels: ["enhancement", "needs-review"]

# Documentation issue labels
labels: ["documentation", "good first issue"]

# Priority labels
labels: ["priority: high", "priority: medium", "priority: low"]
```

### 6.3 Template Naming Convention

```
.github/ISSUE_TEMPLATE/
├── 01_bug_report.yml        # Use numeric prefix to control sorting
├── 02_feature_request.yml
├── 03_documentation.yml
├── 04_question.yml
└── config.yml
```

### 6.4 Internationalization Considerations

Provide multilingual templates for internationalized projects:

```yaml
# English version
name: Bug Report
description: Report a bug

# Chinese version
name: Bug Report (Bug 报告)
description: Report a bug (报告一个问题)
```

### 6.5 Template Maintenance

Regularly review and update templates:

1. **Collect feedback:** Ask contributors about their experience using the templates
2. **Analyze data:** Track which fields are frequently left blank or filled in incorrectly
3. **Continuous optimization:** Adjust template content and validation rules based on feedback
4. **Version control:** Template changes should go through PRs for team review

---

## 7. Automated Label Assignment

### 7.1 Template-Based Auto Labeling

YAML templates support automatic label assignment:

```yaml
# Bug reports automatically assign bug and needs-triage labels
labels: ["bug", "needs-triage"]

# Feature requests automatically assign enhancement label
labels: ["enhancement"]
```

### 7.2 Content-Based Auto Labeling

Use GitHub Actions to automatically assign labels based on Issue content:

```yaml
# .github/workflows/auto-label.yml
name: Auto Label

on:
  issues:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Assign labels based on title
        uses: actions/github-script@v7
        with:
          script: |
            const title = context.payload.issue.title.toLowerCase();
            const labels = [];
            
            if (title.includes('[bug]') || title.includes('bug')) {
              labels.push('bug');
            }
            if (title.includes('[feature]') || title.includes('feature')) {
              labels.push('enhancement');
            }
            if (title.includes('[docs]') || title.includes('documentation')) {
              labels.push('documentation');
            }
            if (title.includes('[security]') || title.includes('security')) {
              labels.push('security');
            }
            
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }

      - name: Assign labels based on content
        uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.issue.body || '';
            const labels = [];
            
            // Detect priority
            if (body.includes('critical')) {
              labels.push('priority: critical');
            } else if (body.includes('high')) {
              labels.push('priority: high');
            }
            
            // Detect operating system
            if (body.includes('Windows')) labels.push('os: windows');
            if (body.includes('macOS')) labels.push('os: macos');
            if (body.includes('Linux')) labels.push('os: linux');
            
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }
```

### 7.3 Using the Labeler Action

```yaml
# .github/workflows/labeler.yml
name: PR Labeler

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
```

```yaml
# .github/labeler.yml
# Assign labels based on modified file paths
frontend:
  - changed-files:
    - any-glob-to-any-file: 'frontend/**'

backend:
  - changed-files:
    - any-glob-to-any-file: 'backend/**'

documentation:
  - changed-files:
    - any-glob-to-any-file:
      - 'docs/**'
      - '*.md'

ci:
  - changed-files:
    - any-glob-to-any-file: '.github/**'
```

---

## 8. Issue/PR Templates Integration with GitHub Actions

### 8.1 Issue Quality Check

Create an Action to check whether Issues follow the template format:

```yaml
# .github/workflows/issue-quality.yml
name: Issue Quality Check

on:
  issues:
    types: [opened]

jobs:
  check:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Check Issue quality
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const body = issue.body || '';
            const checks = [];
            
            // Check for required sections
            const requiredSections = ['## Description', '## Steps to Reproduce'];
            for (const section of requiredSections) {
              if (!body.includes(section)) {
                checks.push(`❌ Missing ${section} section`);
              }
            }
            
            // Check for screenshots (if Bug report)
            if (issue.labels.some(l => l.name === 'bug')) {
              if (!body.includes('![') && !body.includes('Screenshot')) {
                checks.push('⚠️ Bug reports are recommended to include screenshots');
              }
            }
            
            // If there are issues, add a comment
            if (checks.length > 0) {
              const comment = [
                '## Issue Quality Check',
                '',
                'Thank you for your Issue! Here are the check results:',
                '',
                ...checks,
                '',
                'Please supplement the relevant information based on the hints above, which will help us resolve the issue faster.'
              ].join('\n');
              
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: comment
              });
            }
```

### 8.2 PR Checklist Validation

```yaml
# .github/workflows/pr-checklist.yml
name: PR Checklist

on:
  pull_request:
    types: [opened, edited]

jobs:
  checklist:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - name: Check checklist completion
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const body = pr.body || '';
            
            // Count unchecked items
            const unchecked = (body.match(/- \[ \]/g) || []).length;
            const checked = (body.match(/- \[x\]/g) || []).length;
            const total = unchecked + checked;
            
            if (total > 0) {
              const completionRate = Math.round((checked / total) * 100);
              
              // If completion rate is below 80%, add a reminder
              if (completionRate < 80) {
                await github.rest.issues.createComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: pr.number,
                  body: `## Checklist Reminder\n\nCurrent completion: ${completionRate}% (${checked}/${total})\n\nPlease ensure all necessary items are completed before requesting review.`
                });
              }
            }
```

### 8.3 Automatic Reviewer Assignment

```yaml
# .github/workflows/auto-reviewer.yml
name: Auto Assign Reviewer

on:
  pull_request:
    types: [opened]

jobs:
  assign:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - name: Assign reviewers based on changed files
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const files = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr.number
            });
            
            const reviewers = new Set();
            const filePatterns = {
              'frontend/': ['frontend-team'],
              'backend/': ['backend-team'],
              '.github/': ['devops-team'],
              'docs/': ['docs-team']
            };
            
            for (const file of files.data) {
              for (const [pattern, teams] of Object.entries(filePatterns)) {
                if (file.filename.startsWith(pattern)) {
                  teams.forEach(team => reviewers.add(team));
                }
              }
            }
            
            if (reviewers.size > 0) {
              await github.rest.pulls.requestReviewers({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: pr.number,
                reviewers: [...reviewers]
              });
            }
```

### 8.4 Auto-Close Incomplete Issues

```yaml
# .github/workflows/auto-close.yml
name: Auto Close Incomplete Issues

on:
  issues:
    types: [opened]

jobs:
  close:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Check Issue completeness
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const body = issue.body || '';
            
            // Check if it's a blank Issue (not using template)
            if (body.length < 50) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: '## Issue Closed\n\nYour Issue appears to not use a template or has incomplete information. Please resubmit using the provided template and ensure all required information is filled in.\n\n[Create New Issue](https://github.com/' + context.repo.owner + '/' + context.repo.repo + '/issues/new/choose)'
              });
              
              await github.rest.issues.update({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                state: 'closed',
                state_reason: 'not_planned'
              });
            }
```

---

## 9. Template Management Strategy

### 9.1 Template Version Management

Include templates in version control and make changes through PRs:

```markdown
# .github/ISSUE_TEMPLATE/CHANGELOG.md

## Template Change Log

### 2024-01-15
- Added security vulnerability report template
- Updated Bug report template, added browser field

### 2024-01-01
- Initial version released
- Includes Bug report, Feature request, and Documentation improvement templates
```

### 9.2 Template Review Process

1. **Proposal stage:** Create an Issue explaining the reason and content of template changes
2. **Implementation stage:** Create a PR to modify template files
3. **Review stage:** Team members review template changes
4. **Merge stage:** Merge the PR, template takes effect immediately
5. **Feedback stage:** Collect usage feedback for continuous optimization

### 9.3 Template Metrics Monitoring

Monitor template usage through the GitHub API:

```javascript
// Count usage ratio of each template
const issues = await github.rest.issues.listForRepo({
  owner: 'your-org',
  repo: 'your-repo',
  state: 'all',
  per_page: 100
});

const templates = {};
for (const issue of issues.data) {
  const template = issue.body?.includes('## Steps to Reproduce') ? 'bug_report' :
                   issue.body?.includes('## Problem Description') ? 'feature_request' :
                   'other';
  templates[template] = (templates[template] || 0) + 1;
}

console.log('Template usage statistics:', templates);
```

### 9.4 Common Issues and Solutions

**Issue 1: Users don't use templates**

Solutions:
- Set `blank_issues_enabled: false` in `config.yml`
- Use Actions to automatically close Issues that don't use templates
- Clearly require template usage in the contribution guidelines

**Issue 2: Templates are too complex**

Solutions:
- Simplify templates, keep only essential fields
- Use conditional fields (grouped through markdown elements)
- Provide multiple templates for selection

**Issue 3: Old Issues are incompatible after template updates**

Solutions:
- Maintain backward compatibility of templates
- Set new fields as optional
- Guide users to fill in new fields through comments

### 9.5 Advanced Template Techniques

**Conditional content:**

```yaml
- type: markdown
  attributes:
    value: |
      <!-- The following content is only for Bug reports -->
      If you're reporting a Bug, please continue filling in the information below.
      
      <!-- If it's a feature request, you can skip to the feature request section below -->
```

**Template inheritance:**

Reuse template fragments using the `includes` keyword:

```yaml
# .github/ISSUE_TEMPLATE/_common.yml (common fragment, not displayed as a template)
- type: checkboxes
  id: common-terms
  attributes:
    label: Confirmation Items
    options:
      - label: I have searched existing Issues
        required: true
      - label: I am using the latest version
        required: false
```

**Dynamic links:**

```yaml
- type: markdown
  attributes:
    value: |
      📋 Before submitting, please review:
      - [Contribution Guidelines](https://github.com/${{ github.repository }}/blob/main/CONTRIBUTING.md)
      - [FAQ](https://github.com/${{ github.repository }}/wiki/FAQ)
```

---

## Summary

Issue and PR templates are one of the essential infrastructure components for project management. Through well-designed templates, you can:

1. **Standardize communication:** Ensure all Issues and PRs contain necessary information
2. **Improve efficiency:** Reduce back-and-forth communication between maintainers and contributors
3. **Automate workflows:** Work with GitHub Actions for automatic labeling, auto-assignment, and quality checks
4. **Improve experience:** Provide clear guidelines for contributors, lowering the barrier to participation
5. **Data-driven:** Collect structured data through templates to analyze project health

Remember, a good template should be like a good form -- simple, clear, and guiding. Regularly collecting feedback and continuously optimizing templates is a key practice for maintaining healthy project development.

## 10. Advanced Template Techniques and Practical Cases

### 10.1 Multi-Language Template Support

For internationalized projects, you can provide multilingual versions of Issue templates. GitHub automatically displays the corresponding language template based on the user's language preference:

```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: Report a bug
title: "[Bug]: "
labels: ["bug", "needs-triage"]
body:
  - type: markdown
    attributes:
      value: |
        ## English
        Please fill out the form below to report a bug.

        ## 中文
        请填写以下表单来报告一个问题。

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the bug clearly
      placeholder: |
        English: What happened? What did you expect?
        中文：发生了什么？你期望什么？
    validations:
      required: true
```

### 10.2 Dynamically Displaying Different Template Content Based on Labels

Use conditional logic to display different guidance messages:

```yaml
- type: markdown
  attributes:
    value: |
      ## Filling Guide

      **If it's a Bug report:** Please provide reproduction steps, expected behavior, and actual behavior.
      **If it's a Feature request:** Please describe the problem scenario and the expected solution.
      **If it's a Documentation issue:** Please point out inaccurate or missing parts of the documentation.

      ---
      > Please delete the sections that don't apply and only keep the content relevant to your Issue type.
```

### 10.3 Automated Scripts for Collecting System Information

Embed system information collection scripts in Issue templates to help maintainers quickly identify environment issues:

```yaml
- type: textarea
    id: system-info
    attributes:
      label: System Information
      description: |
        Please run the following command and paste the output:
        ```bash
        echo "OS: $(uname -a)" && echo "Node: $(node -v)" && echo "npm: $(npm -v)" && echo "Git: $(git --version)"
        ```
      render: shell
    validations:
      required: true
```

### 10.4 Security Vulnerability Report Template

Security vulnerability reports require special handling and should not be submitted publicly:

```yaml
# .github/ISSUE_TEMPLATE/security_vulnerability.yml
name: Security Vulnerability Report
description: Report a security vulnerability (will be handled through security advisories)
title: "[Security]: "
labels: ["security", "critical"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Security Vulnerability Report

        **Important:** If you've found a critical security vulnerability, please do not submit this Issue publicly.
        Please report it privately through [GitHub Security Advisories](https://github.com/owner/repo/security/advisories/new).

        This template is only for low-risk security issues.

  - type: dropdown
    id: severity
    attributes:
      label: Vulnerability Severity
      options:
        - Low - Information disclosure, low-risk configuration issues
        - Medium - Permission bypass, data leakage risk
        - High - Remote code execution, SQL injection, etc.
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Vulnerability Description
      description: Describe the security vulnerability in detail
    validations:
      required: true

  - type: textarea
    id: impact
    attributes:
      label: Impact Scope
      description: Describe the users and systems that may be affected by this vulnerability
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Reproduction Steps
      description: Provide steps to reproduce the vulnerability (low-risk vulnerabilities only)
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Confirmation Items
      options:
        - label: I understand this vulnerability could be maliciously exploited
          required: true
        - label: I agree not to publicly disclose this vulnerability until a fix is complete
          required: true
```

### 10.5 Performance Issue Report Template

```yaml
# .github/ISSUE_TEMPLATE/performance_issue.yml
name: Performance Issue
description: Report performance-related issues
title: "[Perf]: "
labels: ["performance"]
body:
  - type: textarea
    id: description
    attributes:
      label: Performance Issue Description
      description: Describe the performance issue you've observed
    validations:
      required: true

  - type: textarea
    id: benchmark
    attributes:
      label: Performance Data
      description: Provide performance test data or screenshots
      placeholder: |
        Request response time: XXms
        Memory usage: XX MB
        CPU usage: XX%
    validations:
      required: true

  - type: input
    id: environment
    attributes:
      label: Test Environment
      description: Describe the environment configuration for performance testing
      placeholder: "4-core CPU, 16GB RAM, SSD storage"
    validations:
      required: true

  - type: textarea
    id: profile
    attributes:
      label: Performance Analysis Results
      description: If available, provide output from performance analysis tools
      render: shell
    validations:
      required: false
```

### 10.6 Code Review Checklists in PR Templates

Create dedicated review checklists for different types of PRs:

```markdown
## Review Focus

### For Bug Fix PRs
- [ ] Are there corresponding test cases covering the bug
- [ ] Does the fix address the root cause rather than the symptoms
- [ ] Has it introduced any new regression issues
- [ ] Has the related documentation been updated

### For New Feature PRs
- [ ] Has the feature design been discussed
- [ ] Is there complete test coverage
- [ ] Is the API design backward-compatible
- [ ] Have usage examples been added
- [ ] Has the CHANGELOG been updated

### For Performance Optimization PRs
- [ ] Are there performance benchmark test data
- [ ] Does the optimization affect code readability
- [ ] Has it been tested under different scenarios
- [ ] Is there a rollback plan

### For Dependency Update PRs
- [ ] Have dependency license changes been checked
- [ ] Has the full test suite been run
- [ ] Have security vulnerabilities been checked
- [ ] Has the impact on package size been assessed
```

### 10.7 Using Templates to Guide Community Contributions

Create dedicated community contribution templates:

```yaml
# .github/ISSUE_TEMPLATE/community_contribution.yml
name: Community Contribution
description: Propose a community contribution plan
title: "[Community]: "
labels: ["community", "contribution"]
body:
  - type: textarea
    id: proposal
    attributes:
      label: Contribution Plan
      description: Describe what contribution you plan to make for the community
    validations:
      required: true

  - type: dropdown
    id: type
    attributes:
      label: Contribution Type
      options:
        - Documentation translation
        - Tutorial writing
        - Example code
        - Bug fix
        - New feature development
        - Performance optimization
        - Other
    validations:
      required: true

  - type: input
    id: timeline
    attributes:
      label: Estimated Completion Time
      description: When do you expect to complete this contribution
      placeholder: "Within 2 weeks"
    validations:
      required: false

  - type: textarea
    id: help-needed
    attributes:
      label: Help Needed
      description: Describe what help you need from project maintainers
    validations:
      required: false
```

### 10.8 Internationalization Best Practices for Templates

Provide comprehensive multilingual template support for global open-source projects:

1. **Bilingual template names:** Use `name: Bug Report / Bug Report` format with both languages
2. **Bilingual field labels:** Use `label: Description / Description` format with both languages
3. **Bilingual placeholder text:** Provide examples in both languages in placeholders
4. **Bilingual description text:** Provide descriptions in both languages in markdown elements
5. **Bilingual dropdown options:** Use `Bug Fix / Bug Fix` format with both languages

### 10.9 Template Integration with Project Management Tools

Integrate Issue templates with project management tools (such as GitHub Projects):

```yaml
- type: dropdown
    id: sprint
    attributes:
      label: Sprint
      options:
        - Sprint 1
        - Sprint 2
        - Sprint 3
        - Backlog
    validations:
      required: false

  - type: dropdown
    id: story-points
    attributes:
      label: Story Points
      options:
        - 1 - Simple
        - 2 - Medium
        - 3 - Complex
        - 5 - Very Complex
        - 8 - Needs Splitting
    validations:
      required: false
```

### 10.10 Continuous Optimization Strategy for Templates

Regularly collect and analyze template usage data to continuously optimize template design:

1. **Collect feedback:** Add feedback links in templates, inviting users to rate template quality
2. **Analyze data:** Track which fields are frequently left blank, consider whether these fields are needed
3. **A/B testing:** Try different template designs, compare which design collects more complete information
4. **Version iteration:** Each template change goes through a PR for team review and traceability
5. **Documentation update:** Update related instructions in the contribution guidelines after template changes

---

## 11. Common Template Errors and Solutions

### 11.1 Common Error 1: Templates Are Too Complex

**Problem manifestation:** Templates contain many fields, causing users to feel confused or frustrated when filling them in, resulting in many fields being left blank or filled in randomly.

**Solutions:**

- Simplify templates, keep only the most essential required fields
- Place optional fields at the end of the template, grouped under "Additional Information"
- Provide clear placeholder examples to help users understand the purpose of each field
- Consider creating multiple simple templates for different scenarios instead of one complex template

### 11.2 Common Error 2: Not Providing Enough Guidance

**Problem manifestation:** Users don't know how to fill in certain fields, resulting in inconsistent quality of submitted Issue information.

**Solutions:**

- Add detailed filling instructions in markdown elements
- Provide example content showing the expected filling format
- Use dropdowns and checkboxes instead of free text input
- Add template usage instructions in the contribution guidelines

### 11.3 Common Error 3: Templates Not Updated Timely

**Problem manifestation:** Options in the template are outdated and no longer reflect the actual state of the project, causing users to be unable to select the correct options.

**Solutions:**

- Establish a template review mechanism, regularly check template content
- Include template update tasks in project milestones
- Use a template changelog to record each modification
- Encourage community feedback on template issues

### 11.4 Common Error 4: Ignoring Template Accessibility

**Problem manifestation:** Templates only consider English users, not providing multilingual support for international users.

**Solutions:**

- Use bilingual labels and description text
- Provide multilingual template versions
- Use simple, clear language in templates, avoiding slang and idioms
- Ensure color contrast meets accessibility standards

### 11.5 Common Error 5: Not Fully Utilizing Automation

**Problem manifestation:** Manually processing template-submitted Issues is inefficient and error-prone.

**Solutions:**

- Use automatic label assignment rules
- Configure GitHub Actions to automatically process specific types of Issues
- Use Issue Forms' validation functionality to reduce invalid submissions
- Establish automated workflows to handle standard issues

### 11.6 Common Error 6: PR Templates Lack Specificity

**Problem manifestation:** All types of PRs use the same template, unable to provide dedicated checklists for different types of changes.

**Solutions:**

- Create dedicated templates for different types of PRs (Bug fixes, new features, documentation updates, etc.)
- Use GitHub's multiple PR template functionality
- Dynamically adjust checklists in templates based on change type
- Provide template selection guidance to help users choose the correct template

### 11.7 Common Error 7: Templates Have No Version Management

**Problem manifestation:** Template changes are not recorded, making it impossible to trace historical modifications and difficult to evaluate template improvement effects.

**Solutions:**

- Include template changes in version control
- Use PRs for template modifications for team review
- Establish a template changelog
- Regularly evaluate template usage effectiveness

---

## 12. Template Best Practices Summary

### 12.1 Design Principles

1. **Simplicity:** Only request necessary information, avoid over-engineering
2. **Guidance:** Provide clear instructions and examples to help users fill in correctly
3. **Consistency:** All templates use unified style and formatting
4. **Flexibility:** Allow users to adjust template content based on actual situations
5. **Maintainability:** Establish template update and maintenance mechanisms

### 12.2 Technical Implementation

1. **Use YAML forms:** Provide better user experience and data validation
2. **Use labels appropriately:** Automatically assign labels for easy categorization and filtering
3. **Configure template selectors:** Guide users to select the correct template
4. **Integrate automation:** Use GitHub Actions to automatically process template submissions
5. **Version control:** Include templates in version control to record change history

### 12.3 Team Collaboration

1. **Establish standards:** Create template usage standards and ensure team members follow them
2. **Regular review:** Regularly review template effectiveness and collect team feedback
3. **Continuous improvement:** Continuously optimize template design based on usage
4. **Documentation:** Detailedly explain template usage methods in the contribution guidelines
5. **Train newcomers:** Provide template usage training for new members

### 12.4 Community Management

1. **Multilingual support:** Provide multilingual templates for the international community
2. **Newcomer-friendly:** Design easy-to-understand templates to lower the barrier to participation
3. **Timely response:** Respond and handle Issues submitted through templates promptly
4. **Recognize contributions:** Acknowledge and reward high-quality Issues and PRs
5. **Transparent communication:** Communicate fully with the community when making template changes

---

## 13. Appendix: Template Quick Reference

### 13.1 YAML Form Field Type Quick Reference

| Field Type | Purpose | Key Properties |
|----------|------|----------|
| `markdown` | Display description text | `value` |
| `input` | Single-line text input | `label`, `placeholder`, `required` |
| `textarea` | Multi-line text input | `label`, `placeholder`, `render`, `required` |
| `dropdown` | Dropdown selection | `label`, `options`, `multiple`, `required` |
| `checkboxes` | Checkbox group | `label`, `options` |
| `number` | Number input | `label`, `min`, `max`, `required` |

### 13.2 Validation Rules Quick Reference

```yaml
validations:
  required: true                    # Required field
  regex: "^[a-zA-Z0-9]+$"         # Regex validation
  regex_error: "Can only contain letters and numbers"  # Validation failure message
  min: 0                            # Minimum value (number fields)
  max: 100                          # Maximum value (number fields)
```

### 13.3 Common Label Color Configuration

```yaml
# .github/labels.yml
- name: "bug"
  color: "d73a4a"
  description: "Something isn't working"

- name: "enhancement"
  color: "a2eeef"
  description: "New feature or request"

- name: "documentation"
  color: "0075ca"
  description: "Improvements or additions to documentation"

- name: "good first issue"
  color: "7057ff"
  description: "Good for newcomers"

- name: "help wanted"
  color: "008672"
  description: "Extra attention is needed"

- name: "priority: critical"
  color: "b60205"
  description: "Critical priority"

- name: "priority: high"
  color: "d93f0b"
  description: "High priority"

- name: "priority: medium"
  color: "fbca04"
  description: "Medium priority"

- name: "priority: low"
  color: "0e8a16"
  description: "Low priority"

- name: "status: needs-triage"
  color: "ededed"
  description: "Needs to be triaged"

- name: "status: in-progress"
  color: "1d76db"
  description: "Currently being worked on"

- name: "status: blocked"
  color: "e4e669"
  description: "Blocked by another issue"
```

### 13.4 Template File Checklist

Complete template directory structure reference:

```
.github/
├── ISSUE_TEMPLATE/
│   ├── 01_bug_report.yml           # Bug report
│   ├── 02_feature_request.yml      # Feature request
│   ├── 03_documentation.yml        # Documentation issue
│   ├── 04_performance.yml          # Performance issue
│   ├── 05_security.yml             # Security issue
│   ├── 06_question.yml             # Question
│   ├── 07_community.yml            # Community contribution
│   └── config.yml                  # Template selector configuration
├── PULL_REQUEST_TEMPLATE/
│   ├── bug_fix.md                  # Bug fix PR
│   ├── feature.md                  # New feature PR
│   ├── docs.md                     # Documentation update PR
│   ├── refactor.md                 # Refactoring PR
│   └── dependencies.md             # Dependency update PR
├── PULL_REQUEST_TEMPLATE.md        # Default PR template
├── CONTRIBUTING.md                 # Contribution guidelines
├── CODE_OF_CONDUCT.md              # Code of conduct
└── SECURITY.md                     # Security policy
```

### 13.5 GitHub Actions Workflow Templates for Automatic Template Processing

```yaml
# .github/workflows/issue-triage.yml
name: Issue Auto-Triage

on:
  issues:
    types: [opened, edited]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Auto-assign labels
        uses: actions/github-script@v7
        with:
          script: |
            const title = context.payload.issue.title.toLowerCase();
            const body = (context.payload.issue.body || '').toLowerCase();
            const labels = [];

            // Assign labels based on title keywords
            if (title.includes('[bug]')) labels.push('bug');
            if (title.includes('[feature]')) labels.push('enhancement');
            if (title.includes('[docs]')) labels.push('documentation');
            if (title.includes('[perf]')) labels.push('performance');
            if (title.includes('[security]')) labels.push('security');

            // Assign priority based on content keywords
            if (body.includes('critical')) {
              labels.push('priority: critical');
            } else if (body.includes('high')) {
              labels.push('priority: high');
            }

            // Add needs-triage label
            labels.push('status: needs-triage');

            // Apply labels
            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                labels: labels
              });
            }
```

### 13.6 Common Template Fields Reference

| Field Name | Usage Scenario |
|------|----------|
| Bug Report | Bug report template |
| Feature Request | Feature request template |
| Description | General description field |
| Steps to Reproduce | Bug report field |
| Expected Behavior | Bug report field |
| Actual Behavior | Bug report field |
| Environment | Bug report field |
| Version | Version information field |
| Screenshots | Optional visual aid |
| Additional Information | Supplementary information field |
| Checklist | Self-check confirmation items |
| Related Issues | Related issues field |
| Change Type | PR template field |
| Testing | PR template field |
| Breaking Changes | PR template field |
| Documentation | PR template field |
| Code Review | PR template field |
| Merge Request | PR template field |
| Summary | General summary field |
| Motivation | Feature request field |
| Alternatives | Feature request field |
| Use Case | Feature request field |
| Impact | Evaluation field |
| Priority | Classification field |
| Severity | Bug report field |
| Affected Components | Issue scope field |
| Proposed Solution | Feature request field |
| Acceptance Criteria | Requirement confirmation field |
| Definition of Done | Task completion criteria |
| Release Notes | Version release field |
```

---

**Previous: [README & Documentation](15-readme-docs.md) | Next: [Issue Tracking](16-issues.md)**

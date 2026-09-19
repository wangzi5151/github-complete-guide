# Exercise 24: Creating Issue Forms and PR Templates

## Learning Objectives

Through this exercise, you will master the following skills:

- Understand the value of Issue forms and PR templates
- Create YAML-format Issue forms
- Design different types of Issue templates
- Create Pull Request templates
- Configure automated label assignment
- Set up validation rules for Issues and PRs

## Prerequisites

- A GitHub account and a code repository
- Basic knowledge of YAML syntax
- Familiarity with GitHub Issues and Pull Requests

## Part 1: Understanding Issue Forms

### Why are Issue forms needed?

The traditional way of creating Issues is a free-form text box, which leads to:

- Incomplete information, requiring repeated back-and-forth communication
- Inconsistent formatting, making it difficult to quickly browse and categorize
- Difficulty in automated processing (such as automatic labeling)
- Maintainers spending a lot of time organizing information

Issue forms solve these problems through structured form fields, ensuring submitters provide complete, standardized information.

## Part 2: Creating Basic Issue Forms

Issue forms are defined using YAML format and support various field types, including text inputs, multi-line text areas, dropdown selectors, checkboxes, and more. By combining these field types effectively, you can design Issue forms that are both visually appealing and practical. When designing forms, consider user experience, avoid requiring too many mandatory fields, while ensuring enough information is collected to help maintainers quickly understand and address issues. Good form design should have: clear and understandable field names, appropriate placeholder hints, properly set required and optional fields, and suitable field types to guide users in entering correctly formatted information.

### Step 1: Create the Template Directory

```bash
# Enter the project directory
cd your-project

# Create the Issue template directory
mkdir -p .github/ISSUE_TEMPLATE

# View the directory structure
ls -la .github/ISSUE_TEMPLATE/
```

### Step 2: Create a Bug Report Template

Create the file `.github/ISSUE_TEMPLATE/bug_report.yml`:

```yaml
name: Bug Report
description: Report a bug
title: "[Bug]: "
labels: ["bug", "triage"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thank you for taking the time to report this bug! Please fill in the following information to help us quickly locate and fix the issue.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Clearly and concisely describe the bug
      placeholder: Please describe the issue you encountered...
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Provide detailed steps to reproduce the issue
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: Describe the behavior you expected
      placeholder: Please describe the expected result...
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: Describe the actual behavior
      placeholder: Please describe the actual result...
    validations:
      required: true

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots to help explain the issue
      placeholder: Drag and drop images here to upload...
    validations:
      required: false

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      description: The operating system you are using
      options:
        - Windows 11
        - Windows 10
        - macOS Sonoma
        - macOS Ventura
        - Ubuntu 22.04
        - Ubuntu 20.04
        - Other (please specify in the description)
    validations:
      required: true

  - type: dropdown
    id: browser
    attributes:
      label: Browser
      description: The browser you are using (if it is a frontend issue)
      options:
        - Chrome
        - Firefox
        - Safari
        - Edge
        - Other
        - N/A
    validations:
      required: false

  - type: input
    id: version
    attributes:
      label: Project Version
      description: The project version you are using
      placeholder: "e.g.: 1.2.3"
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Runtime Environment
      description: Provide other relevant environment information
      placeholder: |
        - Node.js version: 20.x
        - npm version: 10.x
        - Database: PostgreSQL 16
    validations:
      required: false

  - type: textarea
    id: logs
    attributes:
      label: Log Information
      description: If there are relevant error logs, please paste them here
      render: shell
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Checklist
      description: Please confirm the following before submitting
      options:
        - label: I have searched existing Issues and confirmed this is not a duplicate
          required: true
        - label: I have read the project documentation and FAQ
          required: true
```

### Step 3: Create a Feature Request Template

Create the file `.github/ISSUE_TEMPLATE/feature_request.yml`:

```yaml
name: Feature Request
description: Suggest a new feature
title: "[Feature]: "
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        Thank you for your feature suggestion! Please fill in the following information to help us better understand your needs.

  - type: textarea
    id: problem
    attributes:
      label: Problem Description
      description: Describe the problem or pain point you are experiencing
      placeholder: When using..., I always feel...
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Desired Solution
      description: Describe the feature you would like
      placeholder: I would like...
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives
      description: Describe other alternatives you have considered
      placeholder: I have tried...
    validations:
      required: false

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How important is this feature to you
      options:
        - Nice to have - would be better with this feature
        - Important - significantly improves user experience
        - Very important - seriously impacts workflow
    validations:
      required: true

  - type: dropdown
    id: category
    attributes:
      label: Feature Category
      description: Which category does this feature belong to
      options:
        - User Interface / User Experience
        - Performance Optimization
        - API / Interface
        - Documentation
        - Testing
        - Other
    validations:
      required: true

  - type: textarea
    id: additional
    attributes:
      label: Additional Information
      description: Provide any other relevant information, screenshots, or references
      placeholder: Add any extra context here...
    validations:
      required: false

  - type: checkboxes
    id: terms
    attributes:
      label: Checklist
      options:
        - label: I am willing to participate in the development of this feature
          required: false
        - label: I have searched existing feature requests and confirmed this is not a duplicate suggestion
          required: true
```

### Step 4: Create a Security Vulnerability Report Template

Create the file `.github/ISSUE_TEMPLATE/security_vulnerability.yml`:

```yaml
name: Security Vulnerability Report
description: Report a security vulnerability (please submit sensitive information through secure channels)
title: "[Security]: "
labels: ["security", "critical"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## ⚠️ Security Vulnerability Report Notice

        If you have discovered a **critical security vulnerability**, please do not report it in a public Issue.
        Please submit it through GitHub's private security vulnerability reporting feature, or send an email to security@example.com.

        For low-risk security issues, you may use this form.

  - type: dropdown
    id: severity
    attributes:
      label: Severity
      description: Assess the severity of this security issue
      options:
        - Low - Limited impact, difficult to exploit
        - Medium - Some impact, requires specific conditions
        - High - May lead to data breach or system compromise
        - Critical - May lead to large-scale security incidents
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Vulnerability Description
      description: Describe the security issue discovered
      placeholder: Please describe the security vulnerability...
    validations:
      required: true

  - type: textarea
    id: impact
    attributes:
      label: Potential Impact
      description: Describe the potential impact of this vulnerability
      placeholder: This vulnerability could lead to...
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Provide steps to reproduce the issue
      placeholder: |
        1. Visit '...'
        2. Enter '...'
        3. Observe the security issue
    validations:
      required: true

  - type: checkboxes
    id: disclosure
    attributes:
      label: Disclosure Plan
      options:
        - label: I agree not to publicly disclose this vulnerability before a fix is released
          required: true
        - label: I am willing to assist in verifying the fix
          required: false
```

### Step 5: Create a Documentation Improvement Template

Create the file `.github/ISSUE_TEMPLATE/documentation.yml`:

```yaml
name: Documentation Improvement
description: Report documentation issues or suggest improvements
title: "[Docs]: "
labels: ["documentation"]
assignees: []
body:
  - type: dropdown
    id: type
    attributes:
      label: Documentation Issue Type
      options:
        - Incorrect / inaccurate information
        - Missing content
        - Unclear instructions
        - Outdated content
        - Translation issues
        - Other
    validations:
      required: true

  - type: input
    id: page
    attributes:
      label: Related Page
      description: Provide the link to the relevant documentation page
      placeholder: "https://docs.example.com/..."
    validations:
      required: false

  - type: textarea
    id: description
    attributes:
      label: Issue Description
      description: Describe the issue in the documentation
      placeholder: In the ... section of the documentation, the following issue exists...
    validations:
      required: true

  - type: textarea
    id: suggestion
    attributes:
      label: Improvement Suggestion
      description: Provide your improvement suggestion
      placeholder: Suggest changing it to...
    validations:
      required: false
```

## Part 3: Creating the Issue Template Configuration File

### Create the Configuration File

Create the file `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: true
contact_links:
  - name: Usage Help
    url: https://github.com/your-org/your-repo/discussions
    about: If you need help with usage, please ask in Discussions
  - name: Security Vulnerability Report
    url: https://github.com/your-org/your-repo/security/advisories/new
    about: For critical security vulnerabilities, please report through private channels
  - name: View Documentation
    url: https://docs.example.com
    about: Before submitting an Issue, please check the project documentation first
```

## Part 4: Creating Pull Request Templates

Pull Request templates are another important tool that guides code contributors in providing standardized descriptions. Similar to Issue forms, PR templates ensure the completeness and consistency of code change descriptions. A good PR template should include change description, change type, test description, screenshots (if UI changes are involved), and a self-checklist. By using PR templates, code reviewers can quickly understand the background and purpose of changes, enabling more efficient code review. Additionally, the self-checklist helps contributors perform self-checks before submitting code to ensure code quality. PR templates also support Markdown format, allowing you to fully utilize tables, lists, links, and other elements to organize information, making descriptions clearer and more professional.

### Step 1: Create a Basic PR Template

Create the file `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Change Description

Briefly describe what changes this PR makes.

## Change Type

Please check the applicable type:

- [ ] Bug Fix (fixed an issue)
- [ ] New Feature (added new functionality)
- [ ] Breaking Change (will cause existing functionality to stop working)
- [ ] Documentation Update
- [ ] Code Refactoring (no functional changes)
- [ ] Performance Optimization
- [ ] Testing Related
- [ ] CI/CD Related
- [ ] Other

## Related Issues

Please link related Issues:

- Fixes #(issue number)
- Closes #(issue number)
- Related to #(issue number)

## Test Description

Describe how you tested these changes:

- [ ] Added new unit tests
- [ ] All existing tests pass
- [ ] Manually tested the following scenarios:
  - [ ] Scenario 1: ...
  - [ ] Scenario 2: ...

## Screenshots (if applicable)

If the changes involve UI, please provide screenshots:

| Before | After |
|--------|-------|
| Screenshot | Screenshot |

## Self-Checklist

Please confirm the following before submitting:

- [ ] My code follows the project's code style
- [ ] I have performed a self code review
- [ ] I have added necessary comments, especially in hard-to-understand areas
- [ ] I have updated the relevant documentation
- [ ] My changes do not produce new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing unit tests pass with my changes
- [ ] Any dependent changes have been merged and published

## Additional Information

Provide any other information you think the reviewer needs to know.
```

### Step 2: Create Templates for Different Types of PRs

You can create multiple PR templates and place them in the `.github/PULL_REQUEST_TEMPLATE/` directory:

```bash
mkdir -p .github/PULL_REQUEST_TEMPLATE
```

Create a bug fix specific template `.github/PULL_REQUEST_TEMPLATE/bugfix.md`:

```markdown
---
name: Bug Fix
about: Fix a bug
labels: bug
---

## Bug Description

Briefly describe the bug being fixed:

## Root Cause Analysis

Explain the root cause that led to this bug:

## Fix Description

Describe your fix:

## Test Verification

- [ ] Added test case to reproduce the bug
- [ ] Verified that the test case now passes
- [ ] No new issues introduced

## Related Issues

Fixes #

## Regression Risk Assessment

Assess the potential regression risk of this fix:

- Low / Medium / High

Risk explanation:
```

Create a feature development specific template `.github/PULL_REQUEST_TEMPLATE/feature.md`:

```markdown
---
name: New Feature
about: Add a new feature
labels: enhancement
---

## Feature Description

Describe this new feature:

## Design Document

If applicable, link to relevant design documents or discussions:

## Implementation Plan

Describe your implementation plan and architecture design:

## Usage Examples

Provide example code for using this new feature:

## Test Coverage

- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Added documentation examples

## Documentation Updates

- [ ] Updated API documentation
- [ ] Updated usage guide
- [ ] Updated CHANGELOG

## Related Issues

Implements #
```

## Part 5: Configuring Automated Label Assignment

Manually adding labels to Issues and Pull Requests is not only time-consuming but also prone to omissions or inconsistencies. By configuring automated label assignment, you can automatically add appropriate labels to Issues and PRs based on predefined rules. GitHub provides multiple automation labeling methods, including file path-based label assignment (suitable for PRs), content keyword-based label assignment (suitable for Issues), and commit message-based label assignment. Automated label assignment not only saves maintainers' time but also helps teams better categorize and track issues. For example, you can automatically add a "frontend" label to PRs that involve frontend code, and add a "performance optimization" label to Issues containing the keyword "performance". Combined with GitHub's project boards and filtering features, automated labels can significantly improve project management efficiency.

### Step 1: Create the Label Configuration File

Create the file `.github/labeler.yml`:

```yaml
# File path-based label configuration
documentation:
  - changed-files:
    - any-glob-to-any-file:
      - docs/**
      - "**/*.md"
      - "**/*.rst"

frontend:
  - changed-files:
    - any-glob-to-any-file:
      - src/components/**
      - src/pages/**
      - src/styles/**
      - "**/*.tsx"
      - "**/*.jsx"
      - "**/*.css"
      - "**/*.scss"

backend:
  - changed-files:
    - any-glob-to-any-file:
      - src/api/**
      - src/services/**
      - src/models/**
      - "**/*.py"
      - "**/*.java"

tests:
  - changed-files:
    - any-glob-to-any-file:
      - tests/**
      - **/*.test.*
      - **/*.spec.*

ci-cd:
  - changed-files:
    - any-glob-to-any-file:
      - .github/**
      - Dockerfile
      - docker-compose.yml

dependencies:
  - changed-files:
    - any-glob-to-any-file:
      - package.json
      - package-lock.json
      - requirements.txt
      - Pipfile
      - pom.xml

database:
  - changed-files:
    - any-glob-to-any-file:
      - migrations/**
      - src/models/**
      - **/*.sql
```

### Step 2: Create the Label Assignment Workflow

Create the file `.github/workflows/labeler.yml`:

```yaml
name: Label Pull Requests

on:
  pull_request_target:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          configuration-path: .github/labeler.yml
          sync-labels: true
```

### Step 3: Automatically Assign Labels Based on Issue Content

Create the file `.github/workflows/issue-labeler.yml`:

```yaml
name: Label Issues

on:
  issues:
    types: [opened, edited]

permissions:
  issues: write

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: github/issue-labeler@v3
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          configuration-path: .github/issue-labeler.yml
```

Create the Issue label configuration `.github/issue-labeler.yml`:

```yaml
# Label configuration based on Issue title and content
bug:
  - "(bug|错误|异常|崩溃|crash|error|exception)"

feature:
  - "(功能|特性|feature|enhancement|建议|suggestion)"

performance:
  - "(性能|慢|卡顿|performance|slow|timeout)"

security:
  - "(安全|漏洞|security|vulnerability|CVE)"

documentation:
  - "(文档|说明|documentation|docs|readme)"

question:
  - "(问题|疑问|如何|怎么|question|how|why)"
```

## Part 6: Advanced Challenges

After mastering the basics of Issue forms and PR template creation, you can try more advanced configurations to further optimize your project's contribution workflow. The following advanced challenges will help you explore more automation features provided by GitHub, including conditional forms, project board integration, and auto-closing inactive Issues. These advanced techniques can significantly improve the automation level of project management, allowing maintainers to devote more energy to core feature development.

### Challenge 1: Create Forms with Conditional Logic

Leverage advanced features of GitHub Issue forms:

```yaml
name: Advanced Bug Report
description: Bug report with conditional fields
body:
  - type: dropdown
    id: bug-type
    attributes:
      label: Bug Type
      options:
        - Frontend Bug
        - Backend Bug
        - Database Bug
    validations:
      required: true

  - type: textarea
    id: frontend-details
    attributes:
      label: Frontend Details
      description: Please provide frontend-related information
      placeholder: |
        - Browser version:
        - Screen resolution:
        - Operating system version:
    validations:
      required: false
    # Note: GitHub currently does not support conditional display, but you can explain through comments

  - type: textarea
    id: backend-details
    attributes:
      label: Backend Details
      description: Please provide backend-related information
      placeholder: |
        - Server operating system:
        - Runtime version:
        - Database version:
    validations:
      required: false
```

### Challenge 2: Create Project Board Automation

Configure GitHub Actions to automatically add Issues to the project board:

```yaml
# .github/workflows/project-board.yml
name: Add to Project Board

on:
  issues:
    types: [opened]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v1.0.2
        with:
          project-url: https://github.com/orgs/your-org/projects/1
          github-token: ${{ secrets.PROJECT_TOKEN }}
          labeled: bug, enhancement
```

### Challenge 3: Create Auto-Close Rules for Issues and PRs

Configure automatic closure of Issues under specific conditions:

```yaml
# .github/workflows/stale.yml
name: Close Stale Issues

on:
  schedule:
    - cron: '0 0 * * *'

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          days-before-stale: 30
          days-before-close: 7
          stale-issue-label: stale
          stale-issue-message: |
            This Issue has been inactive for 30 days and has been marked as stale.
            If this Issue is still relevant, please leave a comment.
            Otherwise, it will be automatically closed in 7 days.
          stale-pr-label: stale
          stale-pr-message: |
            This PR has been inactive for 30 days and has been marked as stale.
            Please update the status or leave a comment.
```

## Verification Checklist

After completing the exercise, please confirm the following:

- [ ] Created at least one Issue form template
- [ ] The form includes multiple field types (input boxes, dropdowns, checkboxes, etc.)
- [ ] Configured the `config.yml` file
- [ ] Created a Pull Request template
- [ ] Understand how to configure automated label assignment
- [ ] Tested the process of creating Issues and PRs

## Frequently Asked Questions

### Q1: How do I test Issue forms?

On the repository's Issues page, click "New Issue" and you will see the configured templates. Select a template to test the various form fields.

### Q2: How do I restrict Issue creation to templates only?

Set `blank_issues_enabled: false` in `config.yml` to disable blank Issues.

### Q3: What should I do if the PR template is not working?

Ensure the PR template file is in the correct location:
- Single template: `.github/PULL_REQUEST_TEMPLATE.md`
- Multiple templates: `.github/PULL_REQUEST_TEMPLATE/*.md`

## Summary

Through this exercise, you learned how to create structured Issue forms and PR templates. These tools can help you standardize your project's contribution workflow, improve team collaboration efficiency, and reduce communication costs. Automated label assignment further enhances the management efficiency of Issues and PRs. In real projects, it is recommended to customize these templates based on your team's actual needs and project characteristics. For example, user-facing projects may need more detailed Bug report forms, while developer-facing tool projects may need more feature request templates. As the project evolves, you may need to continuously adjust and optimize these templates to adapt to new requirements and workflows. Establishing comprehensive contribution guidelines, combined with Issue forms and PR templates, can greatly reduce the maintenance cost of open-source projects and attract more contributors to participate in project development. Continuously optimizing your project management process will help you build an efficient and friendly open-source community.

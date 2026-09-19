# GitHub Security and Permissions Management Complete Guide

## Chapter 1: GitHub Permission Model Overview

### 1.1 Permission Layer Structure

GitHub's permission model uses a three-layer architecture: organization level, team level, repository level. Understanding this layer structure is crucial for correct permission configuration. Each layer has its specific permission management methods and application scenarios.

**Organization Level**: Organization is the highest-level permission management unit in GitHub. Organization owners have the highest permissions, can manage all teams, repositories and members. Organization-level security policies affect all repositories within the organization.

**Team Level**: Team is the permission management unit within organization, used to group members and assign permissions. Teams can have their own repository access permissions, team members inherit team's permissions.

**Repository Level**: Repository is the most basic code management unit, each repository can independently configure collaborator permissions. Repository-level permissions directly determine users' access and operation capabilities for code.

### 1.2 Organization Level Permissions Details

Organization Owner has the highest permissions, can perform following operations:

**Manage Organization Settings**: Modify organization name, avatar, description, website and other basic information. Configure organization's security policies, such as enforcing two-factor authentication, setting IP whitelist, etc.

**Manage Teams**: Create, delete teams, manage team members, configure team's repository access permissions. Team Maintainer can manage members within team, but cannot delete teams or modify organization-level settings.

**Manage Repositories**: Create, delete, transfer repositories, configure repository's default settings. Organization owners can set default branch protection rules for all repositories within organization.

**Configure Security Policies**: Set organization-level security policies, such as enforcing two-factor authentication, configuring SAML SSO, setting IP whitelist, etc. These policies affect all members and repositories within organization.

**Manage Billing**: View and modify organization's subscription plans, manage payment methods, view usage reports.

**Audit Logs**: View audit logs of all activities within organization, including member join/leave, repository access, permission changes, etc. Audit logs are very important for security audits and compliance checks.

### 1.3 Team Level Permissions Details

Team is the permission management unit within organization, used to group members and assign permissions. Teams can have following roles:

**Team Member**: Basic team member, inherits team's repository permissions. Members can view team information, but cannot manage team settings or members.

**Team Maintainer**: Can manage team members and team settings. Maintainers can add or remove members, modify team description, but cannot delete team.

**Team Admin**: In some configurations, team admins have higher-level permissions, can manage team's repository access.

Team permission inheritance rules:
- Team members inherit team's repository permissions
- If user belongs to multiple teams, takes highest permission
- Directly granted repository permissions take priority over team permissions

### 1.4 Repository Level Permissions Details

Repository collaborator permissions are divided into five levels, each level has different operation capabilities:

**Read**: Most basic permission level. Users with this permission can clone repository, view code, view Issues and Pull Requests, but cannot modify anything. Suitable for users who need to view code but don't need to modify.

**Triage**: On top of Read permission, adds ability to manage Issues and Pull Requests. Users with this permission can close, reopen Issues, manage labels, but still cannot modify code. Suitable for users who need to participate in project management but don't need to modify code.

**Write**: On top of Triage permission, adds ability to push code. Users with this permission can create branches, push code, merge Pull Requests. This is the most commonly used permission level for developers.

**Maintain**: On top of Write permission, adds ability to manage repository settings. Users with this permission can manage branch protection rules, configure Webhooks, manage deploy keys, etc. Suitable for advanced developers who need to manage repository configuration.

**Admin**: Highest level of repository permission. Users with this permission can perform all operations, including deleting repository, managing collaborator permissions, transferring repository ownership, etc. Should be granted cautiously.

## Chapter 2: Repository Visibility

### 2.1 Three Visibility Types

GitHub provides three repository visibility types, each suitable for different scenarios:

**Public**: Repository visible to everyone, anyone can view code, clone repository. Public repositories suitable for open source projects, personal portfolios, public documentation, etc. Even for public repositories, should be careful not to commit sensitive information.

**Private**: Repository only visible to authorized users, only users added as collaborators or belonging to authorized teams can access. Private repositories suitable for commercial projects, internal tools, projects containing sensitive configurations, etc.

**Internal**: This is a visibility type specific to GitHub Enterprise. Internal repositories visible to all members within organization, but not visible to external users. Suitable for company internal shared projects, cross-team collaboration documents, etc.

### 2.2 Set Repository Visibility

```bash
# Use CLI to set as private
gh repo edit {owner}/{repo} --visibility private

# Set as public
gh repo edit {owner}/{repo} --visibility public

# Use API
gh api repos/{owner}/{repo} -X PATCH -f private=true
```

### 2.3 Visibility Selection Suggestions

**Scenarios suitable for Public**:
- Open source projects, hoping for community contribution
- Personal portfolio, showcasing technical abilities
- Documentation and tutorials, convenient for others learning
- Public APIs and SDKs, for developers use

**Scenarios suitable for Private**:
- Commercial project source code, containing core business logic
- Internal tools and scripts, for internal use only
- Projects containing sensitive configurations
- Customer projects, needing confidentiality

**Scenarios suitable for Internal**:
- Company internal shared projects, such as internal frameworks, tool libraries
- Cross-team collaboration documents, such as technical specifications, design documents
- Internal standards and specifications, such as code standards, process documents

### 2.4 Public Repository Security Considerations

Even for public repositories, should pay attention to security issues:

```bash
# 1. Never commit sensitive information
# Passwords, API Keys, certificates, private keys, etc.

# 2. Use .gitignore to exclude sensitive files
echo "*.env" >> .gitignore
echo "*.pem" >> .gitignore
echo "config/secrets.yml" >> .gitignore

# 3. Use environment variables to store sensitive information
# In code use process.env.API_KEY

# 4. Regularly check commit history
# Use git-secrets or trufflehog to scan history commits
git log --all --diff-filter=D -- "*.env"
```

## Chapter 3: Branch Protection Rules

### 3.1 Why Branch Protection is Needed

Branch protection is an important security feature provided by GitHub, can prevent following problems:

**Prevent direct push to important branches**: Without protection rules, any user with Write permission can directly push to main branch. Branch protection can force requiring code merge through Pull Request.

**Prevent unaudited code merge**: By configuring required code reviews, ensure all code changes are reviewed by at least one other developer. This helps discover potential errors and security vulnerabilities.

**Prevent code that breaks build from being merged**: By configuring required status checks, ensure all code changes pass automated tests and builds. Only code passing all checks can be merged.

**Prevent force push from overwriting history**: Force push overwrites Git history, may cause other developers' work to be lost. Branch protection can prohibit force push.

### 3.2 Configure Branch Protection Rules

```bash
# Use CLI to create branch protection rule
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["build","test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":2}' \
  -f restrictions=null

# View branch protection rules
gh api repos/{owner}/{repo}/branches/main/protection

# Delete branch protection rules
gh api -X DELETE repos/{owner}/{repo}/branches/main/protection
```

### 3.3 Branch Protection Options Details

| Option | Description | Recommended Configuration |
|--------|-------------|-------------------------|
| Require a pull request | Require merge through PR | ✅ Enable |
| Require approvals | Require review approval | ✅ Enable, at least 1 person |
| Dismiss stale PR approvals | Invalidate old review after new commit | ✅ Enable |
| Require review from Code Owners | Require code owner review | ✅ Enable |
| Require status checks | Require status check pass | ✅ Enable |
| Require branches to be up to date | Require branch is up to date | ✅ Enable |
| Require conversation resolution | Require resolve all conversations | ✅ Enable |
| Require signed commits | Require signed commits | ⚠️ As needed |
| Include administrators | Also apply to administrators | ✅ Enable |
| Restrict who can push | Restrict push personnel | ⚠️ As needed |
| Allow force pushes | Allow force push | ❌ Disable |
| Allow deletions | Allow branch deletion | ❌ Disable |

### 3.4 Using Rulesets

GitHub Rulesets is a more modern branch protection method, providing more flexible configuration:

```bash
# Create ruleset
gh api repos/{owner}/{repo}/rulesets -X POST -f '
{
  "name": "Main Branch Protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"]
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 2,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          {"context": "build"},
          {"context": "test"}
        ],
        "strict_required_status_checks_policy": true
      }
    },
    {
      "type": "non_fast_forward"
    }
  ]
}'
```

### 3.5 CODEOWNERS File

CODEOWNERS file is used to automatically assign code reviewers, ensuring specific code changes are reviewed by corresponding experts:

```
# File location: .github/CODEOWNERS or docs/CODEOWNERS

# Default owners
* @org/default-reviewers

# Frontend code
/src/frontend/ @org/frontend-team
*.css @org/design-team
*.js @org/frontend-team

# Backend code
/src/backend/ @org/backend-team
*.py @org/python-experts

# Documentation
/docs/ @org/docs-team
*.md @org/docs-team

# CI/CD configuration
/.github/ @org/devops-team

# Database related
/db/ @org/dba-team
*.sql @org/dba-team

# Security related
/security/ @org/security-team
```

## Chapter 4: Required Reviews and Status Checks

### 4.1 Configure Required Reviews

Code review is an important part of ensuring code quality. By configuring required reviews, can ensure all code changes are reviewed:

```bash
# Set minimum reviewer count
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -f required_pull_request_reviews='{
    "required_approving_review_count": 2,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "dismissal_restrictions": {
      "users": ["admin-user"],
      "teams": ["core-team"]
    }
  }'
```

### 4.2 Review Configuration Options

| Option | Description |
|--------|-------------|
| required_approving_review_count | Minimum approvals needed (1-6) |
| dismiss_stale_reviews | Whether to invalidate old reviews after new commit |
| require_code_owner_reviews | Whether to require CODEOWNERS review |
| dismissal_restrictions | Who can dismiss reviews |
| pull_request_bypassers | Who can bypass PR requirements |

### 4.3 Configure Status Checks

Status Checks are CI/CD pipeline pass conditions, ensuring code changes don't break builds:

```bash
# Configure required status checks
gh api repos/{owner}/{repo}/branches/main/protection \
  -X PUT \
  -f required_status_checks='{
    "strict": true,
    "contexts": [
      "build",
      "test",
      "lint",
      "security-scan"
    ]
  }'
```

### 4.4 Status Check Best Practices

```yaml
# .github/workflows/status-checks.yml
name: Status Checks

on:
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: make build
      - name: Test
        run: make test

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: make lint

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security Scan
        uses: github/codeql-action/analyze@v2
```

## Chapter 5: GitHub Secrets Management

In modern software development, applications typically need to access various external services and resources, such as databases, cloud services, third-party APIs, etc. These accesses usually require sensitive information (such as passwords, keys, tokens, etc.) for authentication. Writing these sensitive information directly into code is very dangerous practice, because code may be accidentally leaked or made public. GitHub Secrets provides a secure way to store and use these sensitive information.

### 5.1 Types of Secrets

GitHub provides multiple types of Secrets for storing sensitive information. Each type of Secrets has different scope and usage, developers need to choose appropriate type based on actual needs:

| Type | Scope | Usage |
|------|-------|-------|
| Repository Secrets | Single repository | Repository-level sensitive configuration |
| Environment Secrets | Specific environment | Environment-level sensitive configuration |
| Organization Secrets | Organization level | Cross-repo shared configuration |
| Dependabot Secrets | Dependabot | Dependency update usage |

### 5.2 Manage Repository Secrets

Repository Secrets is the most commonly used Secrets type, for storing sensitive information needed by specific repositories. Each repository can independently configure its own Secrets, these Secrets are only available in that repository's GitHub Actions workflows. Repository Secrets management is very simple, can operate through GitHub CLI or web interface.

```bash
# Add Secret using CLI
gh secret set API_KEY --body "your-api-key-here"

# Read from file
gh secret set PRIVATE_KEY --body "$(cat private-key.pem)"

# Use environment
gh secret set DB_PASSWORD --env production --body "secure-password"

# List all Secrets
gh secret list

# Delete Secret
gh secret delete OLD_SECRET
```

### 5.3 Manage Organization Secrets

Organization Secrets allow sharing sensitive information at organization level, avoiding repeated configuration in each repository. Organization Secrets can be configured to be available for all repositories, or only for specified repositories. This mechanism is particularly suitable for scenarios where same credentials need to be used in multiple repositories, such as shared deployment keys, common API tokens, etc.

```bash
# Add organization Secret
gh secret set SHARED_TOKEN --org my-org --body "shared-token"

# Configure repository access for organization Secret
gh secret set SHARED_TOKEN --org my-org \
  --repos "repo1,repo2" \
  --visibility selected

# Visibility options:
# - all: Available for all repositories
# - private: Only available for private repositories
# - selected: Available for specified repositories
```

### 5.4 Use Secrets in Actions

In GitHub Actions workflows, can reference Secrets using special syntax. Secrets are automatically injected into workflow's environment variables for steps to use. Note that Secrets are automatically masked in logs to prevent accidental leakage. However, developers should still avoid printing Secrets to logs, because in some situations may bypass this protection mechanism.

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to server
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: |
          echo "Deploying with API key..."
          # Use environment variables for deployment
```

### 5.5 Secrets Security Best Practices

Secrets security management is an important part of overall security strategy. Improper Secrets management may lead to serious security incidents, such as data leakage, service abuse, etc. The following are practice-verified Secrets security best practices, developers should strictly follow in daily work.

**Principle of Least Privilege**: Only grant necessary Secrets access permissions. Different environments should use different Secrets, avoid cross-environment usage. For example, production environment database password should not be used in test environment.

**Regular Rotation**: Regularly update Secrets values, reduce leakage risk. Recommend rotating key Secrets every 3-6 months. When employee leaves or Secrets leakage suspected, should immediately rotate related Secrets.

**Audit Usage**: Regularly check Secrets usage, ensure no abnormal access. Can view Secrets access records through audit logs, timely discover suspicious behavior.

**Avoid Log Leakage**: Ensure Secrets not printed to logs. In Actions, don't use `echo` to directly output Secrets values. Can use `::add-mask::` command to mark custom values as sensitive information.

## Chapter 6: Environment Protection Rules

Environment is a concept in GitHub Actions used to distinguish different deployment targets. By using environments, developers can configure different protection rules and Secrets for different deployment targets (such as development, testing, staging, production). Environment protection rules can help teams control deployment process, ensure only authorized and verified code can be deployed to important environments.

### 6.1 Create Environment

Environments can be created in repository settings, or dynamically created through API. Each environment can independently configure protection rules, Secrets and variables. Environment creation and management is usually handled by repository administrators or DevOps engineers.

```bash
# Create environment using CLI
gh api repos/{owner}/{repo}/environments/production \
  -X PUT \
  -f wait_timer=30 \
  -f reviewers='[{"type":"Team","id":123}]' \
  -f deployment_branch_policy='{
    "protected_branches": true,
    "custom_branch_policies": false
  }'
```

### 6.2 Environment Protection Rules

Environment protection rules define conditions that must be met before deployment to that environment. These rules can help teams implement deployment approval process, delayed deployment, branch restrictions, etc. By reasonably configuring protection rules, can greatly reduce risk of mis-deployment and unauthorized deployment.

| Rule | Description |
|------|-------------|
| Required reviewers | Deployment requires specified personnel approval |
| Wait timer | Wait specified time (minutes) before deployment |
| Branch restrictions | Restrict branches that can deploy |
| Environment Secrets | Environment-specific Secrets |

### 6.3 Multi-environment Configuration Example

In actual projects, typically need to configure multiple environments to support complete software delivery process. Typical environments include development environment, testing environment, staging environment and production environment. Each environment has different protection levels, production environment usually has strictest protection rules.

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Staging
        env:
          STAGING_API_KEY: ${{ secrets.STAGING_API_KEY }}
        run: ./deploy.sh staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        env:
          PRODUCTION_API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: ./deploy.sh production
```

## Chapter 7: Dependabot Security Updates

In modern software development, projects typically depend on large number of third-party libraries and frameworks. These dependencies may have security vulnerabilities, if not fixed in time, may be exploited by attackers. Manually checking and updating dependencies is tedious and easily overlooked work. Dependabot is GitHub's automated dependency update tool, can help teams timely discover and fix dependency vulnerabilities, maintain project security.

### 7.1 Enable Dependabot

Dependabot configuration is done by creating `.github/dependabot.yml` file in repository. Configuration file defines package managers to monitor, check frequency, reviewers, etc. After enabling Dependabot, it will periodically check project dependencies, when discovering security updates or new versions available, will automatically create Pull Request.

```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "team-lead"
    assignees:
      - "developer"
    labels:
      - "dependencies"
      - "security"

  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 7.2 Dependabot Configuration Options

Dependabot provides rich configuration options, allowing developers to customize dependency update behavior. By reasonably configuring these options, can make Dependabot better adapt to project's specific needs. For example, can set check frequency, limit simultaneous open PR count, specify reviewers and assignees, etc.

| Option | Description |
|--------|-------------|
| package-ecosystem | Package manager type |
| directory | Configuration file directory |
| schedule.interval | Check frequency (daily/weekly/monthly) |
| open-pull-requests-limit | Maximum PR count |
| reviewers | PR reviewers |
| assignees | PR assignees |
| labels | PR labels |
| target-branch | Target branch |
| versioning-strategy | Version strategy |

### 7.3 Dependabot Alerts

Dependabot Alerts is one of Dependabot's core features. When new vulnerability information is published in GitHub's security advisory database, Dependabot will automatically scan all repositories using that dependency, and create security alerts for affected repositories. Developers can view all Dependabot Alerts in repository's Security tab, and fix according to suggestions.

```bash
# View Dependabot Alerts
gh api repos/{owner}/{repo}/dependabot/alerts

# View specific Alert
gh api repos/{owner}/{repo}/dependabot/alerts/{alert_number}

# Update Alert status
gh api repos/{owner}/{repo}/dependabot/alerts/{alert_number} \
  -X PATCH \
  -f state=dismissed \
  -f dismissed_reason=no_bandwidth
```

### 7.4 Dependabot Auto-merge

For low-risk dependency updates (such as patch version updates), can configure auto-merge feature. Auto-merge can reduce developers' manual operations, speed up dependency updates. However, auto-merge should be used cautiously, recommend only enabling auto-merge for update types that have been fully tested.

```yaml
# .github/workflows/dependabot-auto-merge.yml
name: Dependabot Auto Merge

on:
  pull_request:

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v1
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"

      - name: Auto merge minor updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-minor'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Chapter 8: Code Scanning

Code Scanning is GitHub's static code analysis feature, can automatically discover security vulnerabilities and code quality issues in code. By integrating code scanning into development process, teams can discover and fix potential security issues before code merges to main branch, greatly reducing security risks.

### 8.1 What is Code Scanning

Code Scanning uses CodeQL engine for deep code analysis. CodeQL is GitHub's semantic code analysis engine, it converts code into queryable database, then uses predefined query rules to detect various security vulnerabilities and code defects. CodeQL can detect multiple types of security issues, including SQL injection, cross-site scripting (XSS), path traversal, hardcoded credentials, etc.

### 8.2 Enable CodeQL

CodeQL can be enabled through GitHub Actions workflow. After configuring CodeQL scanning, it will automatically run on every code push or Pull Request, analyzing code for security issues. CodeQL supports multiple programming languages, including JavaScript, Python, Java, C/C++, C#, Go, Ruby, etc. For large projects, can configure periodic scans (such as weekly) to continuously monitor code security status.

```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Every Monday UTC 6:00

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
        with:
          category: "/language:${{ matrix.language }}"
```

### 8.3 CodeQL Supported Languages

CodeQL continuously expanding support for different programming languages. Currently, CodeQL has good support for mainstream programming languages, including languages commonly used in frontend, backend and mobile development. Different languages' support levels may vary, recommend checking official documentation for latest support status.

CodeQL supports multiple programming languages, including:

| Language | Support Status |
|----------|----------------|
| JavaScript/TypeScript | Stable |
| Python | Stable |
| Java/Kotlin | Stable |
| C/C++ | Stable |
| C# | Stable |
| Go | Stable |
| Ruby | Stable |
| Swift | beta |
| Rust | beta |

### 8.4 View Scanning Results

After CodeQL scanning completes, results will be displayed in repository's Security tab. Each security alert includes detailed vulnerability description, affected code location, vulnerability severity level, and fix suggestions. Developers can quickly locate and fix security issues based on this information. For false positives or known risks, developers can choose to close alert, and explain reason.

```bash
# View code scanning alerts
gh api repos/{owner}/{repo}/code-scanning/alerts

# View specific alert
gh api repos/{owner}/{repo}/code-scanning/alerts/{alert_number}

# Update alert status
gh api repos/{owner}/{repo}/code-scanning/alerts/{alert_number} \
  -X PATCH \
  -f state=dismissed \
  -f dismissed_reason=false_positive
```

## Chapter 9: Secret Scanning

Key leakage is a common security issue in software development. Developers may accidentally commit API keys, database passwords, access tokens and other sensitive information to code repositories. Once this information is leaked, attackers may use them to access sensitive data or perform unauthorized operations. Secret Scanning is GitHub's key leakage detection feature, can automatically scan repositories for sensitive information, helping developers timely discover and fix key leakage issues.

### 9.1 What is Secret Scanning

Secret Scanning automatically scans repository code and commit history, detecting known key patterns. It supports detecting key formats for hundreds of different services, including AWS, Azure, Google Cloud, GitHub, Slack, etc. When possible key leakage is detected, GitHub will send security alerts to repository administrators, and provide fix suggestions.

### 9.2 Enable Secret Scanning

Secret Scanning can be enabled in repository settings. After enabling, GitHub will automatically scan all code and commit history in repository. For public repositories, Secret Scanning is enabled by default. For private repositories, need to manually enable in repository settings. Additionally, can enable Push Protection feature, to detect key leakage in real-time during code push, preventing sensitive information from being pushed to repository.

```bash
# In repository Settings → Security → Code security and analysis
# Enable "Secret scanning"
# Enable "Push protection"

# Or use API
gh api repos/{owner}/{repo} \
  -X PATCH \
  -f security_and_analysis='{
    "secret_scanning": {
      "status": "enabled"
    },
    "secret_scanning_push_protection": {
      "status": "enabled"
    }
  }'
```

### 9.3 Secret Scanning Features

Secret Scanning provides multiple feature modules, helping developers comprehensively protect key security. These features work together, forming complete key leakage detection and protection system. Developers should fully utilize these features, build multi-layer security protection.

| Feature | Description |
|---------|-------------|
| Secret scanning | Scan repository for known key patterns |
| Push protection | Block pushes containing keys |
| Partner alerts | Key detection integrated with partners |
| Custom patterns | Custom key patterns |

### 9.4 Custom Key Patterns

Besides built-in key detection rules, Secret Scanning also supports custom key patterns. This is very useful for detecting specific key formats used within organization. For example, if organization internally uses specific format API keys, can create custom patterns to detect these keys. Custom patterns use regular expressions, very flexible.

```bash
# Create custom key pattern
gh api repos/{owner}/{repo}/secret-scanning/push-protection/custom-patterns \
  -X POST \
  -f '{
    "name": "Internal API Key",
    "pattern": "internal_api_key_[a-zA-Z0-9]{32}",
    "is_enabled": true
  }'
```

### 9.5 Handle Secret Scanning Alerts

When Secret Scanning detects key leakage, will create security alert. Developers should timely handle these alerts, revoke leaked keys, and generate new keys. Standard process for handling key leakage includes: confirm leakage, revoke leaked key, generate new key, update services using that key, close security alert. Timely handling key leakage can minimize security risks.

```bash
# View alerts
gh api repos/{owner}/{repo}/secret-scanning/alerts

# Update alert status
gh api repos/{owner}/{repo}/secret-scanning/alerts/{alert_number} \
  -X PATCH \
  -f state=resolved \
  -f resolution=revoked

# Resolution options:
# - revoked: Key has been revoked
# - false_positive: False positive
# - wont_fix: Won't fix
# - used_in_tests: Used in tests
```

## Chapter 10: Security Advisories

Security Advisory is GitHub's security vulnerability disclosure mechanism. When security vulnerability is discovered in project, maintainers can create security advisory to coordinate vulnerability fix and disclosure. Security advisory provides a secure space for maintainers and security researchers to privately discuss vulnerability details, until fix solution is ready for public disclosure.

### 10.1 Create Security Advisory

Security advisory creation typically follows responsible disclosure process. First, person discovering vulnerability (can be maintainer, security researcher or user) privately reports vulnerability. Then, maintainer creates security advisory draft, collaborates with reporter to develop fix solution. After fix version released, security advisory is publicized, disclosing vulnerability information and fix solution to community.

```bash
# Create security advisory draft
gh api repos/{owner}/{repo}/security-advisories \
  -X POST \
  -f '{
    "summary": "SQL Injection vulnerability",
    "description": "A SQL injection vulnerability was found in the login endpoint.",
    "severity": "high",
    "vulnerabilities": [
      {
        "package": {
          "ecosystem": "npm",
          "name": "example-package"
        },
        "vulnerable_version_range": "< 1.2.3",
        "patched_versions": ">= 1.2.3"
      }
    ]
  }'
```

### 10.2 Security Advisory Process

Security advisory release is a rigorous process, requires coordinating multiple stakeholders. The following is typical security advisory release process, each step needs careful execution to ensure vulnerability is properly handled, while maximizing user safety.

1. **Discover Vulnerability**: Discover vulnerability through code review, security scanning or external report
2. **Create Security Advisory Draft**: Create private security advisory draft on GitHub
3. **Collaborate with Maintainers to Fix**: Collaborate with project maintainers to develop fix solution
4. **Release Fix Version**: Release new version containing fix
5. **Release Security Advisory**: Publicly disclose vulnerability information and fix solution
6. **CVE Assignment**: If needed, apply for CVE number

## Chapter 11: 2FA Two-Factor Authentication

Two-Factor Authentication (2FA) is an important measure to protect account security. Traditional password authentication only relies on one factor (information user knows), while two-factor authentication requires users to provide two different types of authentication factors. This greatly increases difficulty for attackers to gain account access, even if password is leaked, attackers still cannot access account.

### 11.1 Enable 2FA

Enabling 2FA is the first step to protect GitHub account security. GitHub supports multiple 2FA methods, including TOTP applications, SMS and security keys. Recommend using TOTP application, because it doesn't rely on network connection, and security is higher than SMS. After enabling 2FA, each login requires entering dynamic verification code, ensuring only account holder can access account.

**Enable Steps**:
1. Visit Settings → Password and authentication
2. Click "Enable two-factor authentication"
3. Select authentication method (recommend TOTP application)
4. Scan QR code or enter key
5. Save recovery codes

### 11.2 2FA Authentication Methods

GitHub supports multiple 2FA authentication methods, each method has different security and convenience. Developers should choose appropriate authentication method based on security needs and usage habits. For high-security requirement accounts, recommend using security keys (like YubiKey) as primary authentication method.

| Method | Security | Convenience | Recommended |
|--------|----------|-------------|-------------|
| TOTP Application | High | High | ✅ Recommended |
| SMS | Medium | High | ⚠️ Second choice |
| Security Key | Highest | Medium | ✅ Recommended |
| Recovery Codes | - | - | Must save |

### 11.3 Recommended TOTP Applications

TOTP (Time-based One-Time Password) is time-based one-time password algorithm. TOTP applications generate dynamic verification codes based on current time and shared key, verification codes update every 30 seconds. The following are several commonly used TOTP applications, they all support multi-platform and multi-account management.

- **1Password**: Cross-platform password manager, supports TOTP
- **Authy**: TOTP application supporting multi-device sync
- **Microsoft Authenticator**: Microsoft official TOTP application
- **Google Authenticator**: Google official TOTP application

### 11.4 Recovery Code Management

Recovery codes are the only recovery method when 2FA is lost. When user cannot use 2FA device (such as phone lost, device change, etc.), can use recovery codes to regain account access. Recovery codes are generated when enabling 2FA, will only be displayed once, must immediately save to secure location.

**Recovery Code Secure Storage Suggestions**:
- Save recovery codes to password manager
- Print recovery codes and store in secure physical location
- Don't store recovery codes on devices others can access
- Don't store recovery codes in GitHub repositories
- Regularly check if recovery codes are still valid

### 11.5 Organization Mandatory 2FA

Organization owners can require all members to enable 2FA, this is an important measure to protect organization security. After organization enables mandatory 2FA policy, members who haven't enabled 2FA will not be able to access organization resources. Organization administrators should regularly check members' 2FA status, ensure all members have enabled 2FA. For members who haven't enabled 2FA, should timely remind and provide help.

```bash
# View members who haven't enabled 2FA
gh api orgs/{org}/members?filter=2fa_disabled

# Remove members who haven't enabled 2FA
gh api -X DELETE orgs/{org}/members/{username}
```

## Chapter 12: SSH Key and PAT Security Management

SSH Key and Personal Access Token (PAT) are two main authentication methods for accessing GitHub. SSH Key is used for Git operations (such as clone, push, pull), PAT is used for API access and HTTPS authentication. Correct management of these credentials is crucial for protecting account security. This chapter will provide detailed introduction on how to securely create, use and manage these credentials.

### 12.1 SSH Key Management

SSH Key is a public key encryption-based authentication method, more secure than password authentication. SSH Key consists of public key and private key, public key uploaded to GitHub, private key saved locally. When performing Git operations, SSH client uses private key for authentication, no need to enter password. Recommend using Ed25519 algorithm to generate SSH Key, because it's more secure and faster than RSA.

```bash
# Generate SSH key (recommend Ed25519)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or use RSA
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard  # Linux

# Test connection
ssh -T git@github.com
```

### 12.2 SSH Key Security Best Practices

SSH Key security management is a key part of protecting account security. The following are practice-verified SSH Key security best practices, developers should strictly follow in daily work. These best practices can help developers avoid common security risks, ensure secure SSH Key usage.

**Use Ed25519 Algorithm**: Ed25519 is currently the most secure SSH Key algorithm, more secure and faster than RSA. Recommend all newly generated SSH Keys use Ed25519 algorithm.

**Set Passphrase for Private Key**: Passphrase is additional protection for private key. Even if private key file is leaked, cannot use without passphrase. Recommend setting strong passphrase for all private keys.

**Regularly Rotate SSH Key**: Regularly changing SSH Key can reduce key leakage risk. Recommend rotating SSH Key every 6-12 months, or immediately when key leakage suspected.

**Use Different Keys for Different Devices**: Generate different SSH Keys for different devices, convenient for management and revocation. When a device lost or stolen, only need to revoke that device's key, won't affect other devices.

**Use SSH Config File to Simplify Management**: SSH config file (~/.ssh/config) can simplify multi-key management. Through config file, can specify different keys for different GitHub accounts.

```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work
    IdentitiesOnly yes
```

### 12.3 Personal Access Token (PAT) Management

Personal Access Token (PAT) is authentication method for accessing GitHub API. PAT can replace password for HTTPS authentication, also can be used for API access. GitHub provides two types of PAT: Classic PAT and Fine-grained PAT. Fine-grained PAT provides more precise permission control, recommended to use.

**Classic PAT**: Classic PAT provides broad permission scopes, such as repo, workflow, admin:org, etc. Each permission scope includes multiple sub-permissions, cannot individually control. Classic PAT suitable for scenarios needing broad access permissions.

**Fine-grained PAT**: Fine-grained PAT allows precise control of access permissions for specific repositories. Can individually configure read or write permissions for each repository, greatly improving security. Fine-grained PAT suitable for scenarios only needing access to specific repositories.

```bash
# Create classic PAT
# Settings → Developer settings → Personal access tokens

# Create fine-grained PAT (recommended)
# Settings → Developer settings → Personal access tokens → Fine-grained tokens

# Use PAT
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
gh auth login --with-token <<< "$GITHUB_TOKEN"
```

### 12.4 PAT Permission Scopes

Classic PAT permission scopes define token's accessible resource types. Developers should choose minimum necessary permission scopes based on actual needs, avoid granting excessive permissions. The following are commonly used permission scopes and their descriptions.

| Scope | Description |
|-------|-------------|
| repo | Full repository access |
| workflow | GitHub Actions |
| admin:repo_hook | Webhook management |
| read:org | Organization info |
| user | User info |
| gist | Gist access |

### 12.5 PAT Security Best Practices

PAT security management is equally important as SSH Key. Improper PAT management may lead to unauthorized account access. The following are PAT security best practices, developers should strictly follow in daily work.

**Use Fine-grained PAT**: Fine-grained PAT provides more precise permission control, more secure than classic PAT. Recommend prioritizing fine-grained PAT, only use classic PAT when necessary.

**Set Expiration Time**: Set reasonable expiration time for PAT, avoid long-term valid tokens. After expiration, need to recreate token, this can reduce token leakage risk.

**Regular Rotation**: Regularly change PAT, recommend rotating every 3-6 months. When employee leaves or token leakage suspected, should immediately revoke related tokens.

**Secure Storage**: Store PAT in secure location, such as password manager. Don't store PAT in code, configuration files or documentation.

**Monitor Usage**: Regularly check PAT usage, ensure no abnormal access. Can view PAT usage records through GitHub's security log.

## Chapter 13: Security Best Practices Checklist

Security is a continuous process, requires protection at multiple levels. This chapter provides a comprehensive security best practices checklist, covering personal account security, repository security, organization security, CI/CD security, etc. Developers and teams should regularly review these checklists, ensure security measures are implemented.

### 13.1 Personal Account Security

Personal account security is the foundation of overall security. Every developer should protect their account, avoid unauthorized access. The following is personal account security best practices checklist.

- [ ] Enable 2FA two-factor authentication
- [ ] Use strong password (12+ characters, including uppercase, lowercase, numbers, special characters)
- [ ] Use password manager (1Password, Bitwarden, etc.)
- [ ] Regularly check account activity
- [ ] Review authorized applications
- [ ] Use SSH Key instead of password
- [ ] Create different PATs for different purposes
- [ ] Set PAT expiration time

### 13.2 Repository Security

Repository security is key to protecting code and projects. Every repository should configure appropriate security measures, prevent unauthorized access and code leakage. The following is repository security best practices checklist.

- [ ] Enable branch protection rules
- [ ] Configure required code reviews
- [ ] Enable status checks
- [ ] Use CODEOWNERS file
- [ ] Enable Dependabot security updates
- [ ] Enable Secret Scanning
- [ ] Enable Code Scanning
- [ ] Configure .gitignore to exclude sensitive files
- [ ] Regularly review collaborator permissions
- [ ] Use GitHub Secrets to store sensitive information

### 13.3 Organization Security

Organization security is key to protecting entire team and projects. Organization administrators should configure appropriate security policies, ensure all members and repositories meet security requirements. The following is organization security best practices checklist.

- [ ] Force members to enable 2FA
- [ ] Configure SAML SSO (Enterprise)
- [ ] Use teams to manage permissions
- [ ] Regularly review organization members
- [ ] Configure IP whitelist (Enterprise)
- [ ] Enable audit logs
- [ ] Configure security policy (SECURITY.md)
- [ ] Use Environment Protection Rules
- [ ] Configure Dependabot auto-merge strategy

### 13.4 CI/CD Security

CI/CD security is key to protecting automation processes. Improper CI/CD configuration may lead to sensitive information leakage or unauthorized deployment. The following is CI/CD security best practices checklist.

- [ ] Use minimum privilege GITHUB_TOKEN
- [ ] Configure Environment Protection Rules
- [ ] Review third-party Actions
- [ ] Use Actions pinned versions
- [ ] Don't print Secrets in logs
- [ ] Use OIDC to connect cloud services
- [ ] Regularly rotate Secrets
- [ ] Configure Actions run timeout

### 13.5 SECURITY.md Template

SECURITY.md file is project's security policy document, used to inform users and contributors how to report security vulnerabilities. Every open source project should create SECURITY.md file, defining vulnerability reporting process and response time. The following is SECURITY.md template, developers can modify according to project needs.

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | ✅ Yes |
| 5.0.x   | ❌ No |
| 4.0.x   | ✅ Yes |
| < 4.0   | ❌ No |

## Reporting a Vulnerability

Please report security vulnerabilities to security@example.com.

**Do not** open a public GitHub issue for security vulnerabilities.

### What to include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response timeline:
- Initial response: 48 hours
- Status update: 7 days
- Fix release: 30 days
```

### 13.6 Security Tool Recommendations

Besides GitHub's built-in security features, there are many third-party security tools that can help teams improve code security. These tools can be integrated into CI/CD processes, achieving automated security detection. The following are commonly used security tool recommendations, developers can choose appropriate tools based on project needs.

| Tool | Purpose | Integration Method |
|------|---------|-------------------|
| CodeQL | Static code analysis | GitHub Actions |
| Dependabot | Dependency security updates | Native support |
| Trivy | Container security scanning | GitHub Actions |
| Snyk | Dependency and container scanning | GitHub App |
| SonarQube | Code quality analysis | GitHub Actions |
| GitLeaks | Key leakage detection | GitHub Actions |
| Semgrep | Custom rule scanning | GitHub Actions |

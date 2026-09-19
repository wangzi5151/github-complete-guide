# GitHub Security Best Practices

> This chapter will explain in detail how to protect your GitHub account and repository security, covering account security, repository security, CI/CD security, dependency security and team security.

---

## Table of Contents

1. [Account Security](#account-security)
2. [Repository Security](#repository-security)
3. [CI/CD Security](#cicd-security)
4. [Dependency Security](#dependency-security)
5. [Team Security](#team-security)
6. [Security Incident Response](#security-incident-response)
7. [Security Checklist](#security-checklist)
8. [Related Resources](#related-resources)

---

## Account Security

### 1. Enable Two-Factor Authentication (2FA)

Two-factor authentication is the first line of defense for account security. Even if password is leaked, attackers cannot access your account.

**Setup Steps**:
1. Go to **Settings** → **Password and authentication**
2. Click **Enable two-factor authentication**
3. Select verification method:
   - Authenticator app (recommended)
   - SMS
   - Security key

**Recommended**:
- **Authenticator app**: Google Authenticator, Authy, 1Password
- **Security key**: YubiKey, Titan Security Key

**Why recommend authenticator app?**
- SMS may be intercepted or SIM card hijacked
- Authenticator app generates time-based one-time passwords (TOTP)
- Can be used even when phone is offline

**Backup Recovery Codes**:
After enabling 2FA, GitHub will provide a set of recovery codes. Be sure to store them securely in multiple locations:
- Password manager
- Encrypted USB drive
- Paper backup (stored in secure location)

### 2. Use SSH Keys

SSH keys are more secure than passwords, and you don't need to enter a password every time.

**Generate SSH Key**:
```bash
# Recommend Ed25519 (more secure, faster)
ssh-keygen -t ed25519 -C "your@email.com"

# Or use RSA (better compatibility)
ssh-keygen -t rsa -b 4096 -C "your@email.com"
```

**Security Suggestions**:
- Use different keys for different devices
- Set strong password for keys
- Rotate keys regularly (recommend every 6-12 months)
- Use ssh-agent to manage keys

**Key Management Best Practices**:
```bash
# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to ssh-agent
ssh-add ~/.ssh/id_ed25519

# List added keys
ssh-add -l

# Delete all keys
ssh-add -D
```

### 3. Use Personal Access Token (PAT)

PAT is used to replace the password for API authentication and Git operations.

**Create Token**:
1. **Settings** → **Developer settings** → **Personal access tokens**
2. Click **Generate new token**
3. Select minimum permissions
4. Set expiration time

**Security Suggestions**:
- Use fine-grained token
- Rotate regularly (recommend every 90 days)
- Don't hardcode in code
- Use environment variables or key management tools

**Fine-grained token vs Classic token**:
| Feature | Fine-grained token | Classic token |
|---------|-------------------|---------------|
| Permission scope | Fine-grained (specific repo, specific permissions) | Coarse-grained (all repos or specific repos) |
| Security | Higher | Lower |
| Recommended use | Production | Development/testing |

### 4. Review Login Activity

Regularly check account login activity, promptly handle anomalies.

**View Login Activity**:
1. **Settings** → **Security log**
2. View recent login events
3. Check for abnormal IP addresses or geographic locations

**Set Login Notifications**:
1. **Settings** → **Password and authentication**
2. Enable **Login activity notifications**
3. Select notification method (email, SMS)

---

## Repository Security

### 1. .gitignore Configuration

Ensuring sensitive information is not committed is the foundation of repository security.

**Common Sensitive Information Types**:
- API keys and tokens
- Database credentials
- Private key files
- Environment variable files
- Sensitive data in configuration files

**Complete .gitignore Template**:
```gitignore
# Environment variables
.env
.env.local
.env.*.local
.env.development
.env.production
.env.staging

# Key files
*.pem
*.key
*.p12
*.pfx
id_rsa
id_ed25519
id_dsa

# Configuration files
config.json
credentials.json
secrets.yml
application-local.yml

# Dependency directories
node_modules/
vendor/
venv/
__pycache__/

# Log files
*.log
logs/

# Operating system files
.DS_Store
Thumbs.db

# IDE configuration
.idea/
.vscode/
*.swp
*.swo

# Build artifacts
dist/
build/
target/
```

**Use Templates**:
```bash
# Download official template
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Or use GitHub API
gh api repos/github/gitignore/contents/Node.gitignore -q '.content' | base64 -d > .gitignore
```

### 2. Branch Protection

Branch protection rules can prevent accidental code changes and force pushes.

**Setup Steps**:
1. **Settings** → **Branches**
2. Click **Add rule**
3. Configure protection rules:
   - Require PR review
   - Require status checks to pass
   - Require branch to be up to date
   - Prohibit force push
   - Restrict push permissions

**Advanced Protection Configuration**:
```yaml
# .github/branch-protection.yml (requires GitHub App)
protection:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
    required_status_checks:
      strict: true
      contexts:
        - "ci/build"
        - "ci/test"
        - "security/scan"
    enforce_admins: true
    restrictions:
      users: ["admin-user"]
      teams: ["core-team"]
```

**Protection Rule Best Practices**:
- Set strict protection for `main` and `release` branches
- Require at least 2 code reviews
- Enable status checks (CI/CD, security scanning)
- Prohibit force push
- Regularly review protection rules

### 3. Code Owners (CODEOWNERS)

CODEOWNERS file defines code review responsibilities, ensuring every code change has appropriate reviewers.

**File Location**: `.github/CODEOWNERS` or `docs/CODEOWNERS`

**Example Configuration**:
```
# Default owners
* @team-leads

# Security related code
/security/ @security-team
*.security.* @security-team

# Frontend code
/src/frontend/ @frontend-team
*.js @frontend-team
*.ts @frontend-team
*.jsx @frontend-team
*.tsx @frontend-team

# Backend code
/src/backend/ @backend-team
*.py @backend-team
*.java @backend-team

# Configuration files
*.yml @devops-team
*.yaml @devops-team
Dockerfile @devops-team
docker-compose.yml @devops-team

# Documentation
*.md @docs-team
/docs/ @docs-team

# Dependency files
package.json @security-team
requirements.txt @security-team
```

**CODEOWNERS Best Practices**:
- Assign owners for every directory and file type
- Use teams instead of individuals as owners
- Regularly review and update owners
- Remind to review CODEOWNERS in PR templates

### 4. Secret Scanning

Secret Scanning can detect sensitive information leaked in code.

**Enable Steps**:
1. **Settings** → **Code security**
2. Enable **Secret scanning**
3. Enable **Push protection** (prevent pushing code containing sensitive information)

**Supported Key Types**:
- AWS access keys
- GitHub personal access tokens
- Azure DevOps tokens
- Slack webhook URLs
- Database connection strings
- Private key files

**Custom Patterns**:
```yaml
# .github/secret-scanning.yml
patterns:
  - name: "Internal API Key"
    pattern: "internal-api-[a-zA-Z0-9]{32}"
    alert: true
  - name: "Database Password"
    pattern: "db_password:\\s*[a-zA-Z0-9!@#$%^&*]{16,}"
    alert: true
```

**Handling Detected Keys**:
1. Immediately revoke leaked key
2. Generate new key
3. Update all services using that key
4. Check if other places use same key
5. Update .gitignore to prevent future leaks

### 5. Dependabot

Dependabot can automatically check and update project dependencies, fixing security vulnerabilities.

**Enable Steps**:
1. **Settings** → **Code security**
2. Enable **Dependabot alerts**
3. Enable **Dependabot security updates**
4. Configure automatic updates

**Configuration File**: `.github/dependabot.yml`
```yaml
version: 2
updates:
  # npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Asia/Shanghai"
    open-pull-requests-limit: 10
    reviewers:
      - "frontend-team"
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "deps"
      prefix-development: "deps-dev"
    
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    
  # Docker images
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Dependabot Best Practices**:
- Enable security updates
- Set reasonable update frequency
- Auto-merge minor and patch updates
- Regularly review update logs
- Test code after updates

---

## CI/CD Security

CI/CD pipelines are core of software development, but can also become sources of security vulnerabilities.

### 1. Use Secrets

Secrets are used to store sensitive information, such as API keys, passwords, etc.

**Using Secrets in GitHub Actions**:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: ./deploy.sh
```

**Secrets Types**:
- **Environment Secrets**: Environment-specific keys
- **Repository Secrets**: Repository-level keys
- **Organization Secrets**: Organization-level keys (can be shared across repos)

**Secrets Best Practices**:
- Use environment Secrets instead of repository Secrets
- Use different keys for different environments (dev, test, production)
- Rotate keys regularly
- Restrict Secrets access permissions
- Don't print Secrets in logs

**Prevent Secrets Leakage**:
```yaml
# Use masking to prevent leakage
- name: Use secret
  run: |
    echo "::add-mask::${{ secrets.MY_SECRET }}"
    # Command using key
```

### 2. Restrict Actions Permissions

Follow principle of least privilege, only grant necessary permissions.

**Permission Configuration**:
```yaml
# Workflow level permissions
permissions:
  contents: read
  pages: write
  id-token: write
  issues: write
  pull-requests: write

# Job level permissions
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh
```

**Permission Types**:
- `contents`: Repository content access
- `pages`: GitHub Pages deployment
- `id-token`: OIDC token
- `issues`: Issue management
- `pull-requests`: PR management
- `actions`: Actions management
- `packages`: Package management
- `security-events`: Security events

### 3. Verify Action Sources

When using third-party Actions, must verify their source and integrity.

**Verification Methods**:
```yaml
# Use full commit SHA (most secure)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

# Use tag (more secure, but may be tampered)
- uses: actions/checkout@v4

# Use branch (not recommended)
- uses: actions/checkout@main
```

**Verification Tools**:
```bash
# Use actionlint to check Action syntax
actionlint .github/workflows/*.yml

# Use zizmor to check security issues
zizmor .github/workflows/*.yml
```

### 4. Review Third-party Actions

Before using third-party Actions, must conduct security review.

**Review Checklist**:
- [ ] Check Action's source code
- [ ] View Action's permission requirements
- [ ] Verify Action's maintenance status
- [ ] Check for known vulnerabilities
- [ ] View community reviews and usage

**Review Steps**:
1. **View Source Code**:
   ```bash
   # Clone Action repository
   git clone https://github.com/action/checkout.git
   cd checkout
   
   # Check code
   grep -r "secrets\." .
   grep -r "env\." .
   ```

2. **Check Permission Requirements**:
   ```yaml
   # View action.yml
   name: 'Checkout'
   description: 'Checkout a Git repository'
   inputs:
     repository:
       description: 'Repository name'
       required: false
   ```

3. **Verify Maintenance Status**:
   - Check last update time
   - View Issue and PR count
   - Check version release frequency

### 5. Use Trusted Actions

**Official Actions**:
- `actions/checkout`: Code checkout
- `actions/setup-node`: Node.js setup
- `actions/setup-python`: Python setup
- `actions/cache`: Cache management
- `actions/upload-artifact`: Upload build artifacts

**Trusted Third-party Actions**:
- `docker/build-push-action`: Docker build
- `aws-actions/configure-aws-credentials`: AWS configuration
- `google-github-actions/setup-gcloud`: Google Cloud configuration

### 6. Security Scanning Integration

Integrate security scanning into CI/CD pipeline.

**Code Scanning**:
```yaml
- name: Run CodeQL Analysis
  uses: github/codeql-action/analyze@v3
  with:
    languages: javascript, python
    queries: security-extended
```

**Dependency Scanning**:
```yaml
- name: Run Dependency Review
  uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: high
    deny-licenses: GPL-3.0, AGPL-3.0
```

**Container Scanning**:
```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
```

**Secret Scanning**:
```yaml
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: ${{ github.event.repository.default_branch }}
```

---

## Dependency Security

Dependency security is an important part of software security, many security vulnerabilities come from third-party dependencies.

### 1. Regularly Update Dependencies

Regularly updating dependencies can fix known security vulnerabilities.

**npm Updates**:
```bash
# Update all dependencies
npm update

# Update specific package
npm update package-name

# Update to latest version (may contain breaking changes)
npm install package-name@latest

# Check outdated dependencies
npm outdated

# Use ncu to update package.json
npx npm-check-updates -u
```

**pip Updates**:
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade package-name

# Check outdated dependencies
pip list --outdated

# Use pip-review to update
pip install pip-review
pip-review --local --interactive
```

**composer Updates**:
```bash
# Update all dependencies
composer update

# Update specific package
composer update package-name

# Check outdated dependencies
composer outdated
```

**Automated Updates**:
Use Dependabot or Renovate to automatically update dependencies.

### 2. Use Lock Files

Lock files can ensure team members use the same versions of dependencies.

**Common Lock Files**:
- `package-lock.json` (npm)
- `yarn.lock` (yarn)
- `pnpm-lock.yaml` (pnpm)
- `composer.lock` (composer)
- `Pipfile.lock` (pipenv)
- `poetry.lock` (poetry)
- `Gemfile.lock` (bundler)

**Lock File Best Practices**:
- Commit lock files to version control
- Don't manually edit lock files
- Regularly update lock files
- Verify lock files in CI/CD

**Lock File Verification**:
```yaml
# Verify lock file in GitHub Actions
- name: Verify lock file
  run: |
    npm ci
    # Check for uncommitted changes
    git diff --exit-code package-lock.json
```

### 3. Scan Dependency Vulnerabilities

Use tools to scan dependencies for known vulnerabilities.

**npm Audit**:
```bash
# Run audit
npm audit

# Auto-fix vulnerabilities
npm audit fix

# Force fix (may contain breaking changes)
npm audit fix --force

# Only view high-risk vulnerabilities
npm audit --audit-level=high

# Generate audit report
npm audit --json > audit-report.json
```

**pip Audit**:
```bash
# Install pip-audit
pip install pip-audit

# Run audit
pip-audit

# Fix vulnerabilities
pip-audit --fix

# Generate report
pip-audit --format json > audit-report.json
```

**bundler Audit**:
```bash
# Install bundler-audit
gem install bundler-audit

# Update vulnerability database
bundler-audit update

# Run audit
bundler-audit check

# Run in CI/CD
bundler-audit check --ignore CVE-2023-XXXXX
```

**Comprehensive Audit Tools**:
```bash
# Use Snyk
npm install -g snyk
snyk test

# Use OWASP Dependency-Check
dependency-check --project "My Project" --scan ./src

# Use Trivy
trivy fs --security-checks vuln .
```

### 4. Use Dependency Whitelist

Only allow use of reviewed dependencies.

**npm Whitelist**:
```json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "express": "^4.18.2"
  },
  "overrides": {
    "minimatch": "^5.0.0"
  }
}
```

**pip Whitelist**:
```txt
# requirements.txt
# Only allow specific versions
package==1.2.3
another-package>=2.0.0,<3.0.0
```

**Dependency Review**:
```yaml
# Review dependencies in GitHub Actions
- name: Review dependency changes
  uses: actions/dependency-review-action@v4
  with:
    fail-on-severity: high
    deny-licenses: GPL-3.0, AGPL-3.0
    config-file: ./.github/dependency-review.yml
```

### 5. Monitor Security Advisories

Timely understand security vulnerabilities in dependencies.

**Security Advisory Sources**:
- [GitHub Advisory Database](https://github.com/advisories)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [Snyk Vulnerability Database](https://snyk.io/vuln/)
- [npm Security Advisories](https://www.npmjs.com/advisories)
- [PyPI Security Advisories](https://pypi.org/security/)

**Automated Monitoring**:
```yaml
# Monitor using Dependabot
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    security-updates-only: true
```

### 6. Dependency Security Best Practices

**Choosing Dependencies**:
- Choose actively maintained projects
- Check project's Issues and PRs
- View project's contributor count
- Check project's license
- Avoid deprecated projects

**Managing Dependencies**:
- Regularly review dependencies
- Remove unused dependencies
- Use dependency analysis tools
- Establish dependency review process

**Security Configuration**:
```json
// package.json
{
  "scripts": {
    "audit": "npm audit",
    "audit:fix": "npm audit fix",
    "outdated": "npm outdated",
    "update": "npm update"
  }
}
```

---

## Team Security

Team security is ensuring entire team follows security best practices.

### 1. Principle of Least Privilege

Only grant minimum permissions necessary to complete work.

**Permission Management**:
- Define different permission levels for different roles
- Regularly review permissions (recommend quarterly)
- Timely remove permissions no longer needed
- Use teams instead of individual permissions

**GitHub Permission Levels**:
- **Read**: Read-only access
- **Triage**: Issue and PR management
- **Write**: Code push and branch management
- **Maintain**: Repository management (excluding dangerous operations)
- **Admin**: Full management permissions

**Permission Review Process**:
```bash
# View team permissions using GitHub CLI
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'

# View team members
gh api orgs/{org}/teams/{team}/members --jq '.[].login'

# Audit permissions
gh api repos/{owner}/{repo}/collaborators --jq '.[] | {login, permissions}'
```

### 2. Security Training

Regularly conduct security training to improve team security awareness.

**Training Content**:
- Secure coding practices
- Common security vulnerabilities (OWASP Top 10)
- Key management
- Social engineering prevention
- Security incident response

**Training Resources**:
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Snyk Learn](https://learn.snyk.io/)
- [Secure Code Warrior](https://www.securecodewarrior.com/)

**Training Plan**:
- New employee onboarding training
- Quarterly security training
- Annual security awareness test
- Post-incident review training

### 3. Code Review

Code review is an important means of discovering security vulnerabilities.

**Security Review Checklist**:
- [ ] Input validation
- [ ] Output encoding
- [ ] Authentication and authorization
- [ ] Key and sensitive information handling
- [ ] Error handling
- [ ] Logging
- [ ] Dependency security
- [ ] Configuration security

**Security Review Tools**:
```bash
# Use ESLint security plugin
npm install eslint-plugin-security

# Use Semgrep
semgrep --config=auto .

# Use Bandit (Python)
pip install bandit
bandit -r src/

# Use SonarQube
sonar-scanner -Dsonar.projectKey=my-project
```

**Security Review Process**:
1. Developer submits code
2. Automated security scanning
3. Manual security review
4. Fix security issues
5. Review again
6. Merge code

### 4. Security Policy

Establish clear security policies and processes.

**Security Policy Content**:
- Password policy
- Access control policy
- Data protection policy
- Incident response policy
- Compliance requirements

**Security Policy Template**:
```markdown
# Security Policy

## Report Security Vulnerabilities

If you discover a security vulnerability, please report through:
- Email: security@example.com
- GitHub Security Advisories

## Supported Versions

| Version | Support Status |
|---------|----------------|
| 2.x | ✅ Supported |
| 1.x | ❌ Not Supported |

## Security Updates

We will release updates as soon as possible after discovering security vulnerabilities.
```

### 5. Security Tool Integration

Integrate security tools into development process.

**IDE Security Plugins**:
- VS Code: Security Scanner, SonarLint
- IntelliJ: SonarLint, Find Security Bugs

**CI/CD Security Tools**:
```yaml
# Code scanning
- name: Run CodeQL
  uses: github/codeql-action/analyze@v3

# Dependency scanning
- name: Run Dependency Review
  uses: actions/dependency-review-action@v4

# Secret scanning
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main

# Container scanning
- name: Run Trivy
  uses: aquasecurity/trivy-action@master
```

---

## Security Incident Response

Even with all precautions, security incidents may still occur. Establishing effective incident response mechanisms is crucial.

### 1. Incident Response Plan

**Response Team**:
- Security lead
- Development lead
- Operations lead
- Legal counsel
- PR lead

**Response Process**:
1. **Detection**: Discover security incident
2. **Assessment**: Assess incident severity
3. **Containment**: Limit incident impact scope
4. **Remediation**: Fix security vulnerability
5. **Recovery**: Restore normal service
6. **Review**: Summarize lessons learned

### 2. Incident Classification

**Severity**:
- **P0 (Critical)**: Data breach, service interruption
- **P1 (High)**: Unauthorized access, privilege escalation
- **P2 (Medium)**: Information disclosure, denial of service
- **P3 (Low)**: Security configuration issues, weak passwords

**Response Time**:
- P0: Immediate response (within 15 minutes)
- P1: Response within 1 hour
- P2: Response within 24 hours
- P3: Response within 7 days

### 3. Incident Response Template

```markdown
# Security Incident Response Report

## Incident Overview
- **Incident ID**: INC-2024-001
- **Discovery Time**: 2024-01-15 10:30 UTC
- **Reporter**: John Doe
- **Severity**: P1

## Incident Description
[Detailed incident description]

## Impact Scope
- Affected systems: [System list]
- Affected users: [User count]
- Data breach: [Yes/No]

## Response Measures
1. [Measure 1]
2. [Measure 2]
3. [Measure 3]

## Root Cause
[Root cause analysis]

## Improvement Measures
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

## Timeline
- 10:30: Incident discovered
- 10:45: Response process initiated
- 11:00: Incident contained
- 12:00: Vulnerability fixed
- 13:00: Service restored
```

### 4. Incident Response Tools

**Monitoring Tools**:
- GitHub Security Alerts
- GitHub Audit Log
- GitHub Advanced Security

**Response Tools**:
- GitHub Security Advisories
- GitHub Incident Response
- GitHub Status Page

**Communication Tools**:
- Slack/Teams security channels
- Email lists
- Phone conferences

---

## Security Checklist

### Account Security
- [ ] Enable two-factor authentication
- [ ] Use SSH keys
- [ ] Configure personal access tokens
- [ ] Regularly review login activity

### Repository Security
- [ ] Configure .gitignore
- [ ] Set branch protection
- [ ] Enable Secret Scanning
- [ ] Enable Dependabot
- [ ] Configure CODEOWNERS

### CI/CD Security
- [ ] Use Secrets
- [ ] Restrict Actions permissions
- [ ] Verify Action sources
- [ ] Review third-party Actions

### Dependency Security
- [ ] Regularly update dependencies
- [ ] Use lock files
- [ ] Scan dependency vulnerabilities
- [ ] Monitor security advisories

---

## Related Resources

- [GitHub Security Documentation](https://docs.github.com/en/security)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
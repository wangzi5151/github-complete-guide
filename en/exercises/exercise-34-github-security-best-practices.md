# Exercise 34: GitHub Security Best Practices

## Objectives

Learn how to implement security best practices in GitHub projects to protect code and data.

## Prerequisites

- A GitHub account
- A test repository
- Familiarity with basic Git operations

## Steps

### 1. Enable Two-Factor Authentication

Two-factor authentication is the first line of defense for protecting your account.

**Steps to enable**:

1. Visit [GitHub Settings](https://github.com/settings/security)
2. Click "Enable two-factor authentication"
3. Choose a verification method:
   - Authenticator app (recommended)
   - SMS
   - Security key

**Recommended apps**:
- Google Authenticator
- Authy
- 1Password

### 2. Use SSH Keys

SSH keys are more secure than passwords and don't require entering a password each time.

**Generate an SSH key**:

```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your@email.com"

# Generate RSA key
ssh-keygen -t rsa -b 4096 -C "your@email.com"
```

**Add SSH key to GitHub**:

```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard  # Linux

# Add on GitHub:
# Settings → SSH and GPG keys → New SSH key
```

**Test SSH connection**:

```bash
ssh -T git@github.com
```

### 3. Use Personal Access Tokens

Personal Access Tokens are used to replace passwords for API authentication.

**Create a Token**:

1. Visit [GitHub Settings](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select permission scopes
4. Set an expiration time
5. Click "Generate token"

**Use the Token**:

```bash
# Clone a repository using a token
git clone https://YOUR_TOKEN@github.com/owner/repo.git

# Configure Git to use a token
git config --global credential.helper store
echo "https://YOUR_TOKEN@github.com" > ~/.git-credentials
```

### 4. Configure .gitignore

Ensure sensitive information is not committed to the repository.

**Common .gitignore configuration**:

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Key files
*.pem
*.key
id_rsa
id_ed25519

# Configuration files
config.json
credentials.json
secrets.yml

# Dependency directories
node_modules/
vendor/
venv/

# Log files
*.log
logs/

# OS files
.DS_Store
Thumbs.db

# IDE configuration
.idea/
.vscode/
*.swp
```

### 5. Enable Secret Scanning

Secret Scanning can detect sensitive information leaked in code.

**Steps to enable**:

1. Visit repository settings
2. Click "Code security"
3. Enable "Secret scanning"
4. Enable "Push protection"

**Test Secret Scanning**:

```bash
# Create a file containing sensitive information
echo "API_KEY=1234567890abcdef" > .env

# Commit and push
git add .env
git commit -m "Add .env file"
git push

# GitHub will detect sensitive information and block the push
```

### 6. Enable Dependabot

Dependabot can automatically check and update project dependencies.

**Steps to enable**:

1. Visit repository settings
2. Click "Code security"
3. Enable "Dependabot alerts"
4. Enable "Dependabot security updates"

**Configure Dependabot**:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### 7. Configure Branch Protection

Branch protection rules can prevent accidental code changes.

**Configuration steps**:

1. Visit repository settings
2. Click "Branches"
3. Click "Add rule"
4. Configure protection rules

**Recommended configuration**:

```yaml
# Branch protection rules
required_pull_request_reviews:
  required_approving_review_count: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

required_status_checks:
  strict: true
  contexts:
    - "ci/build"
    - "ci/test"

enforce_admins: true

restrictions:
  users: ["admin-user"]
  teams: ["core-team"]
```

### 8. Configure CODEOWNERS

The CODEOWNERS file defines the responsible persons for code review.

**Create the CODEOWNERS file**:

```bash
# Create .github/CODEOWNERS file
cat > .github/CODEOWNERS << EOF
# Default owners
* @team-leads

# Security-related code
/security/ @security-team

# Frontend code
/src/frontend/ @frontend-team

# Backend code
/src/backend/ @backend-team

# Configuration files
*.yml @devops-team
Dockerfile @devops-team
EOF
```

### 9. Use GitHub Advanced Security

GitHub Advanced Security provides more advanced security features.

**Features include**:
- Code Scanning
- Secret Scanning
- Dependency Review
- Security Overview

**Enable Code Scanning**:

```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

### 10. Security Auditing

Conduct regular security audits to discover and fix security vulnerabilities.

**Security audit checklist**:

```markdown
# Security Audit Checklist

## Account Security
- [ ] Enable two-factor authentication
- [ ] Use SSH keys
- [ ] Configure Personal Access Tokens
- [ ] Regularly review login activity

## Repository Security
- [ ] Configure .gitignore
- [ ] Enable Secret Scanning
- [ ] Enable Dependabot
- [ ] Configure branch protection
- [ ] Configure CODEOWNERS

## CI/CD Security
- [ ] Use Secrets
- [ ] Restrict Actions permissions
- [ ] Verify Action sources
- [ ] Review third-party Actions

## Dependency Security
- [ ] Regularly update dependencies
- [ ] Use lock files
- [ ] Scan for dependency vulnerabilities
- [ ] Monitor security advisories
```

**Use GitHub CLI for security auditing**:

```bash
# Check repository security configuration
gh api repos/{owner}/{repo} --jq '.security_and_analysis'

# Check Secret Scanning status
gh api repos/{owner}/{repo}/secret-scanning/alerts

# Check Dependabot alerts
gh api repos/{owner}/{repo}/vulnerability-alerts

# Check branch protection rules
gh api repos/{owner}/{repo}/branches/main/protection
```

## Challenges

1. **Challenge 1**: Configure complete security settings for your repository
2. **Challenge 2**: Create a security audit script
3. **Challenge 3**: Configure GitHub Advanced Security
4. **Challenge 4**: Create an automated security scanning workflow
5. **Challenge 5**: Develop a security incident response plan

## Reflection

1. Why is security important in software development?
2. How do you balance security and development efficiency?
3. How do you handle security vulnerabilities?
4. How do you train team members on security awareness?

## Related Resources

- [GitHub Security Documentation](https://docs.github.com/en/code-security)
- [GitHub Advanced Security Documentation](https://docs.github.com/en/code-security/advanced-security)
- [GitHub Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)
- [GitHub Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-a-branch-protection-rule)

---

**Previous: [Exercise 33: GitHub API Integration](exercise-33-github-api-integration.md) | Next: [Exercise 35: GitHub Team Collaboration](exercise-35-github-team-collaboration.md)**

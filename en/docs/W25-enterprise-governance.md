# GitHub Enterprise Governance

## Governance Framework

### Governance Levels

```
Organization-level Governance
├── Policy Management
├── Permission Management
├── Security Management
└── Compliance Management

Repository-level Governance
├── Branch Strategy
├── Code Review
├── Access Control
└── Automation

Team-level Governance
├── Collaboration Standards
├── Communication Mechanism
└── Knowledge Management
```

## Policy Management

### Organization Policies

```yaml
# Organization policy document
Organization Policy:
  Code Management:
    - Use Conventional Commits specification
    - PR must pass code review
    - Must pass CI check before merge
  
  Security Management:
    - All repositories must enable Dependabot
    - Must enable Secret Scanning
    - Production branches must enable branch protection
  
  Release Management:
    - Use semantic versioning
    - Release must pass approval
    - Auto-generate Release Notes
```

### Repository Templates

```yaml
# Repository initialization template
Template Content:
  README.md: Basic template
  CONTRIBUTING.md: Contributing guide
  CODE_OF_CONDUCT.md: Code of conduct
  .github/
    ISSUE_TEMPLATE/: Issue templates
    PULL_REQUEST_TEMPLATE.md: PR template
    CODEOWNERS: Code owners
    dependabot.yml: Dependabot configuration
    workflows/: Workflow templates
```

## Permission Management

### Permission Matrix

| Role | Repository | Branch | Issue | PR | Actions |
|------|-----------|--------|-------|-----|---------|
| Owner | Full control | Full control | Full control | Full control | Full control |
| Admin | Full control | Full control | Full control | Full control | Full control |
| Write | Read/Write | Read/Write | Read/Write | Read/Write | Read/Write |
| Triage | Read | Read | Manage | Manage | Read |
| Read | Read | Read | Read | Read | Read |

### CODEOWNERS

```yaml
# CODEOWNERS
# Default owners
* @your-org/core-team

# Frontend code
/src/components/ @your-org/frontend-team
/src/pages/ @your-org/frontend-team

# Backend code
/src/api/ @your-org/backend-team
/src/services/ @your-org/backend-team

# Infrastructure
/terraform/ @your-org/devops-team
/.github/ @your-org/devops-team

# Documentation
/docs/ @your-org/docs-team

# Security related
/src/security/ @your-org/security-team
```

### Branch Protection

```json
// Organization-level branch protection rules
{
  "rules": [
    {
      "pattern": "main",
      "protections": {
        "required_pull_request_reviews": {
          "required_approving_review_count": 2,
          "dismiss_stale_reviews": true,
          "require_code_owner_reviews": true
        },
        "required_status_checks": {
          "strict": true,
          "contexts": ["ci/test", "ci/lint"]
        },
        "enforce_admins": true,
        "restrictions": null
      }
    }
  ]
}
```

## Security Management

### Security Policy

```markdown
# SECURITY.md

## Security Policy

### Supported Versions

| Version | Support Status |
|---------|----------------|
| 5.0.x | ✅ Fully supported |
| 4.0.x | ✅ Security updates |
| < 4.0 | ❌ No longer supported |

### Report Vulnerabilities

Please report security vulnerabilities through:

1. Do **NOT** report publicly
2. Send email to security@your-domain.com
3. Use GitHub Security Advisory

### Response Time

- Critical vulnerabilities: Response within 24 hours
- High vulnerabilities: Response within 72 hours
- Medium vulnerabilities: Response within 1 week
- Low vulnerabilities: Response within 2 weeks
```

### Secret Scanning

```yaml
# Enable Secret Scanning Push Protection
gh api repos/{org}/{repo}/secret-scanning/push-protection \
  --method PUT \
  -f status='enabled'
```

### Dependency Review

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review

on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Dependency Review
      uses: actions/dependency-review-action@v4
      with:
        fail-on-severity: high
        deny-licenses: GPL-3.0, AGPL-3.0
```

## Compliance Management

### Audit Logs

```bash
# View audit logs
gh api orgs/{org}/audit-log \
  --method GET \
  -f phrase='action:repo.create' \
  -f created='>=2024-01-01'

# Export audit logs
gh api orgs/{org}/audit-log \
  --method GET \
  -f phrase='created:>=2024-01-01' \
  -q '.[] | @json' > audit-log.json
```

### Compliance Checks

```yaml
# .github/workflows/compliance.yml
name: Compliance Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
    - name: Check branch protection
      run: |
        gh api repos/{org}/{repo}/branches/main/protection
    
    - name: Check security features
      run: |
        gh api repos/{org}/{repo}/vulnerability-alerts
        gh api repos/{org}/{repo}/secret-scanning/alerts
    
    - name: Check CODEOWNERS
      run: |
        if [ ! -f .github/CODEOWNERS ]; then
          echo "Missing CODEOWNERS file"
          exit 1
        fi
```

## Knowledge Management

### Documentation Structure

```yaml
Documentation Management:
  README.md: Project introduction
  CONTRIBUTING.md: Contributing guide
  CODE_OF_CONDUCT.md: Code of conduct
  SECURITY.md: Security policy
  CHANGELOG.md: Changelog
  docs/: Detailed documentation
    architecture/: Architecture docs
    api/: API documentation
    guides/: Guides
    troubleshooting/: Troubleshooting
```

### Knowledge Base

```markdown
# Knowledge Base Structure

## Development Guide
- Coding standards
- Architecture design
- Best practices

## Operations Guide
- Deployment process
- Monitoring alerts
- Troubleshooting

## Security Guide
- Security policy
- Vulnerability handling
- Compliance requirements
```

## Metrics and Measurement

### Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| PR Review Time | < 24 hours | Time from PR submission to merge |
| CI Pass Rate | > 95% | Proportion of CI checks passed |
| Security Vulnerability Fix Time | < 7 days | Time from discovery to fix |
| Documentation Coverage | > 80% | Proportion of APIs with documentation |
| Test Coverage | > 70% | Code test coverage |

### Measurement Tools

```yaml
# .github/workflows/metrics.yml
name: Metrics Collection

on:
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
    - name: Collect metrics
      run: |
        # Collect PR metrics
        gh api repos/{org}/{repo}/pulls?state=closed \
          --jq '.[] | {created_at: .created_at, merged_at: .merged_at}'
        
        # Collect Issue metrics
        gh api repos/{org}/{repo}/issues?state=closed \
          --jq '.[] | {created_at: .created_at, closed_at: .closed_at}'
```

## Best Practices

1. **Establish Clear Policies**: Formulate clear governance strategies
2. **Automate Governance**: Use tools to automate governance processes
3. **Regular Review**: Regularly review and update policies
4. **Train Team**: Ensure team understands and follows policies
5. **Continuous Improvement**: Continuously improve governance based on feedback

## Related Resources

- [GitHub Organization Management](https://docs.github.com/en/organizations)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [GitHub Audit Logs](https://docs.github.com/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization)
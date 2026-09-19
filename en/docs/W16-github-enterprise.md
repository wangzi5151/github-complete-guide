# GitHub Enterprise Features

> This chapter provides a detailed introduction to GitHub Enterprise's enterprise-level features, including version comparison, SAML SSO configuration, audit logs, IP allow lists, compliance and governance, security features, administration APIs, and best practices.

---

## Table of Contents

1. [Enterprise Version Comparison](#enterprise-version-comparison)
2. [SAML SSO Configuration](#saml-sso-configuration)
3. [Audit Logs](#audit-logs)
4. [IP Allow List](#ip-allow-list)
5. [Compliance and Governance](#compliance-and-governance)
6. [Security Features](#security-features)
7. [Administration API](#administration-api)
8. [Enterprise Deployment](#enterprise-deployment)
9. [Cost Optimization](#cost-optimization)
10. [Best Practices](#best-practices)
11. [Related Resources](#related-resources)

---

## Enterprise Version Comparison

GitHub offers three main versions to meet the needs of teams of different sizes.

### Version Feature Comparison

| Feature | Free | Team ($4/month) | Enterprise ($21/month) |
|------|------|--------------|---------------------|
| Repositories | Unlimited | Unlimited | Unlimited |
| Collaborators | Unlimited | Unlimited | Unlimited |
| GitHub Pages | ✅ | ✅ | ✅ |
| GitHub Actions | 2000 minutes/month | 3000 minutes/month | 50000 minutes/month |
| Storage Limit | 1GB | 2GB | 50GB |
| SAML SSO | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ✅ |
| IP Allow List | ❌ | ❌ | ✅ |
| Advanced Security | ❌ | ❌ | ✅ |
| Support | Community | Priority Support | 24/7 Support |
| SLA | ❌ | ❌ | 99.9% |

### Choosing the Right Version

**Free version is suitable for**:
- Individual developers
- Open source projects
- Small teams (<10 people)
- Learning and experimentation

**Team version is suitable for**:
- Small to medium teams (10-50 people)
- Need priority support
- Need more Actions minutes
- Need code review features

**Enterprise version is suitable for**:
- Large enterprises (>50 people)
- Need SSO/SAML
- Need audit logs
- Need compliance support
- Need advanced security features

### Cost Calculation

**Actions minutes cost**:
```
Free: 2000 minutes/month (free)
Team: 3000 minutes/month ($4/user/month)
Enterprise: 50000 minutes/month ($21/user/month)

Additional minutes: $0.008/minute
```

**Storage cost**:
```
Free: 1GB (free)
Team: 2GB ($4/user/month)
Enterprise: 50GB ($21/user/month)

Additional storage: $0.008/MB/month
```

**Example calculation**:
```
Team size: 100 people
Actions minutes: 100,000 minutes/month
Storage requirement: 100GB

Enterprise cost:
- Base fee: 100 × $21 = $2,100/month
- Additional minutes: (100,000 - 50,000) × $0.008 = $400/month
- Additional storage: (100GB - 50GB) × $0.008 × 1024 = $409.6/month
- Total: $2,100 + $400 + $409.6 = $2,909.6/month
```

## SAML SSO Configuration

SAML SSO (Security Assertion Markup Language Single Sign-On) allows enterprises to use their existing identity providers (IdP) to manage GitHub access.

### Configuring SAML

**Manual configuration steps**:
1. **Settings** → **Authentication security** → **SAML single sign-on**
2. Configure the following information:
   - **Sign on URL**: The login URL of the identity provider
   - **Issuer**: The entity ID of the identity provider
   - **Public certificate**: Upload the public certificate of the identity provider
   - **Signature method**: Select the signature algorithm (SHA-256 recommended)
   - **Digest method**: Select the digest algorithm (SHA-256 recommended)

**Supported identity providers**:
- Azure Active Directory
- Okta
- OneLogin
- PingIdentity
- Google Workspace
- LDAP (via SAML bridge)

### Automatic Configuration with SCIM

SCIM (System for Cross-domain Identity Management) can automatically synchronize user and team information.

**Using GitHub CLI to configure**:
```bash
# Configure SAML SSO
gh api orgs/{org}/identity-provider \
  --method PUT \
  -f type='saml' \
  -f sso_url='https://your-idp.com/saml/sso' \
  -f issuer='your-entity-id' \
  -f certificate='-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----'

# Configure SCIM
gh api orgs/{org}/scim/v2 \
  --method PUT \
  -f scim_url='https://your-idp.com/scim/v2' \
  -f token='your-scim-token'
```

**SCIM features**:
- Automatically create user accounts
- Automatically disable user accounts
- Automatically synchronize team members
- Automatically update user information
- Support group mapping

### SAML SSO Best Practices

**Security configuration**:
- Use strong encryption algorithms (SHA-256)
- Regularly rotate certificates
- Enable two-factor authentication
- Limit SSO administrator permissions

**User management**:
- Use SCIM for automatic synchronization
- Regularly review user permissions
- Promptly disable accounts of departed employees
- Use teams to manage permissions

**Troubleshooting**:
```bash
# Test SAML configuration
gh api orgs/{org}/identity-provider

# View SAML events
gh api orgs/{org}/audit-log --jq '.[] | select(.action | startswith("saml"))'

# Reset SAML configuration
gh api orgs/{org}/identity-provider --method DELETE
```

### SAML SSO Integration Examples

**Azure Active Directory integration**:
```yaml
# Azure AD application configuration
Application ID: your-app-id
Entity ID: https://github.com/orgs/your-org
Reply URL: https://github.com/orgs/your-org/saml/consume
Sign on URL: https://github.com/login
```

**Okta integration**:
```yaml
# Okta application configuration
Single sign-on URL: https://github.com/orgs/your-org/saml/consume
Audience URI: https://github.com/orgs/your-org
Name ID format: emailAddress
Application username: Email
```

## Audit Logs

Audit logs record all important operations in an organization, used for security monitoring and compliance checks.

### Accessing Audit Logs

**Using GitHub CLI**:
```bash
# Get all audit logs
gh api orgs/{org}/audit-log

# Filter by event type
gh api orgs/{org}/audit-log \
  --method GET \
  -f phrase='action:repo.create' \
  -f created='>=2024-01-01'

# Filter by user
gh api orgs/{org}/audit-log \
  --method GET \
  -f phrase='actor:username'

# Filter by repository
gh api orgs/{org}/audit-log \
  --method GET \
  -f phrase='repo:org/repo'
```

**Using API**:
```bash
# Using curl
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/orgs/{org}/audit-log?phrase=action:repo.create"

# Using pagination
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/orgs/{org}/audit-log?per_page=100&page=1"
```

**Using the Web interface**:
1. Go to organization settings
2. Click **Audit log**
3. Use filters to search for events

### Audit Log Event Types

**Repository events**:
| Event | Description |
|------|------|
| `repo.create` | Create repository |
| `repo.destroy` | Delete repository |
| `repo.rename` | Rename repository |
| `repo.transfer` | Transfer repository ownership |
| `repo.visibility_change` | Change repository visibility |
| `repo.archived` | Archive repository |
| `repo.unarchived` | Unarchive repository |

**Member events**:
| Event | Description |
|------|------|
| `org.invite_member` | Invite member |
| `org.remove_member` | Remove member |
| `member.role_change` | Change member role |
| `member.invite` | Invite member |
| `member.remove` | Remove member |

**Team events**:
| Event | Description |
|------|------|
| `team.create` | Create team |
| `team.destroy` | Delete team |
| `team.rename` | Rename team |
| `team.member_add` | Add team member |
| `team.member_remove` | Remove team member |

**Security events**:
| Event | Description |
|------|------|
| `protected_branch.create` | Create protected branch |
| `protected_branch.destroy` | Delete protected branch |
| `protected_branch.update_config` | Update protected branch configuration |
| `secret_scanning_alert.create` | Create secret scanning alert |
| `dependabot_alert.create` | Create Dependabot alert |

### Exporting Audit Logs

**Using GitHub Actions for automatic export**:
```yaml
# .github/workflows/audit-export.yml
name: Export Audit Log

on:
  schedule:
    - cron: '0 0 * * *'  # Execute daily
  workflow_dispatch:  # Manual trigger

jobs:
  export:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Export audit log
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        # Export today's audit log
        gh api orgs/{org}/audit-log \
          --method GET \
          -f phrase='created:>=2024-01-01' \
          -q '.[] | @json' > audit-log-$(date +%Y%m%d).json
        
        # Compress the file
        gzip audit-log-$(date +%Y%m%d).json

    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: audit-log
        path: audit-log-*.json.gz
```

**Using Python script to export**:
```python
#!/usr/bin/env python3
import requests
import json
import gzip
from datetime import datetime, timedelta

# Configuration
ORG = "your-org"
TOKEN = "your-token"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def export_audit_log(start_date, end_date):
    """Export audit log"""
    url = f"https://api.github.com/orgs/{ORG}/audit-log"
    params = {
        "phrase": f"created:{start_date}..{end_date}",
        "per_page": 100
    }
    
    all_events = []
    page = 1
    
    while True:
        params["page"] = page
        response = requests.get(url, headers=HEADERS, params=params)
        events = response.json()
        
        if not events:
            break
            
        all_events.extend(events)
        page += 1
    
    # Save to file
    filename = f"audit-log-{start_date}-{end_date}.json.gz"
    with gzip.open(filename, 'wt', encoding='utf-8') as f:
        json.dump(all_events, f, indent=2)
    
    print(f"Exported {len(all_events)} events to {filename}")
    return all_events

if __name__ == "__main__":
    # Export logs from the last 30 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    export_audit_log(start_date, end_date)
```

### Audit Log Analysis

**Using jq for analysis**:
```bash
# Count event types
gh api orgs/{org}/audit-log --jq '.[] | .action' | sort | uniq -c | sort -rn

# Count active users
gh api orgs/{org}/audit-log --jq '.[] | .actor.login' | sort | uniq -c | sort -rn

# Find failed events
gh api orgs/{org}/audit-log --jq '.[] | select(.status == "failed")'

# Export as CSV
gh api orgs/{org}/audit-log --jq '.[] | [.created_at, .action, .actor.login, .repo.name] | @csv'
```

**Using Python for analysis**:
```python
import json
import pandas as pd
from collections import Counter

def analyze_audit_log(filename):
    """Analyze audit log"""
    with open(filename, 'r') as f:
        events = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(events)
    
    # Count event types
    event_counts = df['action'].value_counts()
    print("Event type statistics:")
    print(event_counts.head(10))
    
    # Count active users
    user_counts = df['actor'].apply(lambda x: x['login']).value_counts()
    print("\nActive user statistics:")
    print(user_counts.head(10))
    
    # Count time distribution
    df['created_at'] = pd.to_datetime(df['created_at'])
    daily_counts = df.groupby(df['created_at'].dt.date).size()
    print("\nDaily event statistics:")
    print(daily_counts.tail(7))
    
    return df
```

### Audit Log Best Practices

**Storage strategy**:
- Retain audit logs for at least 180 days
- Regularly archive old logs
- Use compressed storage to save space
- Establish log indexes for easy querying

**Monitoring strategy**:
- Set up alerts for critical events
- Monitor abnormal activity patterns
- Regularly review security events
- Establish incident response procedures

**Compliance requirements**:
- Meet GDPR requirements
- Meet SOC 2 requirements
- Meet HIPAA requirements (where applicable)
- Regularly conduct compliance audits

## IP Allow List

IP allow lists can restrict access to organization resources to specific IP addresses.

### Configuring IP Allow Lists

**Manual configuration steps**:
1. **Settings** → **Authentication security** → **IP allow list**
2. Add IP addresses or CIDR ranges
3. Enable **Enable IP allow list**

**Supported IP formats**:
- Single IP address: `192.168.1.1`
- CIDR range: `192.168.1.0/24`
- IPv6 address: `2001:db8::1`
- IPv6 range: `2001:db8::/32`

**Common configuration examples**:
```
# Office network
192.168.1.0/24
10.0.0.0/8

# VPN network
172.16.0.0/12

# Cloud service IPs
52.167.144.0/20  # Azure
35.180.0.0/16    # AWS
```

### API Configuration

**Using GitHub CLI**:
```bash
# Enable IP allow list
gh api orgs/{org}/actions/allowed-actions \
  --method PUT \
  -f enabled_all=true

# Only allow verified Actions
gh api orgs/{org}/actions/allowed-actions \
  --method PUT \
  -f enabled_verified_only=true

# Add IP to allow list
gh api orgs/{org}/ip-allowlist \
  --method POST \
  -f ip="192.168.1.0/24" \
  -f name="Office Network"

# Remove IP from allow list
gh api orgs/{org}/ip-allowlist/{id} \
  --method DELETE
```

**Using API for batch management**:
```python
import requests

def manage_ip_allowlist(org, token, action, ips):
    """Manage IP allow list"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    for ip in ips:
        if action == "add":
            url = f"https://api.github.com/orgs/{org}/ip-allowlist"
            data = {"ip": ip, "name": f"Auto-added {ip}"}
            response = requests.post(url, headers=headers, json=data)
        elif action == "remove":
            # First get the ID
            url = f"https://api.github.com/orgs/{org}/ip-allowlist"
            response = requests.get(url, headers=headers)
            for item in response.json():
                if item["ip"] == ip:
                    delete_url = f"{url}/{item['id']}"
                    requests.delete(delete_url, headers=headers)
        
        print(f"{action}: {ip} - {response.status_code}")

# Usage example
ips = ["192.168.1.0/24", "10.0.0.0/8"]
manage_ip_allowlist("your-org", "your-token", "add", ips)
```

### IP Allow List Best Practices

**Security recommendations**:
- Only allow necessary IP ranges
- Regularly review and update the IP list
- Use VPN to centrally manage access
- Monitor abnormal access attempts

**Organizational network architecture**:
```
┌─────────────────────────────────────────┐
│           Enterprise Network Architecture│
├─────────────────────────────────────────┤
│  Office Network (192.168.1.0/24)        │
│    ├── Development Team                 │
│    ├── Testing Team                     │
│    └── Management Team                  │
├─────────────────────────────────────────┤
│  VPN Network (172.16.0.0/12)            │
│    ├── Remote Work                      │
│    └── External Partners                │
├─────────────────────────────────────────┤
│  Cloud Service Network                  │
│    ├── AWS (52.167.144.0/20)            │
│    ├── Azure (35.180.0.0/16)           │
│    └── GCP (35.190.0.0/16)             │
└─────────────────────────────────────────┘
```

## Compliance and Governance

Compliance and governance features help enterprises meet regulatory requirements and internal policies.

### Configuring Branch Protection

**Organization-level branch protection**:
```yaml
# Using Rulesets (recommended)
gh api orgs/{org}/rulesets \
  --method POST \
  -f name='Production Branch Protection' \
  -f target='branch' \
  -f enforcement='active' \
  -f conditions='{"ref_name":{"include":["refs/heads/main"],"exclude":[]}}' \
  -f rules='[
    {"type":"pull_request","parameters":{"required_approving_review_count":2}},
    {"type":"required_status_checks","parameters":{"required_status_checks":[{"context":"ci/test"}]}},
    {"type":"non_fast_forward"}
  ]'
```

**Repository-level branch protection**:
```yaml
# Using Branch Protection Rules
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci/test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":2,"dismiss_stale_reviews":true}' \
  -f restrictions='{"users":["admin-user"],"teams":["core-team"]}'
```

### Code Owners

**CODEOWNERS file configuration**:
```yaml
# .github/CODEOWNERS

# Default owners
* @your-org/core-team

# Documentation team
/docs/ @your-org/docs-team
*.md @your-org/docs-team

# Security team
/src/security/ @your-org/security-team
/security/ @your-org/security-team

# DevOps team
/.github/ @your-org/devops-team
Dockerfile @your-org/devops-team
docker-compose.yml @your-org/devops-team
*.yml @your-org/devops-team

# Frontend team
/src/frontend/ @your-org/frontend-team
*.js @your-org/frontend-team
*.ts @your-org/frontend-team
*.jsx @your-org/frontend-team
*.tsx @your-org/frontend-team

# Backend team
/src/backend/ @your-org/backend-team
*.py @your-org/backend-team
*.java @your-org/backend-team
```

### Compliance Checks

**Automated compliance checks**:
```yaml
# .github/workflows/compliance-check.yml
name: Compliance Check

on:
  pull_request:
    branches: [main]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
    - name: Check branch protection
      run: |
        # Check branch protection rules
        gh api repos/{owner}/{repo}/branches/main/protection
        
    - name: Check CODEOWNERS
      run: |
        # Check CODEOWNERS file
        if [ ! -f .github/CODEOWNERS ]; then
          echo "ERROR: CODEOWNERS file missing"
          exit 1
        fi
        
    - name: Check security policy
      run: |
        # Check security policy
        if [ ! -f SECURITY.md ]; then
          echo "WARNING: SECURITY.md file missing"
        fi
```

### Governance Strategy

**Organizational governance framework**:
```
┌─────────────────────────────────────────┐
│           Organizational Governance     │
│           Framework                     │
├─────────────────────────────────────────┤
│  Policy Layer                           │
│    ├── Security Policy                  │
│    ├── Access Control Policy            │
│    ├── Data Protection Policy           │
│    └── Compliance Policy                │
├─────────────────────────────────────────┤
│  Execution Layer                        │
│    ├── Permission Management            │
│    ├── Branch Protection                │
│    ├── Code Review                      │
│    └── Security Scanning                │
├─────────────────────────────────────────┤
│  Monitoring Layer                       │
│    ├── Audit Logs                       │
│    ├── Security Alerts                  │
│    ├── Compliance Reports               │
│    └── Performance Monitoring           │
└─────────────────────────────────────────┘
```

**Governance best practices**:
- Establish clear governance policies
- Automate compliance checks
- Regularly review and update policies
- Train team members
- Establish incident response procedures

## Security Features

### Secret Scanning

**Enable Secret Scanning**:
```bash
# Enable Push Protection
gh api repos/{org}/{repo}/secret-scanning/push-protection \
  --method PUT \
  -f status='enabled'

# Enable Secret Scanning
gh api repos/{org}/{repo}/secret-scanning \
  --method PUT \
  -f status='enabled'
```

**Custom Secret Scanning patterns**:
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

### Dependency Graph

**Enable dependency graph**:
```bash
# Enable dependency graph
gh api repos/{org}/{repo}/vulnerability-alerts \
  --method PUT \
  -f enabled='true'

# Enable automated security updates
gh api repos/{org}/{repo}/automated-security-fixes \
  --method PUT \
  -f enabled='true'
```

### Code Scanning

**Configure CodeQL**:
```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Execute every Monday

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
        queries: security-extended

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:${{matrix.language}}"
```

## Administration API

### Organization Management

**Get organization information**:
```bash
# Get organization details
gh api orgs/{org}

# Get organization settings
gh api orgs/{org}/settings/billing

# Get organization members
gh api orgs/{org}/members

# Get organization teams
gh api orgs/{org}/teams

# Get organization repositories
gh api orgs/{org}/repos --paginate
```

**Manage organization members**:
```bash
# Invite members
gh api orgs/{org}/invitations \
  --method POST \
  -f email='user@example.com' \
  -f role='direct_member'

# Remove members
gh api orgs/{org}/members/{username} \
  --method DELETE

# Change member role
gh api orgs/{org}/memberships/{username} \
  --method PUT \
  -f role='admin'
```

### Repository Management

**Get repository information**:
```bash
# List repositories
gh api orgs/{org}/repos --paginate

# Get repository details
gh api repos/{owner}/{repo}

# Get repository security features
gh api repos/{owner}/{repo}/vulnerability-alerts

# Get repository secrets
gh api repos/{owner}/{repo}/actions/secrets

# Get repository variables
gh api repos/{owner}/{repo}/actions/variables
```

**Manage repository settings**:
```bash
# Update repository settings
gh api repos/{owner}/{repo} \
  --method PATCH \
  -f has_issues=true \
  -f has_projects=true \
  -f has_wiki=true

# Set repository visibility
gh api repos/{owner}/{repo} \
  --method PATCH \
  -f visibility='private'

# Archive repository
gh api repos/{owner}/{repo} \
  --method PATCH \
  -f archived=true
```

### Team Management

**Manage teams**:
```bash
# Create team
gh api orgs/{org}/teams \
  --method POST \
  -f name='new-team' \
  -f description='New team description' \
  -f privacy='closed'

# Delete team
gh api orgs/{org}/teams/{team_slug} \
  --method DELETE

# Add team member
gh api orgs/{org}/teams/{team_slug}/memberships/{username} \
  --method PUT \
  -f role='member'

# Get team repositories
gh api orgs/{org}/teams/{team_slug}/repos
```

## Enterprise Deployment

### Deployment Options

**GitHub Enterprise Cloud**:
- Hosted on GitHub cloud
- No infrastructure maintenance required
- Automatic scaling and updates
- Suitable for most enterprises

**GitHub Enterprise Server**:
- Self-hosted deployment
- Full control over infrastructure
- Requires self-maintenance
- Suitable for enterprises with strict compliance requirements

**GitHub AE (Azure version of GitHub Enterprise):
- Hosted on Azure
- Integrates with Azure services
- Suitable for Azure users

### Deployment Architecture

**Enterprise deployment architecture**:
```
┌─────────────────────────────────────────┐
│           Enterprise Deployment         │
│           Architecture                  │
├─────────────────────────────────────────┤
│  User Layer                             │
│    ├── Developers                       │
│    ├── Testers                          │
│    ├── Operations Staff                 │
│    └── Management                       │
├─────────────────────────────────────────┤
│  Access Layer                           │
│    ├── SSO/SAML                         │
│    ├── IP Allow List                    │
│    ├── VPN                              │
│    └── Firewall                         │
├─────────────────────────────────────────┤
│  Application Layer                      │
│    ├── GitHub Enterprise                │
│    ├── GitHub Actions                   │
│    ├── GitHub Packages                  │
│    └── GitHub Pages                     │
├─────────────────────────────────────────┤
│  Data Layer                             │
│    ├── Git Repositories                 │
│    ├── Database                         │
│    ├── Cache                            │
│    └── Storage                          │
├─────────────────────────────────────────┤
│  Infrastructure Layer                   │
│    ├── Compute Resources                │
│    ├── Network Resources                │
│    ├── Storage Resources                │
│    └── Security Resources               │
└─────────────────────────────────────────┘
```

### Deployment Best Practices

**High availability**:
- Deploy multiple instances
- Use load balancing
- Configure failover
- Regularly back up data

**Performance optimization**:
- Optimize network configuration
- Use CDN
- Configure caching
- Monitor performance metrics

**Security hardening**:
- Enable all security features
- Configure network isolation
- Regular security audits
- Establish security monitoring

## Cost Optimization

### Cost Analysis

**Main cost items**:
- User license fees
- Actions minutes fees
- Storage fees
- Bandwidth fees
- Support fees

**Cost optimization strategies**:
1. **User management**:
   - Regularly review user permissions
   - Remove inactive users
   - Use teams to manage permissions
   - Optimize license allocation

2. **Actions optimization**:
   - Use caching to reduce build times
   - Optimize workflow configuration
   - Use self-hosted runners
   - Monitor usage

3. **Storage optimization**:
   - Regularly clean up old data
   - Use Git LFS for large files
   - Compress build artifacts
   - Monitor storage usage

### Cost Monitoring

**Using GitHub API to monitor costs**:
```bash
# Get billing information
gh api orgs/{org}/settings/billing

# Get Actions usage
gh api orgs/{org}/settings/billing/actions

# Get Packages usage
gh api orgs/{org}/settings/billing/packages

# Get storage usage
gh api orgs/{org}/settings/billing/storage
```

**Automated cost reports**:
```yaml
# .github/workflows/cost-report.yml
name: Cost Report

on:
  schedule:
    - cron: '0 0 1 * *'  # Execute on the 1st of every month

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
    - name: Generate cost report
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        # Get billing information
        gh api orgs/{org}/settings/billing > billing.json
        
        # Generate report
        echo "Cost Report - $(date +%Y-%m)" > cost-report.md
        echo "=========================" >> cost-report.md
        echo "" >> cost-report.md
        
        # Parse JSON and generate report
        jq -r '.actions_minutes_used_used // 0' billing.json >> cost-report.md
        
        # Send report
        gh api repos/{owner}/{repo}/issues \
          --method POST \
          -f title="Cost Report - $(date +%Y-%m)" \
          -f body="$(cat cost-report.md)"
```

## Best Practices

1. **Enable SSO**: Unify identity authentication, improve security
2. **Configure audit logs**: Track all operations, meet compliance requirements
3. **Set up IP allow lists**: Restrict access sources, enhance security
4. **Use CODEOWNERS**: Clarify code ownership, improve code quality
5. **Regularly review permissions**: Ensure principle of least privilege, reduce security risks
6. **Optimize costs**: Regularly review usage, optimize resource allocation
7. **Establish governance strategy**: Define clear governance policies, ensure compliance
8. **Train the team**: Regularly train team members, improve security awareness

## Related Resources

- [GitHub Enterprise Documentation](https://docs.github.com/en/enterprise-cloud@latest)
- [SAML SSO Documentation](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization)
- [Audit Log Documentation](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-the-audit-log-for-your-enterprise)
- [IP Allow List Documentation](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-allowed-ip-addresses-for-your-organization)
- [Cost Optimization Guide](https://docs.github.com/en/enterprise-cloud@latest/billing/managing-billing-for-your-github-account/about-billing-for-github)

---

**Previous: [DevOps in Practice](W15-devops.md) | Next: [Docker + GitHub Actions Containerization](W17-docker-actions.md)**

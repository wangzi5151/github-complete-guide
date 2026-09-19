# Exercise 28: Configuring GitHub Security Scanning

## Learning Objectives

After completing this exercise, you will be able to:

- Understand the overall architecture of GitHub security features
- Configure and use CodeQL for code scanning
- Enable Secret Scanning to prevent secret leaks
- Configure Dependabot for automatic dependency vulnerability fixes
- View and handle security alerts
- Build a complete security scanning workflow

## Prerequisites

- Have a GitHub repository (public or private)
- Understand basic security concepts
- Familiar with GitHub Actions basics
- Understand common types of security vulnerabilities

## Background Knowledge

### Overview of GitHub Security Features

GitHub provides multi-layered security protection:

1. **Code Scanning**
   - Uses CodeQL to analyze code vulnerabilities
   - Supports multiple programming languages
   - Can be integrated into CI/CD pipelines

2. **Secret Scanning**
   - Detects sensitive information in code
   - Supports 100+ key formats
   - Automatically notifies service providers

3. **Dependabot**
   - Automatically detects dependency vulnerabilities
   - Automatically generates fix PRs
   - Supports multiple package managers

4. **Security Advisories**
   - Privately reports vulnerabilities
   - Coordinates fix releases

---

## Exercise Steps

### Part 1: Enabling CodeQL Code Scanning

#### Step 1: Create the CodeQL Workflow

Create the file `.github/workflows/codeql-analysis.yml`:

```yaml
name: "CodeQL Analysis"

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # Runs every Monday at UTC 00:00
    - cron: '0 0 * * 1'

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    
    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']
        # If you have more languages, you can add:
        # language: ['c-cpp', 'csharp', 'go', 'java-kotlin', 'javascript', 'python', 'ruby', 'swift']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          # Use security-extended queries
          queries: security-extended
          # Or use comprehensive queries
          # queries: security-and-quality
      
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

#### Step 2: Configure Build for Specific Languages

If autobuild is not applicable, you can configure manually. Create the file `.github/workflows/codeql-python.yml`:

```yaml
name: "CodeQL Python Analysis"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze Python
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt || true
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-extended
      
      - name: Manual build
        run: |
          # Add compilation steps here if needed
          echo "Build complete"
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:python"
```

#### Step 3: Configure CodeQL for JavaScript/TypeScript

Create the file `.github/workflows/codeql-javascript.yml`:

```yaml
name: "CodeQL JavaScript Analysis"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'

permissions:
  actions: read
  contents: read
  security-events: write

jobs:
  analyze:
    name: Analyze JavaScript
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript-typescript
          queries: security-extended
          # Custom query configuration
          config: |
            name: "Custom JavaScript Configuration"
            queries:
              - uses: security-extended
              - uses: security-and-quality
            paths:
              - src
              - lib
            paths-ignore:
              - '**/node_modules'
              - '**/test'
              - '**/tests'
              - '**/__tests__'
              - '**/dist'
      
      - name: Autobuild
        uses: github/codeql-action/autobuild@v3
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:javascript-typescript"
```

#### Step 4: Create the CodeQL Configuration File

Create the file `.github/codeql/codeql-config.yml`:

```yaml
name: "CodeQL Configuration"

# Query suites
queries:
  - uses: security-extended
  - uses: security-and-quality

# Custom queries
query-filters:
  - include:
      tags:
        - security
        - correctness
  - exclude:
      id: js/unused-local-variable

# Path configuration
paths:
  - src
  - lib
  - app

paths-ignore:
  - '**/node_modules'
  - '**/test/**'
  - '**/tests/**'
  - '**/__tests__/**'
  - '**/vendor/**'
  - '**/dist/**'
  - '**/build/**'
  - '**/*.test.js'
  - '**/*.test.ts'
  - '**/*.spec.js'
  - '**/*.spec.ts'

# Custom query packs
packs:
  javascript:
    - codeql/javascript-queries
  python:
    - codeql/python-queries
```

Use the configuration file in the workflow:

```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: javascript
    config-file: ./.github/codeql/codeql-config.yml
```

### Part 2: Configuring Secret Scanning

#### Step 5: Enable Secret Scanning

1. Go to the repository's Settings → Security → Code security and analysis
2. Find the "Secret scanning" section
3. Enable the following options:
   - Secret scanning
   - Secret scanning push protection (recommended)

Or via GitHub CLI:

```bash
# Enable Secret Scanning
gh api -X PATCH repos/{owner}/{repo} \
  -f security_and_analysis='{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}'
```

#### Step 6: Create Custom Secret Scanning Patterns

Create the file `.github/secret_scanning.yml`:

```yaml
# Custom secret scanning patterns
# Format: regular expression + secret type description

patterns:
  # Custom API key pattern
  - name: "Custom API Key"
    regex: '(?i)api[_-]?key\s*[:=]\s*["\']?([a-zA-Z0-9]{32,})["\']?'
    confidence: high
    
  # Custom database connection string
  - name: "Database Connection String"
    regex: '(?i)(mysql|postgresql|mongodb)://[^\s]+'
    confidence: high
    
  # AWS key pattern
  - name: "AWS Access Key"
    regex: 'AKIA[0-9A-Z]{16}'
    confidence: high
    
  # Private key pattern
  - name: "Private Key"
    regex: '-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'
    confidence: high
```

#### Step 7: Integrate Secret Detection in CI

Create the file `.github/workflows/secret-detection.yml`:

```yaml
name: Secret Detection

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  detect-secrets:
    name: Detect Secrets
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Install gitleaks
        run: |
          wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
          tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
          sudo mv gitleaks /usr/local/bin/
      
      - name: Run gitleaks
        run: |
          gitleaks detect --source . --verbose --report-format sarif --report-path gitleaks-report.sarif
        continue-on-error: true
      
      - name: Upload SARIF report
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: gitleaks-report.sarif
          category: gitleaks
      
      - name: Check results
        if: failure()
        run: |
          echo "Potential secret leak detected!"
          echo "Please review security alerts and fix the issue."
          exit 1
```

#### Step 8: Create .gitignore to Prevent Secret Commits

Update the `.gitignore` file:

```gitignore
# Environment variables and secret files
.env
.env.local
.env.*.local
*.pem
*.key
*.cert
*.p12
*.pfx

# IDE configuration (may contain secrets)
.idea/
.vscode/settings.json

# Dependency directories
node_modules/
vendor/
venv/

# Build artifacts
dist/
build/
*.egg-info/

# Log files
*.log
logs/

# Operating system files
.DS_Store
Thumbs.db

# Secret files
secrets/
credentials/
*.secret
*.credentials
```

### Part 3: Configuring Dependabot

#### Step 9: Create the Dependabot Configuration File

Create the file `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # GitHub Actions dependencies
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Asia/Shanghai"
    open-pull-requests-limit: 10
    reviewers:
      - "your-team-name"
    labels:
      - "dependencies"
      - "github-actions"
    commit-message:
      prefix: "ci"
      include: "scope"
  
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
      - "your-team-name"
    labels:
      - "dependencies"
      - "npm"
    commit-message:
      prefix: "deps"
      include: "scope"
    # Ignore specific dependency updates
    ignore:
      - dependency-name: "lodash"
        update-types: ["version-update:semver-major"]
      - dependency-name: "express"
        versions: [">=5.0.0"]
    # Group updates
    groups:
      development:
        dependency-type: "development"
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier"
          - "jest"
          - "typescript"
      production:
        dependency-type: "production"
        patterns:
          - "express"
          - "mongoose"
          - "jsonwebtoken"
  
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "tuesday"
      time: "09:00"
      timezone: "Asia/Shanghai"
    open-pull-requests-limit: 10
    reviewers:
      - "your-team-name"
    labels:
      - "dependencies"
      - "python"
    commit-message:
      prefix: "deps"
      include: "scope"
    groups:
      development:
        dependency-type: "development"
        patterns:
          - "pytest*"
          - "ruff"
          - "mypy"
          - "black"
      production:
        dependency-type: "production"
        patterns:
          - "flask*"
          - "requests"
          - "sqlalchemy"
  
  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "docker"
  
  # Terraform dependencies
  - package-ecosystem: "terraform"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "terraform"
```

#### Step 10: Configure Dependabot Security Updates

Enable automatic security updates in the repository settings:

```bash
# Enable automatic security updates using GitHub CLI
gh api -X PATCH repos/{owner}/{repo} \
  -f '{"security_and_analysis":{"dependabot_security_updates":{"status":"enabled"}}}'
```

#### Step 11: Create the Dependabot Auto-Merge Workflow

Create the file `.github/workflows/dependabot-auto-merge.yml`:

```yaml
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
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"
      
      - name: Auto-merge patch updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: |
          gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Auto-merge minor updates (development dependencies)
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-minor' &&
          steps.metadata.outputs.dependency-type == 'development:direct'
        run: |
          gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Add review label
        if: |
          steps.metadata.outputs.update-type == 'version-update:semver-major' ||
          (steps.metadata.outputs.update-type == 'version-update:semver-minor' &&
           steps.metadata.outputs.dependency-type == 'production:direct')
        run: |
          gh pr edit "$PR_URL" --add-label "needs-review"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Part 4: Comprehensive Security Scanning Workflow

#### Step 12: Create a Complete Security Scanning Workflow

Create the file `.github/workflows/security-scan.yml`:

```yaml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # Runs daily at UTC 02:00
    - cron: '0 2 * * *'

permissions:
  actions: read
  contents: read
  security-events: write
  pull-requests: write

jobs:
  # Code scanning
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']
    
    steps:
      - name: Checkout code
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
          category: "/language:${{ matrix.language }}"
  
  # Dependency scanning
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Dependency review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
          deny-licenses: GPL-3.0, AGPL-3.0
  
  # Secret scanning
  secret-scan:
    name: Secret Scanning
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Run trufflehog
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
  
  # SAST scanning
  sast:
    name: SAST Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
            p/ci
  
  # Container scanning
  container-scan:
    name: Container Scan
    runs-on: ubuntu-latest
    if: hashFiles('Dockerfile') != ''
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t test-image .
      
      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'test-image'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload Trivy SARIF report
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
  
  # Security report
  security-report:
    name: Security Report
    runs-on: ubuntu-latest
    needs: [codeql, dependency-review, secret-scan, sast, container-scan]
    if: always()
    
    steps:
      - name: Generate security report
        run: |
          echo "# Security Scan Report" > security-report.md
          echo "" >> security-report.md
          echo "## Scan Time: $(date)" >> security-report.md
          echo "" >> security-report.md
          echo "## Scan Results" >> security-report.md
          echo "" >> security-report.md
          echo "| Check | Status |" >> security-report.md
          echo "|--------|------|" >> security-report.md
          echo "| CodeQL | ${{ needs.codeql.result }} |" >> security-report.md
          echo "| Dependency Review | ${{ needs.dependency-review.result }} |" >> security-report.md
          echo "| Secret Scanning | ${{ needs.secret-scan.result }} |" >> security-report.md
          echo "| SAST | ${{ needs.sast.result }} |" >> security-report.md
          echo "| Container Scan | ${{ needs.container-scan.result }} |" >> security-report.md
      
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-report.md
```

### Part 5: Security Policy Configuration

#### Step 13: Create the Security Policy File

Create the file `SECURITY.md`:

```markdown
# Security Policy

## Supported Versions

| Version | Support Status |
|------|---------|
| Latest version | ✅ Supported |
| Older versions | ❌ Not supported |

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it through the following methods:

1. **Do not** report security vulnerabilities in public issues
2. Use GitHub's private vulnerability reporting feature
3. Or send an email to security@example.com

### Report Content

Please include the following in your report:

- Vulnerability type
- Affected versions
- Steps to reproduce
- Potential impact
- Fix recommendations (if available)

### Response Time

- We will acknowledge receipt of your report within 48 hours
- We will provide an initial assessment within 7 days
- We will release a fix within 30 days (if needed)

## Security Best Practices

### For Users

1. Always use the latest version
2. Regularly check for dependency updates
3. Never hardcode secrets in code
4. Use environment variables to store sensitive information

### For Contributors

1. Follow secure coding guidelines
2. Do not commit code containing secrets
3. Use CodeQL and other tools to check code
4. Fix security alerts promptly

## Security-Related Configuration

### Environment Variables

Use `.env` files for local configuration, do not commit to version control:

```
DATABASE_URL=...
API_KEY=...
SECRET_KEY=...
```

### Dependency Management

Use Dependabot to automatically update dependencies and regularly check security advisories.
```

#### Step 14: Create the CODEOWNERS File

Create the file `.github/CODEOWNERS`:

```
# Security-related files require security team review
SECURITY.md @your-org/security-team
.github/workflows/ @your-org/security-team
.github/dependabot.yml @your-org/security-team

# Dependency files require review
package.json @your-org/backend-team
package-lock.json @your-org/backend-team
requirements.txt @your-org/backend-team

# Docker files require review
Dockerfile @your-org/devops-team
docker-compose.yml @your-org/devops-team
```

---

## Verifying Exercise Results

### Checklist

After completing the exercise, verify the following:

- [ ] CodeQL workflow has been created and can run successfully
- [ ] Secret Scanning is enabled
- [ ] Dependabot configuration has been created
- [ ] Security policy file has been created
- [ ] Security scanning workflow can detect test vulnerabilities

### Verification Commands

```bash
# Check CodeQL workflow syntax
actionlint .github/workflows/codeql-analysis.yml

# Check Dependabot configuration
gh api repos/{owner}/{repo}/vulnerability-alerts

# Manually trigger security scan
gh workflow run security-scan.yml

# View security alerts
gh api repos/{owner}/{repo}/code-scanning/alerts
```

### Testing Security Scanning

Create a test file `test-vulnerabilities.js` to verify the scanning works:

```javascript
// Test SQL injection vulnerability (for testing only, do not use in production code)
function getUserData(userId) {
  const query = "SELECT * FROM users WHERE id = " + userId;  // SQL injection vulnerability
  return db.query(query);
}

// Test XSS vulnerability
function displayUserInput(input) {
  document.getElementById("output").innerHTML = input;  // XSS vulnerability
}

// Test hardcoded secret
const API_KEY = "sk-1234567890abcdef";  // Hardcoded secret

// Test insecure regex
function validateInput(input) {
  return /^(a+)+$/.test(input);  // ReDoS vulnerability
}
```

CodeQL should be able to detect these vulnerabilities and generate alerts.

---

## Advanced Challenges

### Challenge 1: Custom CodeQL Query

Create a custom CodeQL query file `.github/codeql/custom-query.ql`:

```ql
/**
 * @name Hardcoded credentials
 * @description Detect hardcoded credentials in source code
 * @kind problem
 * @problem.severity error
 * @security-severity 9.0
 * @precision high
 * @id javascript/hardcoded-credentials
 * @tags security
 *       external/cwe/cwe-798
 */

import javascript

from DataFlow::Node source, string name
where
  source = any(ConstantExpr c).flow() and
  (
    name = source.(DataFlow::PropRead).getPropertyName() and
    name.toLowerCase().matches(["%password%", "%secret%", "%key%", "%token%"])
  )
select source, "Hardcoded credential found: " + name
```

### Challenge 2: Integrate Third-Party Security Tools

Integrate more security tools in the workflow:

```yaml
- name: Run OWASP ZAP scan
  uses: zaproxy/action-full-scan@v0.7.0
  with:
    target: 'https://your-app.example.com'

- name: Run SonarQube scan
  uses: sonarsource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Challenge 3: Create a Security Dashboard

Use GitHub Pages to create a security dashboard:

```yaml
name: Security Dashboard

on:
  schedule:
    - cron: '0 0 * * *'

jobs:
  dashboard:
    runs-on: ubuntu-latest
    
    steps:
      - name: Collect security data
        run: |
          # Fetch CodeQL alerts
          # Fetch Dependabot alerts
          # Generate report
          # Deploy to GitHub Pages
```

### Challenge 4: Implement a Security Gate

Enforce security checks before merging PRs:

```yaml
name: Security Gate

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  security-gate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Check security alerts
        run: |
          ALERTS=$(gh api repos/{owner}/{repo}/code-scanning/alerts --jq '[.[] | select(.state == "open")] | length')
          
          if [ "$ALERTS" -gt 0 ]; then
            echo "There are $ALERTS unresolved security alerts"
            exit 1
          fi
```

---

## Security Scanning In-Depth

### Common Types of Security Vulnerabilities

Understanding vulnerability types helps make better use of security scanning tools. Injection vulnerabilities are one of the most common security issues, including SQL injection, command injection, and LDAP injection. Attackers construct malicious input to make the application execute unintended commands or queries. Cross-site scripting attacks allow attackers to execute malicious scripts in a victim's browser, stealing session credentials or performing phishing attacks. Cross-site request forgery attacks exploit an authenticated user's identity to perform malicious actions without their knowledge. Insecure deserialization can lead to remote code execution, where attackers trigger vulnerabilities through crafted serialized data. Sensitive data exposure includes unencrypted password storage, logging sensitive information, or exposing system details in error messages.

### How Code Scanning Works

Code scanning tools detect security issues through static analysis techniques. Pattern matching is the most basic detection method, using predefined rules to match known insecure code patterns. Data flow analysis tracks the flow of data through the program, identifying data flows from untrusted sources to sensitive operations. Control flow analysis examines program execution paths, identifying code branches that could lead to security issues. Taint analysis is an advanced technique that marks data from external inputs as "tainted" and tracks whether this data reaches sensitive operation points without proper handling. Semantic analysis understands the meaning of code, enabling detection of security issues at the logical level.

### Incident Response for Secret Leaks

When a secret leak is detected, immediate incident response measures are needed. The first step is to immediately revoke the leaked key to prevent attacker exploitation. The second step is to check usage logs of the leaked key to confirm whether it has been used maliciously. The third step is to generate new keys and update all services using that key. The fourth step is to review code commit history to confirm the scope and timing of the leak. The fifth step is to analyze the cause of the leak, whether it was human error or a process deficiency. The sixth step is to improve protective measures, such as enabling push protection, strengthening code review, or using a key management service. The seventh step is to write an incident report documenting the event and improvement measures for team learning.

### Risk Assessment of Dependency Vulnerabilities

Risk assessment of dependency vulnerabilities requires considering multiple factors. Vulnerability severity can be measured by CVSS score, with higher scores indicating greater risk. Vulnerability exploitability determines the difficulty for attackers to exploit the vulnerability, with remotely exploitable vulnerabilities being more dangerous than local ones. The impact scope of vulnerabilities includes confidentiality, integrity, and availability impacts. How dependencies are used is also critical, as vulnerabilities in development dependencies typically carry lower risk than those in production dependencies. Whether there is publicly available exploit code will significantly increase risk. Patch availability determines the urgency of remediation, with vulnerabilities that have available fixes being prioritized.

### Shift-Left Security Philosophy and Practice

Shift-left security refers to moving security checks from later stages of the development pipeline to earlier stages. Traditional security checks are typically performed before deployment or after going live, when the cost of fixing discovered issues is already high. The shift-left philosophy aims to start security checks at the coding stage. When developers submit code, security plugins in integrated development environments can detect security issues in real-time. During code commits, pre-commit hooks can prevent code containing secrets or known vulnerabilities from being submitted. During code review, security scan results can serve as review reference. During continuous integration, automated security scanning ensures every build meets security standards. Through this approach, security issues can be discovered and fixed at the earliest stage, significantly reducing remediation costs.

### Security Compliance and Auditing

For enterprise applications, security compliance and auditing are essential. Common security compliance standards include SOC 2, ISO 27001, PCI DSS, and GDPR. GitHub's security features can help meet these compliance requirements. CodeQL scan results can serve as evidence for security audits, proving that code has undergone automated security checks. Secret Scanning enablement records can demonstrate that the organization has taken measures to prevent secret leaks. Dependabot configuration and execution records can prove that dependency management meets security requirements. It is recommended to regularly export security scan reports and archive them for audit purposes. Additionally, establish a security incident response process to ensure rapid response and handling when security issues are discovered.

### Team Security Awareness Training

Tools are only part of security protection, and team security awareness is equally important. It is recommended to regularly organize security training covering common types of security vulnerabilities and prevention measures, secure coding best practices, security tool usage, and security incident response processes. Establish a security champion program by cultivating a security champion in each team, responsible for promoting security practices and assisting in resolving security issues. Create a security knowledge base by collecting and organizing security-related documentation, case studies, and best practices. Regularly conduct security drills simulating the discovery, reporting, and handling of security incidents to improve the team's emergency response capability.

### Security Metrics

Measuring the effectiveness of security scanning requires establishing a metrics system. Vulnerability discovery rate measures the number and types of vulnerabilities found by security scanning tools. Mean time to remediation measures the average time from vulnerability discovery to fix completion. False positive rate measures the accuracy of security scanning tools, with high false positive rates impacting developer productivity. Coverage rate measures the code scope and language types covered by security scanning. Dependency health measures the number and severity of known vulnerabilities in project dependencies. Secret leak prevention rate measures the number of successfully blocked secret leaks. It is recommended to regularly track and analyze these metrics to continuously improve security scanning configuration and processes.

---

## Frequently Asked Questions

### Q1: How long does a CodeQL scan take?

Scan time depends on:
- Codebase size
- Number of languages selected
- Query complexity

Typically small projects take 5-10 minutes, large projects may take 30 minutes or more.

### Q2: How to reduce false positives?

1. Use `paths-ignore` to exclude test files
2. Adjust query configuration
3. Use comments in code to mark false positives
4. Use custom query filters

### Q3: What if Secret Scanning detects a false positive?

1. Mark as "False positive" in repository settings
2. Exclude specific patterns in `.github/secret_scanning.yml`
3. Use environment variables instead of hardcoding

### Q4: How to automatically test Dependabot PRs?

1. Configure CI workflow to run on PRs
2. Use `pull_request` trigger
3. Configure auto-merge conditions

---

## Further Reading

- [GitHub Advanced Security Official Documentation](https://docs.github.com/en/code-security)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)

---

## Exercise Summary

Through this exercise, you have learned to:

1. ✅ Configure CodeQL for code scanning
2. ✅ Enable Secret Scanning to prevent secret leaks
3. ✅ Configure Dependabot for automatic dependency vulnerability fixes
4. ✅ Create a comprehensive security scanning workflow
5. ✅ Establish security policy and reporting mechanisms

Security scanning is an important part of modern software development. It is recommended to integrate security checks into the CI/CD pipeline to achieve shift-left security.

# Exercise 14: Security Scan Practice

## Learning Objectives

- Configure CodeQL code scanning
- Use Trivy to scan container vulnerabilities
- Configure Dependabot automatic updates

## Steps

### Step 1: CodeQL Analysis

```yaml
# .github/workflows/codeql.yml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: javascript
    
    - name: Autobuild
      uses: github/codeql-action/autobuild@v3
    
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

### Step 2: Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Step 3: Container Scanning

```yaml
# .github/workflows/container-scan.yml
name: Container Scan

on:
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Build image
      run: docker build -t my-app:scan .
    
    - name: Run Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my-app:scan'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
    
    - name: Upload results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: 'trivy-results.sarif'
```

## Hands-on Tasks

1. Configure CodeQL code scanning
2. Configure Dependabot automatic updates
3. Create a container security scanning workflow
4. Review scan results

## Verification Checklist

- [ ] Able to configure CodeQL analysis
- [ ] Able to configure Dependabot
- [ ] Able to run container scanning
- [ ] Able to interpret scan results

## Next Steps

Continue to [Exercise 15: Release Management Practice](exercise-15-release-management.md)

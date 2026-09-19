# Chapter 7: Security and DevOps Practices

## 7.1 GitHub Security Basics

### Account Security

**Two-Factor Authentication (2FA):**

1. Go to **Settings** → **Password and authentication**
2. Click **Enable two-factor authentication**
3. Choose a verification method:
   - Authenticator App (recommended)
   - SMS/voice message
   - Security key
4. Save recovery codes

**Personal Access Token (PAT):**

1. Go to **Settings** → **Developer settings** → **Personal access tokens**
2. Click **Generate new token**
3. Select permission scopes
4. Save the generated token

### Repository Security

**Branch Protection Rules:**

1. Go to **Settings** → **Branches**
2. Click **Add rule**
3. Configure protection rules:

```
┌─────────────────────────────────────────────┐
│  Branch protection rules                     │
│                                             │
│  Branch name pattern: [main           ]      │
│                                             │
│  ☑ Require a pull request before merging    │
│    ☑ Required number of approvals: [1  ▼]   │
│    ☑ Dismiss stale pull request approvals   │
│    ☑ Require review from Code Owners        │
│                                             │
│  ☑ Require status checks to pass            │
│    ☑ Require branches to be up to date      │
│                                             │
│  ☑ Do not allow bypassing the above settings│
│                                             │
│             [Create]                         │
└─────────────────────────────────────────────┘
```

**CODEOWNERS:**

Create a `.github/CODEOWNERS` file:

```yaml
# Default owners
* @your-org/core-team

# Frontend code
/src/components/ @your-org/frontend-team

# Backend code
/src/api/ @your-org/backend-team

# Infrastructure
/terraform/ @your-org/devops-team
```

## 7.2 Secret Scanning

### What is Secret Scanning?

GitHub automatically scans repositories for sensitive information (such as API keys, passwords, etc.) and sends alerts.

### Enabling Secret Scanning

1. Go to **Settings** → **Code security and analysis**
2. Enable **Secret scanning**
3. Enable **Push protection**

```
┌─────────────────────────────────────────────┐
│  Code security and analysis                  │
│                                             │
│  Secret scanning                             │
│  ○ Disable  ● Enable  ← Enabled             │
│                                             │
│  Push protection                             │
│  ○ Disable  ● Enable  ← Enabled             │
│                                             │
└─────────────────────────────────────────────┘
```

### Custom Secret Patterns

Create `.github/secret-scanning.yml`:

```yaml
custom-patterns:
  - name: Internal API Key
    pattern: 'internal-api-key-[a-zA-Z0-9]{32}'
    description: Internal API keys
```

## 7.3 Dependabot

### What is Dependabot?

Dependabot automatically checks project dependencies for security vulnerabilities and provides update recommendations.

### Enabling Dependabot

1. Go to **Settings** → **Code security and analysis**
2. Enable **Dependabot alerts**
3. Enable **Dependabot security updates**

### Configuring Dependabot

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "automated"
  
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Auto-Merging Security Updates

```yaml
# .github/workflows/auto-merge.yml
name: Auto Merge Dependabot

on:
  pull_request:

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    
    steps:
    - name: Fetch Dependabot metadata
      id: metadata
      uses: dependabot/fetch-metadata@v1
      with:
        github-token: "${{ secrets.GITHUB_TOKEN }}"
    
    - name: Auto-merge minor and patch updates
      if: steps.metadata.outputs.update-type != 'version-update:semver-major'
      run: gh pr merge --auto --squash "$PR_URL"
      env:
        PR_URL: ${{github.event.pull_request.html_url}}
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 7.4 Code Scanning

### What is Code Scanning?

Code Scanning uses CodeQL to analyze code for security vulnerabilities.

### Configuring Code Scanning

**Step 1:** Go to **Security** → **Code scanning**

**Step 2:** Click **Set up**

**Step 3:** Select CodeQL

```
┌─────────────────────────────────────────────┐
│  Set up code scanning                        │
│                                             │
│  Select a tool:                              │
│                                             │
│  ● CodeQL  ← Recommended                    │
│  ○ Third-party tools                         │
│                                             │
│  Select languages:                           │
│  ☑ JavaScript/TypeScript                     │
│  ☑ Python                                   │
│  ☑ Java/Kotlin                               │
│                                             │
│             [Set up CodeQL]                 │
└─────────────────────────────────────────────┘
```

### Creating a Workflow

Create `.github/workflows/codeql.yml`:

```yaml
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
    
    strategy:
      fail-fast: false
      matrix:
        language: ['javascript', 'python']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}
    
    - name: Autobuild
      uses: github/codeql-action/autobuild@v3
    
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

## 7.5 CI/CD Basics

### What is CI/CD?

- **CI (Continuous Integration):** Continuously integrates code changes into the main branch
- **CD (Continuous Deployment):** Automatically deploys code to production

### GitHub Actions Basics

**Workflow File Structure:**

```
.github/
└── workflows/
    └── ci.yml
```

**Basic Template:**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    
    - name: Install dependencies
      run: npm install
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
```

### Secrets Management

**Adding Secrets:**

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Enter name and value

```
┌─────────────────────────────────────────────┐
│  Secrets and variables / Actions             │
│                                             │
│  Repository secrets                          │
│                                             │
│  Name: [API_KEY            ]                 │
│  Value: [••••••••••••       ]                │
│                                             │
│           [Add secret]                      │
└─────────────────────────────────────────────┘
```

**Using Secrets:**

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

## 7.6 Deployment Practices

### Deploying to GitHub Pages

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      pages: write
      id-token: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Pages
      uses: actions/configure-pages@v4
    
    - name: Build
      run: npm run build
    
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './dist'
    
    - name: Deploy to GitHub Pages
      uses: actions/deploy-pages@v4
```

### Deploying to Vercel

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

### Deploying to Docker

```yaml
name: Docker Build and Push

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKERHUB_USERNAME }}/my-app:latest
```

## 7.7 Monitoring and Alerting

### Monitoring Workflow

```yaml
name: Monitor

on:
  schedule:
    - cron: '0 * * * *'  # Every hour

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Health check
      run: |
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
        if [ "$STATUS" != "200" ]; then
          echo "Service is down!"
          exit 1
        fi
```

### Alert Notifications

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Build failed: ${{ github.repository }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## 7.8 Chapter Summary

This chapter covered GitHub security and DevOps practices, including:

- Account and repository security
- Secret Scanning
- Dependabot
- Code Scanning
- CI/CD basics
- Deployment practices
- Monitoring and alerting

**Key Takeaways:**
- Security is an essential part of development
- CI/CD can improve development efficiency
- Automation is the core of DevOps

**Next Steps:**
[Hands-on Exercise →](exercises/exercise-1-create-repo.md)

# GitHub Actions Automation

## What is GitHub Actions?

GitHub Actions is GitHub's CI/CD platform, can automate build, test and deployment processes.

## Basic Concepts

| Concept | Description |
|---------|-------------|
| **Workflow** | Automated workflow, defined by YAML |
| **Event** | Event that triggers workflow |
| **Job** | A group of steps |
| **Step** | Single task |
| **Action** | Reusable work unit |
| **Runner** | Server that executes workflow |

## Create Workflow

### File Structure

```
.github/
└── workflows/
    └── ci.yml
```

### Basic Template

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

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
```

## Common Workflows

### Node.js Project

```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18, 20, 22]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        
    - run: npm ci
    - run: npm run build
    - run: npm test
```

### Deploy to GitHub Pages

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

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

## Secrets Management

Add in repository **Settings** → **Secrets and variables** → **Actions**:

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

## Cache Optimization

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

## Workflow Syntax

### Trigger Events

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Execute daily
  workflow_dispatch:       # Manual trigger
```

### Conditional Execution

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh
```

## Actions Marketplace

Visit [github.com/marketplace?type=actions](https://github.com/marketplace?type=actions) to discover commonly used Actions.

## Next Step

[GitHub Pages Static Website →](20-github-pages.md)
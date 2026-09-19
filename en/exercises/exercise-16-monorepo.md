# Exercise 16: Monorepo Management in Practice

## Learning Objectives

- Use pnpm workspaces
- Configure Turborepo
- Create an incremental build workflow

## Steps

### Step 1: Initialize the Monorepo

```bash
mkdir my-monorepo && cd my-monorepo
pnpm init
```

### Step 2: Configure workspace

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
```

### Step 3: Create package structure

```
my-monorepo/
├── package.json
├── pnpm-workspace.yaml
├── turbo.json
├── packages/
│   ├── shared/
│   │   ├── package.json
│   │   └── src/
│   ├── web/
│   │   ├── package.json
│   │   └── src/
│   └── api/
│       ├── package.json
│       └── src/
```

### Step 4: Configure Turborepo

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {}
  }
}
```

### Step 5: Create CI workflow

```yaml
# .github/workflows/monorepo.yml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: pnpm/action-setup@v2
      with:
        version: 8
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'pnpm'
    - run: pnpm install --frozen-lockfile
    - run: pnpm turbo build test lint
```

## Hands-on Tasks

1. Initialize a pnpm workspace
2. Create multiple packages
3. Configure Turborepo
4. Create an incremental build workflow

## Verification Checklist

- [ ] Able to initialize a pnpm workspace
- [ ] Able to configure Turborepo
- [ ] Able to run incremental builds
- [ ] Able to create Monorepo CI

## Completion

Congratulations on completing all exercises! You have mastered:
- Git fundamentals
- GitHub core features
- CI/CD pipelines
- Docker containerization
- Security scanning
- Release management
- Monorepo management

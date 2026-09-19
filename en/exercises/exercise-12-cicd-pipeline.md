# Exercise 12: CI/CD Pipeline in Practice

## Learning Objectives

- Build a complete CI/CD pipeline
- Integrate testing, building, and deployment
- Use matrix strategies and caching

## Steps

### Step 1: Create the Workflow

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    - run: npm ci
    - run: npm test

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: npm run build
    - uses: actions/upload-artifact@v4
      with:
        name: build
        path: dist/
```

### Step 2: Add Caching

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Step 3: Add Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Hands-On Tasks

1. Create a complete pipeline with lint, test, and build
2. Add a matrix strategy for the test job
3. Add dependency caching
4. Configure concurrency control

## Verification Checklist

- [ ] Able to create CI/CD workflows
- [ ] Able to use matrix strategies
- [ ] Able to configure caching
- [ ] Able to use artifacts

## Next Steps

Continue to [Exercise 13: Docker Deployment in Practice](exercise-13-docker-deploy.md)

# Exercise 19: GitHub Actions Reusable Workflows

## Learning Objectives

- Create reusable workflows
- Invoke reusable workflows
- Use matrix strategies

## Steps

### Step 1: Create a Reusable Workflow

```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build

on:
  workflow_call:
    inputs:
      node-version:
        required: false
        type: string
        default: '20'
      run-tests:
        required: false
        type: boolean
        default: true
    outputs:
      build-version:
        description: "Build version"
        value: ${{ jobs.build.outputs.version }}
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.value }}
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    
    - run: npm ci
    - run: npm run build
    
    - name: Get version
      id: version
      run: echo "value=$(node -p 'require(\"./package.json\").version')" >> $GITHUB_OUTPUT
    
    - name: Run tests
      if: ${{ inputs.run-tests }}
      run: npm test
```

### Step 2: Invoke the Reusable Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '20'
      run-tests: true
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Step 3: Use a Matrix Strategy

```yaml
# .github/workflows/matrix.yml
name: Matrix Build

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, windows-latest]
      fail-fast: false
    
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - run: npm ci
    - run: npm test
```

## Hands-On Task

1. Create a reusable workflow
2. Configure input parameters and outputs
3. Invoke the reusable workflow
4. Use a matrix strategy to test across multiple environments

## Verification Checklist

- [ ] Reusable workflow has been created
- [ ] Input parameters are configured
- [ ] Outputs are configured
- [ ] Calling the workflow works correctly
- [ ] Matrix strategy works correctly

## Next Steps

Continue to [Exercise 20: GitHub Projects Board Management](exercise-20-project-board.md)

# GitHub Actions Advanced Usage

## Reusable Workflows

### Creating Reusable Workflows

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
        description: "Build version number"
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
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    
    - run: npm ci
    - run: npm run build
    
    - name: Get version
      id: version
      run: echo "value=$(node -p 'require(\"./package.json\").version')" >> $GITHUB_OUTPUT
    
    - name: Run tests
      if: ${{ inputs.run-tests }}
      run: npm test
```

### Calling Reusable Workflows

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

## Matrix Strategy

### Basic Matrix

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [18, 20, 22]
    
    steps:
    - uses: actions/checkout@v4
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm ci
    - run: npm test
```

### Advanced Matrix Configuration

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # One failure doesn't affect others
      matrix:
        os: [ubuntu-latest]
        node-version: [18, 20, 22]
        include:
          - os: windows-latest
            node-version: 20
          - os: macos-latest
            node-version: 20
        exclude:
          - os: ubuntu-latest
            node-version: 18
    
    steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm test
```

## Concurrency

### Basic Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel currently running old workflows
```

### Environment-level Concurrency

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    concurrency:
      group: deploy-staging
      cancel-in-progress: false  # Deployment does not allow cancellation
    
    steps:
    - uses: actions/checkout@v4
    - run: npm run deploy:staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    
    steps:
    - uses: actions/checkout@v4
    - run: npm run deploy:production
```

## Self-hosted Runner

### Installing Runner

```bash
# Download Runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf actions-runner-linux-x64-2.311.0.tar.gz

# Configure
./config.sh --url https://github.com/your-org/your-repo --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### Using Runner

```yaml
jobs:
  build:
    runs-on: self-hosted  # Use self-hosted Runner
    
    steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run build
```

### Runner Labels

```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
    
  gpu:
    runs-on: [self-hosted, gpu]
```

## Environment Variables and Secrets

### Environment Variables

```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      BUILD_VERSION: ${{ github.sha }}
    
    steps:
    - run: echo "Building version $BUILD_VERSION"
```

### Secrets Management

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy
      run: |
        echo "Deploying..."
        curl -X POST ${{ secrets.DEPLOY_WEBHOOK }} \
          -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}" \
          -d '{"version": "${{ github.sha }}"}'
```

### Environment Secrets

```yaml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # Use environment-level Secrets
    
    steps:
    - run: echo "Deploying to production"
      env:
        API_KEY: ${{ secrets.API_KEY }}  # Obtain from production environment
```

## Workflow Optimization

### Caching Dependencies

```yaml
steps:
- uses: actions/checkout@v4

- name: Cache Node.js
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- run: npm ci
```

### Conditional Execution

```yaml
steps:
- uses: actions/checkout@v4

- name: Build
  run: npm run build
  if: github.event_name == 'push'

- name: Test
  run: npm test
  if: github.event_name == 'pull_request'
```

### Continue on Error

```yaml
steps:
- name: Try something
  run: npm run risky-command
  continue-on-error: true  # Continue even if it fails

- name: Check result
  if: steps.try.outcome == 'failure'
  run: echo "Previous step failed but we're continuing"
```

## Best Practices

1. **Use Reusable Workflows**: Reduce duplicate configurations
2. **Matrix Testing**: Ensure compatibility
3. **Concurrency Control**: Avoid resource waste
4. **Cache Dependencies**: Speed up builds
5. **Use Secrets**: Don't hardcode sensitive information
6. **Environment Protection**: Production environment requires approval

## Related Resources

- [Reusable Workflows Documentation](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Matrix Strategy Documentation](https://docs.github.com/en/actions/using-jobs/using-a-matrix-strategy-for-jobs)
- [Self-hosted Runner Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)

---

**Previous: [GitHub Actions Automation](19-github-actions.md) | Next: [GitHub Advanced Security](W10-advanced-security.md)**

# Exercise 32: GitHub Actions Matrix Strategy

## Goal

Learn how to use GitHub Actions matrix strategy to test multiple configurations in parallel.

## Prerequisites

- Have a GitHub account
- Familiar with GitHub Actions basics
- Have a test project

## Steps

### 1. Understanding Matrix Strategy

Matrix strategy allows you to run multiple jobs in parallel in a single workflow, each using different configurations.

**Basic syntax**:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### 2. Creating a Basic Matrix

**Example: Testing multiple Node.js versions**:

```yaml
# .github/workflows/test-matrix.yml
name: Test Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18, 20]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```

### 3. Using a Multi-Dimensional Matrix

**Example: Testing multiple operating systems and Node.js versions**:

```yaml
# .github/workflows/test-multi-dim.yml
name: Test Multi-Dimensional Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```

### 4. Using Matrix Exclusions

**Example: Excluding specific combinations**:

```yaml
# .github/workflows/test-exclude.yml
name: Test Exclude

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
        exclude:
          - os: windows-latest
            node-version: 16
          - os: macos-latest
            node-version: 16
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
```

### 5. Using Matrix Inclusions

**Example: Including specific configurations**:

```yaml
# .github/workflows/test-include.yml
name: Test Include

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [16, 18]
        include:
          - os: ubuntu-latest
            node-version: 20
            experimental: true
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
        continue-on-error: ${{ matrix.experimental || false }}
```

### 6. Using Matrix Variables

**Example: Using matrix variables**:

```yaml
# .github/workflows/test-variables.yml
name: Test Variables

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            node-version: 18
            python-version: '3.9'
          - os: windows-latest
            node-version: 18
            python-version: '3.9'
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install Node.js dependencies
        run: npm ci
      
      - name: Install Python dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: |
          npm test
          python -m pytest
```

### 7. Using Matrix for Deployment

**Example: Deploying to multiple environments**:

```yaml
# .github/workflows/deploy-matrix.yml
name: Deploy Matrix

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [staging, production]
        include:
          - environment: staging
            url: https://staging.example.com
          - environment: production
            url: https://example.com
    environment: ${{ matrix.environment }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Deploy to ${{ matrix.environment }}
        run: |
          echo "Deploying to ${{ matrix.environment }}"
          echo "URL: ${{ matrix.url }}"
          # Deployment commands
```

### 8. Using Matrix for Code Quality Checks

**Example: Running multiple code quality tools**:

```yaml
# .github/workflows/quality-matrix.yml
name: Quality Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        tool: [eslint, prettier, stylelint]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ${{ matrix.tool }}
        run: npx ${{ matrix.tool }} .
```

### 9. Using Matrix for Security Scanning

**Example: Running multiple security scanning tools**:

```yaml
# .github/workflows/security-matrix.yml
name: Security Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        tool: [trivy, snyk, sonarqube]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Run ${{ matrix.tool }}
        uses: ${{ matrix.tool }}-action@v1
        with:
          # Tool-specific configuration
```

### 10. Using Matrix for Performance Testing

**Example: Running multiple performance tests**:

```yaml
# .github/workflows/performance-matrix.yml
name: Performance Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  performance:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test: [load, stress, endurance]
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ${{ matrix.test }} test
        run: npm run test:${{ matrix.test }}
```

## Challenges

1. **Challenge 1**: Create a matrix strategy to test multiple Python versions
2. **Challenge 2**: Create a matrix strategy to deploy to multiple environments
3. **Challenge 3**: Create a matrix strategy to run multiple security scanning tools
4. **Challenge 4**: Create a matrix strategy to perform performance testing
5. **Challenge 5**: Create a matrix strategy to perform code quality checks

## Reflection

1. How does matrix strategy improve CI/CD efficiency?
2. How to balance the comprehensiveness of the matrix and execution time?
3. What are the limitations of matrix strategy?
4. How to optimize the cost of matrix strategy?

## Related Resources

- [GitHub Actions matrix strategy documentation](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions best practices](https://docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions)

---

**Previous: [Exercise 31: GitHub Copilot Advanced Usage](exercise-31-github-copilot-advanced.md) | Next: [Exercise 33: GitHub API Integration](exercise-33-github-api-integration.md)**

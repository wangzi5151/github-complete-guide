# Exercise 26: Creating Reusable GitHub Actions Workflows

## Learning Objectives

After completing this exercise, you will be able to:

- Understand the concept and advantages of reusable workflows
- Create reusable workflows triggered by `workflow_call`
- Call reusable workflows in multiple workflows
- Pass input parameters and secrets to reusable workflows
- Use output values from reusable workflows
- Share standardized CI/CD processes across an organization

## Prerequisites

- Have completed the relevant content of Exercises 1-25
- Have a GitHub repository with GitHub Actions enabled
- Understand the basic syntax of GitHub Actions workflows
- Be familiar with YAML format

## Background Knowledge

### What Are Reusable Workflows

Reusable workflows are a mechanism provided by GitHub Actions that allow you to encapsulate workflow logic as independent components that can be called by other workflows. This means you can:

1. **Avoid duplicate code**: Write common CI/CD logic once and use it across multiple repositories
2. **Standardize processes**: Ensure teams or organizations use consistent build, test, and deployment processes
3. **Simplify maintenance**: Updating one place affects all callers
4. **Improve efficiency**: New projects can quickly adopt mature CI/CD processes

### Limitations of Reusable Workflows

- A reusable workflow can call at most 4 levels of nested reusable workflows
- A reusable workflow can have at most 10 input parameters and 10 secrets
- A reusable workflow can have at most 10 output parameters
- Environment variables cannot be shared between reusable workflows and callers

---

## Exercise Steps

### Part 1: Creating a Basic Reusable Workflow

#### Step 1: Create the Reusable Workflow Directory Structure

First, create the necessary directory structure in your repository:

```bash
mkdir -p .github/workflows
```

#### Step 2: Create a Reusable Node.js Build Workflow

Create the file `.github/workflows/reusable-node-build.yml`:

```yaml
name: Reusable Node.js Build

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version'
        required: false
        type: string
        default: '18'
      working-directory:
        description: 'Working directory'
        required: false
        type: string
        default: '.'
      run-tests:
        description: 'Whether to run tests'
        required: false
        type: boolean
        default: true
      build-command:
        description: 'Build command'
        required: false
        type: string
        default: 'npm run build'
    secrets:
      NPM_TOKEN:
        description: 'NPM publish token'
        required: false
    outputs:
      build-artifact:
        description: 'Build artifact path'
        value: ${{ jobs.build.outputs.artifact-path }}
      test-result:
        description: 'Test result'
        value: ${{ jobs.build.outputs.test-result }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      artifact-path: ${{ steps.build.outputs.artifact-path }}
      test-result: ${{ steps.test.outputs.result }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
          cache-dependency-path: '${{ inputs.working-directory }}/package-lock.json'

      - name: Install dependencies
        working-directory: ${{ inputs.working-directory }}
        run: npm ci

      - name: Run linting
        working-directory: ${{ inputs.working-directory }}
        run: npm run lint --if-present

      - name: Run tests
        if: ${{ inputs.run-tests }}
        id: test
        working-directory: ${{ inputs.working-directory }}
        run: |
          npm test
          echo "result=passed" >> $GITHUB_OUTPUT

      - name: Build project
        id: build
        working-directory: ${{ inputs.working-directory }}
        run: |
          ${{ inputs.build-command }}
          echo "artifact-path=${{ inputs.working-directory }}/dist" >> $GITHUB_OUTPUT

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: ${{ inputs.working-directory }}/dist
          retention-days: 7
```

#### Step 3: Create a Reusable Python Build Workflow

Create the file `.github/workflows/reusable-python-build.yml`:

```yaml
name: Reusable Python Build

on:
  workflow_call:
    inputs:
      python-version:
        description: 'Python version'
        required: false
        type: string
        default: '3.11'
      working-directory:
        description: 'Working directory'
        required: false
        type: string
        default: '.'
      test-command:
        description: 'Test command'
        required: false
        type: string
        default: 'pytest'
      lint-command:
        description: 'Linting command'
        required: false
        type: string
        default: 'ruff check .'
    secrets:
      PYPI_TOKEN:
        description: 'PyPI publish token'
        required: false

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
          cache: 'pip'
          cache-dependency-path: '${{ inputs.working-directory }}/requirements*.txt'

      - name: Install dependencies
        working-directory: ${{ inputs.working-directory }}
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt || true

      - name: Run linting
        working-directory: ${{ inputs.working-directory }}
        run: ${{ inputs.lint-command }}

      - name: Run tests
        working-directory: ${{ inputs.working-directory }}
        run: ${{ inputs.test-command }}

      - name: Build package
        working-directory: ${{ inputs.working-directory }}
        run: |
          pip install build
          python -m build

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: python-dist
          path: ${{ inputs.working-directory }}/dist/
          retention-days: 7
```

### Part 2: Calling Reusable Workflows

#### Step 4: Create a Workflow That Calls the Node.js Reusable Workflow

Create the file `.github/workflows/ci.yml`:

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Call the reusable Node.js build workflow
  build-frontend:
    uses: ./.github/workflows/reusable-node-build.yml
    with:
      node-version: '20'
      working-directory: './frontend'
      run-tests: true
      build-command: 'npm run build:production'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

  # Call the reusable Node.js build workflow (backend)
  build-backend:
    uses: ./.github/workflows/reusable-node-build.yml
    with:
      node-version: '20'
      working-directory: './backend'
      run-tests: true
      build-command: 'npm run build'

  # Deploy using build artifacts
  deploy:
    needs: [build-frontend, build-backend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Display build info
        run: |
          echo "Frontend build path: ${{ needs.build-frontend.outputs.build-artifact }}"
          echo "Test result: ${{ needs.build-frontend.outputs.test-result }}"

      - name: Download frontend build artifact
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: ./deploy/frontend

      - name: Deploy to server
        run: |
          echo "Deploying frontend and backend..."
          # Actual deployment commands
```

#### Step 5: Create a Workflow That Calls the Python Reusable Workflow

Create the file `.github/workflows/python-ci.yml`:

```yaml
name: Python CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-api:
    uses: ./.github/workflows/reusable-python-build.yml
    with:
      python-version: '3.11'
      working-directory: './api'
      test-command: 'pytest --cov=api --cov-report=xml'
      lint-command: 'ruff check . && mypy .'
    secrets:
      PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}

  build-cli:
    uses: ./.github/workflows/reusable-python-build.yml
    with:
      python-version: '3.12'
      working-directory: './cli'
      test-command: 'pytest tests/ -v'
```

### Part 3: Using Reusable Workflows Across Repositories

#### Step 6: Create an Organization-Level Reusable Workflow Repository

Suppose you have an organization `my-org`, create a dedicated repository `shared-workflows`:

```
my-org/shared-workflows/
├── .github/
│   └── workflows/
│       ├── ci-node.yml
│       ├── ci-python.yml
│       ├── deploy-aws.yml
│       └── security-scan.yml
└── README.md
```

#### Step 7: Call Organization-Level Reusable Workflows from Other Repositories

Create `.github/workflows/ci.yml` in another repository:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  # Call the organization-level reusable workflow
  ci:
    uses: my-org/shared-workflows/.github/workflows/ci-node.yml@v1
    with:
      node-version: '20'
      run-tests: true
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

  # Call the organization-level deployment workflow
  deploy:
    needs: ci
    if: github.ref == 'refs/heads/main'
    uses: my-org/shared-workflows/.github/workflows/deploy-aws.yml@v1
    with:
      environment: production
      region: us-east-1
    secrets:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Part 4: Advanced Usage

#### Step 8: Create a Reusable Workflow with Conditional Execution

Create the file `.github/workflows/reusable-deploy.yml`:

```yaml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: string
      region:
        description: 'Deployment region'
        required: false
        type: string
        default: 'us-east-1'
      dry-run:
        description: 'Whether this is a dry run'
        required: false
        type: boolean
        default: false
    secrets:
      DEPLOY_KEY:
        required: true
    outputs:
      deployment-url:
        description: 'Deployment URL'
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    outputs:
      url: ${{ steps.deploy.outputs.url }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure deployment environment
        run: |
          echo "Deploying to ${{ inputs.environment }} environment"
          echo "Region: ${{ inputs.region }}"

      - name: Execute deployment
        id: deploy
        if: ${{ !inputs.dry-run }}
        run: |
          # Actual deployment logic
          DEPLOY_URL="https://${{ inputs.environment }}.example.com"
          echo "url=$DEPLOY_URL" >> $GITHUB_OUTPUT
          echo "Deployment complete: $DEPLOY_URL"

      - name: Simulate deployment
        if: ${{ inputs.dry-run }}
        run: echo "This is a dry run, no actual deployment"
```

#### Step 9: Create a Reusable Workflow with Matrix Strategy

Create the file `.github/workflows/reusable-multi-platform.yml`:

```yaml
name: Reusable Multi-Platform Build

on:
  workflow_call:
    inputs:
      platforms:
        description: 'Target platform list (JSON array)'
        required: false
        type: string
        default: '["ubuntu-latest", "windows-latest", "macos-latest"]'
      node-versions:
        description: 'Node.js version list (JSON array)'
        required: false
        type: string
        default: '["18", "20"]'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: ${{ fromJson(inputs.platforms) }}
        node-version: ${{ fromJson(inputs.node-versions) }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.os }}-node${{ matrix.node-version }}
          path: dist/
```

#### Step 10: Call the Matrix Reusable Workflow

Create the file `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  # Multi-platform build
  build:
    uses: ./.github/workflows/reusable-multi-platform.yml
    with:
      platforms: '["ubuntu-latest", "windows-latest", "macos-latest"]'
      node-versions: '["18", "20", "22"]'

  # Create release
  release:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Download all build artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: artifacts/**/*
          generate_release_notes: true
```

---

## Verify Exercise Results

### Checklist

After completing the exercise, verify the following:

- [ ] Reusable workflow files are created with correct syntax
- [ ] Caller workflows correctly reference reusable workflows
- [ ] Input parameters and secrets are passed correctly
- [ ] Output values can be accessed by callers
- [ ] Workflows run successfully in GitHub Actions

### Verification Commands

```bash
# Validate YAML syntax
yamllint .github/workflows/*.yml

# Check workflow syntax with actionlint
actionlint .github/workflows/*.yml

# Test locally (requires act)
act workflow_call -W .github/workflows/reusable-node-build.yml
```

---

## Advanced Challenges

### Challenge 1: Create a Complete CI/CD Reusable Workflow Suite

Create the following reusable workflow suite:

```yaml
# reusable-lint.yml - Code quality checks
# reusable-test.yml - Test execution
# reusable-build.yml - Build and packaging
# reusable-deploy.yml - Deployment and release
# reusable-notify.yml - Notification sending
```

### Challenge 2: Implement Versioned Reusable Workflows

Use Git tags to manage workflow versions:

```yaml
# Use a specific version in the caller
uses: my-org/shared-workflows/.github/workflows/ci.yml@v1.2.0

# Use a major version tag (automatically gets the latest patch)
uses: my-org/shared-workflows/.github/workflows/ci.yml@v1
```

### Challenge 3: Create Dynamic Reusable Workflows

Implement a reusable workflow that dynamically selects execution steps based on input:

```yaml
on:
  workflow_call:
    inputs:
      build-type:
        type: string
        # 'frontend', 'backend', 'mobile', 'all'

jobs:
  build:
    steps:
      - name: Frontend build
        if: inputs.build-type == 'frontend' || inputs.build-type == 'all'
        run: npm run build:frontend

      - name: Backend build
        if: inputs.build-type == 'backend' || inputs.build-type == 'all'
        run: npm run build:backend

      - name: Mobile build
        if: inputs.build-type == 'mobile' || inputs.build-type == 'all'
        run: npm run build:mobile
```

### Challenge 4: Implement Automatic Documentation Generation for Reusable Workflows

Create a script to automatically generate documentation from reusable workflow inputs, outputs, and secrets:

```bash
#!/bin/bash
# generate-workflow-docs.sh

for workflow in .github/workflows/reusable-*.yml; do
  echo "## $(basename $workflow .yml)"
  echo ""
  echo "### Input Parameters"
  yq '.on.workflow_call.inputs | to_entries | .[] | "- **\(.key)**: \(.value.description) (default: \(.value.default))"' "$workflow"
  echo ""
  echo "### Secrets"
  yq '.on.workflow_call.secrets | to_entries | .[] | "- **\(.key)**: \(.value.description)"' "$workflow"
  echo ""
done
```

---

## Reusable Workflow Design Patterns and Best Practices

### Design Pattern 1: Layered Architecture Pattern

In large organizations, it is recommended to adopt a layered architecture to organize reusable workflows. The bottom layer consists of base workflows responsible for fundamental operations such as code checkout, environment configuration, and cache management. The middle layer consists of domain workflows tailored to specific technology stacks, such as frontend build workflows, backend test workflows, or database migration workflows. The top layer consists of business workflows that combine multiple domain workflows to complete a full business process. This layered approach allows each layer to evolve and be maintained independently while ensuring code reusability and readability.

### Design Pattern 2: Template Method Pattern

Reusable workflows can define the skeleton of an algorithm, deferring the implementation of certain steps to the caller. For example, a general deployment workflow can define the standard process of checking out code, installing dependencies, running tests, building artifacts, and deploying to production, while the specific deployment step can be dynamically specified through input parameters. This approach ensures process consistency while allowing each project to customize configuration based on its own requirements.

### Design Pattern 3: Strategy Pattern

Different execution strategies can be selected through input parameters. For example, a test workflow can choose a unit test strategy, integration test strategy, or end-to-end test strategy based on input parameters. Each strategy corresponds to different test commands, environment configurations, and report formats. The caller only needs to specify the strategy name, and the workflow will automatically select the corresponding execution path.

### Naming Convention Recommendations

The naming of reusable workflows should follow clear and consistent principles. It is recommended to use the following naming format: first is a purpose prefix, such as `ci` for continuous integration, `cd` for continuous deployment, `test` for testing, `build` for building, `deploy` for deployment, and `notify` for notifications. Next is a technology stack identifier, such as `node`, `python`, `java`, `docker`, etc. Finally is an environment or variant identifier, such as `prod`, `staging`, `lite`, `full`, etc. Complete naming examples include `ci-node-standard.yml`, `deploy-aws-production.yml`, `test-python-integration.yml`, etc.

### Version Management Strategy

For organization-level reusable workflows, version management is critical. It is recommended to use semantic versioning, where the major version indicates incompatible breaking changes, the minor version indicates backward-compatible new features, and the patch version indicates backward-compatible bug fixes. Additionally, create a floating tag for each major version, such as `v1`, `v2`, so that callers can choose to use a fixed exact version or a floating major version. Document the changes for each version in detail in the release notes of the shared workflow repository to help team members understand the impact of upgrades.

### Security Considerations

The security of reusable workflows should not be overlooked. First, access to reusable workflows should be restricted to ensure only authorized personnel can modify shared workflows. Second, exercise extreme caution when using `secrets: inherit` to pass secrets, only passing necessary secrets. Third, validate input parameters of reusable workflows to prevent injection attacks. Fourth, regularly review and update shared workflows to ensure the latest Actions versions and security patches are used. Finally, establish a workflow review process at the organization level, requiring all changes to shared workflows to undergo code review and security review.

### Performance Optimization Tips

Optimizing the execution efficiency of reusable workflows can be approached from multiple aspects. Proper use of caching mechanisms can significantly reduce dependency installation time; it is recommended to cache the cache directories of package managers such as npm, pip, and Maven. Use matrix strategies to execute tasks in parallel, fully utilizing the concurrent execution capabilities provided by GitHub Actions. Set appropriate timeout values to prevent tasks from hanging for extended periods. Use conditional execution to skip unnecessary steps, such as running relevant tests only when specific files change. Optimize the size of build artifacts by uploading only necessary files, reducing upload and download time.

### Team Collaboration Recommendations

Promoting reusable workflows within a team requires establishing clear collaboration guidelines. Create a workflow contribution guide explaining how to create, test, and submit new reusable workflows. Establish workflow maintainer roles responsible for reviewing and merging workflow changes. Organize regular workflow sharing sessions to keep team members informed about available workflows and their usage. Establish a workflow usage feedback mechanism to collect issues encountered during use and improvement suggestions. Maintain a workflow catalog document listing all available reusable workflows along with their purposes, parameters, and usage examples.

### Monitoring and Alerting

The running status of reusable workflows needs continuous monitoring. It is recommended to configure email or instant messaging notifications for workflow run failures. Regularly check workflow run statistics, including success rates, average run times, and resource consumption. Set up run time alerts to notify relevant personnel promptly when workflow run times increase abnormally. Analyze workflow usage to identify the most frequently used workflows, prioritizing them for optimization and maintenance. Establish a workflow health metrics system to evaluate reliability, performance, security, and maintainability.

### Migration Strategy

Migrating existing duplicate workflows to reusable workflows requires a gradual approach. First, identify the most frequently duplicated workflow segments and prioritize extracting them. Second, create reusable workflows and validate them in a pilot project. Third, gradually switch other projects to using reusable workflows while retaining the old workflows as backups. Fourth, after verifying that all projects are running normally, delete the old workflows. Maintain communication with the team throughout the entire migration process to resolve any issues encountered promptly.

---

## Frequently Asked Questions

### Q1: What is the difference between reusable workflows and composite actions?

| Feature | Reusable Workflows | Composite Actions |
|---------|-------------------|-------------------|
| Trigger | `workflow_call` | `uses` in a step |
| Runtime | Independent job | Steps within the current job |
| Available Features | Full workflow capabilities | Limited step capabilities |
| Use Case | Complete CI/CD processes | Encapsulating multiple steps |

### Q2: How do I debug reusable workflows?

1. Use `workflow_dispatch` to manually trigger tests
2. Add debug output in the workflow
3. Use the `act` tool for local testing
4. Check GitHub Actions run logs

### Q3: What triggers do reusable workflows support?

Reusable workflows only support `workflow_call` as the trigger, but callers can use any trigger (push, pull_request, schedule, etc.).

### Q4: How do I share reusable workflows within an organization?

1. Create a dedicated shared workflow repository
2. Set the repository to public or allow organization access
3. Call using the `org/repo/.github/workflows/name.yml@ref` format
4. Use version tags to manage workflow versions

---

## Further Reading

- [GitHub Actions: Reusing workflows official documentation](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Sharing workflows with your organization](https://docs.github.com/en/actions/using-workflows/sharing-workflows-secrets-and-runners-with-your-organization)
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

## Exercise Summary

Through this exercise, you have learned:

1. ✅ Create reusable workflows triggered by `workflow_call`
2. ✅ Define input parameters, secrets, and output values
3. ✅ Call reusable workflows in multiple workflows
4. ✅ Share organization-level reusable workflows across repositories
5. ✅ Use advanced features such as matrix strategies and conditional execution

Reusable workflows are a powerful tool for implementing CI/CD standardization and automation. It is recommended to promote their use within teams to improve development efficiency and code quality.

# GitHub Workflow for Frontend Developers

> This document provides a complete GitHub workflow guide for frontend developers, covering repository management, CI/CD, automated testing, performance monitoring, code quality assurance, and other core aspects, helping frontend teams establish an efficient and standardized development process.

---

## Table of Contents

1. [Frontend Project GitHub Repository Structure](#1-frontend-project-github-repository-structure)
2. [Frontend Project CI/CD](#2-frontend-project-cicd)
3. [Static Website Deployment Solutions](#3-static-website-deployment-solutions)
4. [Frontend Automated Testing](#4-frontend-automated-testing)
5. [Lighthouse CI Automated Performance Testing](#5-lighthouse-ci-automated-performance-testing)
6. [Frontend Code Quality Tools](#6-frontend-code-quality-tools)
7. [Dependency Management and Security](#7-dependency-management-and-security)
8. [Storybook and Component Library Management](#8-storybook-and-component-library-management)
9. [Frontend Monorepo Management](#9-frontend-monorepo-management)
10. [npm/pnpm Package Publishing Workflow](#10-npmpnpm-package-publishing-workflow)
11. [Frontend Internationalization (i18n) Collaboration](#11-frontend-internationalization-i18n-collaboration)
12. [Design Mockups and Code Collaboration](#12-design-mockups-and-code-collaboration)
13. [GitHub Usage Experience for Domestic Frontend Teams](#13-github-usage-experience-for-domestic-frontend-teams)

---

## 1. Frontend Project GitHub Repository Structure

### 1.1 Standard Frontend Project Directory Structure

A well-structured frontend project repository should have a clear directory structure to facilitate team collaboration and automated tool integration. Below is a typical React project structure:

```
my-frontend-app/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # Continuous integration pipeline
│   │   ├── deploy.yml              # Deployment pipeline
│   │   ├── lighthouse.yml          # Performance testing pipeline
│   │   └── release.yml             # Release pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md           # Bug report template
│   │   └── feature_request.md      # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md    # PR template
│   ├── CODEOWNERS                  # Code owners configuration
│   └── dependabot.yml              # Dependency update configuration
├── src/
│   ├── components/                 # Shared components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   └── index.ts
│   ├── pages/                      # Page components
│   ├── hooks/                      # Custom hooks
│   ├── utils/                      # Utility functions
│   ├── services/                   # API service layer
│   ├── stores/                     # State management
│   ├── styles/                     # Global styles
│   ├── types/                      # TypeScript type definitions
│   ├── locales/                    # Internationalization resources
│   └── App.tsx
├── public/                         # Static assets
├── tests/                          # Test configuration and utilities
│   ├── setup.ts
│   └── mocks/
├── scripts/                        # Build and deployment scripts
├── docs/                           # Project documentation
├── .eslintrc.js                    # ESLint configuration
├── .prettierrc                     # Prettier configuration
├── .stylelintrc.js                 # Stylelint configuration
├── .lintstagedrc.js                # lint-staged configuration
├── tsconfig.json                   # TypeScript configuration
├── vite.config.ts                  # Vite build configuration
├── package.json
├── pnpm-lock.yaml
└── README.md
```

### 1.2 `.github` Directory Details

The `.github` directory is the core configuration directory for GitHub projects, containing workflows, templates, code review rules, and other key configurations.

**CODEOWNERS File Example:**

```
# Global code owners
*                       @frontend-team

# Component library maintained by specific members
/src/components/        @zhangsan @lisi

# Build configuration changes require architect approval
/vite.config.ts         @architect-wang
/tsconfig.json          @architect-wang
/.github/               @devops-team

# Internationalization files maintained by the translation team
/src/locales/           @i18n-team
```

**Issue Template Configuration (`.github/ISSUE_TEMPLATE/config.yml`):**

```yaml
blank_issues_enabled: false
contact_links:
  - name: Feature Discussion
    url: https://github.com/orgs/your-org/discussions
    about: Please discuss new feature ideas in Discussions
  - name: View Documentation
    url: https://your-docs-site.com
    about: View project documentation for help
```

### 1.3 Branch Management Strategy

Frontend projects are recommended to adopt Git Flow or Trunk-Based Development:

| Strategy | Use Case | Branch Model | Pros | Cons |
|------|---------|---------|------|------|
| Git Flow | Large projects, version releases | main/develop/feature/release/hotfix | Clear standards, suitable for multi-version parallel development | Complex process, frequent merge conflicts |
| Trunk-Based | Continuous deployment, small teams | main/feature-short-lived | Fast speed, fewer conflicts | Requires comprehensive automated testing |
| GitHub Flow | Simple projects, rapid iteration | main/feature | Simple and easy to learn | Not suitable for complex release processes |

**Git Flow Example:**

```bash
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/user-login

# Push after development is complete
git push origin feature/user-login

# Create PR on GitHub with target branch as develop
# Merge after Code Review passes

# Release process
git checkout -b release/v1.2.0 develop
# After fixing release-related issues
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags
```

### 1.4 Commit Standards

Frontend projects should strictly follow the Conventional Commits specification to facilitate CHANGELOG generation and automated version management:

```
<type>(<scope>): <subject>

[body]

[footer]
```

**Common type descriptions:**

| type | Description | Example |
|------|------|------|
| feat | New feature | `feat(login): Add WeChat QR code login` |
| fix | Bug fix | `fix(cart): Fix quantity selector overflow issue` |
| docs | Documentation update | `docs: Update API documentation` |
| style | Code formatting adjustment | `style: Standardize indentation to 2 spaces` |
| refactor | Code refactoring | `refactor(hooks): Extract common useRequest logic` |
| perf | Performance optimization | `perf(list): Optimize large data rendering with virtual list` |
| test | Test-related | `test(login): Add unit tests for login module` |
| chore | Build/tool changes | `chore: Upgrade vite to 5.0` |
| ci | CI configuration changes | `ci: Add Lighthouse CI checks` |
| revert | Rollback | `revert: Revert feat(login) WeChat login` |

**Using commitlint for automatic validation:**

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional husky
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'chore', 'ci', 'revert'
    ]],
    'scope-enum': [2, 'always', [
      'login', 'cart', 'product', 'user', 'order',
      'payment', 'common', 'config', 'deps'
    ]],
    'subject-max-length': [2, 'always', 100],
    'body-max-line-length': [1, 'always', 200],
  }
};
```

---

## 2. Frontend Project CI/CD

### 2.1 React Project GitHub Actions

**Complete React + TypeScript Project CI Pipeline:**

```yaml
# .github/workflows/ci.yml
name: React App CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '9'

jobs:
  lint:
    name: Code Linting
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: ESLint check
        run: pnpm eslint . --ext .ts,.tsx --format json --output-file eslint-report.json

      - name: Prettier check
        run: pnpm prettier --check "src/**/*.{ts,tsx,css,scss}"

      - name: Stylelint check
        run: pnpm stylelint "src/**/*.{css,scss}"

      - name: TypeScript type check
        run: pnpm tsc --noEmit

      - name: Upload check report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: lint-reports
          path: eslint-report.json

  test:
    name: Automated Testing
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run unit tests
        run: pnpm test -- --coverage --reporters=default --reporters=jest-junit
        env:
          JEST_JUNIT_OUTPUT_DIR: ./test-results

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          echo "Current code coverage: ${COVERAGE}%"
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "::warning::Code coverage ${COVERAGE}% is below threshold of 80%"
          fi

  build:
    name: Build Verification
    runs-on: ubuntu-latest
    needs: test
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install pnpm
        uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build project
        run: pnpm build
        env:
          NODE_ENV: production

      - name: Analyze build artifact size
        run: |
          echo "## Build Artifact Analysis" >> $GITHUB_STEP_SUMMARY
          echo "| File Type | Size | File Count |" >> $GITHUB_STEP_SUMMARY
          echo "|---------|------|---------|" >> $GITHUB_STEP_SUMMARY
          for ext in js css html json png jpg svg woff2; do
            SIZE=$(find dist -name "*.${ext}" -exec du -ch {} + 2>/dev/null | tail -1 | cut -f1)
            COUNT=$(find dist -name "*.${ext}" | wc -l)
            if [ "$COUNT" -gt 0 ]; then
              echo "| .${ext} | ${SIZE:-0} | ${COUNT} |" >> $GITHUB_STEP_SUMMARY
            fi
          done

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.node-version }}
          path: dist/
          retention-days: 7
```

### 2.2 Vue 3 Project GitHub Actions

```yaml
# .github/workflows/vue-ci.yml
name: Vue 3 App CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Vue type check (vue-tsc)
        run: pnpm vue-tsc --noEmit

      - name: ESLint
        run: pnpm eslint . --ext .vue,.ts,.tsx

      - name: Unit tests (Vitest)
        run: pnpm vitest run --coverage
        env:
          VITE_API_BASE_URL: https://test-api.example.com

      - name: Build
        run: pnpm build

      - name: Deploy preview (PR environment)
        if: github.event_name == 'pull_request'
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./
```

### 2.3 Angular Project GitHub Actions

```yaml
# .github/workflows/angular-ci.yml
name: Angular App CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      - name: Lint
        run: npx ng lint

      - name: Unit tests (Karma)
        run: npx ng test --watch=false --code-coverage --browsers=ChromeHeadless

      - name: E2E tests (Playwright)
        run: npx playwright install --with-deps chromium && npx ng e2e

      - name: Build
        run: npx ng build --configuration=production

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          directory: ./coverage
          token: ${{ secrets.CODECOV_TOKEN }}
```

### 2.4 Svelte/SvelteKit Project GitHub Actions

```yaml
# .github/workflows/sveltekit-ci.yml
name: SvelteKit CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Svelte Check
        run: pnpm svelte-kit sync && pnpm svelte-check

      - name: Lint
        run: pnpm lint

      - name: Test (Vitest)
        run: pnpm test -- --coverage

      - name: Build
        run: pnpm build

      - name: Adapter verification
        run: ls -la build/
```

### 2.5 Complete CI/CD Pipeline Design for Frontend Projects

A mature frontend project CI/CD pipeline should include the following stages:

```
Code Commit → Code Linting → Unit Testing → Build Verification → E2E Testing → Preview Deployment → Production Deployment → Monitoring
```

**Responsibilities of each stage:**

| Stage | Tools | Duration | Failure Handling |
|------|------|------|---------|
| Code Linting | ESLint/Prettier/Stylelint | 1-2 minutes | Block merge |
| Unit Testing | Jest/Vitest | 2-5 minutes | Block merge |
| Build Verification | Vite/Webpack | 2-4 minutes | Block merge |
| E2E Testing | Playwright/Cypress | 5-15 minutes | Block merge (optional) |
| Preview Deployment | Vercel/Netlify | 1-3 minutes | Alert notification |
| Production Deployment | GitHub Actions | 3-10 minutes | Automatic rollback |
| Monitoring | Sentry/Lighthouse | Continuous | Alert notification |

---

## 3. Static Website Deployment Solutions

### 3.1 GitHub Pages Deployment

GitHub Pages is the simplest free static website hosting solution, suitable for personal projects, documentation sites, and small applications.

**Basic deployment configuration:**

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm build

      - name: Configure GitHub Pages
        uses: actions/configure-pages@v4

      - name: Upload build artifacts
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**SPA Route Handling (Vue Router / React Router):**

Since GitHub Pages does not support server-side routing, SPA applications need special handling:

```yaml
# Create 404.html after build to handle SPA routing
- name: SPA route handling
  run: |
    cp dist/index.html dist/404.html
```

Or use the `spa-github-pages` solution, adding a redirect script in `index.html`.

**Custom Domain Configuration:**

```yaml
# Configure custom domain in repository Settings > Pages
# Or auto-configure in the build step
- name: Configure custom domain
  if: github.ref == 'refs/heads/main'
  run: |
    echo "www.example.com" > dist/CNAME
```

### 3.2 Vercel Deployment

Vercel is one of the most popular deployment platforms for frontend projects, offering an excellent developer experience.

**Auto-deployment configuration:**

```json
// vercel.json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://api.example.com/$1" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

**GitHub Actions and Vercel Integration:**

```yaml
# .github/workflows/vercel-deploy.yml
name: Vercel Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel environment configuration
        run: vercel pull --yes --environment=${{ github.ref == 'refs/heads/main' && 'production' || 'preview' }} --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build
        run: vercel build --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy
        id: deploy
        run: |
          if [ "${{ github.ref }}" = "refs/heads/main" ]; then
            url=$(vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }})
          else
            url=$(vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }})
          fi
          echo "url=$url" >> $GITHUB_OUTPUT

      - name: Comment PR deployment link
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 Preview deployment: ${{ steps.deploy.outputs.url }}`
            })
```

### 3.3 Netlify Deployment

```yaml
# .github/workflows/netlify-deploy.yml
name: Netlify Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile && pnpm build

      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v3
        with:
          publish-dir: ./dist
          production-deploy: ${{ github.ref == 'refs/heads/main' }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Deploy from GitHub Actions - ${{ github.sha }}"
          netlify-config-path: ./netlify.toml
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

**Netlify configuration file:**

```toml
# netlify.toml
[build]
  command = "pnpm build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[plugins]]
  package = "@netlify/plugin-lighthouse"
```

### 3.4 Cloudflare Pages Deployment

Cloudflare Pages provides global CDN and Workers support, suitable for performance-demanding projects.

```yaml
# .github/workflows/cloudflare-pages.yml
name: Cloudflare Pages Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile && pnpm build

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy dist --project-name=my-app
```

### 3.5 Deployment Solution Comparison

| Feature | GitHub Pages | Vercel | Netlify | Cloudflare Pages |
|------|-------------|--------|---------|-----------------|
| Free Quota | 100GB/month | 100GB/month | 100GB/month | Unlimited bandwidth |
| Build Time | Requires self-built CI | 6000 minutes/month | 300 minutes/month | 500 runs/month |
| Custom Domain | Supported | Supported | Supported | Supported |
| SSL Certificate | Automatic | Automatic | Automatic | Automatic |
| Serverless | Not supported | Supported | Supported | Workers |
| Preview Deployment | Not supported | Supported | Supported | Supported |
| Domestic Access | Slower | Slower | Slower | Faster |
| Suitable Scenarios | Documentation/Blogs | Full-stack applications | Static sites | Globalized applications |

---

## 4. Frontend Automated Testing

### 4.1 Jest Unit Testing

Jest is the most popular testing framework in the React ecosystem, also widely used in Vue and Angular projects.

**Jest configuration example:**

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterSetup: ['<rootDir>/tests/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/tests/__mocks__/fileMock.js',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/main.tsx',
  ],
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

**React component test example:**

```typescript
// src/components/UserCard/UserCard.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { UserCard } from './UserCard';
import { fetchUser } from '@/services/user';

vi.mock('@/services/user');

const mockUser = {
  id: '1',
  name: '张三',
  email: 'zhangsan@example.com',
  avatar: 'https://example.com/avatar.jpg',
};

describe('UserCard', () => {
  beforeEach(() => {
    vi.mocked(fetchUser).mockResolvedValue(mockUser);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should render user information correctly', async () => {
    render(<UserCard userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('张三')).toBeInTheDocument();
      expect(screen.getByText('zhangsan@example.com')).toBeInTheDocument();
    });
  });

  it('should show loading state', () => {
    render(<UserCard userId="1" />);
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('should handle loading failure', async () => {
    vi.mocked(fetchUser).mockRejectedValue(new Error('Network error'));

    render(<UserCard userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load')).toBeInTheDocument();
    });
  });

  it('should trigger callback when button is clicked', async () => {
    const onEdit = vi.fn();
    render(<UserCard userId="1" onEdit={onEdit} />);

    await waitFor(() => {
      expect(screen.getByText('张三')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }));
    expect(onEdit).toHaveBeenCalledWith(mockUser);
  });
});
```

### 4.2 Cypress E2E Testing

```javascript
// cypress/e2e/login.cy.ts
describe('Login functionality', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should display login form', () => {
    cy.get('[data-testid="login-form"]').should('be.visible');
    cy.get('input[name="username"]').should('exist');
    cy.get('input[name="password"]').should('exist');
    cy.get('button[type="submit"]').should('contain', 'Login');
  });

  it('should show validation errors on empty form submission', () => {
    cy.get('button[type="submit"]').click();
    cy.get('.error-message').should('have.length', 2);
    cy.get('.error-message').first().should('contain', 'Please enter username');
  });

  it('should login successfully and redirect', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 200,
      body: { token: 'fake-jwt-token', user: { name: 'Test User' } },
    }).as('loginRequest');

    cy.get('input[name="username"]').type('testuser');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    cy.wait('@loginRequest');
    cy.url().should('include', '/dashboard');
    cy.get('.user-name').should('contain', 'Test User');
  });

  it('should show error message on login failure', () => {
    cy.intercept('POST', '/api/auth/login', {
      statusCode: 401,
      body: { message: 'Invalid username or password' },
    });

    cy.get('input[name="username"]').type('wronguser');
    cy.get('input[name="password"]').type('wrongpass');
    cy.get('button[type="submit"]').click();

    cy.get('.alert-error').should('contain', 'Invalid username or password');
  });
});
```

### 4.3 Playwright E2E Testing

Playwright is a next-generation E2E testing tool that supports multiple browsers, automatic waiting, and better debugging experience.

```typescript
// tests/e2e/shopping.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Shopping flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('browse products and add to cart', async ({ page }) => {
    // Browse product list
    await page.getByRole('link', { name: 'Product List' }).click();
    await expect(page.getByTestId('product-list')).toBeVisible();

    // Click first product
    const firstProduct = page.getByTestId('product-card').first();
    const productName = await firstProduct.getByTestId('product-name').textContent();
    await firstProduct.click();

    // Add to cart
    await page.getByRole('button', { name: 'Add to Cart' }).click();

    // Verify cart count
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // Verify cart content
    await page.getByTestId('cart-icon').click();
    await expect(page.getByTestId('cart-item')).toContainText(productName!);
  });

  test('complete checkout flow', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.getByLabel('Username').fill('testuser');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();
    await expect(page.getByText('Welcome back')).toBeVisible();

    // Add product
    await page.goto('/products/1');
    await page.getByRole('button', { name: 'Add to Cart' }).click();

    // Checkout
    await page.getByRole('button', { name: 'Go to Checkout' }).click();
    await expect(page).toHaveURL('/checkout');

    // Fill in shipping address
    await page.getByLabel('Recipient').fill('John Doe');
    await page.getByLabel('Phone').fill('13800138000');
    await page.getByLabel('Detailed Address').fill('123 Main Street, Chaoyang District, Beijing');

    // Submit order
    await page.getByRole('button', { name: 'Submit Order' }).click();
    await expect(page.getByText('Order submitted successfully')).toBeVisible();
  });

  test('page performance verification', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;

    expect(loadTime).toBeLessThan(3000);

    // Verify core Web Vitals
    const metrics = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          resolve(entries.map((e) => ({ name: e.name, value: e.value })));
        }).observe({ type: 'largest-contentful-paint', buffered: true });
      });
    });
    console.log('Performance metrics:', metrics);
  });
});
```

**Playwright configuration file:**

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/e2e-results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## 5. Lighthouse CI Automated Performance Testing

### 5.1 Basic Lighthouse CI Configuration

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile && pnpm build

      - name: Start local server
        run: pnpm preview &
        env:
          PORT: 4173

      - name: Wait for server to be ready
        run: npx wait-on http://localhost:4173 --timeout 30000

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v12
        with:
          urls: |
            http://localhost:4173/
            http://localhost:4173/login
            http://localhost:4173/products
          configPath: .lighthouserc.json
          uploadArtifacts: true
          temporaryPublicStorage: true
```

**Lighthouse CI configuration file:**

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "settings": {
        "preset": "desktop",
        "chromeFlags": "--no-sandbox --headless"
      }
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.8 }],
        "categories:accessibility": ["warn", { "minScore": 0.9 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }],
        "categories:seo": ["warn", { "minScore": 0.9 }],
        "first-contentful-paint": ["warn", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 300 }]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### 5.2 Lighthouse CI and PR Comment Integration

```yaml
- name: Run Lighthouse CI and comment
  uses: treosh/lighthouse-ci-action@v12
  id: lighthouse
  with:
    urls: |
      http://localhost:4173/
    uploadArtifacts: true

- name: Generate Lighthouse report comment
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const results = JSON.parse(fs.readFileSync('${{ steps.lighthouse.outputs.manifest }}', 'utf8'));

      let comment = '## 🔦 Lighthouse Performance Report\n\n';
      comment += '| Page | Performance | Accessibility | Best Practices | SEO |\n';
      comment += '|------|------|---------|---------|----|\n';

      for (const result of results) {
        const summary = result.summary;
        const url = result.url;
        const perf = (summary.performance * 100).toFixed(0);
        const a11y = (summary.accessibility * 100).toFixed(0);
        const bp = (summary['best-practices'] * 100).toFixed(0);
        const seo = (summary.seo * 100).toFixed(0);

        const score = (s) => s >= 90 ? '🟢' : s >= 50 ? '🟠' : '🔴';
        comment += `| ${url} | ${score(summary.performance)} ${perf} | ${score(summary.accessibility)} ${a11y} | ${score(summary['best-practices'])} ${bp} | ${score(summary.seo)} ${seo} |\n`;
      }

      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

---

## 6. Frontend Code Quality Tools

### 6.1 ESLint Configuration

Modern frontend projects are recommended to use ESLint Flat Config format:

```javascript
// eslint.config.js
import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import importPlugin from 'eslint-plugin-import';
import prettierConfig from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      'react': reactPlugin,
      'react-hooks': reactHooksPlugin,
      'import': importPlugin,
    },
    rules: {
      // TypeScript rules
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',

      // React rules
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',

      // Import rules
      'import/order': ['error', {
        groups: ['builtin', 'external', 'internal', 'parent', 'sibling', 'index'],
        'newlines-between': 'always',
        alphabetize: { order: 'asc' },
      }],

      // General rules
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'prefer-const': 'error',
      'no-var': 'error',
    },
    settings: {
      react: { version: 'detect' },
    },
  },
  prettierConfig,
];
```

### 6.2 Prettier Configuration

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100,
  "bracketSpacing": true,
  "arrowParens": "always",
  "endOfLine": "lf",
  "plugins": ["prettier-plugin-tailwindcss"],
  "overrides": [
    {
      "files": "*.md",
      "options": { "printWidth": 80 }
    }
  ]
}
```

### 6.3 Stylelint Configuration

```javascript
// .stylelintrc.js
module.exports = {
  extends: [
    'stylelint-config-standard',
    'stylelint-config-standard-scss',
    'stylelint-config-prettier',
  ],
  rules: {
    'selector-class-pattern': '^[a-z][a-zA-Z0-9]+$',
    'no-empty-source': null,
    'scss/operator-no-newline-after': null,
    'declaration-block-no-redundant-longhand-properties': null,
  },
};
```

### 6.4 Husky + lint-staged Configuration

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{css,scss}": [
      "stylelint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

### 6.5 Code Quality Checks in GitHub Actions

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Check code formatting
        run: |
          pnpm eslint . --format json --output-file eslint.json || true
          pnpm prettier --check "src/**/*" || true

      - name: Code quality report
        uses: actions/github-script@v7
        if: always()
        with:
          script: |
            const fs = require('fs');
            try {
              const eslintResults = JSON.parse(fs.readFileSync('eslint.json', 'utf8'));
              const errors = eslintResults.reduce((sum, f) => sum + f.errorCount, 0);
              const warnings = eslintResults.reduce((sum, f) => sum + f.warningCount, 0);

              let report = `## 📊 Code Quality Report\n\n`;
              report += `- ❌ Errors: ${errors}\n`;
              report += `- ⚠️ Warnings: ${warnings}\n`;
              report += `- 📁 Files checked: ${eslintResults.length}\n`;

              if (errors > 0) {
                report += `\n### Error Details\n`;
                for (const file of eslintResults.filter(f => f.errorCount > 0)) {
                  report += `\n**${file.filePath}**\n`;
                  for (const msg of file.messages.filter(m => m.severity === 2)) {
                    report += `- L${msg.line}: ${msg.message} (${msg.ruleId})\n`;
                  }
                }
              }

              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: report
              });
            } catch (e) {
              console.log('Failed to generate report:', e.message);
            }
```

---

## 7. Dependency Management and Security

### 7.1 Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "Asia/Shanghai"
    open-pull-requests-limit: 10
    reviewers:
      - "frontend-team"
    labels:
      - "dependencies"
      - "automated"
    groups:
      react:
        patterns:
          - "react*"
          - "@types/react*"
      testing:
        patterns:
          - "jest*"
          - "@testing-library/*"
          - "vitest*"
          - "playwright*"
      build:
        patterns:
          - "vite*"
          - "esbuild*"
          - "rollup*"
      lint:
        patterns:
          - "eslint*"
          - "prettier*"
          - "stylelint*"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "ci"
      - "dependencies"
```

### 7.2 Renovate Configuration

Renovate is an alternative to Dependabot, offering more customization options:

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:best-practices",
    ":semanticCommits"
  ],
  "schedule": ["before 9am on monday"],
  "timezone": "Asia/Shanghai",
  "labels": ["dependencies"],
  "reviewers": ["team:frontend"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "matchPackagePatterns": ["^@testing-library"],
      "groupName": "testing libraries",
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^react"],
      "groupName": "React"
    },
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

### 7.3 Dependency Security Auditing

```yaml
# .github/workflows/security.yml
name: Dependency Security

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  push:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Security audit
        run: pnpm audit --json > audit-report.json || true

      - name: Check licenses
        run: |
          pnpm add -D license-checker
          npx license-checker --json --out licenses.json
          # Check for GPL or AGPL licenses
          node -e "
            const licenses = require('./licenses.json');
            const problematic = Object.entries(licenses)
              .filter(([_, info]) => /GPL|AGPL/.test(info.licenses));
            if (problematic.length > 0) {
              console.error('Found restricted licenses:');
              problematic.forEach(([pkg, info]) => {
                console.error('  ' + pkg + ': ' + info.licenses);
              });
              process.exit(1);
            }
          "

      - name: Create Issue (when vulnerability found)
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('audit-report.json', 'utf8'));

            let body = '## 🔒 Dependency Security Vulnerability Report\n\n';
            body += `Found ${report.metadata.vulnerabilities.total} vulnerabilities\n\n`;
            body += '| Severity | Count |\n|---------|------|\n';

            const vulns = report.metadata.vulnerabilities;
            body += `| 🔴 Critical | ${vulns.critical} |\n`;
            body += `| 🟠 High | ${vulns.high} |\n`;
            body += `| 🟡 Moderate | ${vulns.moderate} |\n`;
            body += `| 🟢 Low | ${vulns.low} |\n`;

            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '🔒 Dependency Security Vulnerability Found',
              body: body,
              labels: ['security', 'dependencies']
            });
```

---

## 8. Storybook and Component Library Management

### 8.1 Storybook Basic Configuration

```yaml
# .github/workflows/storybook.yml
name: Storybook

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-storybook:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build Storybook
        run: pnpm build-storybook

      - name: Deploy Storybook to Chromatic
        if: github.event_name == 'push'
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
          exitOnceUploaded: true

      - name: PR preview deployment
        if: github.event_name == 'pull_request'
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
          exitZeroOnChanges: true
```

### 8.2 Storybook Component Documentation Example

```typescript
// src/components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'danger'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    isLoading: { control: 'boolean' },
    isDisabled: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    children: 'Secondary Button',
    variant: 'secondary',
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading...',
    variant: 'primary',
    isLoading: true,
  },
};

export const AllSizes: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
      <Button size="sm">Small Button</Button>
      <Button size="md">Medium Button</Button>
      <Button size="lg">Large Button</Button>
    </div>
  ),
};
```

### 8.3 Visual Regression Testing

```yaml
# .github/workflows/visual-test.yml
name: Visual Regression Test

on: [pull_request]

jobs:
  visual-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Run visual regression test
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
          onlyChanged: true
          diagnostics: true
```

---

## 9. Frontend Monorepo Management

### 9.1 Turborepo Configuration

```yaml
# .github/workflows/monorepo-ci.yml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Turborepo requires full git history

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build (only changed packages)
        run: pnpm turbo build --filter=...[origin/main]

      - name: Test (only changed packages)
        run: pnpm turbo test --filter=...[origin/main]

      - name: Lint (only changed packages)
        run: pnpm turbo lint --filter=...[origin/main]

      - name: Change detection report
        run: |
          echo "## 📦 Changed Package Analysis" >> $GITHUB_STEP_SUMMARY
          CHANGED=$(pnpm turbo --filter=...[origin/main] --dry=json 2>/dev/null | jq -r '.packages[]' || echo "Unable to detect")
          echo "Changed packages: $CHANGED" >> $GITHUB_STEP_SUMMARY
```

**Turborepo configuration file:**

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "inputs": ["src/**", "tests/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### 9.2 Nx Configuration

```yaml
# .github/workflows/nx-ci.yml
name: Nx Monorepo CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Nx affected projects
        run: npx nx affected -t lint test build --base=origin/main --head=HEAD

      - name: Nx Cloud distributed caching
        run: npx nx run-many -t build --parallel=3
        env:
          NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}
```

### 9.3 Monorepo Package Publishing

```yaml
# .github/workflows/monorepo-release.yml
name: Monorepo Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - run: pnpm install --frozen-lockfile

      - name: Create Release PR
        uses: changesets/action@v1
        with:
          publish: pnpm release
          version: pnpm changeset version
          title: "chore: version release"
          commit: "chore: version release"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## 10. npm/pnpm Package Publishing Workflow

### 10.1 Automated Package Publishing

```yaml
# .github/workflows/publish.yml
name: Publish Package

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - run: pnpm install --frozen-lockfile

      - name: Run tests
        run: pnpm test

      - name: Build
        run: pnpm build

      - name: Publish to npm
        run: pnpm publish --no-git-checks --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Publish to GitHub Packages
        run: pnpm publish --no-git-checks --access public --registry https://npm.pkg.github.com
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 10.2 Semantic Versioning Management

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install semantic-release
        run: npm install -g semantic-release @semantic-release/changelog @semantic-release/git

      - name: Execute release
        run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**semantic-release configuration:**

```javascript
// .releaserc.js
module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    '@semantic-release/changelog',
    '@semantic-release/npm',
    '@semantic-release/github',
    ['@semantic-release/git', {
      assets: ['CHANGELOG.md', 'package.json'],
      message: 'chore(release): ${nextRelease.version} [skip ci]',
    }],
  ],
};
```

---

## 11. Frontend Internationalization (i18n) Collaboration

### 11.1 Internationalization Resource Management

```yaml
# .github/workflows/i18n.yml
name: i18n Management

on:
  push:
    branches: [main]
    paths:
      - 'src/locales/**'

jobs:
  validate-translations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check translation completeness
        run: |
          node scripts/check-translations.js

      - name: Check translation format
        run: |
          pnpm i18next-parser src/**/*.{ts,tsx} --config i18next-parser.config.js
          git diff --exit-code src/locales/ || (echo "Translation files have unprocessed keys" && exit 1)

  sync-translations:
    runs-on: ubuntu-latest
    needs: validate-translations
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Sync translations to Crowdin
        uses: crowdin/github-action@v1
        with:
          upload_sources: true
          upload_translations: false
          download_translations: true
          create_pull_request: true
          pull_request_title: 'chore(i18n): Update translation files'
          pull_request_labels: 'i18n'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_PERSONAL_TOKEN }}
```

### 11.2 Translation Completeness Check Script

```javascript
// scripts/check-translations.js
const fs = require('fs');
const path = require('path');

const LOCALES_DIR = path.join(__dirname, '../src/locales');
const BASE_LANG = 'zh-CN';
const TARGET_LANGS = ['en-US', 'ja-JP'];

function loadTranslations(lang) {
  const filePath = path.join(LOCALES_DIR, `${lang}.json`);
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function getKeys(obj, prefix = '') {
  let keys = [];
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (typeof value === 'object' && value !== null) {
      keys = keys.concat(getKeys(value, fullKey));
    } else {
      keys.push(fullKey);
    }
  }
  return keys;
}

const baseTranslations = loadTranslations(BASE_LANG);
const baseKeys = getKeys(baseTranslations).sort();

let hasError = false;

for (const lang of TARGET_LANGS) {
  const translations = loadTranslations(lang);
  const langKeys = getKeys(translations).sort();

  const missing = baseKeys.filter((k) => !langKeys.includes(k));
  const extra = langKeys.filter((k) => !baseKeys.includes(k));

  if (missing.length > 0) {
    console.error(`❌ ${lang} is missing the following translation keys:`);
    missing.forEach((k) => console.error(`   - ${k}`));
    hasError = true;
  }

  if (extra.length > 0) {
    console.warn(`⚠️ ${lang} has extra translation keys:`);
    extra.forEach((k) => console.warn(`   - ${k}`));
  }

  console.log(`✅ ${lang}: ${langKeys.length}/${baseKeys.length} translation keys`);
}

if (hasError) {
  process.exit(1);
}

console.log('\n🎉 All translation files are complete!');
```

---

## 12. Design Mockups and Code Collaboration

### 12.1 Figma + GitHub Integration Workflow

```yaml
# .github/workflows/design-sync.yml
name: Design Sync

on:
  issues:
    types: [labeled]

jobs:
  design-review:
    if: contains(github.event.label.name, 'design-review')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract Figma link
        id: figma
        uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.issue.body;
            const figmaRegex = /https:\/\/www\.figma\.com\/file\/[^\s]+/g;
            const links = body.match(figmaRegex) || [];
            return links[0] || '';

      - name: Sync design tokens
        run: |
          # Export design tokens from Figma
          npx style-dictionary build --config design-tokens.config.js

      - name: Create design spec PR
        if: steps.figma.outputs.result != ''
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'design: Sync design tokens'
          body: |
            Automatically synced design token changes from Figma.
            Figma link: ${{ steps.figma.outputs.result }}
          branch: design/token-sync
          labels: design, automated
```

### 12.2 Design Token Management

```javascript
// design-tokens.config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'src/styles/tokens/',
      files: [
        {
          destination: '_variables.css',
          format: 'css/variables',
          options: {
            outputReferences: true,
          },
        },
      ],
    },
    scss: {
      transformGroup: 'scss',
      buildPath: 'src/styles/tokens/',
      files: [
        {
          destination: '_variables.scss',
          format: 'scss/variables',
        },
      ],
    },
    js: {
      transformGroup: 'js',
      buildPath: 'src/styles/tokens/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6',
        },
      ],
    },
  },
};
```

---

## 13. GitHub Usage Experience for Domestic Frontend Teams

### 13.1 Network Acceleration Solutions

Accessing GitHub from China often encounters slow speeds. Here are several solutions:

**Solution 1: Using GitHub Actions Mirror Acceleration**

```yaml
# Use domestic npm mirror
- name: Set npm mirror
  run: |
    pnpm config set registry https://registry.npmmirror.com

# Use domestic pip mirror (if using Python tools)
- name: Set pip mirror
  run: |
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**Solution 2: Using Gitee Mirror Sync**

```yaml
# .github/workflows/mirror.yml
name: Mirror to Gitee

on:
  push:
    branches: [main]

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Sync to Gitee
        uses: wearerequired/git-mirror-action@master
        env:
          SSH_PRIVATE_KEY: ${{ secrets.GITEE_RSA_PRIVATE_KEY }}
        with:
          source-repo: git@github.com:your-org/your-repo.git
          destination-repo: git@gitee.com:your-org/your-repo.git
```

**Solution 3: GitHub Proxy Acceleration**

```yaml
# Use proxy in CI
- name: Set Git proxy
  run: |
    git config --global http.proxy http://your-proxy:port
    git config --global https.proxy http://your-proxy:port
```

### 13.2 Domestic Deployment Solution Integration

```yaml
# .github/workflows/deploy-china.yml
name: Deploy to China

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
          registry-url: 'https://registry.npmmirror.com'

      - run: pnpm install --frozen-lockfile
      - run: pnpm build

      - name: Upload to Alibaba Cloud OSS
        uses: manyuanrong/setup-ossutil@v3.0
        with:
          access-key-id: ${{ secrets.ALIYUN_ACCESS_KEY_ID }}
          access-key-secret: ${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}
          endpoint: oss-cn-hangzhou.aliyuncs.com
          bucket: your-bucket-name

      - name: Deploy to OSS
        run: |
          ossutil cp -r dist/ oss://your-bucket-name/ --update
          ossutil set-meta oss://your-bucket-name/ --update \
            --header "Cache-Control:public,max-age=31536000" \
            --include "*.js" --include "*.css"

      - name: Refresh CDN cache
        run: |
          # Use Alibaba Cloud CDN API to refresh cache
          aliyun cdn RefreshObjectCaches \
            --ObjectPath "https://www.example.com/" \
            --ObjectType "Directory"

  deploy-to-tencent:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to Tencent Cloud COS
        uses: zkqiang/tencent-cos-action@v1.0.0
        with:
          args: delete -r -f / && upload -r dist/ /
          secret_id: ${{ secrets.TENCENT_SECRET_ID }}
          secret_key: ${{ secrets.TENCENT_SECRET_KEY }}
          bucket: your-bucket-name
          region: ap-guangzhou

      - name: Refresh Tencent Cloud CDN
        run: |
          pip install coscmd
          coscmd refresh-cdn --url "https://www.example.com/*"
```

### 13.3 Best Practices for Domestic Frontend Teams

**1. Code Standards Unification**

```json
// .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
```

**2. Team Collaboration Standards Document Template**

```markdown
# Frontend Team GitHub Collaboration Standards

## Branch Naming Standards
- Feature branches: `feature/requirement-number-short-description`
- Fix branches: `fix/bug-number-short-description`
- Hotfix: `hotfix/issue-description`

## PR Standards
1. Title format: `type(scope): description`
2. Must link to Issue
3. Must pass CI checks
4. At least 2 people Code Review
5. Use PR template to fill in change description

## Code Review Focus Points
- Whether code style conforms to standards
- Whether there are potential performance issues
- Whether there are security risks
- Whether tests are sufficient
- Whether documentation is updated
```

**3. Domestic CI/CD Optimization**

| Optimization Item | Solution | Effect |
|--------|------|------|
| npm install speed | Use npmmirror | 5-10x speedup |
| Docker images | Use Alibaba Cloud image registry | 3-5x speedup |
| Build cache | GitHub Actions Cache | 50% build time reduction |
| Parallel testing | Sharded testing + parallel execution | 60% test time reduction |
| Incremental builds | Turborepo/Nx caching | 70% build time reduction |

### 13.4 Common Issues and Solutions

**Issue 1: GitHub Actions dependency download timeout**

```yaml
# Solution: Increase timeout and add retry mechanism
- name: Install dependencies
  run: |
    for i in 1 2 3; do
      pnpm install --frozen-lockfile && break
      echo "Attempt $i failed, waiting 10 seconds before retrying..."
      sleep 10
    done
  timeout-minutes: 15
```

**Issue 2: Git LFS large file transfer slow**

```yaml
# Solution: Use CDN to host static assets
- name: Upload static assets to CDN
  run: |
    # Upload large files to CDN, Git repository only stores references
    curl -T dist/assets/vendor.js \
      -H "Authorization: ${{ secrets.CDN_TOKEN }}" \
      https://cdn.example.com/upload/
```

**Issue 3: Frequent multi-team collaboration conflicts**

```yaml
# Solution: Use CODEOWNERS + required reviews
# .github/CODEOWNERS
/src/components/  @component-team
/src/pages/       @page-team
/src/services/    @backend-team
/.github/         @devops-team
```

### 13.5 Recommended Toolchain Combinations

| Project Type | Package Manager | Build Tool | Testing Framework | Deployment Platform |
|---------|---------|---------|---------|---------|
| React SPA | pnpm | Vite | Vitest + Playwright | Vercel |
| Vue 3 Project | pnpm | Vite | Vitest + Cypress | Netlify |
| Next.js Project | pnpm | Next.js | Jest + Playwright | Vercel |
| Nuxt Project | pnpm | Nuxt | Vitest + Playwright | Cloudflare Pages |
| Component Library | pnpm | Vite/Storybook | Vitest + Chromatic | npm + Storybook |
| Monorepo | pnpm | Turborepo | Vitest | Independent deployment per platform |
| Documentation Site | pnpm | VitePress | - | GitHub Pages |

---

## Summary

This document covers the complete GitHub workflow for frontend developers to collaborate efficiently. From repository structure design, CI/CD pipeline setup, automated testing, performance monitoring to code quality assurance, each aspect provides detailed configuration examples and best practices.

**Key Takeaways:**

1. **Automation First**: Fully automate code linting, testing, building, and deployment to reduce manual operations
2. **Quality Gates**: Set up quality gates through CI pipelines to ensure code quality
3. **Security First**: Use Dependabot/Renovate to manage dependency security
4. **Team Collaboration**: Improve collaboration efficiency through CODEOWNERS, PR templates, and Commit standards
5. **Domestic Optimization**: Use mirror acceleration, CDN deployment, and other solutions to optimize domestic usage experience

By leveraging these tools and processes, frontend teams can significantly improve development efficiency and code quality, achieving rapid iteration and stable releases.

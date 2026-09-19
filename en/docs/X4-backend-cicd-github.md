# GitHub CI/CD Guide for Backend Developers

> This document provides a comprehensive GitHub CI/CD practice guide for backend developers, covering automated pipeline setup for mainstream backend languages, containerized deployment, database migration, API testing, performance testing, and other core aspects, helping backend teams build a stable and reliable continuous integration and continuous deployment system.

---

## Table of Contents

1. [Backend Project GitHub Repository Structure](#1-backend-project-github-repository-structure)
2. [GitHub Actions for Java/Spring Boot Projects](#2-github-actions-for-javaspring-boot-projects)
3. [GitHub Actions for Python/Django/Flask Projects](#3-github-actions-for-pythondjangoflask-projects)
4. [GitHub Actions for Go Projects](#4-github-actions-for-go-projects)
5. [GitHub Actions for Node.js/Nest.js Projects](#5-github-actions-for-nodejsnestjs-projects)
6. [GitHub Actions for Rust Projects](#6-github-actions-for-rust-projects)
7. [Database Migration Automation](#7-database-migration-automation)
8. [API Testing Automation](#8-api-testing-automation)
9. [Containerized Deployment](#9-containerized-deployment)
10. [Kubernetes Deployment Automation](#10-kubernetes-deployment-automation)
11. [Backend Code Quality Checks](#11-backend-code-quality-checks)
12. [Performance Testing Automation](#12-performance-testing-automation)
13. [Multi-Environment Deployment Strategy](#13-multi-environment-deployment-strategy)
14. [Domestic Server Deployment Solutions](#14-domestic-server-deployment-solutions)

---

## 1. Backend Project GitHub Repository Structure

### 1.1 Standard Backend Project Directory Structure

A well-structured backend project repository should have a clear layered architecture to facilitate team collaboration, automated building, and deployment. Below are recommended directory structures for different languages:

**Java/Spring Boot Project Structure:**

```
my-spring-app/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Continuous Integration
│   │   ├── deploy.yml                # Deployment Pipeline
│   │   └── release.yml               # Release Pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── src/
│   ├── main/
│   │   ├── java/com/example/app/
│   │   │   ├── controller/           # Controller Layer
│   │   │   ├── service/              # Service Layer
│   │   │   ├── repository/           # Data Access Layer
│   │   │   ├── model/                # Entity Classes
│   │   │   ├── dto/                  # Data Transfer Objects
│   │   │   ├── config/               # Configuration Classes
│   │   │   ├── exception/            # Exception Handling
│   │   │   ├── util/                 # Utility Classes
│   │   │   └── Application.java
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       ├── db/migration/         # Database Migration Scripts
│   │       └── static/
│   └── test/
│       ├── java/com/example/app/
│       │   ├── controller/
│       │   ├── service/
│       │   └── integration/          # Integration Tests
│       └── resources/
│           └── application-test.yml
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.test.yml
├── docs/
│   ├── api/                          # API Documentation
│   └── architecture/                 # Architecture Documentation
├── scripts/
│   ├── build.sh
│   ├── deploy.sh
│   └── migration.sh
├── pom.xml                           # Maven Configuration
├── .gitignore
├── README.md
└── CHANGELOG.md
```

**Python/Django Project Structure:**

```
my-django-app/
├── .github/
│   └── workflows/
├── myproject/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tests/
│   │   └── migrations/
│   └── orders/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── tests/
│       └── migrations/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── docker/
├── scripts/
├── manage.py
├── pyproject.toml
├── .env.example
└── README.md
```

**Go Project Structure (following golang-standards/project-layout):**

```
my-go-app/
├── .github/
│   └── workflows/
├── cmd/
│   └── server/
│       └── main.go                   # Application Entry Point
├── internal/
│   ├── handler/                      # HTTP Handlers
│   ├── service/                      # Business Logic
│   ├── repository/                   # Data Access
│   ├── model/                        # Data Models
│   ├── middleware/                    # Middleware
│   └── config/                       # Configuration
├── pkg/                              # Reusable Public Libraries
│   ├── logger/
│   ├── database/
│   └── response/
├── api/
│   └── openapi/                      # OpenAPI Specification
├── migrations/                       # Database Migrations
├── deployments/
│   ├── docker/
│   └── k8s/
├── scripts/
├── test/
│   ├── integration/
│   └── e2e/
├── go.mod
├── go.sum
├── Makefile
├── Dockerfile
└── README.md
```

### 1.2 Backend Project `.github` Directory Configuration

**CODEOWNERS File:**

```
# Backend project code owners
*                           @backend-team

# API interface changes require architect approval
/api/                       @architect-zhang
/src/controller/            @architect-zhang

# Database migrations require DBA approval
/src/main/resources/db/     @dba-team
/migrations/                @dba-team

# Configuration file changes require DevOps approval
/docker/                    @devops-team
/.github/                   @devops-team
/deployments/               @devops-team

# Security-related code requires security team approval
/src/**/security/           @security-team
/src/**/auth/               @security-team
```

**Pull Request Template:**

```markdown
## Change Description

### Change Type
- [ ] New Feature (feat)
- [ ] Bug Fix (fix)
- [ ] Refactor (refactor)
- [ ] Performance Optimization (perf)
- [ ] Documentation Update (docs)
- [ ] Test (test)
- [ ] Build/CI (chore)

### Change Description
<!-- Please describe your changes -->

### Database Changes
- [ ] Includes database migration
- [ ] No database changes

### API Changes
- [ ] Includes API changes (please update API documentation)
- [ ] No API changes

### Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] API tests added
- [ ] Manual testing passed

### Deployment Notes
<!-- Are there any special deployment requirements? -->

### Related Issues
<!-- Please link related issue numbers -->
```

### 1.3 Backend Project Branch Management Strategy

Backend projects typically require stricter branch management, especially when involving database migrations and multi-environment deployment:

```
main (production) ← release/v1.2.0 ← develop (development) ← feature/user-auth
                                  ↑
                                  hotfix/critical-bug
```

**Environment-Branch Mapping:**

| Environment | Branch | Trigger | Purpose |
|------|------|---------|------|
| development | develop | Auto Deploy | Daily development testing |
| staging | release/* | Auto Deploy | Pre-release verification |
| production | main | Manual Approval | Production environment |
| hotfix | hotfix/* | Manual Deploy | Emergency fixes |

---

## 2. GitHub Actions for Java/Spring Boot Projects

### 2.1 Complete Spring Boot CI Pipeline

```yaml
# .github/workflows/spring-boot-ci.yml
name: Spring Boot CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  JAVA_VERSION: '21'
  GRADLE_VERSION: '8.5'

jobs:
  code-quality:
    name: Code Quality Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # SonarQube needs full history

      - name: Setup JDK
        uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'gradle'

      - name: Gradle Build Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      - name: Compile Check
        run: ./gradlew compileJava compileTestJava

      - name: Checkstyle Check
        run: ./gradlew checkstyleMain checkstyleTest
        continue-on-error: true

      - name: SpotBugs Static Analysis
        run: ./gradlew spotbugsMain
        continue-on-error: true

      - name: SonarQube Analysis
        if: github.event_name == 'pull_request'
        run: ./gradlew sonarqube
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

  test:
    name: Automated Testing
    runs-on: ubuntu-latest
    needs: code-quality
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'gradle'

      - name: Run Unit Tests
        run: ./gradlew test
        env:
          SPRING_DATASOURCE_URL: jdbc:postgresql://localhost:5432/testdb
          SPRING_DATASOURCE_USERNAME: testuser
          SPRING_DATASOURCE_PASSWORD: testpass
          SPRING_REDIS_HOST: localhost
          SPRING_REDIS_PORT: 6379

      - name: Generate Test Report
        if: always()
        run: ./gradlew jacocoTestReport

      - name: Check Code Coverage
        run: ./gradlew jacocoTestCoverageVerification

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: build/reports/tests/
          retention-days: 30

      - name: Upload Coverage Report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: build/reports/jacoco/

      - name: Publish Test Results
        if: always()
        uses: dorny/test-reporter@v1
        with:
          name: Unit Test Results
          path: '**/build/test-results/test/TEST-*.xml'
          reporter: java-junit

  integration-test:
    name: Integration Test
    runs-on: ubuntu-latest
    needs: test
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: integrationdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'gradle'

      - name: Run Integration Tests
        run: ./gradlew integrationTest
        env:
          SPRING_PROFILES_ACTIVE: integration-test
          SPRING_DATASOURCE_URL: jdbc:postgresql://localhost:5432/integrationdb

      - name: Upload Integration Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: integration-test-reports
          path: build/reports/tests/integrationTest/

  build:
    name: Build and Package
    runs-on: ubuntu-latest
    needs: [test, integration-test]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'gradle'

      - name: Build Executable JAR
        run: ./gradlew bootJar

      - name: Build Docker Image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myapp:latest

      - name: Save Docker Image
        run: docker save myapp:${{ github.sha }} | gzip > myapp-image.tar.gz

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            build/libs/*.jar
            myapp-image.tar.gz
          retention-days: 7

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4

      - name: Download Build Artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-artifacts

      - name: OWASP Dependency Check
        run: ./gradlew dependencyCheckAnalyze
        continue-on-error: true

      - name: Trivy Container Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Scan Results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

### 2.2 Spring Boot Project Release Process

```yaml
# .github/workflows/spring-boot-release.yml
name: Spring Boot Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'gradle'

      - name: Build
        run: ./gradlew bootJar

      - name: Publish to GitHub Packages
        run: ./gradlew publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: build/libs/*.jar
          generate_release_notes: true
```

---

## 3. GitHub Actions for Python/Django/Flask Projects

### 3.1 Django Project CI Pipeline

```yaml
# .github/workflows/django-ci.yml
name: Django CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: '3.12'
  DJANGO_SETTINGS_MODULE: 'myproject.settings.testing'

jobs:
  lint:
    name: Code Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements/testing.txt

      - name: Ruff Code Check
        run: ruff check .

      - name: Ruff Format Check
        run: ruff format --check .

      - name: MyPy Type Check
        run: mypy .
        continue-on-error: true

      - name: Django System Check
        run: python manage.py check --deploy

  test:
    name: Automated Testing
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install Dependencies
        run: pip install -r requirements/testing.txt

      - name: Database Migration
        run: python manage.py migrate
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0

      - name: Run Tests
        run: |
          pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0
          DJANGO_SETTINGS_MODULE: myproject.settings.testing

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: |
            test-results.xml
            htmlcov/

      - name: Upload Coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    name: Build Image
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: |
          docker build -t mydjangoapp:${{ github.sha }} .

      - name: Run Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: mydjangoapp:${{ github.sha }}
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

### 3.2 Flask/FastAPI Project CI Pipeline

```yaml
# .github/workflows/fastapi-ci.yml
name: FastAPI CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          pip install uv
          uv pip install -r requirements.txt --system

      - name: Code Check
        run: |
          ruff check src/
          ruff format --check src/

      - name: Run Tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb
          TESTING: true

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

### 3.3 Python Project Dependency Management

```yaml
# .github/workflows/python-dependencies.yml
name: Python Dependencies

on:
  schedule:
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Check Dependency Updates
        run: |
          pip install pip-audit safety
          pip-audit
          safety check -r requirements/production.txt

      - name: Create Dependency Update PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore(deps): Update Python Dependencies'
          body: |
            Automatically checked and updated dependency changes.

            Please confirm before merging:
            - [ ] All tests pass
            - [ ] No breaking changes
          branch: chore/update-dependencies
          labels: dependencies, automated
```

---

## 4. GitHub Actions for Go Projects

### 4.1 Go Project Complete CI Pipeline

```yaml
# .github/workflows/go-ci.yml
name: Go CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  GO_VERSION: '1.22'

jobs:
  lint:
    name: Code Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: true

      - name: golangci-lint
        uses: golangci/golangci-lint-action@v4
        with:
          version: latest
          args: --timeout=5m

      - name: go vet
        run: go vet ./...

      - name: Check go mod tidy
        run: |
          go mod tidy
          git diff --exit-code go.mod go.sum

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: true

      - name: Run Tests
        run: |
          go test -v -race -coverprofile=coverage.out -covermode=atomic ./...
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable
          REDIS_URL: redis://localhost:6379

      - name: Generate Coverage Report
        run: go tool cover -html=coverage.out -o coverage.html

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.out

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.html

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    strategy:
      matrix:
        goos: [linux, darwin, windows]
        goarch: [amd64, arm64]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: true

      - name: Build Binary
        run: |
          CGO_ENABLED=0 GOOS=${{ matrix.goos }} GOARCH=${{ matrix.goarch }} \
            go build -ldflags="-s -w -X main.version=${{ github.sha }}" \
            -o bin/myapp-${{ matrix.goos }}-${{ matrix.goarch }} ./cmd/server
        env:
          GOOS: ${{ matrix.goos }}
          GOARCH: ${{ matrix.goarch }}

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: binary-${{ matrix.goos }}-${{ matrix.goarch }}
          path: bin/

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}

      - name: govulncheck Vulnerability Check
        run: |
          go install golang.org/x/vuln/cmd/govulncheck@latest
          govulncheck ./...

      - name: gosec Security Scan
        uses: securego/gosec@master
        with:
          args: ./...

  benchmark:
    name: Performance Benchmark
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-go@v5
        with:
          go-version: ${{ env.GO_VERSION }}
          cache: true

      - name: Run Benchmark Tests
        run: go test -bench=. -benchmem ./... | tee benchmark.txt

      - name: Store Benchmark Results
        uses: actions/cache@v4
        with:
          path: ./benchmark.txt
          key: ${{ runner.os }}-benchmark-${{ github.sha }}

      - name: Compare Benchmark Results
        if: github.event_name == 'pull_request'
        run: |
          go install golang.org/x/perf/cmd/benchstat@latest
          # Get base branch results for comparison
          git stash
          git checkout ${{ github.base_ref }}
          go test -bench=. -benchmem ./... > benchmark-base.txt || true
          git checkout -
          git stash pop
          benchstat benchmark-base.txt benchmark.txt || true
```

### 4.2 Go Project Makefile

```makefile
# Makefile
.PHONY: all build test lint clean docker

APP_NAME := myapp
VERSION := $(shell git describe --tags --always --dirty)
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')
LDFLAGS := -ldflags "-s -w -X main.version=$(VERSION) -X main.buildTime=$(BUILD_TIME)"

all: lint test build

build:
	CGO_ENABLED=0 go build $(LDFLAGS) -o bin/$(APP_NAME) ./cmd/server

build-all:
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build $(LDFLAGS) -o bin/$(APP_NAME)-linux-amd64 ./cmd/server
	GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 go build $(LDFLAGS) -o bin/$(APP_NAME)-darwin-arm64 ./cmd/server

test:
	go test -v -race -coverprofile=coverage.out ./...

test-integration:
	go test -v -tags=integration ./test/integration/...

lint:
	golangci-lint run --timeout=5m

bench:
	go test -bench=. -benchmem ./...

docker:
	docker build -t $(APP_NAME):$(VERSION) .

clean:
	rm -rf bin/
	rm -f coverage.out coverage.html

migrate-up:
	migrate -path migrations -database "$(DATABASE_URL)" up

migrate-down:
	migrate -path migrations -database "$(DATABASE_URL)" down

migrate-create:
	migrate create -ext sql -dir migrations -seq $(name)
```

---

## 5. GitHub Actions for Node.js/Nest.js Projects

### 5.1 NestJS Project CI Pipeline

```yaml
# .github/workflows/nestjs-ci.yml
name: NestJS CI

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
    name: Code Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: ESLint
        run: pnpm lint

      - name: TypeScript Type Check
        run: pnpm tsc --noEmit

      - name: Format Check
        run: pnpm format:check

  test:
    name: Automated Testing
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Unit Tests
        run: pnpm test:cov
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 5432
          DATABASE_USER: testuser
          DATABASE_PASSWORD: testpass
          DATABASE_NAME: testdb
          REDIS_HOST: localhost
          REDIS_PORT: 6379

      - name: E2E Tests
        run: pnpm test:e2e
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 5432
          DATABASE_USER: testuser
          DATABASE_PASSWORD: testpass
          DATABASE_NAME: testdb
          REDIS_HOST: localhost
          REDIS_PORT: 6379

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: coverage/

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          directory: ./coverage

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm build

      - name: Verify Build Artifacts
        run: |
          ls -la dist/
          node -e "require('./dist/main.js')"

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  api-test:
    name: API Test
    runs-on: ubuntu-latest
    needs: build
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Start Application
        run: |
          pnpm build
          pnpm start:prod &
          sleep 10
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 5432
          DATABASE_USER: testuser
          DATABASE_PASSWORD: testpass
          DATABASE_NAME: testdb

      - name: Run API Tests
        run: |
          npm install -g newman
          newman run test/api/postman_collection.json \
            --environment test/api/environment.json \
            --reporters cli,junit \
            --reporter-junit-export api-test-results.xml

      - name: Upload API Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-test-results
          path: api-test-results.xml
```

### 5.2 Express/Fastify Project CI

```yaml
# .github/workflows/express-ci.yml
name: Express CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
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

      - run: npm run lint

      - run: npm test
        env:
          CI: true

      - run: npm run build
```

---

## 6. GitHub Actions for Rust Projects

### 6.1 Rust Project Complete CI Pipeline

```yaml
# .github/workflows/rust-ci.yml
name: Rust CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  CARGO_TERM_COLOR: always
  RUST_VERSION: '1.78'

jobs:
  check:
    name: Code Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt

      - name: Cargo Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/bin/
            ~/.cargo/registry/index/
            ~/.cargo/registry/cache/
            ~/.cargo/git/db/
            target/
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Format Check
        run: cargo fmt --all -- --check

      - name: Clippy Static Analysis
        run: cargo clippy --all-targets --all-features -- -D warnings

      - name: Check Documentation
        run: cargo doc --no-deps --document-private-items
        env:
          RUSTDOCFLAGS: "-D warnings"

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: check
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/
            target/
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Run Tests
        run: cargo test --all-features --verbose
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb
          RUST_LOG: debug

      - name: Run Integration Tests
        run: cargo test --all-features --test '*'
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb

      - name: Code Coverage
        run: |
          cargo install cargo-tarpaulin
          cargo tarpaulin --all-features --out xml
        env:
          DATABASE_URL: postgres://testuser:testpass@localhost:5432/testdb

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./cobertura.xml

  build:
    name: Build
    runs-on: ${{ matrix.os }}
    needs: test
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        include:
          - os: ubuntu-latest
            artifact: linux-amd64
          - os: macos-latest
            artifact: macos-arm64
          - os: windows-latest
            artifact: windows-amd64
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/
            target/
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Build
        run: cargo build --release

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: binary-${{ matrix.artifact }}
          path: target/release/myapp*

  security:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Cargo Audit
        uses: actions-rs/audit-check@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency Vulnerability Check
        run: |
          cargo install cargo-audit
          cargo audit

  benchmark:
    name: Performance Benchmark
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - name: Run Benchmark Tests
        run: cargo bench --all-features -- --output-format bencher | tee output.txt

      - name: Store Benchmark Results
        uses: actions/cache@v4
        with:
          path: output.txt
          key: ${{ runner.os }}-bench-${{ github.sha }}
```

### 6.2 Rust Project Release Process

```yaml
# .github/workflows/rust-release.yml
name: Rust Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable

      - name: Build
        run: cargo build --release

      - name: Package
        run: |
          cd target/release
          tar czf myapp-${{ github.ref_name }}-${{ runner.os }}.tar.gz myapp*
        if: runner.os != 'Windows'

      - name: Package (Windows)
        if: runner.os == 'Windows'
        run: |
          Compress-Archive -Path target/release/myapp.exe -DestinationPath myapp-${{ github.ref_name }}-Windows.zip

      - name: Publish to crates.io
        if: runner.os == 'ubuntu-latest'
        run: cargo publish
        env:
          CARGO_REGISTRY_TOKEN: ${{ secrets.CARGO_REGISTRY_TOKEN }}

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            target/release/*.tar.gz
            target/release/*.zip
```

---

## 7. Database Migration Automation

### 7.1 Flyway Database Migration

```yaml
# .github/workflows/db-migration.yml
name: Database Migration

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/main/resources/db/migration/**'
      - 'migrations/**'

jobs:
  validate-migration:
    name: Validate Migration Scripts
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: migrationdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Install Flyway
        run: |
          wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/10.4.0/flyway-commandline-10.4.0-linux-x64.tar.gz | tar xz
          echo "$PWD/flyway-10.4.0" >> $GITHUB_PATH

      - name: Validate Migration Scripts
        run: |
          flyway -url=jdbc:postgresql://localhost:5432/migrationdb \
            -user=testuser -password=testpass \
            -locations=filesystem:src/main/resources/db/migration \
            validate

      - name: Execute Migration
        run: |
          flyway -url=jdbc:postgresql://localhost:5432/migrationdb \
            -user=testuser -password=testpass \
            -locations=filesystem:src/main/resources/db/migration \
            migrate

      - name: Check Migration Status
        run: |
          flyway -url=jdbc:postgresql://localhost:5432/migrationdb \
            -user=testuser -password=testpass \
            -locations=filesystem:src/main/resources/db/migration \
            info

  deploy-migration:
    name: Deploy Migration
    needs: validate-migration
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Execute Production Migration
        run: |
          flyway -url=${{ secrets.PROD_DATABASE_URL }} \
            -user=${{ secrets.PROD_DATABASE_USER }} \
            -password=${{ secrets.PROD_DATABASE_PASSWORD }} \
            -locations=filesystem:src/main/resources/db/migration \
            migrate

      - name: Notify Migration Result
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Database migration completed successfully\nBranch: ${{ github.ref }}\nCommit: ${{ github.sha }}"
            }
```

### 7.2 Liquibase Database Migration

```yaml
# .github/workflows/liquibase-migration.yml
name: Liquibase Migration

on:
  push:
    branches: [main]
    paths:
      - 'db/changelog/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Validate Changelog
        uses: liquibase/liquibase-github-action@v4
        with:
          operation: validate
          changelog-file: db/changelog/db.changelog-master.xml
          url: jdbc:postgresql://localhost:5432/testdb
          username: testuser
          password: testpass

      - name: Execute Migration
        uses: liquibase/liquibase-github-action@v4
        with:
          operation: update
          changelog-file: db/changelog/db.changelog-master.xml
          url: jdbc:postgresql://localhost:5432/testdb
          username: testuser
          password: testpass

      - name: Generate Migration Report
        uses: liquibase/liquibase-github-action@v4
        with:
          operation: status
          changelog-file: db/changelog/db.changelog-master.xml
          url: jdbc:postgresql://localhost:5432/testdb
          username: testuser
          password: testpass
```

### 7.3 Python Alembic Migration

```yaml
# .github/workflows/alembic-migration.yml
name: Alembic Migration

on:
  push:
    branches: [main]
    paths:
      - 'alembic/versions/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: pip install -r requirements.txt alembic

      - name: Validate Migration
        run: alembic check
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb

      - name: Execute Migration
        run: alembic upgrade head
        env:
          DATABASE_URL: postgresql://testuser:testpass@localhost:5432/testdb

      - name: Generate Migration Script
        run: alembic history > migration-history.txt

      - name: Upload Migration Record
        uses: actions/upload-artifact@v4
        with:
          name: migration-history
          path: migration-history.txt
```

### 7.4 Go migrate Migration

```yaml
# .github/workflows/go-migrate.yml
name: Go Migrate

on:
  push:
    branches: [main]
    paths:
      - 'migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Install golang-migrate
        run: |
          curl -L https://github.com/golang-migrate/migrate/releases/download/v4.17.0/migrate.linux-amd64.tar.gz | tar xz
          sudo mv migrate /usr/local/bin/

      - name: Validate Migration Files
        run: migrate -path migrations -database postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable validate

      - name: Execute Migration
        run: migrate -path migrations -database postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable up

      - name: Check Migration Version
        run: migrate -path migrations -database postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable version

      - name: Generate Migration Diff
        if: failure()
        run: |
          echo "Migration failed, please check migration scripts"
          migrate -path migrations -database postgres://testuser:testpass@localhost:5432/testdb?sslmode=disable version
```

---

## 8. API Testing Automation

### 8.1 Postman/Newman API Testing

```yaml
# .github/workflows/api-test.yml
name: API Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  api-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Start Application
        run: |
          # Start application based on project type
          docker-compose -f docker-compose.test.yml up -d
          sleep 30

      - name: Run Newman API Tests
        uses: anthropics/newman-action@v1
        with:
          collection: test/api/collection.json
          environment: test/api/environment.json
          reporters: cli,junit,htmlextra
          reporter-junit-export: api-test-results.xml
          reporter-htmlextra-export: api-test-report.html

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: api-test-reports
          path: |
            api-test-results.xml
            api-test-report.html

      - name: Publish Test Results
        if: always()
        uses: dorny/test-reporter@v1
        with:
          name: API Test Results
          path: api-test-results.xml
          reporter: java-junit
```

### 8.2 REST Assured (Java) API Testing

```java
// src/test/java/com/example/api/UserApiTest.java
package com.example.api;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.*;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class UserApiTest {

    @LocalServerPort
    private int port;

    @BeforeEach
    void setUp() {
        RestAssured.port = port;
        RestAssured.basePath = "/api/v1";
    }

    @Test
    @Order(1)
    void shouldCreateUser() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "password": "securePassword123"
                }
                """)
        .when()
            .post("/users")
        .then()
            .statusCode(201)
            .body("name", equalTo("John Doe"))
            .body("email", equalTo("john@example.com"))
            .body("id", notNullValue());
    }

    @Test
    @Order(2)
    void shouldGetUserById() {
        given()
            .pathParam("id", 1)
        .when()
            .get("/users/{id}")
        .then()
            .statusCode(200)
            .body("name", equalTo("John Doe"));
    }

    @Test
    @Order(3)
    void shouldReturn404ForNonExistentUser() {
        given()
            .pathParam("id", 999)
        .when()
            .get("/users/{id}")
        .then()
            .statusCode(404)
            .body("message", equalTo("User not found"));
    }

    @Test
    @Order(4)
    void shouldValidateInput() {
        given()
            .contentType(ContentType.JSON)
            .body("""
                {
                    "name": "",
                    "email": "invalid-email"
                }
                """)
        .when()
            .post("/users")
        .then()
            .statusCode(400)
            .body("errors", hasSize(greaterThan(0)));
    }
}
```

### 8.3 pytest API Testing (Python)

```python
# tests/api/test_users.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_headers(client):
    response = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}

class TestUserAPI:
    @pytest.mark.asyncio
    async def test_create_user(self, client, auth_headers):
        response = await client.post("/api/v1/users", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "securePassword123"
        }, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_get_user(self, client, auth_headers):
        # Create user
        create_response = await client.post("/api/v1/users", json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "securePassword123"
        }, headers=auth_headers)
        user_id = create_response.json()["id"]

        # Get user
        response = await client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Jane Smith"

    @pytest.mark.asyncio
    async def test_user_not_found(self, client, auth_headers):
        response = await client.get("/api/v1/users/999", headers=auth_headers)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_validation_error(self, client, auth_headers):
        response = await client.post("/api/v1/users", json={
            "name": "",
            "email": "invalid"
        }, headers=auth_headers)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_list_users(self, client, auth_headers):
        response = await client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json()["items"], list)

    @pytest.mark.asyncio
    async def test_update_user(self, client, auth_headers):
        # Create user
        create_response = await client.post("/api/v1/users", json={
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "password": "securePassword123"
        }, headers=auth_headers)
        user_id = create_response.json()["id"]

        # Update user
        response = await client.put(f"/api/v1/users/{user_id}", json={
            "name": "Bob Wilson (Updated)"
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Bob Wilson (Updated)"

    @pytest.mark.asyncio
    async def test_delete_user(self, client, auth_headers):
        # Create user
        create_response = await client.post("/api/v1/users", json={
            "name": "Alice Brown",
            "email": "alice@example.com",
            "password": "securePassword123"
        }, headers=auth_headers)
        user_id = create_response.json()["id"]

        # Delete user
        response = await client.delete(f"/api/v1/users/{user_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify deletion
        response = await client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
        assert response.status_code == 404
```

### 8.4 Go API Testing

```go
// tests/api/user_test.go
package api_test

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCreateUser(t *testing.T) {
    app := setupTestApp()

    body := map[string]string{
        "name":     "John Doe",
        "email":    "john@example.com",
        "password": "securePassword123",
    }
    jsonBody, _ := json.Marshal(body)

    req := httptest.NewRequest(http.MethodPost, "/api/v1/users", bytes.NewBuffer(jsonBody))
    req.Header.Set("Content-Type", "application/json")
    resp, err := app.Test(req)

    require.NoError(t, err)
    assert.Equal(t, http.StatusCreated, resp.StatusCode)

    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    assert.Equal(t, "John Doe", result["name"])
    assert.NotNil(t, result["id"])
}

func TestGetUser(t *testing.T) {
    app := setupTestApp()

    // Create user
    createBody := map[string]string{
        "name":     "Jane Smith",
        "email":    "jane@example.com",
        "password": "securePassword123",
    }
    jsonBody, _ := json.Marshal(createBody)
    createReq := httptest.NewRequest(http.MethodPost, "/api/v1/users", bytes.NewBuffer(jsonBody))
    createReq.Header.Set("Content-Type", "application/json")
    createResp, _ := app.Test(createReq)

    var created map[string]interface{}
    json.NewDecoder(createResp.Body).Decode(&created)
    userID := created["id"]

    // Get user
    req := httptest.NewRequest(http.MethodGet, "/api/v1/users/"+fmt.Sprintf("%v", userID), nil)
    resp, err := app.Test(req)

    require.NoError(t, err)
    assert.Equal(t, http.StatusOK, resp.StatusCode)

    var user map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&user)
    assert.Equal(t, "Jane Smith", user["name"])
}

func TestUserNotFound(t *testing.T) {
    app := setupTestApp()

    req := httptest.NewRequest(http.MethodGet, "/api/v1/users/999", nil)
    resp, err := app.Test(req)

    require.NoError(t, err)
    assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}
```

---

## 9. Containerized Deployment

### 9.1 Multi-Stage Docker Build

**Java/Spring Boot Dockerfile:**

```dockerfile
# docker/Dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app

COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts ./
RUN ./gradlew dependencies --no-daemon

COPY src/ src/
RUN ./gradlew bootJar --no-daemon

# Runtime stage
FROM eclipse-temurin:21-jre-alpine AS runtime
WORKDIR /app

RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /app/build/libs/*.jar app.jar

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

**Python/Django Dockerfile:**

```dockerfile
# docker/Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install --no-cache-dir --prefix=/install -r requirements/production.txt

FROM python:3.12-slim AS runtime
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY . .

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

**Go Dockerfile:**

```dockerfile
# docker/Dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server ./cmd/server

FROM alpine:3.19 AS runtime
WORKDIR /app

RUN apk --no-cache add ca-certificates tzdata && \
    addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /app/server .

RUN chown appuser:appgroup server
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["./server"]
```

**Node.js/NestJS Dockerfile:**

```dockerfile
# docker/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

FROM node:20-alpine AS runtime
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9 --activate

RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/main.js"]
```

**Rust Dockerfile:**

```dockerfile
# docker/Dockerfile
FROM rust:1.78-alpine AS builder
WORKDIR /app

RUN apk add --no-cache musl-dev

COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

COPY src/ src/
RUN touch src/main.rs && cargo build --release

FROM alpine:3.19 AS runtime
WORKDIR /app

RUN apk --no-cache add ca-certificates tzdata && \
    addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /app/target/release/myapp .

RUN chown appuser:appgroup myapp
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["./myapp"]
```

### 9.2 Docker Compose Configuration

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
      - SPRING_PROFILES_ACTIVE=docker
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### 9.3 GitHub Actions Docker Build and Push

```yaml
# .github/workflows/docker-build.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract Metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Scan Results
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## 10. Kubernetes Deployment Automation

### 10.1 Kubernetes Manifest Files

```yaml
# deployments/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: ghcr.io/myorg/myapp:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: redis-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: myapp-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 10.2 GitHub Actions Kubernetes Deployment

```yaml
# .github/workflows/k8s-deploy.yml
name: Kubernetes Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Update Image Version
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n production

      - name: Wait for Deployment to Complete
        run: |
          kubectl rollout status deployment/myapp -n production --timeout=300s

      - name: Verify Deployment
        run: |
          kubectl get pods -n production -l app=myapp
          kubectl get svc -n production

      - name: Rollback (on Deployment Failure)
        if: failure()
        run: |
          kubectl rollout undo deployment/myapp -n production

  smoke-test:
    name: Smoke Test
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Health Check
        run: |
          for i in {1..10}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
            if [ "$STATUS" = "200" ]; then
              echo "Health check passed"
              exit 0
            fi
            echo "Waiting for service to be ready... ($i/10)"
            sleep 10
          done
          echo "Health check failed"
          exit 1

      - name: API Smoke Test
        run: |
          # Basic API test
          curl -f https://api.example.com/api/v1/health
          curl -f https://api.example.com/api/v1/version
```

### 10.3 Kustomize Multi-Environment Management

```yaml
# deployments/k8s/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - hpa.yaml

commonLabels:
  app: myapp

---
# deployments/k8s/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
  - ../../base
namespace: production
replicas:
  - name: myapp
    count: 3
patches:
  - target:
      kind: Deployment
      name: myapp
    patch: |
      - op: replace
        path: /spec/template/spec/containers/0/resources/requests/memory
        value: "512Mi"
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: "1Gi"

---
# deployments/k8s/overlays/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
bases:
  - ../../base
namespace: staging
replicas:
  - name: myapp
    count: 1
```

---

## 11. Backend Code Quality Checks

### 11.1 SonarQube Integration

```yaml
# .github/workflows/sonarqube.yml
name: SonarQube Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarQube Scan
        uses: sonarqube-quality-gate-action@master
        with:
          scanMetadataReportFile: target/sonar/report-task.txt
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

      - name: SonarQube Quality Gate
        uses: sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**sonar-project.properties Configuration:**

```properties
# sonar-project.properties
sonar.projectKey=my-backend-app
sonar.projectName=My Backend App
sonar.projectVersion=1.0

sonar.sources=src/main
sonar.tests=src/test
sonar.java.binaries=build/classes
sonar.java.libraries=build/libs

sonar.coverage.jacoco.xmlReportPaths=build/reports/jacoco/test/jacocoTestReport.xml
sonar.junit.reportPaths=build/test-results/test

sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

sonar.exclusions=**/generated/**,**/test/**
```

### 11.2 Codecov Integration

```yaml
# .github/workflows/codecov.yml
name: Codecov

on: [push, pull_request]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Tests and Generate Coverage
        run: |
          # Run tests based on project type
          ./gradlew test jacocoTestReport

      - name: Upload to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: build/reports/jacoco/test/jacocoTestReport.xml
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true
          verbose: true

      - name: Codecov Coverage Check
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          flags: unittests
          name: codecov-umbrella
```

### 11.3 Code Quality Report Integration

```yaml
# .github/workflows/quality-report.yml
name: Quality Report

on: [pull_request]

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Tests and Checks
        run: |
          ./gradlew test jacocoTestReport checkstyleMain

      - name: Generate Quality Report
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');

            // Read test results
            const testResults = fs.readFileSync('build/reports/tests/test/index.html', 'utf8');

            // Read coverage
            const coverage = fs.readFileSync('build/reports/jacoco/test/jacocoTestReport.csv', 'utf8');

            // Read Checkstyle results
            let checkstyle = 'No Checkstyle results';
            try {
              checkstyle = fs.readFileSync('build/reports/checkstyle/main.xml', 'utf8');
            } catch (e) {}

            let report = `## 📊 Code Quality Report\n\n`;
            report += `### Test Results\n`;
            report += `See [Test Report](https://github.com/${context.repo.owner}/${context.repo.repo}/actions/runs/${context.runId})\n\n`;

            report += `### Code Coverage\n`;
            const lines = coverage.split('\n');
            if (lines.length > 1) {
              const headers = lines[0].split(',');
              const values = lines[1].split(',');
              report += `| Metric | Coverage |\n|------|--------|\n`;
              for (let i = 0; i < headers.length; i++) {
                if (headers[i].includes('COVERED') || headers[i].includes('MISSED')) {
                  report += `| ${headers[i]} | ${values[i]} |\n`;
                }
              }
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

---

## 12. Performance Testing Automation

### 12.1 JMeter Performance Testing

```yaml
# .github/workflows/performance-test.yml
name: Performance Test

on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM
  workflow_dispatch:
    inputs:
      threads:
        description: 'Concurrent thread count'
        default: '100'
      duration:
        description: 'Test duration (seconds)'
        default: '300'

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install JMeter
        run: |
          wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar xzf apache-jmeter-5.6.3.tgz
          echo "$PWD/apache-jmeter-5.6.3/bin" >> $GITHUB_PATH

      - name: Run Performance Test
        run: |
          THREADS=${{ github.event.inputs.threads || '100' }}
          DURATION=${{ github.event.inputs.duration || '300' }}

          jmeter -n -t test/performance/load-test.jmx \
            -Jthreads=$THREADS \
            -Jduration=$DURATION \
            -l results.jtl \
            -e -o report/

      - name: Upload Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: performance-report
          path: report/

      - name: Analyze Results
        run: |
          # Extract key metrics
          TOTAL=$(grep -c "true" results.jtl || echo 0)
          SUCCESS=$(grep -c "true,true" results.jtl || echo 0)
          ERROR_RATE=$(echo "scale=2; ($TOTAL - $SUCCESS) * 100 / $TOTAL" | bc)

          echo "## 🚀 Performance Test Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|------|-----|" >> $GITHUB_STEP_SUMMARY
          echo "| Total Requests | $TOTAL |" >> $GITHUB_STEP_SUMMARY
          echo "| Successful Requests | $SUCCESS |" >> $GITHUB_STEP_SUMMARY
          echo "| Error Rate | ${ERROR_RATE}% |" >> $GITHUB_STEP_SUMMARY

          if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
            echo "::error::Error rate ${ERROR_RATE}% exceeds threshold 5%"
            exit 1
          fi
```

### 12.2 k6 Performance Testing

```javascript
// test/performance/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latency = new Trend('latency');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Maintain 100 users
    { duration: '2m', target: 200 },   // Ramp up to 200 users
    { duration: '5m', target: 200 },   // Maintain 200 users
    { duration: '2m', target: 0 },     // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    errors: ['rate<0.05'],             // Error rate < 5%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  // Test user login
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify({
    username: 'testuser',
    password: 'testpass',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status is 200': (r) => r.status === 200,
    'login has token': (r) => r.json('token') !== undefined,
  }) || errorRate.add(1);

  const token = loginRes.json('token');

  // Test get user list
  const usersRes = http.get(`${BASE_URL}/api/v1/users`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(usersRes, {
    'users status is 200': (r) => r.status === 200,
    'users has items': (r) => r.json('items') !== undefined,
  }) || errorRate.add(1);

  latency.add(usersRes.timings.duration);

  // Test create user
  const createRes = http.post(`${BASE_URL}/api/v1/users`, JSON.stringify({
    name: `User ${Date.now()}`,
    email: `user${Date.now()}@example.com`,
    password: 'testpass123',
  }), {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  });

  check(createRes, {
    'create status is 201': (r) => r.status === 201,
  }) || errorRate.add(1);

  sleep(1);
}

export function handleSummary(data) {
  return {
    'performance-results.json': JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}
```

```yaml
# .github/workflows/k6-performance.yml
name: k6 Performance Test

on:
  schedule:
    - cron: '0 2 * * 0'
  workflow_dispatch:

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update && sudo apt-get install k6

      - name: Run k6 Test
        run: |
          k6 run test/performance/load-test.js \
            --out json=results.json \
            --summary-export=summary.json

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: |
            results.json
            summary.json

      - name: Performance Report
        if: always()
        run: |
          echo "## 🚀 k6 Performance Test Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          cat summary.json | jq -r '
            "| Metric | Value |\n|------|-----|\n" +
            "| Total Requests | " + .metrics.http_reqs.values.count + " |\n" +
            "| Average Response Time | " + (.metrics.http_req_duration.values.avg | tostring) + "ms |\n" +
            "| P95 Response Time | " + (.metrics.http_req_duration.values["p(95)"] | tostring) + "ms |\n" +
            "| Error Rate | " + ((.metrics.http_req_failed.values.rate * 100) | tostring) + "% |"
          ' >> $GITHUB_STEP_SUMMARY
```

---

## 13. Multi-Environment Deployment Strategy

### 13.1 Environment Configuration Management

```yaml
# .github/workflows/multi-env-deploy.yml
name: Multi Environment Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myapp:latest

      - name: Push Image
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}
          docker push myapp:latest

  deploy-dev:
    name: Deploy to Development
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: development
      url: https://dev.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Development
        run: |
          kubectl config use-context dev-cluster
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n development
          kubectl rollout status deployment/myapp -n development

      - name: Run Smoke Test
        run: |
          curl -f https://dev.example.com/health

  deploy-staging:
    name: Deploy to Staging
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Staging
        run: |
          kubectl config use-context staging-cluster
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n staging
          kubectl rollout status deployment/myapp -n staging

      - name: Run Integration Tests
        run: |
          npm install -g newman
          newman run test/api/staging-collection.json --environment test/api/staging-env.json

      - name: Performance Benchmark
        run: |
          k6 run test/performance/smoke-test.js -e BASE_URL=https://staging.example.com

  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production (Canary Release)
        run: |
          kubectl config use-context prod-cluster

          # Canary release: update 1 Pod first
          kubectl set image deployment/myapp-canary myapp=myapp:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp-canary -n production

          # Wait 5 minutes for observation
          sleep 300

          # Check canary Pod health
          if kubectl get pods -n production -l app=myapp,version=canary | grep -q Running; then
            echo "Canary release healthy, starting full rollout"
            kubectl set image deployment/myapp myapp=myapp:${{ github.sha }} -n production
            kubectl rollout status deployment/myapp -n production
          else
            echo "Canary release failed, rolling back"
            kubectl rollout undo deployment/myapp-canary -n production
            exit 1
          fi

      - name: Verify Production Deployment
        run: |
          curl -f https://api.example.com/health
          curl -f https://api.example.com/api/v1/version | jq .

      - name: Notify Deployment Result
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment ${{ job.status == 'success' ? 'succeeded' : 'failed' }}\nVersion: ${{ github.sha }}\nTime: ${{ github.event.head_commit.timestamp }}"
            }
```

### 13.2 Blue-Green Deployment Strategy

```yaml
# .github/workflows/blue-green-deploy.yml
name: Blue-Green Deploy

on:
  workflow_dispatch:
    inputs:
      target:
        description: 'Target environment (blue/green)'
        required: true
        type: choice
        options:
          - blue
          - green

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Determine Current and Target Environment
        id: env
        run: |
          CURRENT=$(kubectl get svc myapp-active -n production -o jsonpath='{.spec.selector.slot}')
          if [ "$CURRENT" = "blue" ]; then
            echo "current=blue" >> $GITHUB_OUTPUT
            echo "target=green" >> $GITHUB_OUTPUT
          else
            echo "current=green" >> $GITHUB_OUTPUT
            echo "target=blue" >> $GITHUB_OUTPUT
          fi

      - name: Deploy to Target Environment
        run: |
          TARGET=${{ steps.env.outputs.target }}
          kubectl set image deployment/myapp-$TARGET myapp=myapp:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp-$TARGET -n production

      - name: Switch Traffic
        run: |
          TARGET=${{ steps.env.outputs.target }}
          kubectl patch svc myapp-active -n production -p "{\"spec\":{\"selector\":{\"slot\":\"$TARGET\"}}}"

      - name: Verify Switch
        run: |
          sleep 30
          curl -f https://api.example.com/health

      - name: Rollback (on Failure)
        if: failure()
        run: |
          CURRENT=${{ steps.env.outputs.current }}
          kubectl patch svc myapp-active -n production -p "{\"spec\":{\"selector\":{\"slot\":\"$CURRENT\"}}}"
```

### 13.3 Version Rollback Strategy

```yaml
# .github/workflows/rollback.yml
name: Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to (leave empty for previous version)'
        required: false
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Execute Rollback
        run: |
          if [ -z "${{ inputs.version }}" ]; then
            kubectl rollout undo deployment/myapp -n ${{ inputs.environment }}
          else
            kubectl rollout undo deployment/myapp --to-revision=${{ inputs.version }} -n ${{ inputs.environment }}
          fi
          kubectl rollout status deployment/myapp -n ${{ inputs.environment }}

      - name: Verify Rollback
        run: |
          sleep 30
          curl -f https://${{ inputs.environment }}.example.com/health

      - name: Notify Rollback
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ Rollback executed\nEnvironment: ${{ inputs.environment }}\nVersion: ${{ inputs.version || 'Previous version' }}\nOperator: ${{ github.actor }}"
            }
```

---

## 14. Domestic Server Deployment Solutions

### 14.1 Alibaba Cloud Container Service Deployment

```yaml
# .github/workflows/aliyun-deploy.yml
name: Aliyun Deploy

on:
  push:
    branches: [main]

env:
  REGISTRY: registry.cn-hangzhou.aliyuncs.com
  NAMESPACE: my-namespace
  IMAGE_NAME: myapp

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Alibaba Cloud Container Registry
        run: |
          docker login -u ${{ secrets.ALIYUN_CR_USERNAME }} -p ${{ secrets.ALIYUN_CR_PASSWORD }} ${{ env.REGISTRY }}

      - name: Build and Push Image
        run: |
          FULL_IMAGE=${{ env.REGISTRY }}/${{ env.NAMESPACE }}/${{ env.IMAGE_NAME }}
          docker build -t $FULL_IMAGE:${{ github.sha }} .
          docker tag $FULL_IMAGE:${{ github.sha }} $FULL_IMAGE:latest
          docker push $FULL_IMAGE:${{ github.sha }}
          docker push $FULL_IMAGE:latest

  deploy-ack:
    name: Deploy to Alibaba Cloud ACK
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.ALIYUN_KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to ACK
        run: |
          FULL_IMAGE=${{ env.REGISTRY }}/${{ env.NAMESPACE }}/${{ env.IMAGE_NAME }}
          kubectl set image deployment/myapp myapp=$FULL_IMAGE:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp -n production --timeout=300s

      - name: Verify Deployment
        run: |
          kubectl get pods -n production
          kubectl get svc -n production
```

### 14.2 Tencent Cloud Container Service Deployment

```yaml
# .github/workflows/tencent-deploy.yml
name: Tencent Cloud Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Tencent Cloud Container Registry
        run: |
          docker login -u ${{ secrets.TCR_USERNAME }} -p ${{ secrets.TCR_PASSWORD }} ccr.ccs.tencentyun.com

      - name: Build and Push Image
        run: |
          IMAGE=ccr.ccs.tencentyun.com/my-namespace/myapp
          docker build -t $IMAGE:${{ github.sha }} .
          docker push $IMAGE:${{ github.sha }}

  deploy-tke:
    name: Deploy to Tencent Cloud TKE
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.TKE_KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to TKE
        run: |
          IMAGE=ccr.ccs.tencentyun.com/my-namespace/myapp
          kubectl set image deployment/myapp myapp=$IMAGE:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp -n production
```

### 14.3 Huawei Cloud Container Service Deployment

```yaml
# .github/workflows/huawei-deploy.yml
name: Huawei Cloud Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Huawei Cloud SWR
        run: |
          docker login -u ${{ secrets.HW_SWR_USERNAME }} -p ${{ secrets.HW_SWR_PASSWORD }} swr.cn-north-4.myhuaweicloud.com

      - name: Build and Push Image
        run: |
          IMAGE=swr.cn-north-4.myhuaweicloud.com/my-namespace/myapp
          docker build -t $IMAGE:${{ github.sha }} .
          docker push $IMAGE:${{ github.sha }}

  deploy-cce:
    name: Deploy to Huawei Cloud CCE
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Configure kubeconfig
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.CCE_KUBE_CONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to CCE
        run: |
          IMAGE=swr.cn-north-4.myhuaweicloud.com/my-namespace/myapp
          kubectl set image deployment/myapp myapp=$IMAGE:${{ github.sha }} -n production
          kubectl rollout status deployment/myapp -n production
```

### 14.4 Domestic Deployment Optimization Tips

**1. Mirror Acceleration Configuration**

```yaml
# Use domestic mirror sources in CI
- name: Configure npm mirror
  run: npm config set registry https://registry.npmmirror.com

- name: Configure pip mirror
  run: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

- name: Configure Docker mirror acceleration
  run: |
    sudo mkdir -p /etc/docker
    sudo tee /etc/docker/daemon.json <<-'EOF'
    {
      "registry-mirrors": [
        "https://mirror.ccs.tencentyun.com",
        "https://registry.docker-cn.com"
      ]
    }
    EOF
    sudo systemctl daemon-reload
    sudo systemctl restart docker
```

**2. Multi-Region Deployment Strategy**

```yaml
# Multi-region deployment matrix
strategy:
  matrix:
    region:
      - name: cn-hangzhou
        endpoint: registry.cn-hangzhou.aliyuncs.com
      - name: cn-beijing
        endpoint: registry.cn-beijing.aliyuncs.com
      - name: cn-shanghai
        endpoint: registry.cn-shanghai.aliyuncs.com
```

**3. CDN Static Asset Acceleration**

```yaml
- name: Upload to Alibaba Cloud OSS + CDN
  run: |
    # Upload static assets to OSS
    ossutil cp -r dist/ oss://my-bucket/assets/ --update

    # Refresh CDN cache
    aliyun cdn RefreshObjectCaches \
      --ObjectPath "https://cdn.example.com/assets/" \
      --ObjectType "Directory"
```

**4. Domestic Monitoring Integration**

```yaml
- name: Deploy Monitoring
  run: |
    # Configure Alibaba Cloud ARMS monitoring
    kubectl apply -f - <<EOF
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: arms-agent-config
    data:
      APP_NAME: myapp
      LICENSE_KEY: ${{ secrets.ARMS_LICENSE_KEY }}
    EOF
```

### 14.5 Domestic Deployment Solutions Comparison

| Cloud Provider | Container Service | Image Registry | CI/CD Integration | Advantages |
|---------|---------|---------|-----------|------|
| Alibaba Cloud | ACK | ACR | CloudEffect | Mature ecosystem, rich documentation |
| Tencent Cloud | TKE | TCR | CODING | Optimized for gaming/social scenarios |
| Huawei Cloud | CCE | SWR | DevCloud | Enterprise-grade security, hybrid cloud |
| AWS China | EKS | ECR | CodeStar | Global deployment capabilities |

---

## Summary

This document provides a comprehensive GitHub CI/CD practice guide for backend developers, covering the full automation process from code commit to production deployment.

**Key Takeaways:**

1. **Automation First**: Automate code checks, testing, building, and deployment to reduce manual operations and human errors
2. **Multi-Language Support**: Detailed CI configurations for mainstream backend languages including Java, Python, Go, Node.js, and Rust
3. **Containerized Deployment**: Use Docker multi-stage builds to optimize image size, Kubernetes orchestration for elastic scaling
4. **Quality Gates**: Ensure code quality through tools like SonarQube and Codecov, automated performance testing to ensure system stability
5. **Multi-Environment Management**: Automated deployment across dev/staging/prod environments, supporting canary releases and blue-green deployment
6. **Domestic Optimization**: Deployment solutions for major domestic cloud providers including Alibaba Cloud, Tencent Cloud, and Huawei Cloud

By effectively utilizing these tools and processes, backend teams can build a stable and reliable CI/CD system, achieving rapid iteration and high-quality delivery.

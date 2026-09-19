# Exercise 7: Using GitHub Actions

## Goal

Learn how to create and use GitHub Actions workflows.

## Steps

### 1. Create a Practice Repository

```bash
mkdir actions-practice
cd actions-practice
git init

echo "# Actions Practice" > README.md
git add README.md
git commit -m "Initial commit"

git remote add origin git@github.com:your-username/actions-practice.git
git push -u origin main
```

### 2. Create a Basic Workflow

Create `.github/workflows/ci.yml`:

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
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        
    - name: Install dependencies
      run: npm install
      
    - name: Run tests
      run: npm test
      
    - name: Build project
      run: npm run build
```

### 3. Create package.json

```json
{
  "name": "actions-practice",
  "version": "1.0.0",
  "scripts": {
    "test": "echo \"Tests passed!\" && exit 0",
    "build": "echo \"Build successful!\" && exit 0"
  }
}
```

### 4. Commit and Push

```bash
git add .
git commit -m "feat: Add CI workflow"
git push
```

### 5. Observe the Workflow Run

1. Go to the repository **Actions** tab
2. Check the workflow run status
3. Click to view details

### 6. Add More Steps

Update `.github/workflows/ci.yml`:

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
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        
    - name: Cache dependencies
      uses: actions/cache@v4
      with:
        path: ~/.npm
        key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
        
    - name: Install dependencies
      run: npm install
      
    - name: Run linter
      run: echo "Linting..."
      
    - name: Run tests
      run: npm test
      
    - name: Build project
      run: npm run build
      
    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: build-output
        path: dist/
```

### 7. Using Secrets

1. Go to the repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add a secret: `MY_SECRET`

Use it in the workflow:

```yaml
- name: Use secret
  run: echo "Secret value is available"
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
```

### 8. Create a Matrix Build

```yaml
name: Matrix Build

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18, 20, 22]
        
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        
    - run: npm install
    - run: npm test
```

## Key Concepts

- Workflow file structure
- Trigger events
- Jobs and steps
- Using Actions
- Caching dependencies
- Uploading artifacts
- Matrix builds
- Using Secrets

## Next Steps

[Exercise 8: Setting Up GitHub Discussions →](exercise-8-discussions.md)

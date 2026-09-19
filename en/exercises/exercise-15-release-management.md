# Exercise 15: Release Management in Practice

## Learning Objectives

- Use semantic versioning
- Automatically generate Release Notes
- Automatically publish to npm

## Steps

### Step 1: Create a Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        registry-url: 'https://registry.npmjs.org'
    
    - run: npm ci
    - run: npm test
    
    - name: Create Release
      uses: softprops/action-gh-release@v2
      with:
        generate_release_notes: true
    
    - run: npm publish
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Step 2: Configure Release Notes Template

```yaml
# .github/release.yml
changelog:
  categories:
    - title: 🚀 Features
      labels:
        - enhancement
    - title: 🐛 Bug Fixes
      labels:
        - bug
    - title: 📝 Documentation
      labels:
        - documentation
    - title: 🔒 Security
      labels:
        - security
```

## Hands-On Tasks

1. Create an automated release workflow
2. Configure Release Notes template
3. Test the release process
4. Publish a release

## Verification Checklist

- [ ] Able to create a release workflow
- [ ] Able to configure Release Notes
- [ ] Able to publish to npm
- [ ] Able to use semantic versioning

## Next Steps

Continue to [Exercise 16: Monorepo Management in Practice](exercise-16-monorepo.md)

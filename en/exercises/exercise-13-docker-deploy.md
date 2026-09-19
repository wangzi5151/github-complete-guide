# Exercise 13: Docker Deployment in Practice

## Learning Objectives

- Write a Dockerfile
- Build images using GitHub Actions
- Push to a container registry

## Steps

### Step 1: Create a Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/index.js"]
```

### Step 2: Create .dockerignore

```
node_modules
.git
.github
*.md
.env
```

### Step 3: Create a Workflow

```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Login to GHCR
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:${{ github.ref_name }}
```

## Practice Tasks

1. Create a Dockerfile
2. Create .dockerignore
3. Create a Docker build workflow
4. Test image building and pushing

## Verification Checklist

- [ ] Able to write a Dockerfile
- [ ] Able to configure .dockerignore
- [ ] Able to create a Docker build workflow
- [ ] Able to push to GHCR

## Next Step

Continue to [Exercise 14: Security Scanning in Practice](exercise-14-security-scan.md)

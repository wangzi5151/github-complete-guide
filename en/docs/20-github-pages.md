# GitHub Pages Static Website

## What is GitHub Pages?

GitHub Pages is free static website hosting service, can deploy website directly from repository.

**Applicable Scenarios:**
- Personal blog
- Project documentation
- Portfolio showcase
- Learning notes

## Create Website (Detailed with Screenshots)

### Method 1: Directly on main Branch (Simplest)

**Step 1: Create index.html File**

Create an `index.html` file in repository:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>My Website</title>
</head>
<body>
    <h1>Welcome to My Website!</h1>
    <p>This is my first GitHub Pages website.</p>
</body>
</html>
```

**Step 2: Commit and Push**

```bash
git add index.html
git commit -m "Add homepage"
git push
```

**Step 3: Enable GitHub Pages**

1. Open repository page
2. Click **Settings** tab
3. Find **Pages** in left menu
4. Source select **main** branch
5. Click **Save**

```
┌─────────────────────────────────────────────┐
│  GitHub Pages                                │
│                                             │
│  Build and deployment                        │
│                                             │
│  Source: [Deploy from a branch ▼]            │
│                                             │
│  Branch:                                     │
│  [main ▼]  [/ (root) ▼]                     │
│                                             │
│  ☑ Save  ← Click to save                    │
│                                             │
│  Your site is live at                        │
│  https://username.github.io/repo-name/      │
└─────────────────────────────────────────────┘
```

**Step 4: Visit Website**

After deployment complete (usually takes 1-2 minutes), visit:
```
https://your-username.github.io/repo-name/
```

### Method 2: Using docs Directory

**Step 1: Create docs Directory**

```bash
mkdir docs
```

**Step 2: Create index.html**

```bash
echo "<h1>Hello World</h1>" > docs/index.html
```

**Step 3: Commit and Push**

```bash
git add docs/
git commit -m "Add documentation site"
git push
```

**Step 4: Configure Pages**

1. Open repository **Settings** → **Pages**
2. Source select **main** branch's **/docs** directory
3. Click **Save**

### Method 3: Using GitHub Actions

**Step 1: Configure Pages**

1. Open repository **Settings** → **Pages**
2. Source select **GitHub Actions**

```
┌─────────────────────────────────────────────┐
│  GitHub Pages                                │
│                                             │
│  Build and deployment                        │
│                                             │
│  Source: [GitHub Actions ▼]                  │
│                                             │
└─────────────────────────────────────────────┘
```

**Step 2: Create Workflow File**

Create `.github/workflows/pages.yml`:

```yaml
name: Deploy to Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: npm ci && npm run build
    - uses: actions/upload-pages-artifact@v3
      with:
        path: ./dist
        
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
    - id: deployment
      uses: actions/deploy-pages@v4
```

## Custom Domain

### Purchase Domain

Recommended domain providers:
- Alibaba Cloud
- Tencent Cloud
- GoDaddy
- Namecheap

### Setup Steps

**Step 1: Add CNAME File**

Create `CNAME` file in repository root:

```bash
echo "yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

**Step 2: Configure DNS**

Add in domain provider console:

| Record Type | Host Record | Record Value |
|-------------|-------------|--------------|
| CNAME | @ | username.github.io |
| CNAME | www | username.github.io |

**Step 3: Enable HTTPS**

1. Open **Settings** → **Pages**
2. Check **Enforce HTTPS**

```
┌─────────────────────────────────────────────┐
│  GitHub Pages                                │
│                                             │
│  Custom domain: [yourdomain.com]            │
│                                             │
│  ☑ Enforce HTTPS  ← Check to enable        │
│                                             │
└─────────────────────────────────────────────┘
```

## Using Jekyll (Built-in Tool)

Jekyll is GitHub Pages' built-in static site generator, can use Markdown for writing.

### Basic Configuration

Create `_config.yml` file:

```yaml
title: My Blog
description: A simple blog
theme: minima
```

### Create Articles

Create Markdown files in `_posts` directory:

```markdown
---
layout: post
title: "Hello World"
date: 2024-01-01
categories: blog
---

This is my first article.

## Title

Body content...
```

### Theme Selection

```yaml
# _config.yml
remote_theme: pages-themes/cayman@v0.2.0
plugins:
  - jekyll-remote-theme
```

## View Deployment Status

### View Pages Deployment History

1. Open repository **Actions** tab
2. Click **pages build and deployment** workflow
3. View deployment status

```
┌─────────────────────────────────────────────┐
│  Actions                                     │
│                                             │
│  workflows / pages build and deployment      │
│                                             │
│  ✓ Deploy to GitHub Pages                    │
│    ✓ build                                   │
│    ✓ deploy                                  │
│                                             │
│  Deployment time: 2 minutes ago              │
│  Status: Success ✓                           │
└─────────────────────────────────────────────┘
```

### View Pages Settings

```
┌─────────────────────────────────────────────┐
│  GitHub Pages                                │
│                                             │
│  Your site is published at                   │
│  https://username.github.io/repo-name/      │
│                                             │
│  Last deployment: 2 minutes ago              │
│  Deployment status: ✓ Success               │
│                                             │
│  [Visit site]  ← Click to visit website     │
└─────────────────────────────────────────────┘
```

## Limitations

| Limitation | Description |
|------------|-------------|
| Repository size | 1GB |
| Published site size | 1GB |
| Bandwidth | 100GB/month |
| Build count | Max 10 per hour |

## Common Framework Deployment

### React (Create React App)

```yaml
- name: Build
  run: npm run build
  
- name: Deploy
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./build
```

### Vue

```yaml
- name: Build
  run: npm run build
  
- name: Deploy
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./dist
```

---

## Practice Exercise

### Exercise: Create Your First GitHub Pages Website

**Task 1: Create Repository**
1. Create new repository `my-first-website` on GitHub
2. Clone to local

**Task 2: Create Website File**
1. Create `index.html` file
2. Enter simple HTML code
3. Commit and push

**Task 3: Enable GitHub Pages**
1. Open repository **Settings** → **Pages**
2. Source select **main** branch
3. Click **Save**

**Task 4: Visit Website**
1. Wait 1-2 minutes
2. Visit `https://your-username.github.io/my-first-website/`
3. Seeing website content means success

**Verification Method:**
- Website can be accessed normally
- Shows content you created

## Next Step

[GitHub Projects Management →](21-github-projects.md)
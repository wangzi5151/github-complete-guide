# Exercise 5: Deploying Websites with GitHub Pages

## Goal

Learn to deploy static websites using GitHub Pages.

## Steps

### 1. Create Practice Repository

```bash
mkdir github-pages-practice
cd github-pages-practice
git init
```

### 2. Create Website Files

Create `index.html`:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My GitHub Pages Site</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        p { color: #666; line-height: 1.6; }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello GitHub Pages!</h1>
        <p>This is my first GitHub Pages site.</p>
        <p>Deployed in: 2024</p>
        <div class="footer">
            <p>Built with ❤️ using GitHub Pages</p>
        </div>
    </div>
</body>
</html>
```

### 3. Commit and Push

```bash
git add index.html
git commit -m "Initial commit"

git remote add origin git@github.com:your-username/github-pages-practice.git
git push -u origin main
```

### 4. Enable GitHub Pages

1. Go to the repository **Settings**
2. Click **Pages** in the left sidebar
3. Select **main** branch under Source
4. Click **Save**

### 5. Access Your Site

Wait a few minutes, then visit:
```
https://your-username.github.io/github-pages-practice/
```

## Advanced: Using a Custom Domain

### 1. Add CNAME File

```bash
echo "yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

### 2. Configure DNS

Add the following at your domain registrar:
- Type: CNAME
- Host: @ or www
- Value: `your-username.github.io`

### 3. Enable HTTPS

**Settings** → **Pages** → ✅ **Enforce HTTPS**

## Advanced: Using Jekyll

### 1. Create `_config.yml`

```yaml
title: My Site
description: A website powered by Jekyll
theme: minima
```

### 2. Create a Post

Create `_posts/2024-01-01-hello-world.md`:

```markdown
---
layout: post
title: "Hello World"
date: 2024-01-01
categories: blog
---

This is my first blog post.
```

### 3. Commit and Push

```bash
git add .
git commit -m "Add Jekyll configuration"
git push
```

## Advanced: Deploying with GitHub Actions

### 1. Create a Workflow

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
    
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: '.'
        
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

### 2. Enable GitHub Pages

**Settings** → **Pages** → Select **GitHub Actions** as Source

## Key Takeaways

- Basic GitHub Pages usage
- Custom domain configuration
- Jekyll static site generator
- GitHub Actions automated deployment

## Next Steps

[Exercise 6: Contributing to Open Source Projects →](exercise-6-open-source.md)

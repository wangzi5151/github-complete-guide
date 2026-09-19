# Chapter 5: Detailed Guide to GitHub Core Features

## 5.1 Repository Management

### Creating a Repository

#### Method 1: Web-based Creation (Recommended for Beginners)

**Step 1:** Log in to GitHub, click the **+** icon in the top right corner, and select **New repository**

```
┌─────────────────────────────────────────────┐
│  +  [🔔]  [Avatar]                          │
│  │                                          │
│  └─→ New repository  ← Click this           │
│      Import repository                      │
│      New organization                        │
└─────────────────────────────────────────────┘
```

**Step 2:** Fill in repository information

```
┌─────────────────────────────────────────────┐
│  Create a new repository                     │
│                                             │
│  Owner: [your-username ▼]                   │
│                                             │
│  Repository name: [my-project          ]     │
│  Description:     [This is a sample     ]   │
│                    [project              ]   │
│                                             │
│  ○ Public  ← Anyone can see it              │
│  ○ Private ← Only you and collaborators     │
│               can see it                    │
│                                             │
│  ☑ Add a README file  ← Strongly recommended│
│                                             │
│  Add .gitignore: [None ▼]                   │
│  Choose a license: [None ▼]                 │
│                                             │
│        [Create repository]                  │
└─────────────────────────────────────────────┘
```

**Step 3:** Click **Create repository** to complete creation

#### Method 2: Command Line Creation

```bash
# Use GitHub CLI
gh repo create my-repo --public --description "My project"

# Create a private repository
gh repo create my-repo --private
```

### Repository Page Overview

```
┌─────────────────────────────────────────────┐
│  your-username / my-project                  │
│                                             │
│  [Code]  [Issues]  [Pull requests]          │
│  [Actions]  [Projects]  [Wiki]              │
│  [Security]  [Insights]  [Settings]          │
├─────────────────────────────────────────────┤
│                                             │
│  📁 README.md                               │
│  📁 src/                                    │
│  📁 .gitignore                              │
│                                             │
│  This is a sample project...                │
│                                             │
└─────────────────────────────────────────────┘
```

**Tab Descriptions:**

| Tab | Function |
|------|------|
| **Code** | View code files |
| **Issues** | Issue tracking |
| **Pull requests** | Code merge requests |
| **Actions** | Automation workflows |
| **Projects** | Project boards |
| **Wiki** | Project documentation |
| **Security** | Security settings |
| **Insights** | Data analytics |
| **Settings** | Repository settings |

### Repository Settings

**Accessing Settings:**
1. Open the repository page
2. Click the **Settings** tab

**Basic Settings:**

```
┌─────────────────────────────────────────────┐
│  Settings                                    │
│                                             │
│  General  ← Basic settings                  │
│  Access                                       │
│  Branches                                    │
│  Tags                                        │
│  Webhooks                                    │
│  ...                                         │
├─────────────────────────────────────────────┤
│                                             │
│  Repository name: [my-project          ]     │
│  Description:     [This is a sample     ]   │
│                    [project              ]   │
│  Website:         [https://example.com]      │
│  Topics:          [react] [javascript]       │
│                                             │
│           [Save changes]                    │
└─────────────────────────────────────────────┘
```

### Adding Collaborators

**Steps:**
1. Go to **Settings** → **Collaborators**
2. Click **Add people**
3. Enter the other person's GitHub username
4. Click **Add [username] to this repository**

```
┌─────────────────────────────────────────────┐
│  Collaborators                                │
│                                             │
│  Search by username, full name, or email:    │
│  ┌─────────────────────────────────────┐    │
│  │ username                            │    │
│  └─────────────────────────────────────┘    │
│                                             │
│           [Add to repository]               │
└─────────────────────────────────────────────┘
```

### Deleting a Repository

**⚠️ Warning: This operation is irreversible!**

**Steps:**
1. Go to **Settings**
2. Scroll to the bottom of the page
3. Find the **Danger Zone** section
4. Click **Delete this repository**
5. Enter the repository name to confirm deletion

```
┌─────────────────────────────────────────────┐
│  Danger Zone                                 │
│                                             │
│  Delete this repository                      │
│  Once you delete a repository, there is no  │
│  going back.                                │
│                                             │
│  [Delete this repository]                   │
└─────────────────────────────────────────────┘
```

## 5.2 Issue Management

### Creating an Issue

**Step 1:** Go to the repository's **Issues** page

**Step 2:** Click **New issue**

```
┌─────────────────────────────────────────────┐
│  Issues                                      │
│                                             │
│  [New issue]  ← Click this button           │
│                                             │
│  Filters: [Open ▼] [Labels ▼] [Assignee ▼] │
└─────────────────────────────────────────────┘
```

**Step 3:** Fill in the Issue information

```
┌─────────────────────────────────────────────┐
│  New issue                                   │
│                                             │
│  Title: [Bug: Homepage fails to load    ]    │
│                                             │
│  Description:                                │
│  ┌─────────────────────────────────────┐    │
│  │ ## Description                       │    │
│  │ The homepage fails to load           │    │
│  │ properly in certain situations       │    │
│  │                                     │    │
│  │ ## Steps to Reproduce               │    │
│  │ 1. Open the homepage                │    │
│  │ 2. Click the login button            │    │
│  │ 3. The page displays blank           │    │
│  │                                     │    │
│  │ ## Expected Behavior                │    │
│  │ Should display the login form        │    │
│  │                                     │    │
│  │ ## Environment                      │    │
│  │ - OS: Windows 11                    │    │
│  │ - Browser: Chrome 120               │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ☑ Assignees: [Select assignees]            │
│  ☑ Labels: [bug] [help wanted]              │
│  ☑ Milestone: [v1.0]                       │
│                                             │
│        [Submit new issue]                   │
└─────────────────────────────────────────────┘
```

**Step 4:** Click **Submit new issue**

### Using Issue Templates

Many repositories provide Issue templates, which allow you to create standardized Issues more quickly:

```
┌─────────────────────────────────────────────┐
│  Choose a template                           │
│                                             │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ 🐛 Bug     │  │ ✨ Feature  │          │
│  │ Report      │  │ Request     │          │
│  │             │  │             │          │
│  │ [Use        │  │ [Use        │          │
│  │  template]  │  │  template]  │          │
│  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────┘
```

### Managing Issue Labels

**Creating Custom Labels:**

1. On the Issues page, click **Labels**
2. Click **New label**
3. Fill in the information:
   - **Label name**: The name of the label
   - **Description**: Description
   - **Color**: Color
4. Click **Add label**

```
┌─────────────────────────────────────┐
│  New label                           │
│                                     │
│  Label name: [priority: high   ]    │
│  Description: [High priority    ]   │
│              [issue              ]   │
│  Color: [🔴]                        │
│                                     │
│     [Add label]                     │
└─────────────────────────────────────┘
```

### Closing an Issue

**Method 1: Close on the Issue Page**

1. Open the Issue page
2. Click **Close issue** at the bottom

**Method 2: Auto-close Using Keywords**

```bash
# Use keywords in commit messages
git commit -m "fix: fix login issue, closes #42"
git commit -m "fix: fix multiple issues, fixes #42, fixes #43"
```

**Keywords:**
- `closes #42`
- `fixes #42`
- `resolves #42`

## 5.3 Pull Requests

### Creating a PR

**Step 1:** Push the feature branch to remote

```bash
git push -u origin feature-new-button
```

**Step 2:** Open the PR creation page

```
┌─────────────────────────────────────────────┐
│  feature-new-button had recent pushes       │
│                                             │
│  [Compare & pull request]  ← Click to       │
│                               create PR     │
└─────────────────────────────────────────────┘
```

**Step 3:** Select branches

```
┌─────────────────────────────────────────────┐
│  Compare changes                             │
│                                             │
│  base: [main ▼]  ← Target branch            │
│     ...                                     │
│  compare: [feature-new-button ▼]  ← Your    │
│                                   branch    │
│                                             │
│  [Create pull request]                       │
└─────────────────────────────────────────────┘
```

**Step 4:** Fill in PR information

```
┌─────────────────────────────────────────────┐
│  Open a pull request                         │
│                                             │
│  Title: [feat: Add new button feature   ]    │
│                                             │
│  Description:                                │
│  ┌─────────────────────────────────────┐    │
│  │ ## Change Description               │    │
│  │ Added a new button                   │    │
│  │                                     │    │
│  │ ## Change Type                      │    │
│  │ - [x] New feature (feat)            │    │
│  │ - [ ] Bug fix (fix)                 │    │
│  │                                     │    │
│  │ ## Testing                          │    │
│  │ - [x] Tests added                   │    │
│  │ - [x] All tests passed              │    │
│  │                                     │    │
│  │ ## Related Issue                    │    │
│  │ Closes #42                          │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ☑ Reviewers: [Add reviewers]               │
│  ☑ Labels: [enhancement]                    │
│                                             │
│        [Create pull request]                │
└─────────────────────────────────────────────┘
```

**Step 5:** Click **Create pull request**

### Reviewing a PR

**Viewing Code Changes:**

1. Click the **Files changed** tab
2. Review the code changes

```
┌─────────────────────────────────────────────┐
│  Files changed  (3)                          │
│                                             │
│  ─ src/button.ts (+5 -2)                    │
│                                             │
│     1  │ const button = () => {             │
│  -   2  │   return <button>Click</button>;  │
│  +   2  │   return <button className="new"> ││
│  +   3  │     Click                         │
│  +   4  │   </button>;                      │
│     5  │ };                                 │
│                                             │
│  Click the + next to a line number to add   │
│  a comment                                 │
└─────────────────────────────────────────────┘
```

**Adding Inline Comments:**

1. Hover over the line number in the code
2. Click the **+** button that appears
3. Enter your comment in the popup
4. Click **Start review**

```
┌─────────────────────────────────────┐
│  💬 Leave a comment                  │
│                                     │
│  I suggest using a more specific    │
│  class name here                    │
│                                     │
│  ○ Comment  ← Comment only         │
│  ○ Approve  ← Approve              │
│  ○ Request changes ← Request       │
│                        changes      │
│                                     │
│     [Start review]                  │
└─────────────────────────────────────┘
```

### Merging a PR

**Merge Conditions:**
- ✅ All reviewers have approved
- ✅ CI checks have passed
- ✅ No conflicts

**Merge Operations:**

1. Find the merge button at the bottom of the PR page
2. Select the merge method
3. Click **Merge pull request**
4. Click **Confirm merge**

```
┌─────────────────────────────────────────────┐
│  Merge pull request                          │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  ○ Create a merge commit            │    │
│  │    Preserve full commit history     │    │
│  │                                     │    │
│  │  ○ Squash and merge                 │    │
│  │    Squash into a single commit      │    │
│  │                                     │    │
│  │  ○ Rebase and merge                 │    │
│  │    Linear history                   │    │
│  └─────────────────────────────────────┘    │
│                                             │
│        [Merge pull request]                 │
└─────────────────────────────────────────────┘
```

## 5.4 GitHub Actions

### What are GitHub Actions?

GitHub Actions is GitHub's CI/CD platform that automates build, test, and deployment workflows.

### Creating a Workflow

**Step 1:** Create a `.github/workflows` directory in your repository

**Step 2:** Create a YAML file (e.g., `ci.yml`)

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
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        
    - name: Install dependencies
      run: npm install
      
    - name: Run tests
      run: npm test
```

**Step 3:** Commit and push

```bash
git add .github/workflows/ci.yml
git commit -m "ci: Add CI workflow"
git push
```

### Viewing Workflows

1. Go to the repository's **Actions** page
2. View workflow run status

```
┌─────────────────────────────────────────────┐
│  Actions                                     │
│                                             │
│  workflows / CI                              │
│                                             │
│  ✓ Build and Test                            │
│    ✓ build                                   │
│    ✓ test                                    │
│                                             │
│  Deployed: 2 minutes ago                     │
│  Status: Success ✓                           │
└─────────────────────────────────────────────┘
```

### Common Workflow Templates

**Node.js Project:**

```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18, 20, 22]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        
    - run: npm ci
    - run: npm run build
    - run: npm test
```

**Deploy to GitHub Pages:**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      pages: write
      id-token: write
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Build
      run: npm run build
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './dist'
        
    - name: Deploy to GitHub Pages
      uses: actions/deploy-pages@v4
```

## 5.5 GitHub Pages

### Enabling GitHub Pages

**Step 1:** Go to the repository's **Settings** → **Pages**

**Step 2:** Select Source

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
│           [Save]                            │
└─────────────────────────────────────────────┘
```

**Step 3:** Wait for deployment to complete

### Accessing the Website

After deployment is complete, visit:
```
https://your-username.github.io/repository-name/
```

### Custom Domain

**Step 1:** Purchase a domain

**Step 2:** Add a CNAME file

```bash
echo "yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

**Step 3:** Configure DNS

Add the following records in your domain provider's control panel:

| Record Type | Host Name | Record Value |
|----------|----------|--------|
| CNAME | @ | username.github.io |
| CNAME | www | username.github.io |

**Step 4:** Enable HTTPS

1. Open **Settings** → **Pages**
2. Check **Enforce HTTPS**

## 5.6 GitHub Projects

### Creating a Project

```bash
# Use CLI to create a project
gh project create --title "Project Name" --owner your-org
```

### Project Views

| View | Description |
|------|------|
| **Board** | Board view |
| **Table** | Table view |
| **Roadmap** | Roadmap view |
| **Calendar** | Calendar view |

### Automation

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, closed]
  pull_request:
    types: [opened, closed, ready_for_review]

jobs:
  auto-add:
    runs-on: ubuntu-latest
    steps:
    - name: Add to project
      uses: actions/add-to-project@v0.5.0
      with:
        project-url: https://github.com/orgs/your-org/projects/1
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 5.7 Chapter Summary

This chapter provided a detailed overview of GitHub's core features, including:

- Repository Management: Creating, settings, collaborators
- Issue Management: Creating, labels, closing
- Pull Requests: Creating, reviewing, merging
- GitHub Actions: Workflow configuration
- GitHub Pages: Website hosting
- GitHub Projects: Project management

**Key Takeaways:**
- Mastering these features is fundamental to using GitHub
- Practice frequently and apply these features in real projects

**Next Steps:**
[Collaboration & Advanced Topics →](22-fork-contribute.md)

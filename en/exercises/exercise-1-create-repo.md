# Exercise 1: Create Your First Repository

## Goal

Learn how to create a repository on GitHub and perform basic operations.

## Steps

### 1. Create a repository on GitHub

1. Log in to GitHub
2. Click the **+** in the top right corner → **New repository**
3. Fill in the information:
   - Repository name: `my-first-repo`
   - Description: "My first GitHub repository"
   - Select **Public**
   - ✅ Add a README file
4. Click **Create repository**

### 2. Clone the repository to your local machine

```bash
git clone git@github.com:your-username/my-first-repo.git
cd my-first-repo
```

### 3. Create a file and commit

```bash
# Create a new file
echo "# My First Repo" > index.html

# Check the status
git status

# Add the file
git add index.html

# Commit
git commit -m "feat: add homepage file"

# Push
git push
```

### 4. Create a new branch

```bash
# Create and switch to a new branch
git checkout -b feature/add-about

# Create the About page
echo "<h1>About Me</h1>" > about.html

# Commit and push
git add about.html
git commit -m "feat: add about page"
git push -u origin feature/add-about
```

### 5. Create a Pull Request

1. Open the repository on GitHub
2. Click **Pull requests**
3. Click **New pull request**
4. Select the `feature/add-about` branch
5. Fill in the title and description
6. Click **Create pull request**

### 6. Merge the Pull Request

1. Wait for checks to pass
2. Click **Merge pull request**
3. Click **Confirm merge**

## Verification

After completing the steps above, you should see:
- A repository named `my-first-repo` on GitHub
- The repository contains `index.html` and `about.html` files
- A merged Pull Request

## Next Step

[Exercise 2: Branching and Merging Exercise →](exercise-2-branch-merge.md)

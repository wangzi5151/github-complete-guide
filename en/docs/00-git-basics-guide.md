# Chapter 4: Git Basic Commands in Detail

## 4.1 Repository Operations

### Creating a New Repository

#### Method 1: Create on GitHub Web

**Step 1:** Log in to GitHub, click the **+** icon in the top right corner, and select **New repository**

**Step 2:** Fill in repository information
- Repository name: repository name
- Description: repository description (optional)
- Public/Private: choose visibility
- Check **Add a README file**

**Step 3:** Click **Create repository**

#### Method 2: Create Locally

```bash
# Create a new directory
mkdir my-project
cd my-project

# Initialize Git repository
git init
```

**What does `git init` do:**
- Creates the `.git` directory
- Initializes repository structure
- Creates the default branch (usually main)

#### Method 3: Clone an Existing Repository

```bash
# Clone a repository
git clone https://github.com/user/repo.git

# Clone into a specific directory
git clone https://github.com/user/repo.git my-folder

# Clone a specific branch
git clone -b develop https://github.com/user/repo.git
```

### Checking Repository Status

```bash
git status
```

**Example Output:**

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
        modified:   src/index.js

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/utils.js

no changes added to commit (use "git add" and/or "git commit -a")
```

**Status Explanation:**
- `Changes not staged for commit`: modified but not staged
- `Untracked files`: new files, not tracked by Git
- `Changes to be committed`: staged, waiting to be committed

## 4.2 File Operations

### Adding Files to the Staging Area

```bash
# Add a single file
git add index.html

# Add multiple files
git add index.html style.css

# Add all changes
git add .

# Add all .js files
git add *.js

# Add all files in the src directory
git add src/
```

**What is the Staging Area?**

The staging area (Staging Area) is an intermediate area used to prepare content for the next commit. You can selectively add files instead of committing all changes at once.

```
Working directory → Staging area → Repository
       git add    git commit
```

### Committing Changes

```bash
# Commit staged content
git commit -m "Description"

# Commit with detailed description
git commit -m "Description" -m "Detailed description"

# Add all changes and commit (skip git add)
git commit -am "Description"

# Amend the most recent commit
git commit --amend -m "New description"
```

**Commit Message Convention:**

```
type(scope): description

Detailed description (optional)

Related Issue (optional)
```

**Type Descriptions:**
- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation update
- `style`: code formatting (does not affect functionality)
- `refactor`: refactoring
- `test`: tests
- `chore`: build/tooling

**Examples:**
```bash
git commit -m "feat: add user login feature"
git commit -m "fix: fix login page styling issue"
git commit -m "docs: update README installation instructions"
```

### Viewing File Differences

```bash
# View differences between working directory and staging area
git diff

# View differences between staging area and repository
git diff --staged

# View differences between two commits
git diff abc1234 def5678

# View differences for a specific file
git diff index.html
```

## 4.3 Branch Operations

### Viewing Branches

```bash
# View local branches
git branch

# View all branches (including remote)
git branch -a

# View branches with last commit
git branch -v

# View merged branches
git branch --merged

# View unmerged branches
git branch --no-merged
```

**Example Output:**
```
* main          abc1234 latest commit message
  feature-login def5678 add login feature
  feature-cart  ghi9012 shopping cart feature
```

The one marked with `*` is the current branch.

### Creating Branches

```bash
# Create a new branch
git branch feature-login

# Create and switch to a new branch (recommended)
git checkout -b feature-login

# Or use new syntax
git switch -c feature-login

# Create a branch based on a specific commit
git checkout -b feature-login abc1234

# Create a local branch based on a remote branch
git checkout -b feature-login origin/feature-login
```

### Switching Branches

```bash
# Switch to an existing branch
git checkout feature-login

# Or use new syntax
git switch feature-login
```

### Merging Branches

```bash
# Switch to the target branch
git checkout main

# Merge the feature branch
git merge feature-login

# Merge and create a merge commit
git merge --no-ff feature-login

# Abort the merge
git merge --abort
```

**Merge Types:**

1. **Fast-forward merge**
```
Before merge:
main:    A --- B --- C
                      \
feature:               D --- E

After merge:
main:    A --- B --- C --- D --- E
```

2. **Three-way merge**
```
Before merge:
main:    A --- B --- C --- F
                      \
feature:               D --- E

After merge:
main:    A --- B --- C --- F --- M (merge commit)
                      \         /
feature:               D --- E
```

### Deleting Branches

```bash
# Delete a merged branch
git branch -d feature-login

# Force delete a branch
git branch -D feature-login

# Delete a remote branch
git push origin --delete feature-login
```

### Renaming Branches

```bash
# Rename the current branch
git branch -m new-name

# Rename a specific branch
git branch -m old-name new-name
```

## 4.4 Remote Operations

### Viewing Remote Repositories

```bash
# View remote repository list
git remote -v

# View detailed remote repository info
git remote show origin
```

### Adding Remote Repositories

```bash
# Add a remote repository
git remote add origin https://github.com/user/repo.git

# Add multiple remote repositories
git remote add upstream https://github.com/owner/repo.git
```

### Pushing to Remote

```bash
# Push the current branch
git push

# Push to a specific branch
git push origin main

# First push and set upstream branch
git push -u origin main

# Push all branches
git push --all

# Push tags
git push --tags
```

### Pulling from Remote

```bash
# Fetch remote changes (without merging)
git fetch

# Pull and merge
git pull

# Pull and rebase
git pull --rebase

# Pull a specific remote branch
git pull origin main
```

### Viewing Remote Branches

```bash
# View remote branches
git branch -r

# View all branches (local + remote)
git branch -a

# View detailed info for remote branches
git branch -vv
```

## 4.5 Viewing History

### Viewing Commit History

```bash
# View all commits
git log

# View compact history
git log --oneline

# View graphical history
git log --graph --oneline

# View the last 5 commits
git log -5

# View history for a specific file
git log index.html

# View commits by a specific author
git log --author="Zhang"

# Filter by date
git log --since="2024-01-01"
git log --until="2024-12-31"
```

**Example Output:**
```
* abc1234 (HEAD -> main) feat: add user login
* def5678 fix: fix styling issue
* ghi9012 docs: update README
* jkl3456 feat: initialize project
```

### Viewing Commit Details

```bash
# View detailed info for a specific commit
git show abc1234

# View file changes for a specific commit
git show --stat abc1234
```

### Viewing File Changes

```bash
# View differences between working directory and staging area
git diff

# View differences between staging area and repository
git diff --staged

# View changes from a specific commit
git diff abc1234^ abc1234

# View changes for a specific file
git diff index.html
```

## 4.6 Undo Operations

### Undoing Working Directory Changes

```bash
# Discard working directory changes
git restore index.html

# Discard all changes
git restore .
```

### Undoing Staging Area Changes

```bash
# Remove a file from staging area (keep working directory changes)
git restore --staged index.html

# Remove all files from staging area
git restore --staged .
```

### Amending the Most Recent Commit

```bash
# Amend commit message
git commit --amend -m "New commit message"

# Add a file to the most recent commit
git add forgotten-file.js
git commit --amend --no-edit
```

### Reverting Commits

```bash
# Revert to a specific commit (keep changes in working directory)
git reset abc1234

# Revert to a specific commit (keep changes in staging area)
git reset --soft abc1234

# Revert to a specific commit (discard all changes)
git reset --hard abc1234

# Revert the most recent commit
git reset HEAD~1
```

**Three modes of `reset`:**

| Mode | Description |
|------|------|
| `--soft` | Keep working directory and staging area changes |
| `--mixed` (default) | Keep working directory changes, clear staging area |
| `--hard` | Discard all changes |

### Creating a Reverse Commit

```bash
# Create a new commit to revert a previous commit
git revert abc1234
```

## 4.7 Tag Operations

### Viewing Tags

```bash
# List all tags
git tag

# View tag details
git show v1.0.0

# Search tags by pattern
git tag -l "v1.*"
```

### Creating Tags

```bash
# Create a lightweight tag
git tag v1.0.0

# Create an annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create a tag for a specific commit
git tag -a v1.0.0 abc1234 -m "Release version 1.0.0"
```

### Pushing Tags

```bash
# Push a single tag
git push origin v1.0.0

# Push all tags
git push origin --tags
```

### Deleting Tags

```bash
# Delete a local tag
git tag -d v1.0.0

# Delete a remote tag
git push origin --delete v1.0.0
```

### Checking Out Tags

```bash
# Check out a tag (read-only)
git checkout v1.0.0

# Create a branch based on a tag
git checkout -b release-1.0.0 v1.0.0
```

## 4.8 Stash Operations

### Stashing Current Changes

```bash
# Stash all changes
git stash

# Stash with a description
git stash save "Working on login feature"

# Stash untracked files
git stash -u

# Stash all files (including ignored)
git stash -a
```

### Viewing Stash List

```bash
git stash list
```

**Example Output:**
```
stash@{0}: On main: Working on login feature
stash@{1}: WIP on main: abc1234 some commit
```

### Restoring Stashed Changes

```bash
# Restore the most recent stash (keep stash record)
git stash apply

# Restore the most recent stash (delete stash record)
git stash pop

# Restore a specific stash
git stash apply stash@{2}

# Restore a specific stash and delete the record
git stash pop stash@{2}
```

### Deleting Stashes

```bash
# Delete the most recent stash
git stash drop

# Delete a specific stash
git stash drop stash@{0}

# Delete all stashes
git stash clear
```

### Viewing Stash Details

```bash
# View detailed content of the most recent stash
git stash show -p

# View detailed content of a specific stash
git stash show -p stash@{2}
```

## 4.9 Chapter Summary

This chapter provided a detailed introduction to Git basic commands, including:

- Repository operations: create, clone, check status
- File operations: add, commit, view differences
- Branch operations: create, switch, merge, delete
- Remote operations: add, push, pull
- History viewing: log, diff, details
- Undo operations: amend, revert, reverse commit
- Tag operations: create, push, delete
- Stash operations: stash, restore, delete

**Key Takeaways:**
- Mastering these commands is the foundation of using Git
- Practice more to deepen your understanding through hands-on experience
- Don't panic when encountering problems — most operations can be undone

**Next Step:**
[GitHub Core Features →](14-create-repo.md)

# Exercise 2: Branch and Merge Practice

## Goal

Master Git branch creation, switching, merging, and deletion operations.

## Steps

### 1. Create a Practice Repository

```bash
mkdir branch-practice
cd branch-practice
git init
echo "# Branch Practice" > README.md
git add README.md
git commit -m "Initial commit"
```

### 2. Create Multiple Branches

```bash
# Create a feature branch
git checkout -b feature-1
echo "Feature 1" > feature1.txt
git add feature1.txt
git commit -m "feat: add feature 1"

# Return to the main branch
git checkout main

# Create another feature branch
git checkout -b feature-2
echo "Feature 2" > feature2.txt
git add feature2.txt
git commit -m "feat: add feature 2"

# View all branches
git branch -a
```

### 3. Merge a Branch

```bash
# Merge feature-1 into main
git checkout main
git merge feature-1

# View history
git log --oneline --graph --all
```

### 4. Handle Merge Conflicts

```bash
# Modify a file on the main branch
echo "Main changes" > shared.txt
git add shared.txt
git commit -m "main: modify shared.txt"

# Modify the same file on the feature-2 branch
git checkout feature-2
echo "Feature 2 changes" > shared.txt
git add shared.txt
git commit -m "feat: modify shared.txt"

# Attempt to merge (there will be a conflict)
git checkout main
git merge feature-2
```

### 5. Resolve the Conflict

1. Open `shared.txt`
2. Choose the content to keep
3. Delete the conflict markers
4. Commit

```bash
# After manually editing the file
git add shared.txt
git commit -m "resolve merge conflict"
```

### 6. Delete Branches

```bash
# Delete merged branches
git branch -d feature-1
git branch -d feature-2

# View remaining branches
git branch
```

### 7. Push to Remote

```bash
git remote add origin git@github.com:your-username/branch-practice.git
git push -u origin main
```

## Challenge Task

1. Create a branch named `hotfix`
2. Fix a bug on the `hotfix` branch
3. Merge the `hotfix` branch into `main`
4. Delete the `hotfix` branch

## Key Concepts

- `git branch`: view and create branches
- `git checkout`: switch branches
- `git merge`: merge branches
- `git branch -d`: delete a branch
- `git log --graph`: view branch graph

## Next Step

[Exercise 3: Pull Request Workflow →](exercise-3-pull-request.md)

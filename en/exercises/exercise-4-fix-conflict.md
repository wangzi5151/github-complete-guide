# Exercise 4: Fix Merge Conflict

## Goal

Learn to identify and resolve Git merge conflicts.

## Steps

### 1. Create a Practice Repository

```bash
mkdir conflict-practice
cd conflict-practice
git init

# Create initial file
echo "Hello World" > greeting.txt
git add greeting.txt
git commit -m "Initial commit"

git remote add origin git@github.com:your-username/conflict-practice.git
git push -u origin main
```

### 2. Simulate a Conflict Scenario

```bash
# Create two branches
git checkout -b alice-branch
git checkout main
git checkout -b bob-branch

# Alice's changes
git checkout alice-branch
echo "Hello Alice" > greeting.txt
git add greeting.txt
git commit -m "Alice: modify greeting"

# Bob's changes
git checkout bob-branch
echo "Hello Bob" > greeting.txt
git add greeting.txt
git commit -m "Bob: modify greeting"

# Push branches
git push -u origin alice-branch
git push -u origin bob-branch
```

### 3. Create a Conflicting PR

On GitHub:
1. Create a PR from `alice-branch` to `main`
2. Merge the PR
3. Create a PR from `bob-branch` to `main`

You will now see that the PR has a conflict.

### 4. Resolve the Conflict

#### Method 1: Resolve Locally

```bash
# Update main branch
git checkout main
git pull

# Attempt to merge bob-branch
git merge bob-branch
# This will produce a conflict

# View conflicted files
git status

# Open greeting.txt, you will see:
# <<<<<<< HEAD
# Hello Alice
# =======
# Hello Bob
# >>>>>>> bob-branch
```

#### Method 2: Edit the File Manually

Open `greeting.txt` and choose the content to keep:

```text
Hello Alice and Bob
```

#### Method 3: Use a Tool to Resolve

```bash
# Use VS Code
code greeting.txt

# In VS Code, conflicts will be highlighted
# You can use "Accept Current", "Accept Incoming", "Accept Both" buttons
```

### 5. Complete the Merge

```bash
# Mark as resolved
git add greeting.txt

# Complete the commit
git commit -m "Resolve merge conflict between Alice and Bob"

# Push to remote
git push
```

### 6. Resolve in a PR

If a conflict is found in a PR:

```bash
# Resolve locally
git checkout bob-branch
git merge main
# Resolve the conflict
git add greeting.txt
git commit -m "Resolve conflict with main branch"
git push
```

The PR will update automatically.

## Conflict Markers Explained

```text
<<<<<<< HEAD (content from current branch)
This is the modification from the current branch
=======
This is the content from the branch being merged
>>>>>>> branch-name
```

## Advanced Tips

### Use rebase to Avoid Conflicts

```bash
# On the feature branch
git checkout alice-branch
git rebase main
# After resolving conflicts
git rebase --continue
```

### Abort a Merge

```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort
```

### Preventing Conflicts

1. **Sync frequently**: Pull from main regularly
2. **Small commits**: Reduce the scope of conflicts
3. **Communication and collaboration**: Avoid modifying the same file at the same time

## Key Takeaways

- Understanding conflict markers
- Manually resolving conflicts
- Using tools to resolve conflicts
- `git merge --abort` to abort a merge
- `git rebase` to avoid conflicts

## Next Step

[Exercise 5: Deploy a Website with GitHub Pages →](exercise-5-github-pages.md)

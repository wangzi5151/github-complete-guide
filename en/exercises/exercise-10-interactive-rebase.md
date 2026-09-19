# Exercise 10: Interactive Rebase in Practice

## Learning Objectives

- Master the use of `git rebase -i`
- Learn to squash commits
- Understand how to reorder commits
- Learn to modify commit messages

## Scenario Description

During development, you have created multiple small commits. Now you need to clean up the commit history before submitting a PR to make it clearer.

## Steps

### Step 1: Create a Test Repository

```bash
mkdir rebase-practice
cd rebase-practice
git init
```

### Step 2: Create Initial Commit

```bash
echo "# Project" > README.md
git add .
git commit -m "feat: Initialize project"
```

### Step 3: Create Multiple Commits

```bash
# Commit 1
echo "Feature 1" > feature1.js
git add .
git commit -m "feat: Add feature 1"

# Commit 2 (Fix Typo)
echo "Feature 1 fix" >> feature1.js
git add .
git commit -m "fix: Fix feature 1 typo"

# Commit 3
echo "Feature 2" > feature2.js
git add .
git commit -m "feat: Add feature 2"

# Commit 4 (Space Fix)
echo "Feature 2 " >> feature2.js
git add .
git commit -m "chore: Fix space"

# Commit 5
echo "Feature 3" > feature3.js
git add .
git commit -m "feat: Add feature 3"
```

### Step 4: View Commit History

```bash
git log --oneline
```

### Step 5: Start Interactive Rebase

```bash
# Reorder the last 5 commits
git rebase -i HEAD~5
```

## Interactive Rebase Commands

### Common Commands

| Command | Description |
|------|------|
| `pick` | Keep the commit |
| `reword` | Keep the commit, modify commit message |
| `edit` | Pause the commit, allow modifying content |
| `squash` | Squash the commit into the previous commit |
| `fixup` | Squash the commit into the previous commit, discard commit message |
| `drop` | Delete the commit |

### Operation Examples

The editor will open and display:

```
pick abc1234 feat: Add feature 1
pick def5678 fix: Fix feature 1 typo
pick ghi9012 feat: Add feature 2
pick jkl3456 chore: Fix space
pick mno7890 feat: Add feature 3
```

Change to:

```
pick abc1234 feat: Add feature 1
fixup def5678 fix: Fix feature 1 typo
pick ghi9012 feat: Add feature 2
fixup jkl3456 chore: Fix space
pick mno7890 feat: Add feature 3
```

## Hands-on Tasks

### Task 1: Squash Commits

1. Create 3 related commits
2. Use `squash` to combine them into one commit
3. Write a new commit message

```bash
# Create test commits
echo "Code 1" > file1.js
git add . && git commit -m "feat: Add file 1"

echo "Code 2" > file2.js
git add . && git commit -m "feat: Add file 2"

echo "Code 3" > file3.js
git add . && git commit -m "feat: Add file 3"

# Squash commits
git rebase -i HEAD~3
```

### Task 2: Reorder Commit Order

1. Create 3 separate commits
2. Use interactive rebase to reorder them
3. Verify the order has changed

### Task 3: Modify Commit Message

1. Create a commit
2. Use `reword` to modify the commit message
3. Verify the message has been updated

### Task 4: Edit Commit Content

1. Create a commit
2. Use `edit` to pause the commit
3. Modify file content
4. Continue rebase

```bash
git rebase -i HEAD~1
# Change pick to edit
# Save and exit

# Modify file
echo "Modified content" > file.js
git add .
git commit --amend

# Continue rebase
git rebase --continue
```

## Advanced Tips

### Using rebase to merge branches

```bash
# Rebase feature branch onto main
git checkout feature
git rebase main

# Continue after resolving conflicts
git rebase --continue

# If you want to abort
git rebase --abort
```

### Automated rebase

```bash
# Auto-squash the last 3 commits
GIT_SEQUENCE_EDITOR="sed -i '2s/pick/fixup/'" git rebase -i HEAD~3
```

## Verification Checklist

- [ ] Can start interactive rebase
- [ ] Can use `pick`, `squash`, `fixup` commands
- [ ] Can reorder commit order
- [ ] Can modify commit messages
- [ ] Can edit commit content
- [ ] Understand `rebase --continue` and `rebase --abort`

## FAQ

### Q: What's the difference between rebase and merge?
A: rebase rewrites commit history, producing a linear history; merge preserves the original commit history.

### Q: When should you not rebase?
A: You should not rebase public branches that have already been pushed to remote.

### Q: How to handle rebase conflicts?
A: After resolving conflicts, use `git add` to mark them as resolved, then use `git rebase --continue`.

## Next Steps

After completing this exercise, please continue to [Exercise 11: Advanced GitHub CLI Usage](exercise-11-github-cli.md)
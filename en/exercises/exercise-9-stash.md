# Exercise 9: Git Stash in Practice

## Learning Objectives

- Master the basic operations of git stash
- Understand the use cases for stash
- Learn to manage multiple stashes

## Scenario Description

You are developing a new feature when you suddenly need to switch to another branch to fix an urgent bug. Use stash to temporarily save your work.

## Steps

### Step 1: Create a Test Repository

```bash
mkdir stash-practice
cd stash-practice
git init
```

### Step 2: Create Initial Files

```bash
echo "# Project Description" > README.md
echo "console.log('Hello');" > app.js
git add .
git commit -m "feat: initial commit"
```

### Step 3: Start New Feature Development

```bash
echo "// New feature code" >> app.js
echo "// More code" >> app.js
git status
```

### Step 4: Use Stash to Save Work

```bash
# Save current work
git stash save "Working on new feature"

# View stash list
git stash list
```

### Step 5: Switch Branch to Fix Bug

```bash
# Create and switch to fix branch
git checkout -b fix/urgent-bug

# Fix the bug
echo "// Fixed code" > bugfix.js
git add .
git commit -m "fix: fix urgent bug"

# Switch back to original branch
git checkout main
```

### Step 6: Restore Stashed Content

```bash
# Restore most recent stash
git stash pop

# View file contents
cat app.js
```

## Advanced Operations

### View Stash Details

```bash
# View detailed content of a stash
git stash show -p stash@{0}

# View a specific stash
git stash show -p stash@{1}
```

### Manage Multiple Stashes

```bash
# Save multiple stashes
git stash save "Feature 1"
git stash save "Feature 2"
git stash save "Feature 3"

# View all stashes
git stash list

# Apply a specific stash (without deleting)
git stash apply stash@{1}

# Delete a specific stash
git stash drop stash@{1}
```

### Clear All Stashes

```bash
# Delete all stashes
git stash clear

# Or delete specific stashes
git stash drop stash@{0}
git stash drop stash@{1}
```

## Hands-on Tasks

### Task 1: Create and Manage Stashes

1. Create a new file `feature.js`
2. Add some content but do not commit
3. Use stash to save the changes
4. Create another file `temp.js`
5. Use stash to save again
6. View the stash list
7. Restore the first stash

### Task 2: Handle Stash Conflicts

1. Modify file A and stash
2. On another branch, modify file A and commit
3. Switch back to the original branch
4. Try `git stash pop`
5. Resolve the conflict

### Task 3: Use the `-u` Flag

```bash
# Save untracked files
git stash save -u "Including new files"
```

1. Create a new file (untracked)
2. Stash using the `-u` flag
3. Verify the new file was saved in the stash

## Verification Checklist

- [ ] Able to use `git stash save`
- [ ] Able to use `git stash list`
- [ ] Able to use `git stash pop`
- [ ] Able to use `git stash apply`
- [ ] Able to use `git stash show`
- [ ] Able to manage multiple stashes
- [ ] Able to handle stash conflicts

## Frequently Asked Questions

### Q: What is the difference between stash and commit?
A: Stash is a temporary save that does not create a new commit; commit permanently saves to the history.

### Q: Does stash save untracked files?
A: Not by default. You need to use the `-u` flag.

### Q: How to recover a deleted stash?
A: Use the reflog feature of `git stash`:
```bash
git fsck --no-reflogs | grep commit
git stash apply <commit-hash>
```

## Next Steps

After completing this exercise, please continue to [Exercise 10: Interactive Rebase in Practice](exercise-10-interactive-rebase.md)

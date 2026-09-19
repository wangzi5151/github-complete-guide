# Exercise 3: Pull Request Workflow

## Goal

Master the complete workflow of collaborative development using Pull Requests.

## Prerequisites

### 1. Create a Practice Repository

```bash
# Create a repository on GitHub named pr-practice
gh repo create pr-practice --public

# Clone it locally
git clone git@github.com:your-username/pr-practice.git
cd pr-practice

# Create an initial file
echo "# PR Practice" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

## Steps

### 1. Create a Feature Branch

```bash
git checkout -b feature/add-todo
```

### 2. Implement the Feature

Create `todo.js`:

```javascript
// todo.js
const todos = [];

function addTodo(text) {
  todos.push({
    id: Date.now(),
    text,
    completed: false
  });
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
  }
}

function removeTodo(id) {
  const index = todos.findIndex(t => t.id === id);
  if (index > -1) {
    todos.splice(index, 1);
  }
}

module.exports = { addTodo, toggleTodo, removeTodo };
```

### 3. Commit and Push

```bash
git add todo.js
git commit -m "feat: add todo functionality"

git push -u origin feature/add-todo
```

### 4. Create a Pull Request

```bash
# Using GitHub CLI
gh pr create \
  --title "feat: add todo functionality" \
  --body "## Description of Changes
- Added addTodo function
- Added toggleTodo function
- Added removeTodo function

## Testing
- [x] Local testing passed

## Related Issues
None"
```

### 5. Code Review

On GitHub:
1. Review the PR's code changes
2. Add review comments
3. Click **Review changes**
4. Select **Approve** or **Request changes**

### 6. Respond to Review

If changes are needed:

```bash
# Make changes based on review feedback
git add todo.js
git commit -m "fix: add parameter validation based on review"
git push
```

The PR will update automatically.

### 7. Merge the PR

```bash
# Using GitHub CLI
gh pr merge --merge
```

### 8. Cleanup

```bash
# Delete the merged remote branch
git push origin --delete feature/add-todo

# Delete the local branch
git checkout main
git pull
git branch -d feature/add-todo
```

## PR Template

Create `.github/pull_request_template.md`:

```markdown
## Description of Changes
<!-- Describe what this PR does -->

## Type of Change
- [ ] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Documentation update (docs)
- [ ] Other

## Testing
- [ ] Tests added
- [ ] All tests passed

## Screenshots (if applicable)
```

## Best Practices

1. **Clear PR titles**: Follow Conventional Commits
2. **Complete descriptions**: Explain what was changed and why
3. **Small commits**: One PR does one thing
4. **Respond promptly**: Don't make reviewers wait

## Next Steps

[Exercise 4: Fix Merge Conflicts →](exercise-4-fix-conflict.md)

# Exercise 6: Participating in Open Source Projects

## Objective

Learn how to Fork a project, create PRs, and participate in open source contributions.

## Steps

### 1. Find a Suitable Project

Search using the following labels:
- `good first issue`
- `help wanted`
- `beginner friendly`

### 2. Fork the Project

1. Find the target repository
2. Click the **Fork** button in the top right corner
3. Wait for the Fork to complete

### 3. Clone Your Fork

```bash
git clone git@github.com:your-username/project-name.git
cd project-name
```

### 4. Add the Upstream Repository

```bash
git remote add upstream git@github.com:original-author/project-name.git

# Verify
git remote -v
```

### 5. Create a Feature Branch

```bash
# Sync with the latest upstream code
git fetch upstream
git checkout main
git merge upstream/main

# Create a feature branch
git checkout -b fix/typo-in-readme
```

### 6. Make Changes

For example, fix a typo in the README:

```bash
# Edit the file
vim README.md

# Commit
git add README.md
git commit -m "docs: Fix typo in README"
```

### 7. Push to Your Fork

```bash
git push origin fix/typo-in-readme
```

### 8. Create a Pull Request

1. Open your Fork page
2. Click **Compare & pull request**
3. Confirm:
   - base repository: the original author's repository
   - head repository: your Fork
4. Fill in the PR description
5. Click **Create pull request**

### 9. Write a Good PR Description

```markdown
## Description of Changes
Fixed the typo "installtion" in the README, changed to "installation".

## Type of Change
- [x] Documentation update (docs)

## Related Issue
None

## Screenshots
None
```

### 10. Wait for Review

- Respond to reviewer comments
- Make changes based on feedback
- Be patient and friendly

## Best Practices

### Before Submitting
1. Read CONTRIBUTING.md
2. Understand the code standards
3. Check if there are already related Issues/PRs

### When Submitting
1. Use clear commit messages
2. One PR should only do one thing
3. Write a good PR description

### After Submitting
1. Respond to feedback in a timely manner
2. Be polite and professional
3. Accept that it may be rejected

## Common Questions

### Q: What if my PR is rejected?
**A:** This is very normal, don't be discouraged. Ask for the reason, learn and improve, or look for other contribution opportunities.

### Q: How do I sync upstream updates?
**A:**
```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Q: How do I revert a commit in a PR?
**A:**
```bash
git revert commit-hash
git push
```

## Types of Open Source Contributions

1. **Fix Bugs**: The simplest way to contribute
2. **Improve Documentation**: Add explanations, fix errors
3. **Add Tests**: Improve code quality
4. **Add Features**: Larger changes
5. **Translate Content**: Help more people

## Key Takeaways

- The concept and usage of Fork
- Syncing with upstream repositories
- Creating high-quality PRs
- Open source contribution etiquette

## Congratulations!

After completing this exercise, you have mastered the basic usage of GitHub. Keep participating in open source projects and you will become more and more proficient!

## Recommended Resources

- [First Timers Only](https://www.firsttimersonly.com/)
- [Good First Issues](https://goodfirstissue.dev/)
- [Up For Grabs](https://up-for-grabs.net/)

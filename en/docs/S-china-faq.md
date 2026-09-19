# Chinese Developer FAQ

## Account Related

### Q: Can't receive verification code when registering GitHub account?

**Solution**:
1. Use foreign email (Gmail, Outlook)
2. Check spam folder
3. Try using different browser
4. Try again later

### Q: What to do if GitHub account is restricted?

**Solution**:
1. Contact GitHub support
2. Provide identity verification
3. Wait for unblocking

### Q: How to delete GitHub account?

**Steps**:
1. Go to Settings
2. Scroll to bottom
3. Click Delete account
4. Confirm deletion

---

## Network Related

### Q: Cannot access GitHub?

**Solution**:
1. Modify hosts file
2. Use acceleration proxy
3. Configure VPN/proxy
4. Use domestic mirrors

### Q: git push is very slow?

**Solution**:
```bash
# Use SSH instead of HTTPS
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Use shallow clone
git clone --depth 1

# Configure proxy
git config --global http.proxy http://127.0.0.1:7890
```

### Q: GitHub Pages cannot be accessed?

**Solution**:
1. Wait a few minutes (first deployment needs time)
2. Check repository settings
3. Use custom domain
4. Configure DNS

---

## Git Related

### Q: Git Chinese filename shows garbled text?

**Solution**:
```bash
git config --global core.quotepath false
```

### Q: How to write Chinese in Git commit message?

**Solution**:
```bash
git commit -m "feat: Add new feature"
```

### Q: How to ignore file permission changes?

**Solution**:
```bash
git config --global core.fileMode false
```

### Q: How to set default branch to main?

**Solution**:
```bash
git config --global init.defaultBranch main
```

---

## Collaboration Related

### Q: How to participate in international open source projects?

**Suggestions**:
1. Start with documentation contributions
2. Fix simple bugs
3. Use English for communication
4. Follow project standards

### Q: How to participate in GitHub with poor English?

**Suggestions**:
1. Use translation tools
2. Learn common terms
3. Start with domestic projects
4. Participate in Chinese communities

### Q: How to showcase projects on GitHub?

**Suggestions**:
1. Write good README
2. Add documentation
3. Write tests
4. Use tags
5. Update regularly

---

## Security Related

### Q: How to protect GitHub account?

**Suggestions**:
1. Enable two-factor authentication
2. Use SSH keys
3. Change password regularly
4. Don't share credentials

### Q: How to detect sensitive information in code?

**Solution**:
```bash
# Use git-secrets
git secrets --install
git secrets --scan

# Use truffleHog
trufflehog git file://.
```

### Q: How to prevent accidental commit of sensitive information?

**Solution**:
1. Use .gitignore
2. Use pre-commit hook
3. Regularly check code

---

## Performance Related

### Q: How to accelerate GitHub access?

**Solutions**:
1. Modify hosts
2. Use proxy
3. Use mirrors
4. Use SSH

### Q: How to optimize large repository cloning?

**Solution**:
```bash
# Shallow clone
git clone --depth 1

# Clone specific branch only
git clone --single-branch --branch main

# Use sparse checkout
git sparse-checkout init
git sparse-checkout set dir1 dir2
```

### Q: How to clean Git repository?

**Solution**:
```bash
# Garbage collection
git gc

# Clean untracked files
git clean -fd

# Compress history
git repack -a -d
```

---

## Tool Related

### Q: Which Git clients are recommended?

**Recommendations**:
| Tool | Platform | Features |
|------|----------|----------|
| GitKraken | Cross-platform | Powerful features |
| SourceTree | Windows/Mac | Free |
| GitHub Desktop | Cross-platform | Simple and easy to use |
| VS Code | Cross-platform | Integrated development |

### Q: How to configure Git aliases?

**Examples**:
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all"
```

### Q: How to use GitHub CLI?

**Installation**:
```bash
# macOS
brew install gh

# Windows
winget install GitHub.cli

# Linux
sudo apt install gh
```

**Usage**:
```bash
# Login
gh auth login

# Create repository
gh repo create my-repo --public

# Create PR
gh pr create --title "New feature" --body "Description"
```

---

## More Questions

If the above didn't solve your problem, you can:

1. Search [GitHub Discussions](https://github.com/wangzi5151/github-complete-guide/discussions)
2. Submit [Issue](https://github.com/wangzi5151/github-complete-guide/issues)
3. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/git)
# Exercise 18: GitHub Enterprise Setup Practice

## Learning Objectives

- Configure organization-level policies
- Set up branch protection
- Configure security features

## Steps

### Step 1: Create an Organization

```bash
# Create organization
gh api orgs \
  --method POST \
  -f login="my-org" \
  -f profile_name="My Organization" \
  -f billing_email="admin@example.com"
```

### Step 2: Configure CODEOWNERS

```yaml
# .github/CODEOWNERS
* @your-username
/docs/ @your-username
/src/ @your-username
```

### Step 3: Configure Branch Protection

```bash
# Use API to configure branch protection
gh api repos/{org}/{repo}/branches/main/protection \
  --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["ci/test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

### Step 4: Configure Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Step 5: Configure Security Alerts

```bash
# Enable Secret Scanning
gh api repos/{org}/{repo}/secret-scanning \
  --method PUT \
  -f status='enabled'

# Enable Dependabot alerts
gh api repos/{org}/{repo}/vulnerability-alerts \
  --method PUT \
  -f enabled='true'
```

## Practical Tasks

1. Create a GitHub organization
2. Configure CODEOWNERS
3. Configure branch protection rules
4. Configure Dependabot
5. Enable security features

## Verification Checklist

- [ ] Organization created
- [ ] CODEOWNERS configured
- [ ] Branch protection enabled
- [ ] Dependabot configured
- [ ] Security features enabled

## Next Steps

Continue to [Exercise 19: GitHub Actions Reusable Workflows](exercise-19-reusable-workflows.md)

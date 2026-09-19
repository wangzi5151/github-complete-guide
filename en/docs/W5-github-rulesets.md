# GitHub Rulesets Introduction

## What are Rulesets?

GitHub Rulesets is the next-generation alternative to branch protection rules. It provides more flexible ways to control push, merge, and delete operations for branches and tags.

## Rulesets vs Legacy Protection Rules

| Feature | Rulesets | Legacy Protection Rules |
|---------|----------|------------------------|
| Scope | Repository, Organization, Enterprise | Repository only |
| Conditions | Multiple condition combinations | Branch name matching only |
| Nested Rules | Supported | Not supported |
| Priority | Supported | Not supported |
| Bypass Permissions | More flexible | Simpler |

## Creating a Ruleset

### Creating via Web UI

1. Go to repository **Settings** → **Rules** → **Rulesets**
2. Click **New ruleset** → **New branch ruleset**
3. Configure the rules

### Creating via API

```bash
gh api repos/{owner}/{repo}/rulesets \
  --method POST \
  -f name='Main Branch Protection' \
  -f target='branch' \
  -f enforcement='active' \
  -f conditions='{"ref_name":{"include":["refs/heads/main"],"exclude":[]}}' \
  -f rules='[{"type":"pull_request","parameters":{"required_approving_review_count":1,"dismiss_stale_reviews_on_push":true,"require_last_push_approval":false}}]'
```

## Common Rule Types

### Branch Protection Rules

```json
{
  "type": "pull_request",
  "parameters": {
    "required_approving_review_count": 2,
    "dismiss_stale_reviews_on_push": true,
    "require_last_push_approval": false,
    "require_review_thread_resolution": true
  }
}
```

### Required Status Checks

```json
{
  "type": "required_status_checks",
  "parameters": {
    "required_status_checks": [
      {"context": "ci/build"},
      {"context": "ci/test"}
    ],
    "strict_required_status_checks_policy": true
  }
}
```

### Prevent Force Pushes

```json
{
  "type": "non_fast_forward"
}
```

### Require Signed Commits

```json
{
  "type": "required_linear_history"
}
```

### File Size Limits

```json
{
  "type": "file_parameters",
  "parameters": {
    "max_file_size": 10240
  }
}
```

## Organization-Level Rulesets

### Creating Organization Rulesets

1. Go to organization **Settings** → **Repository** → **Rulesets**
2. Click **New ruleset** → **New branch ruleset**
3. Select the scope

### Inheriting Organization Rulesets

Repositories can inherit organization-level Rulesets:

1. Go to repository **Settings** → **Rules** → **Rulesets**
2. Check if organization-level Rulesets are already applied
3. Repository-level Rulesets will override organization-level rules

## Advanced Usage

### Multiple Condition Combinations

```yaml
name: Release Branch
target: branch
enforcement: active
conditions:
  ref_name:
    include:
      - "refs/heads/release/*"
      - "refs/heads/main"
    exclude: []
rules:
  - type: pull_request
    parameters:
      required_approving_review_count: 2
  - type: required_status_checks
    parameters:
      required_status_checks:
        - context: "ci/build"
        - context: "ci/test"
  - type: non_fast_forward
```

### Creating Ruleset Collections

```bash
# Create Ruleset collection
gh api orgs/{org}/rulesets \
  --method POST \
  -f name='Default Branch Rules' \
  -f target='branch' \
  -f enforcement='active' \
  -f conditions='{"ref_name":{"include":["refs/heads/main"]}}' \
  -f rules='[{"type":"pull_request","parameters":{"required_approving_review_count":1}}]'
```

## Managing Rulesets

### Viewing All Rulesets

```bash
# Repository level
gh api repos/{owner}/{repo}/rulesets

# Organization level
gh api orgs/{org}/rulesets
```

### Disabling a Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets/{ruleset_id} \
  --method PATCH \
  -f enforcement='disabled'
```

### Deleting a Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets/{ruleset_id} \
  --method DELETE
```

## Best Practices

1. **Start Simple**: Begin with basic protection rules and gradually add complex ones
2. **Use Organization-Level Rules**: Standardize your team's branch management strategy
3. **Document Rules**: Explain your branch strategy in the README
4. **Review Regularly**: Check if the rules are still applicable
5. **Use Condition Combinations**: Apply different rules to different branches

## Frequently Asked Questions

### Q: What's the difference between a Ruleset and a Ruleset collection?
A: A Ruleset is a single rule set, while a Ruleset collection is a combination of multiple Rulesets that can be applied by priority.

### Q: How to bypass a Ruleset?
A: You need to configure bypass options. Usually only repository administrators or designated users can bypass.

### Q: Will Rulesets affect existing branches?
A: Yes, Rulesets will immediately apply to existing branches that meet the conditions.

## Related Resources

- [GitHub Rulesets Official Documentation](https://docs.github.com/en/repositories/configuring-your-warehouse/managing-rulesets)
- [Branch Protection Rules Migration Guide](https://docs.github.com/en/repositories/configuring-your-repository/managing-rules/migrating-to-rulesets)

---

**Previous: [GitHub Projects Project Management](21-github-projects.md) | Next: [Fork and Open Source Contribution](22-fork-contribute.md)**
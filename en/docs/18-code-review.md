# Code Review

## What is Code Review?

Code Review is an important part of team collaboration development, letting others check your code.

**Benefits:**
- Improve code quality
- Share knowledge
- Discover potential problems
- Unify code style
- Team collaboration

## Review Process

### 1. Pre-review Preparation

1. Read PR description and associated Issue
2. Understand change context
3. Test code locally (optional)

### 2. Review Key Points

| Category | Check Items |
|----------|-------------|
| **Functionality** | Logic correctness, edge cases |
| **Design** | Architecture reasonableness |
| **Readability** | Naming, comments, structure |
| **Performance** | Performance issues |
| **Security** | Security vulnerabilities |
| **Testing** | Test adequacy |
| **Documentation** | Documentation update needed |

## Review Code on GitHub Web (Detailed with Screenshots)

### Request Review

**Step 1: Add Reviewer in PR**

1. Open PR page
2. Find **Reviewers** on right side
3. Click gear icon
4. Select reviewer

```
┌─────────────────────────────────────────────┐
│  Reviewers                                   │
│                                             │
│  👤 @reviewer1  ← Reviewer                   │
│                                             │
│  [Request reviews from...]  ← Click to add  │
└─────────────────────────────────────────────┘
```

### Review Code

**Step 1: View Code Differences**

1. Click **Files changed** tab on PR page
2. View code changes

```
┌─────────────────────────────────────────────┐
│  #1 feat: Add new button                     │
│                                             │
│  [Conversation] [Commits] [Checks] [Files]  │
│                                     ↑       │
│                              Click here to view │
├─────────────────────────────────────────────┤
│                                             │
│  Files changed (3)                           │
│                                             │
│  ─ src/button.ts (+5 -2)                    │
│                                             │
│     1  │ const button = () => {             │
│  -   2  │   return <button>Click</button>;  │
│  +   2  │   return <button className="new"> ││
│  +   3  │     Click                         │
│  +   4  │   </button>;                      │
│     5  │ };                                 │
│                                             │
└─────────────────────────────────────────────┘
```

**Step 2: Add Inline Comment**

1. Hover mouse next to code line number
2. Click **+** button that appears

```
     1  │ const button = () => {        [+]  ← Click this
     2  │   return <button>Click</button>;
     3  │ };
```

3. Enter comment in popup

```
┌─────────────────────────────────────┐
│  💬 Leave a comment                  │
│                                     │
│  Suggest using more specific class name here │
│  instead of simple "new"             │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ 💡 Suggestion  ← Click to add │    │
│  └─────────────────────────────┘    │
│                                     │
│  ☐ Add to review                    │
│                                     │
│     [Start review]                  │
└─────────────────────────────────────┘
```

**Step 3: Use Code Suggestion**

After clicking **Suggestion** button, can provide modification suggestion:

```
┌─────────────────────────────────────┐
│  💬 Leave a comment                  │
│                                     │
│  Suggest modifying class name:       │
│                                     │
│  ```suggestion                      │
│  return <button className="primary">││
│  ```                                │
│                                     │
│  ☑ Add to review                    │
│                                     │
│     [Start review]                  │
└─────────────────────────────────────┘
```

This way the reviewee can directly accept your modification suggestion!

**Step 4: Submit Review**

After review complete, click **Review changes** in top right corner of page:

```
┌─────────────────────────────────────┐
│  Review changes                      │
│                                     │
│  Leave a comment:                   │
│  ┌─────────────────────────────┐    │
│  │ Code looks good, but suggest modifying │    │
│  │ class naming method          │    │
│  └─────────────────────────────┘    │
│                                     │
│  ○ Comment  ← Comment only, doesn't block merge │
│  ○ Approve  ← Approve PR           │
│  ○ Request changes ← Request changes │
│                                     │
│     [Submit review]                 │
└─────────────────────────────────────┘
```

**Three Review Results:**

| Option | Description | When to Use |
|--------|-------------|-------------|
| **Comment** | Comment only | Don't oppose merge, just give suggestions |
| **Approve** | Approve | Code quality good, can merge |
| **Request changes** | Request changes | Problems need fixing |

### View Review Status

On PR page can see review status:

```
┌─────────────────────────────────────────────┐
│  #1 feat: Add new button                     │
│                                             │
│  Reviewers                                   │
│  ✅ @reviewer1 approved  ← Review passed    │
│                                             │
│  Checks                                     │
│  ✅ CI / test  ← Test passed                │
│  ✅ CI / lint  ← Code check passed          │
│                                             │
│  Ready to merge  ← Can merge                │
└─────────────────────────────────────────────┘
```

## Provide Good Feedback

### Good Feedback Examples

```
✅ Specifically point out problem location
✅ Explain why there's a problem
✅ Provide improvement suggestion
✅ Use code suggestion
```

**Example:**
```
The class name "new" here is not descriptive enough, suggest changing to "primary"
to indicate this is a primary button.

```suggestion
className="primary"
```
```

### Bad Feedback Examples

```
❌ "Code is bad"
❌ "This has problems"
❌ Non-constructive criticism
❌ Tone too strong
```

## Automated Review

### Linter Integration

```yaml
# .github/workflows/lint.yml
name: Lint
on: pull_request
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint
```

### Test Check

```yaml
name: Test
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

## Code Review Best Practices

### As Reviewer

1. **Review promptly**: Don't delay
2. **Stay friendly**: Constructive criticism
3. **Distinguish priority**: Must fix vs suggested fix
4. **Point out strengths**: Don't just pick faults

### As Reviewee

1. **Don't personalize**: Review is about code, not about people
2. **Consider seriously**: Every feedback has value
3. **Respond promptly**: Don't let PR sit too long
4. **Can discuss**: Can discuss if you disagree

---

## Practice Exercise

### Exercise: Conduct Code Review

**Task 1: Create Test PR**
1. Create a repository
2. Create feature branch and modify code
3. Push to remote
4. Create PR

**Task 2: Review Code**
1. Open PR's **Files changed** page
2. Find code line to comment on
3. Click **+** button to add comment
4. Use **Suggestion** feature
5. Click **Start review**

**Task 3: Submit Review**
1. Click **Review changes**
2. Select **Approve** or **Comment**
3. Click **Submit review**

**Verification Method:**
- PR page shows your review comment
- Review status shows your decision

## Next Step

[GitHub Actions Automation →](19-github-actions.md)
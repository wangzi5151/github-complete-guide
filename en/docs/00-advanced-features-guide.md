# Chapter 8: GitHub Advanced Features

## 8.1 GitHub Copilot

### What is GitHub Copilot?

GitHub Copilot is an AI programming assistant that can help you write code, generate tests, write documentation, and more.

### Feature Matrix

| Feature | Free | Pro | Business | Enterprise |
|------|------|-----|----------|------------|
| Code Completion | ✅ Limited | ✅ | ✅ | ✅ |
| Copilot Chat | ✅ Limited | ✅ | ✅ | ✅ |
| Agent Mode | ❌ | ✅ | ✅ | ✅ |
| Extensions | ❌ | ✅ | ✅ | ✅ |

### How to Use

**Install the Extension:**

1. Open VS Code
2. Click the Extensions icon
3. Search for "GitHub Copilot"
4. Click **Install**

**Basic Usage:**

1. Write a comment or function signature
2. Copilot automatically suggests code
3. Press `Tab` to accept the suggestion

**Example:**

```javascript
// Write a comment
// Calculate the sum of two numbers

// Copilot will automatically generate the code
function add(a, b) {
  return a + b;
}
```

### Copilot Chat

Press `Ctrl+I` in VS Code to open Copilot Chat:

```
┌─────────────────────────────────────────────┐
│  Copilot Chat                                │
│                                             │
│  [Enter a question or instruction]           │
│                                             │
│  Examples:                                   │
│  - "Explain what this code does"             │
│  - "Help me write a unit test"               │
│  - "How to optimize this code"               │
│  - "Fix this bug"                            │
└─────────────────────────────────────────────┘
```

### Agent Mode

Agent mode can execute multi-step tasks:

```bash
# Let Agent create a complete project structure
"Create an Express API project with user authentication, database connection, and Docker configuration"

# Let Agent fix CI/CD
"Check the GitHub Actions failure logs and fix the workflow"

# Let Agent refactor code
"Refactor this function into a clearer structure, add error handling"
```

### Copilot Extensions

Extensions allow Copilot to call external services:

```
┌─────────────────────────────────────────────┐
│  Copilot Extensions                          │
│                                             │
│  @github     - GitHub platform operations    │
│  @terminal   - Terminal command assistance    │
│  @workspace  - Project workspace search       │
│  @docker     - Docker configuration help      │
│  @kubernetes - K8s YAML generation            │
└─────────────────────────────────────────────┘
```

## 8.2 GitHub Codespaces

### What are Codespaces?

Codespaces is a cloud development environment provided by GitHub that lets you write code directly in your browser.

### Enabling Codespaces

**Step 1:** Open the repository page

**Step 2:** Click the **Code** button

**Step 3:** Select the **Codespaces** tab

**Step 4:** Click **Create codespace on main**

```
┌─────────────────────────────────────────────┐
│  Code                                        │
│                                             │
│  Local    Codespaces                         │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Create codespace on main            │    │
│  │                                     │    │
│  │ 2-core • 8 GB RAM • 15 GB          │    │
│  │ Free for 120 hours/month            │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Configuring Codespaces

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "forwardPorts": [3000],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode"
      ]
    }
  }
}
```

### Using Codespaces

1. Open Codespace in the browser
2. Use it like local VS Code
3. Code syncs automatically
4. Supports terminal, debugging, and extensions

## 8.3 GitHub Models

### What are GitHub Models?

GitHub Models is an AI model platform provided by GitHub that allows you to use various AI models directly on GitHub.

### Supported Models

| Model | Provider | Use Case |
|------|--------|------|
| GPT-4o | OpenAI | General conversation, code generation |
| GPT-4o-mini | OpenAI | Lightweight tasks |
| Claude 3.5 Sonnet | Anthropic | Code analysis, conversation |
| Llama 3.1 | Meta | Open-source general-purpose model |
| Mistral | Mistral AI | European open-source model |

### How to Use

**Using via API:**

```bash
# Set API Key
export GITHUB_TOKEN="your-github-token"

# Call GPT-4o
curl -X POST "https://models.inference.ai.azure.com/chat/completions" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello, who are you?"}
    ]
  }'
```

**Using the Python SDK:**

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a Python function to sort a list"}
    ]
)

print(response.choices[0].message.content)
```

### Using in GitHub Actions

```yaml
name: AI Code Review

on:
  pull_request:

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Get PR diff
      id: diff
      run: |
        DIFF=$(gh pr diff ${{ github.event.pull_request.number }})
        echo "diff<<EOF" >> $GITHUB_OUTPUT
        echo "$DIFF" >> $GITHUB_OUTPUT
        echo "EOF" >> $GITHUB_OUTPUT
    
    - name: AI Review
      run: |
        curl -X POST "https://models.inference.ai.azure.com/chat/completions" \
          -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{
            "model": "gpt-4o",
            "messages": [
              {"role": "system", "content": "Review this code change and provide feedback."},
              {"role": "user", "content": "${{ steps.diff.outputs.diff }}"}
            ]
          }'
```

## 8.4 GitHub Advanced Security

### Secret Scanning Push Protection

Block commits containing sensitive information during push:

1. Go to **Settings** → **Code security and analysis**
2. Enable **Push protection**

### Code Scanning

Use CodeQL to analyze code for security vulnerabilities:

1. Go to **Security** → **Code scanning**
2. Click **Set up**
3. Select CodeQL
4. Configure scanning options

### Dependency Review

Review dependencies for security vulnerabilities in PRs:

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review

on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Dependency Review
      uses: actions/dependency-review-action@v4
      with:
        fail-on-severity: high
```

## 8.5 GitHub API

### REST API

```bash
# Get repository information
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/owner/repo"

# Create an Issue
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Bug report", "body": "Description"}' \
  "https://api.github.com/repos/owner/repo/issues"
```

### GraphQL API

```graphql
query {
  repository(owner: "your-org", name: "your-repo") {
    issues(first: 10) {
      edges {
        node {
          title
          state
          author {
            login
          }
        }
      }
    }
  }
}
```

### Using GitHub CLI

```bash
# List repositories
gh repo list

# Create an Issue
gh issue create --title "Bug" --body "Description"

# Create a PR
gh pr create --title "Feature" --body "Description"

# View a PR
gh pr view 123
```

## 8.6 GitHub Webhooks

### What are Webhooks?

Webhooks allow you to automatically send notifications to external services when events occur on GitHub.

### Creating a Webhook

1. Go to repository **Settings** → **Webhooks**
2. Click **Add webhook**
3. Configure:

```
┌─────────────────────────────────────────────┐
│  Add webhook                                 │
│                                             │
│  Payload URL: [https://your-server.com/webhook]│
│  Content type: [application/json ▼]          │
│  Secret: [your-secret-token     ]            │
│                                             │
│  Events:                                     │
│  ● Just the push event                      │
│  ○ Send me everything                       │
│  ○ Let me select individual events          │
│                                             │
│       [Add webhook]                          │
└─────────────────────────────────────────────┘
```

### Processing a Webhook

```javascript
const crypto = require('crypto');

// Verify Webhook signature
function verifyWebhook(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${digest}`)
  );
}

// Process Webhook
app.post('/webhook', (req, res) => {
  const signature = req.headers['x-hub-signature-256'];
  
  if (!verifyWebhook(JSON.stringify(req.body), signature, process.env.WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }
  
  const event = req.headers['x-github-event'];
  const payload = req.body;
  
  switch (event) {
    case 'push':
      handlePush(payload);
      break;
    case 'pull_request':
      handlePullRequest(payload);
      break;
  }
  
  res.status(200).send('OK');
});
```

## 8.7 GitHub Projects

### What are Projects?

GitHub Projects is a project management tool that provides Kanban boards, tables, roadmaps, and other views.

### Creating a Project

```bash
# Create a project using CLI
gh project create --title "My Project" --owner your-org
```

### Project Views

| View | Description |
|------|------|
| **Board** | Kanban view, similar to Trello |
| **Table** | Table view, similar to Excel |
| **Roadmap** | Roadmap view, timeline |
| **Calendar** | Calendar view |

### Automation

```yaml
# .github/workflows/project-automation.yml
name: Project Automation

on:
  issues:
    types: [opened, closed]
  pull_request:
    types: [opened, closed, ready_for_review]

jobs:
  auto-add:
    runs-on: ubuntu-latest
    steps:
    - name: Add to project
      uses: actions/add-to-project@v0.5.0
      with:
        project-url: https://github.com/orgs/your-org/projects/1
        github-token: ${{ secrets.GITHUB_TOKEN }}
```

## 8.8 GitHub Packages

### What are Packages?

GitHub Packages is a package management service for publishing and managing packages.

### Supported Package Managers

| Package Manager | Language |
|----------|------|
| npm | JavaScript |
| NuGet | .NET |
| RubyGems | Ruby |
| Maven | Java |
| Docker | Containers |

### Publishing npm Packages

**Step 1:** Configure `.npmrc`

```
registry=https://npm.pkg.github.com
```

**Step 2:** Publish

```bash
npm publish
```

### Publishing with GitHub Actions

```yaml
name: Publish Package

on:
  push:
    tags: ['v*']

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
    - uses: actions/checkout@v4
    
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        registry-url: 'https://npm.pkg.github.com'
    
    - run: npm ci
    - run: npm publish
      env:
        NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 8.9 Chapter Summary

This chapter covered GitHub's advanced features in detail, including:

- GitHub Copilot: AI programming assistant
- GitHub Codespaces: Cloud development environment
- GitHub Models: AI model platform
- GitHub Advanced Security: Security features
- GitHub API: Automation interface
- GitHub Webhooks: Event notifications
- GitHub Projects: Project management
- GitHub Packages: Package management

**Key Takeaways:**
- These advanced features can significantly improve development efficiency
- Choose the right features based on project needs
- Continue learning new features

**Next:**
[China Developer Zone →](Q-china-acceleration.md)

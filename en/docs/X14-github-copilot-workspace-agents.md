# GitHub Copilot Workspace and AI Agent Development

> **Target Audience**: Developers who want to gain in-depth knowledge of GitHub Copilot advanced features, AI Agent development, and automated workflows  
> **Estimated Learning Time**: 4-5 hours  
> **Prerequisites**: Git/GitHub basics, at least one programming language, basic AI concepts

---

## Table of Contents

1. [Copilot Workspace Overview and Architecture](#1-copilot-workspace-overview-and-architecture)
2. [Copilot Workspace Workflow](#2-copilot-workspace-workflow)
3. [Deep Dive into Copilot Agent Mode](#3-deep-dive-into-copilot-agent-mode)
4. [Copilot Extensions Development Guide](#4-copilot-extensions-development-guide)
5. [GitHub AI Platform and GitHub Models API](#5-github-ai-platform-and-github-models-api)
6. [Building a Custom GitHub Copilot Extension](#6-building-a-custom-github-copilot-extension)
7. [GitHub Actions + AI Agent Automation](#7-github-actions--ai-agent-automation)
8. [AI-Assisted Code Review](#8-ai-assisted-code-review)
9. [AI-Assisted Issue Triage and Management](#9-ai-assisted-issue-triage-and-management)
10. [AI-Assisted Documentation Generation](#10-ai-assisted-documentation-generation)
11. [AI-Assisted Test Generation](#11-ai-assisted-test-generation)
12. [GitHub Next Experimental Features](#12-github-next-experimental-features)
13. [Impact of AI on Open Source Communities](#13-impact-of-ai-on-open-source-communities)
14. [AI Toolchain for Chinese Developers](#14-ai-toolchain-for-chinese-developers)

---

## 1. Copilot Workspace Overview and Architecture

### 1.1 What is Copilot Workspace

GitHub Copilot Workspace is GitHub's **AI-native development environment** that deeply integrates AI capabilities into the entire development workflow. Unlike traditional Copilot code completion, Copilot Workspace can understand the context of an entire project and assist developers in completing the full process from issue analysis to code implementation.

**Core Concept**:

```
Traditional Development Workflow:
Issue → Manual Analysis → Manual Design → Manual Coding → Manual Testing → PR

Copilot Workspace Workflow:
Issue → AI Analysis → AI Design → Human + AI Coding → AI-Assisted Testing → PR
```

### 1.2 Architecture Design

Copilot Workspace architecture is divided into multiple layers:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Web IDE    │  │  CLI Tool   │  │  VS Code    │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
├─────────┼────────────────┼────────────────┼─────────────┤
│         └────────────────┼────────────────┘             │
│                    API Gateway Layer                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │         GitHub REST / GraphQL API               │    │
│  └─────────────────────┬───────────────────────────┘    │
├─────────────────────────┼───────────────────────────────┤
│                    AI Service Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Copilot     │  │ Code        │  │ Issue        │     │
│  │ Models      │  │ Analysis    │  │ Understanding│     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         └────────────────┼────────────────┘             │
│                    Model Inference Layer                   │
│  ┌─────────────────────────────────────────────────┐    │
│  │    GPT-4o / Claude / Gemini / Custom Models     │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                    Data Storage Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Code Index  │  │ Context     │  │ User         │     │
│  │             │  │ Cache       │  │ Preferences  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Core Components

**1. Code Indexing Engine**

Copilot Workspace builds a **semantic index** for repositories, supporting:
- Code structure analysis (AST parsing)
- Dependency graph construction
- Symbol reference tracking
- Cross-file context understanding

**2. Context Manager**

```python
# Simplified model of the context manager
class ContextManager:
    def __init__(self, repo):
        self.repo = repo
        self.code_index = CodeIndex(repo)
        self.conversation_history = []
    
    def build_context(self, issue_number):
        issue = self.repo.get_issue(issue_number)
        relevant_files = self.code_index.find_relevant_files(issue.body)
        related_code = self.code_index.get_related_code(relevant_files)
        
        return {
            'issue': issue,
            'relevant_files': relevant_files,
            'related_code': related_code,
            'recent_changes': self.repo.get_recent_changes(),
            'conversation': self.conversation_history
        }
```

**3. Task Planner**

Copilot Workspace breaks down complex tasks into executable subtasks:

```
Issue: "Add user authentication feature"
    ├── Analyze requirements
    │   ├── Understand existing authentication mechanisms
    │   ├── Identify files that need to be modified
    │   └── Determine technical solution
    ├── Design solution
    │   ├── Data model design
    │   ├── API endpoint design
    │   └── Middleware design
    ├── Implement code
    │   ├── Create user model
    │   ├── Implement authentication service
    │   ├── Add routes
    │   └── Write tests
    └── Verify results
        ├── Run tests
        ├── Code review
        └── Update documentation
```

### 1.4 Copilot Workspace vs Traditional IDE

| Feature | Traditional IDE | Copilot Workspace |
|---------|----------------|-------------------|
| Code Completion | Syntax-based | Semantic and context-based |
| Refactoring | Manual operations | AI-assisted automatic refactoring |
| Debugging | Breakpoint debugging | AI analyzes root causes |
| Testing | Manual test writing | AI generates test cases |
| Documentation | Manual writing | AI auto-generation |
| Issue Understanding | Manual reading | AI automatic analysis |
| Code Review | Purely manual | AI + human collaboration |

---

## 2. Copilot Workspace Workflow

### 2.1 Issue → Plan → Code → PR Complete Flow

Copilot Workspace's core workflow consists of four phases:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Issue   │───▶│   Plan   │───▶│   Code   │───▶│    PR    │
│ Analysis │    │ Planning │    │Implementation│   │Submit   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
 Understand       Design         Write Code     Create PR
 Requirements     Solution                      Request Review
 Identify Code    Define Scope   Generate Tests Merge Code
 Context          Task Breakdown Run Validation
```

### 2.2 Phase 1: Issue Analysis

When you launch Copilot Workspace on a GitHub Issue, the AI will:

1. **Parse Issue Content**: Understand the problem description, reproduction steps, and expected behavior
2. **Search Related Code**: Find files and functions related to the Issue in the repository
3. **Analyze Code Context**: Understand the structure, dependencies, and design patterns of existing code
4. **Generate Analysis Report**: Summarize the root cause and potential solutions

**Example**:

```markdown
## Issue #123: Session expiration time is incorrect after user login

### Description
After user login, the session expires after 30 minutes, but the configuration file is set to 24 hours.

### Steps to Reproduce
1. User logs in
2. Wait 30 minutes
3. Access a page that requires authentication
4. Being redirected to the login page

### Expected Behavior
The session should expire after 24 hours.
```

**Copilot Workspace Analysis Result**:

```markdown
## AI Analysis

### Problem Location
- File: `src/middleware/session.js:45`
- Issue: `maxAge` configuration uses a hardcoded value of `30 * 60 * 1000` (30 minutes)
- Instead of reading `config.session.maxAge` from the configuration file

### Related Files
1. `src/middleware/session.js` - Session middleware
2. `config/default.json` - Configuration file
3. `src/routes/auth.js` - Authentication routes

### Suggested Solution
Modify line 45 of `session.js` to read session expiration time from the configuration file.
```

### 2.3 Phase 2: Solution Planning

After understanding the problem, Copilot Workspace generates a detailed implementation plan:

```markdown
## Implementation Plan

### Files to Modify
1. `src/middleware/session.js`
   - Modify line 45: Use `config.session.maxAge` instead of hardcoded value
   - Add configuration validation: Ensure maxAge is a valid number

2. `config/default.json`
   - Confirm `session.maxAge` configuration exists with value `86400000` (24 hours)

3. `tests/session.test.js`
   - Add test case: Verify session uses configured expiration time

### Task Breakdown
- [ ] 1. Fix hardcoded value in session.js
- [ ] 2. Add configuration validation logic
- [ ] 3. Write unit tests
- [ ] 4. Run existing tests to ensure no regression

### Expected Impact
- Fix incorrect session expiration time issue
- No impact on other features
- Increased test coverage
```

### 2.4 Phase 3: Code Implementation

Based on the plan, Copilot Workspace generates code modifications:

```javascript
// src/middleware/session.js - Before modification
const sessionMiddleware = session({
  secret: config.session.secret,
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 30 * 60 * 1000  // Hardcoded 30 minutes
  }
});

// src/middleware/session.js - After modification
const sessionMiddleware = session({
  secret: config.session.secret,
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: config.session.maxAge || 24 * 60 * 60 * 1000  // Read from config, default 24 hours
  }
});
```

```javascript
// tests/session.test.js - New tests
describe('Session Configuration', () => {
  it('should use configured maxAge for session cookie', () => {
    const config = {
      session: {
        secret: 'test-secret',
        maxAge: 24 * 60 * 60 * 1000  // 24 hours
      }
    };
    
    const middleware = createSessionMiddleware(config);
    expect(middleware.cookie.maxAge).toBe(24 * 60 * 60 * 1000);
  });

  it('should use default maxAge when not configured', () => {
    const config = {
      session: {
        secret: 'test-secret'
      }
    };
    
    const middleware = createSessionMiddleware(config);
    expect(middleware.cookie.maxAge).toBe(24 * 60 * 60 * 1000);
  });
});
```

### 2.5 Phase 4: PR Creation

After code implementation is complete, Copilot Workspace automatically creates a Pull Request:

```markdown
## PR #456: Fix session expiration time configuration issue

### Issue
Closes #123

Session expiration time was using a hardcoded 30-minute value instead of reading from the configuration file.

### Solution
- Modify `session.js` to read expiration time from `config.session.maxAge`
- Add configuration validation and default value handling
- Add unit tests to cover configuration scenarios

### Tests
- [x] New unit tests pass
- [x] No regression in existing tests
- [x] Manual testing verifies session expiration time is 24 hours

### Changed Files
- `src/middleware/session.js` - Fix configuration reading
- `tests/session.test.js` - Add new test cases
```

### 2.6 Workflow Best Practices

```markdown
## Best Practices for Using Copilot Workspace

### Issue Writing
1. Provide clear problem description
2. Include reproduction steps
3. Specify expected behavior
4. Attach error logs or screenshots

### Solution Review
1. Carefully review AI-generated solutions
2. Confirm modification scope is reasonable
3. Check if edge cases are missed
4. Verify correctness of technical solution

### Code Review
1. Do not blindly accept AI-generated code
2. Check if code style conforms to project standards
3. Verify logic correctness
4. Ensure sufficient test coverage

### PR Management
1. Supplement AI-generated PR descriptions
2. Add necessary context information
3. Tag relevant reviewers
4. Link related Issues
```

---

## 3. Deep Dive into Copilot Agent Mode

### 3.1 What is Copilot Agent Mode

Copilot Agent Mode is Copilot's **autonomous agent mode** that can independently execute complex development tasks, not just provide suggestions.

**Agent Mode vs Traditional Mode**:

```
Traditional Copilot:
Developer Input → Copilot Suggestion → Developer Selection → Developer Execution

Agent Mode:
Developer Describes Task → Agent Analysis → Agent Planning → Agent Execution → Developer Review
```

### 3.2 Agent Mode Core Capabilities

**1. Multi-file Editing**

Agent Mode can modify multiple files simultaneously while maintaining code consistency:

```python
# Agent can understand cross-file dependencies
# For example: When modifying a database model, simultaneously update:
# - Data model definition
# - Database migration files
# - API endpoints
# - Serializers
# - Test files
```

**2. Terminal Command Execution**

Agent can execute terminal commands to complete tasks:

```bash
# Operations Agent can perform
npm install <package>      # Install dependencies
npm run test               # Run tests
git add . && git commit    # Commit code
docker build .             # Build image
```

**3. Error Fix Loop**

Agent has **self-healing** capabilities:

```
Execute Code → Detect Error → Analyze Cause → Fix Code → Re-execute
    │                                          │
    └──────────────── Loop Until Success ──────┘
```

### 3.3 Agent Mode Use Cases

**Scenario 1: Rapid Prototyping**

```markdown
## User Prompt
"Create a simple TODO application using React + TypeScript + Tailwind CSS,
with CRUD functionality, storing data in localStorage."

## Agent Execution Process
1. Create React project: `npx create-react-app todo-app --template typescript`
2. Install Tailwind CSS: `npm install -D tailwindcss postcss autoprefixer`
3. Create component structure:
   - `src/components/TodoApp.tsx`
   - `src/components/TodoItem.tsx`
   - `src/components/TodoInput.tsx`
4. Implement core functionality
5. Run tests to verify
```

**Scenario 2: Code Refactoring**

```markdown
## User Prompt
"Refactor class components in the project to function components using React Hooks."

## Agent Execution Process
1. Scan all class components in the project
2. Analyze state and lifecycle methods of each component
3. Refactor to function components one by one
4. Replace state and lifecycle with useState and useEffect
5. Run tests to ensure functionality is unchanged
```

**Scenario 3: Bug Fix**

```markdown
## User Prompt
"Fix the memory leak issue described in Issue #789."

## Agent Execution Process
1. Read Issue #789 description
2. Analyze related code
3. Identify root cause of memory leak
4. Implement fix
5. Add test cases
6. Run tests to verify
```

### 3.4 Agent Mode Configuration

```json
// .github/copilot-agent-config.json
{
  "agent": {
    "model": "gpt-4o",
    "maxIterations": 10,
    "autoApprove": {
      "fileReads": true,
      "fileWrites": false,
      "terminalCommands": false
    },
    "constraints": {
      "maxFilesPerTask": 20,
      "maxLinesPerFile": 500,
      "allowedCommands": [
        "npm test",
        "npm run lint",
        "git status"
      ],
      "blockedCommands": [
        "rm -rf",
        "sudo",
        "chmod 777"
      ]
    },
    "context": {
      "includeTestFiles": true,
      "includeDocumentation": true,
      "maxContextTokens": 8000
    }
  }
}
```

### 3.5 Agent Mode Security Considerations

```markdown
## Agent Mode Security Best Practices

### Permission Control
1. Default to not auto-approving file writes
2. Limit executable terminal commands
3. Set maximum iteration count to prevent infinite loops
4. Monitor Agent resource usage

### Code Review
1. All Agent-generated code requires human review
2. Check for security vulnerabilities introduced
3. Verify compliance with project standards
4. Ensure no sensitive information is leaked

### Audit Logging
1. Record all Agent operations
2. Save Agent decision-making process
3. Support rollback to previous state
4. Regularly review Agent behavior patterns
```

---

## 4. Copilot Extensions Development Guide

### 4.1 What are Copilot Extensions

Copilot Extensions are a mechanism to **extend Copilot's capabilities**, allowing third-party developers to add new features and data sources to Copilot.

**Types of Copilot Extensions**:

```
Copilot Extensions Categories:
├── Chat Extensions
│   └── Add new commands and skills in Copilot Chat
├── Coding Agent Extensions
│   └── Extend Agent Mode capabilities
└── Content Exclusions
    └── Control what content Copilot can access
```

### 4.2 Copilot Extension Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Copilot                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Extension Runtime                   │    │
│  └─────────────────────┬───────────────────────────┘    │
├─────────────────────────┼───────────────────────────────┤
│                    Extension API                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │         Copilot Extension Protocol              │    │
│  └─────────────────────┬───────────────────────────┘    │
├─────────────────────────┼───────────────────────────────┤
│                    Your Extension                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ HTTP Server │  │ Auth Module │  │ Business     │     │
│  │             │  │             │  │ Logic        │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

### 4.3 Chat Extension Development

**Basic Structure**:

```typescript
// src/extension.ts
import { createApp } from '@copilot-extensions/extension-sdk';

const app = createApp({
  name: 'my-extension',
  version: '1.0.0',
});

// Handle Copilot Chat messages
app.onMessage(async (message, context) => {
  const userMessage = message.body;
  
  // Call external API
  const response = await fetch('https://api.example.com/data', {
    method: 'POST',
    body: JSON.stringify({ query: userMessage }),
  });
  
  const data = await response.json();
  
  // Return formatted response
  return {
    type: 'markdown',
    content: `## Query Results\n\n${formatData(data)}`,
  };
});

// Register slash commands
app.command('/search', async (args, context) => {
  const results = await searchDatabase(args);
  return {
    type: 'markdown',
    content: formatSearchResults(results),
  };
});

app.command('/deploy', async (args, context) => {
  // Verify user permissions
  if (!context.user.hasPermission('deploy')) {
    return {
      type: 'error',
      content: 'You do not have deployment permissions',
    };
  }
  
  // Execute deployment
  const result = await deployApplication(args);
  return {
    type: 'markdown',
    content: `Deployment successful!\n\n${result.summary}`,
  };
});

export default app;
```

### 4.4 manifest.yml Configuration

```yaml
# manifest.yml
name: my-extension
description: A sample Copilot Extension
version: 1.0.0

# Entrypoint
entrypoint:
  type: http
  url: https://your-server.com/copilot

# Permission declarations
permissions:
  - name: repository_read
    description: Read repository content
  - name: issues_read
    description: Read Issue information

# Command registration
commands:
  - name: /search
    description: Search database
    usage: "/search <query>"
  - name: /deploy
    description: Deploy application
    usage: "/deploy <environment>"

# Context configuration
context:
  include_repository: true
  include_issues: true
  include_pull_requests: true
```

### 4.5 Extension Authentication and Security

```typescript
// src/auth.ts
import { verifyCopilotToken } from '@copilot-extensions/extension-sdk';

export async function authenticateRequest(req: Request): Promise<UserContext> {
  // 1. Verify Copilot Token
  const token = req.headers.get('x-copilot-token');
  if (!token) {
    throw new Error('Missing authentication token');
  }

  // 2. Verify Token validity
  const payload = await verifyCopilotToken(token);
  
  // 3. Verify user permissions
  const user = await getUserFromPayload(payload);
  if (!user.hasAccess) {
    throw new Error('User does not have access');
  }

  // 4. Verify request origin
  const origin = req.headers.get('origin');
  if (!isValidOrigin(origin)) {
    throw new Error('Invalid request origin');
  }

  return {
    userId: user.id,
    permissions: user.permissions,
    repository: payload.repository,
  };
}
```

### 4.6 Extension Testing

```typescript
// tests/extension.test.ts
import { createTestClient } from '@copilot-extensions/extension-sdk/testing';
import app from '../src/extension';

describe('My Extension', () => {
  const client = createTestClient(app);

  test('should handle /search command', async () => {
    const response = await client.sendCommand('/search test query');
    
    expect(response.type).toBe('markdown');
    expect(response.content).toContain('Query Results');
  });

  test('should reject unauthorized deploy', async () => {
    const response = await client.sendCommand('/deploy production', {
      user: { hasPermission: () => false },
    });
    
    expect(response.type).toBe('error');
    expect(response.content).toContain('do not have deployment permissions');
  });

  test('should handle message with context', async () => {
    const response = await client.sendMessage('How many Issues does this repository have?', {
      repository: { owner: 'test', name: 'repo' },
    });
    
    expect(response.type).toBe('markdown');
  });
});
```

---

## 5. GitHub AI Platform and GitHub Models API

### 5.1 GitHub Models Overview

GitHub Models is GitHub's **AI Model-as-a-Service platform** that allows developers to directly access and use various AI models on GitHub.

**Supported Models**:

```
GitHub Models Supported Models:
├── Language Models
│   ├── GPT-4o
│   ├── GPT-4o-mini
│   ├── Claude 3.5 Sonnet
│   ├── Llama 3.1
│   └── Mistral Large
├── Code Models
│   ├── CodeLlama
│   ├── StarCoder2
│   └── Mixtral Code
├── Image Models
│   ├── DALL-E 3
│   └── Stable Diffusion
└── Embedding Models
    ├── text-embedding-3-small
    └── text-embedding-3-large
```

### 5.2 GitHub Models API Usage

**Basic Usage**:

```python
# Using GitHub Models API
import requests

GITHUB_TOKEN = "ghp_your_token_here"
ENDPOINT = "https://models.inference.ai.azure.com"

def chat_with_model(messages, model="gpt-4o"):
    response = requests.post(
        f"{ENDPOINT}/chat/completions",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )
    return response.json()

# Usage example
messages = [
    {"role": "system", "content": "You are a helpful programming assistant."},
    {"role": "user", "content": "Explain what Docker is?"}
]

result = chat_with_model(messages)
print(result["choices"][0]["message"]["content"])
```

**Python SDK Usage**:

```python
# Using OpenAI SDK to access GitHub Models
from openai import OpenAI

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="ghp_your_token_here"
)

# Text generation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a Python expert."},
        {"role": "user", "content": "Write a quicksort algorithm."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)

# Code generation
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a code generation assistant."},
        {"role": "user", "content": "Generate a React component that implements a counter."}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)
```

### 5.3 GitHub Models Pricing

```markdown
## GitHub Models Pricing (2024)

### Free Tier
- 1,000 requests per month
- Supports all base models
- Limited concurrent requests

### Pro Tier ($4/month)
- 10,000 requests per month
- Supports advanced models
- Higher concurrency limits
- Priority support

### Enterprise Tier
- Custom quotas
- Private model deployment
- Enterprise-grade support
- SLA guarantees
```

### 5.4 Model Selection Guide

```markdown
## Model Selection Guide

### Code Generation
- **GPT-4o**: Most powerful general-purpose code generation
- **CodeLlama**: Focused on code understanding, cost-effective
- **StarCoder2**: Open-source code model, suitable for local deployment

### Text Processing
- **GPT-4o**: Most powerful text understanding and generation
- **Claude 3.5 Sonnet**: Excels at long text processing
- **Mistral Large**: Excellent multilingual support

### Image Generation
- **DALL-E 3**: High-quality image generation
- **Stable Diffusion**: Open-source, deployable locally

### Embeddings
- **text-embedding-3-small**: Cost-effective
- **text-embedding-3-large**: Higher accuracy
```

---

## 6. Building a Custom GitHub Copilot Extension

### 6.1 Extension Development Environment Setup

```bash
# 1. Create project directory
mkdir my-copilot-extension
cd my-copilot-extension

# 2. Initialize Node.js project
npm init -y

# 3. Install dependencies
npm install @copilot-extensions/extension-sdk
npm install -D typescript @types/node

# 4. Configure TypeScript
npx tsc --init

# 5. Create project structure
mkdir -p src tests

# 6. Create entry files
touch src/index.ts
touch manifest.yml
```

### 6.2 Complete Extension Example: Code Search

```typescript
// src/index.ts
import { createApp, CopilotContext } from '@copilot-extensions/extension-sdk';
import { Octokit } from '@octokit/rest';

const app = createApp({
  name: 'code-search',
  version: '1.0.0',
});

// Initialize GitHub client
const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
});

// Code search command
app.command('/search-code', async (args: string, context: CopilotContext) => {
  const { repository } = context;
  
  if (!repository) {
    return {
      type: 'error',
      content: 'Unable to retrieve repository information',
    };
  }

  try {
    // Use GitHub API to search code
    const { data } = await octokit.search.code({
      q: `${args} repo:${repository.owner}/${repository.name}`,
      per_page: 5,
    });

    if (data.total_count === 0) {
      return {
        type: 'markdown',
        content: `No code found related to "${args}".`,
      };
    }

    // Format search results
    const results = data.items.map((item, index) => {
      return `### ${index + 1}. ${item.name}
- **Path**: \`${item.path}\`
- **Repository**: ${item.repository.full_name}
- **Score**: ${item.score}
`;
    }).join('\n');

    return {
      type: 'markdown',
      content: `## Code Search Results: "${args}"\n\nFound ${data.total_count} results, showing top 5:\n\n${results}`,
    };
  } catch (error) {
    return {
      type: 'error',
      content: `Search failed: ${error.message}`,
    };
  }
});

// File content viewer command
app.command('/view-file', async (args: string, context: CopilotContext) => {
  const { repository } = context;
  const [filePath, branch] = args.split(' ');

  if (!filePath) {
    return {
      type: 'error',
      content: 'Please specify a file path, e.g.: /view-file src/index.ts',
    };
  }

  try {
    const { data } = await octokit.repos.getContent({
      owner: repository.owner,
      repo: repository.name,
      path: filePath,
      ref: branch || 'main',
    });

    if ('content' in data) {
      const content = Buffer.from(data.content, 'base64').toString('utf-8');
      const ext = filePath.split('.').pop() || '';
      
      return {
        type: 'markdown',
        content: `## ${filePath}\n\n\`\`\`${ext}\n${content}\n\`\`\``,
      };
    }

    return {
      type: 'error',
      content: 'Unable to read file content',
    };
  } catch (error) {
    return {
      type: 'error',
      content: `Failed to read file: ${error.message}`,
    };
  }
});

// Code analysis command
app.command('/analyze', async (args: string, context: CopilotContext) => {
  const { repository } = context;

  try {
    // Get repository statistics
    const [repoData, languages, contributors] = await Promise.all([
      octokit.repos.get({
        owner: repository.owner,
        repo: repository.name,
      }),
      octokit.repos.listLanguages({
        owner: repository.owner,
        repo: repository.name,
      }),
      octokit.repos.listContributors({
        owner: repository.owner,
        repo: repository.name,
        per_page: 10,
      }),
    ]);

    const languageStats = Object.entries(languages.data)
      .map(([lang, bytes]) => `- ${lang}: ${formatBytes(bytes)}`)
      .join('\n');

    const topContributors = contributors.data
      .slice(0, 5)
      .map((c, i) => `${i + 1}. ${c.login} (${c.contributions} commits)`)
      .join('\n');

    return {
      type: 'markdown',
      content: `## Repository Analysis: ${repository.owner}/${repository.name}

### Basic Information
- **Description**: ${repoData.data.description || 'None'}
- **Stars**: ${repoData.data.stargazers_count}
- **Forks**: ${repoData.data.forks_count}
- **Open Issues**: ${repoData.data.open_issues_count}
- **Created**: ${new Date(repoData.data.created_at).toLocaleDateString()}

### Language Statistics
${languageStats}

### Top Contributors
${topContributors}
`,
    };
  } catch (error) {
    return {
      type: 'error',
      content: `Analysis failed: ${error.message}`,
    };
  }
});

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default app;
```

### 6.3 Extension Deployment

```yaml
# GitHub Actions Deployment Workflow
# .github/workflows/deploy-extension.yml
name: Deploy Copilot Extension

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build
        run: npm run build
        
      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: 'my-copilot-extension'
          package: './dist'
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
          
      - name: Update Extension Registration
        run: |
          gh api \
            --method PATCH \
            /repos/${{ github.repository }}/copilot/extensions/my-extension \
            --field url="https://my-copilot-extension.azurewebsites.net"
```

---

## 7. GitHub Actions + AI Agent Automation

### 7.1 AI-Assisted CI/CD Workflow

```yaml
# .github/workflows/ai-powered-ci.yml
name: AI-Powered CI/CD

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: AI Code Review
        uses: github/copilot-code-review-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
  ai-test-generation:
    runs-on: ubuntu-latest
    if: github.event.action == 'opened'
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Tests with AI
        uses: your-org/ai-test-generator@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          model: gpt-4o
          
  ai-documentation:
    runs-on: ubuntu-latest
    if: github.event.action == 'opened'
    steps:
      - uses: actions/checkout@v4
      
      - name: Update Documentation
        uses: your-org/ai-doc-updater@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 7.2 Custom AI Agent Action

```typescript
// src/ai-agent-action.ts
import * as core from '@actions/core';
import * as github from '@actions/github';
import OpenAI from 'openai';

async function run() {
  try {
    // Get input parameters
    const githubToken = core.getInput('github-token');
    const openaiKey = core.getInput('openai-api-key');
    const task = core.getInput('task');

    // Initialize clients
    const octokit = github.getOctokit(githubToken);
    const openai = new OpenAI({ apiKey: openaiKey });
    
    const context = github.context;
    const pr = context.payload.pull_request;

    if (!pr) {
      core.setFailed('This action only works on pull requests');
      return;
    }

    // Get PR changed files
    const { data: files } = await octokit.rest.pulls.listFiles({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: pr.number,
    });

    // Build context
    const fileChanges = files.map(f => ({
      filename: f.filename,
      patch: f.patch,
      status: f.status,
    }));

    // Use AI to analyze code changes
    const analysis = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a code review expert. Analyze the code changes in this Pull Request,
providing detailed review comments including:
1. Code quality
2. Potential issues
3. Improvement suggestions
4. Security considerations`
        },
        {
          role: 'user',
          content: `PR Title: ${pr.title}
PR Description: ${pr.body}

Changed Files:
${JSON.stringify(fileChanges, null, 2)}`
        }
      ],
      temperature: 0.3,
      max_tokens: 2000,
    });

    const review = analysis.choices[0].message.content;

    // Post review comment
    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      body: `## 🤖 AI Code Review\n\n${review}`,
    });

    // Set output
    core.setOutput('review', review);

  } catch (error) {
    core.setFailed(`Action failed: ${error.message}`);
  }
}

run();
```

### 7.3 Automated Issue Processing Agent

```yaml
# .github/workflows/issue-agent.yml
name: AI Issue Agent

on:
  issues:
    types: [opened]

jobs:
  process-issue:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Analyze Issue
        id: analyze
        uses: your-org/issue-analyzer@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-key: ${{ secrets.OPENAI_API_KEY }}
          
      - name: Auto-label
        if: steps.analyze.outputs.labels != ''
        uses: actions/github-script@v7
        with:
          script: |
            const labels = '${{ steps.analyze.outputs.labels }}'.split(',');
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: labels
            });
            
      - name: Add Comment
        if: steps.analyze.outputs.comment != ''
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '${{ steps.analyze.outputs.comment }}'
            });
```

### 7.4 AI-Assisted Release Management

```yaml
# .github/workflows/ai-release.yml
name: AI Release Manager

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Generate Release Notes
        id: release-notes
        uses: openai/release-notes-generator@v1
        with:
          openai-key: ${{ secrets.OPENAI_API_KEY }}
          from-tag: ${{ github.event.before }}
          to-tag: ${{ github.ref }}
          
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.release-notes.outputs.notes }}
          draft: false
          prerelease: ${{ contains(github.ref, 'beta') || contains(github.ref, 'alpha') }}
```

---

## 8. AI-Assisted Code Review

### 8.1 Custom AI Review Bot

```typescript
// src/ai-reviewer.ts
import { Probot } from 'probot';
import OpenAI from 'openai';

export default function aiReviewer(app: Probot) {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  app.on(['pull_request.opened', 'pull_request.synchronize'], async (context) => {
    const pr = context.payload.pull_request;
    
    // Get PR file changes
    const files = await context.octokit.pulls.listFiles({
      owner: context.repo().owner,
      repo: context.repo().repo,
      pull_number: pr.number,
    });

    // Filter files that need review
    const reviewableFiles = files.data.filter(file => 
      !file.filename.match(/\.(md|txt|json|yml|yaml)$/) &&
      file.patch
    );

    if (reviewableFiles.length === 0) {
      return;
    }

    // Perform AI review on each file
    const reviews = await Promise.all(
      reviewableFiles.map(async (file) => {
        const response = await openai.chat.completions.create({
          model: 'gpt-4o',
          messages: [
            {
              role: 'system',
              content: `You are a code review expert. Review the following code changes and identify:
1. Potential bugs
2. Security vulnerabilities
3. Performance issues
4. Code style issues
5. Improvement suggestions

Use Markdown format, marking each issue with [severity], where severity can be:
- [critical] Critical issue, must fix
- [warning] Warning, recommended to fix
- [info] Informational, optional fix
- [suggestion] Suggestion`
            },
            {
              role: 'user',
              content: `File: ${file.filename}
Status: ${file.status}

Changes:
\`\`\`diff
${file.patch}
\`\`\``
            }
          ],
          temperature: 0.3,
        });

        return {
          filename: file.filename,
          review: response.choices[0].message.content,
        };
      })
    );

    // Build review comment
    const reviewBody = reviews
      .map(r => `### ${r.filename}\n\n${r.review}`)
      .join('\n\n---\n\n');

    // Post review comment
    await context.octokit.issues.createComment({
      owner: context.repo().owner,
      repo: context.repo().repo,
      issue_number: pr.number,
      body: `## 🤖 AI Code Review Report\n\n${reviewBody}`,
    });

    // Add labels based on severity
    const hasCritical = reviews.some(r => r.review.includes('[critical]'));
    if (hasCritical) {
      await context.octokit.issues.addLabels({
        owner: context.repo().owner,
        repo: context.repo().repo,
        issue_number: pr.number,
        labels: ['ai-review: critical'],
      });
    }
  });
}
```

### 8.2 Review Rules Configuration

```yaml
# .github/ai-review-config.yml
ai_review:
  enabled: true
  model: gpt-4o
  
  rules:
    # Security rules
    security:
      - pattern: "eval\\("
        severity: critical
        message: "Using eval() may lead to code injection vulnerabilities"
        
      - pattern: "innerHTML"
        severity: warning
        message: "Using innerHTML may lead to XSS vulnerabilities"
        
      - pattern: "password.*=.*['\"]"
        severity: critical
        message: "Hardcoded password detected"
    
    # Performance rules
    performance:
      - pattern: "SELECT \\* FROM"
        severity: warning
        message: "Avoid using SELECT *, only query needed fields"
        
      - pattern: "console\\.log"
        severity: info
        message: "console.log should be removed from production code"
    
    # Code quality rules
    quality:
      - pattern: "catch \\(e\\) \\{\\}"
        severity: warning
        message: "Empty catch block will hide errors"
        
      - pattern: "TODO|FIXME|HACK"
        severity: info
        message: "TODO/FIXME comment detected, please verify if addressed"
  
  # File exclusion rules
  exclude:
    - "*.md"
    - "*.txt"
    - "test/**"
    - "docs/**"
  
  # Review language
  language: en-US
  
  # Maximum number of files
  max_files: 50
  
  # Maximum file size (bytes)
  max_file_size: 100000
```

### 8.3 Review Results Analysis

```typescript
// src/review-analyzer.ts
interface ReviewMetrics {
  totalFiles: number;
  criticalIssues: number;
  warnings: number;
  suggestions: number;
  securityIssues: number;
  performanceIssues: number;
}

export function analyzeReviewResults(reviews: any[]): ReviewMetrics {
  const metrics: ReviewMetrics = {
    totalFiles: reviews.length,
    criticalIssues: 0,
    warnings: 0,
    suggestions: 0,
    securityIssues: 0,
    performanceIssues: 0,
  };

  for (const review of reviews) {
    const content = review.review;
    
    // Count different types of issues
    metrics.criticalIssues += (content.match(/\[critical\]/g) || []).length;
    metrics.warnings += (content.match(/\[warning\]/g) || []).length;
    metrics.suggestions += (content.match(/\[suggestion\]/g) || []).length;
    
    // Count security and performance issues
    if (content.includes('security') || content.includes('Security')) {
      metrics.securityIssues++;
    }
    if (content.includes('performance') || content.includes('Performance')) {
      metrics.performanceIssues++;
    }
  }

  return metrics;
}

export function generateReviewSummary(metrics: ReviewMetrics): string {
  let summary = '## Review Statistics\n\n';
  summary += `| Metric | Count |\n`;
  summary += `|--------|-------|\n`;
  summary += `| Files Reviewed | ${metrics.totalFiles} |\n`;
  summary += `| Critical Issues | ${metrics.criticalIssues} |\n`;
  summary += `| Warnings | ${metrics.warnings} |\n`;
  summary += `| Suggestions | ${metrics.suggestions} |\n`;
  summary += `| Security Issues | ${metrics.securityIssues} |\n`;
  summary += `| Performance Issues | ${metrics.performanceIssues} |\n`;
  
  return summary;
}
```

---

## 9. AI-Assisted Issue Triage and Management

### 9.1 Automatic Classification System

```typescript
// src/issue-classifier.ts
import OpenAI from 'openai';

interface ClassificationResult {
  category: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  labels: string[];
  assignee?: string;
  comment?: string;
}

export class IssueClassifier {
  private openai: OpenAI;
  
  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async classify(issue: {
    title: string;
    body: string;
    labels: string[];
  }): Promise<ClassificationResult> {
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are an Issue classification expert. Based on the Issue title and content, perform the following classifications:

1. Category:
   - bug: Bug report
   - feature: Feature request
   - documentation: Documentation issue
   - question: Question/inquiry
   - enhancement: Enhancement suggestion
   - performance: Performance issue
   - security: Security issue

2. Priority:
   - critical: Critical issue, affects production
   - high: High priority, affects main functionality
   - medium: Medium priority, does not affect main functionality
   - low: Low priority, can be handled later

3. Suggested labels: Appropriate label list

Please return the result in JSON format.`
        },
        {
          role: 'user',
          content: `Issue Title: ${issue.title}
Issue Content: ${issue.body}
Existing Labels: ${issue.labels.join(', ')}`
        }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.1,
    });

    const result = JSON.parse(response.choices[0].message.content);
    
    return {
      category: result.category,
      priority: result.priority,
      labels: [...new Set([...issue.labels, ...result.labels])],
    };
  }
}
```

### 9.2 Issue Priority Sorting

```typescript
// src/issue-prioritizer.ts
export class IssuePrioritizer {
  async prioritizeIssues(issues: any[]): Promise<any[]> {
    // Use AI to evaluate the priority of each Issue
    const prioritized = await Promise.all(
      issues.map(async (issue) => {
        const priority = await this.evaluatePriority(issue);
        return { ...issue, priorityScore: priority };
      })
    );

    // Sort by priority
    return prioritized.sort((a, b) => b.priorityScore - a.priorityScore);
  }

  private async evaluatePriority(issue: any): Promise<number> {
    // Calculate priority score based on multiple factors
    let score = 0;

    // Factor 1: Label weights
    const labelWeights = {
      'bug': 3,
      'security': 5,
      'performance': 4,
      'feature': 2,
      'documentation': 1,
    };
    
    for (const label of issue.labels) {
      score += labelWeights[label.name] || 0;
    }

    // Factor 2: Issue age (older = higher priority)
    const ageInDays = (Date.now() - new Date(issue.created_at).getTime()) / (1000 * 60 * 60 * 24);
    score += Math.min(ageInDays / 7, 5); // Maximum 5 points

    // Factor 3: Reaction count (community attention)
    const reactionCount = issue.reactions?.total_count || 0;
    score += Math.min(reactionCount, 10); // Maximum 10 points

    // Factor 4: Comment count (discussion activity)
    const commentCount = issue.comments || 0;
    score += Math.min(commentCount / 2, 5); // Maximum 5 points

    // Factor 5: Linked PR count
    const linkedPRs = issue.pull_request ? 1 : 0;
    score += linkedPRs * 2;

    return score;
  }
}
```

### 9.3 Auto-Response System

```typescript
// src/auto-responder.ts
import OpenAI from 'openai';

export class AutoResponder {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async generateResponse(issue: {
    title: string;
    body: string;
    labels: string[];
  }): Promise<string | null> {
    // Only auto-generate responses for specific Issue types
    const shouldRespond = this.shouldAutoRespond(issue);
    if (!shouldRespond) {
      return null;
    }

    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a friendly open source community assistant. Generate appropriate responses based on Issue type:

For bug reports:
- Thank the user for reporting
- Ask for more information (if needed)
- Provide possible solutions or workarounds

For feature requests:
- Thank the user for the suggestion
- Ask about use cases
- Explain current plans

For questions:
- Provide detailed answers
- Point to relevant documentation
- Suggest searching existing Issues

Keep responses concise, friendly, and helpful.`
        },
        {
          role: 'user',
          content: `Issue Title: ${issue.title}
Issue Content: ${issue.body}
Labels: ${issue.labels.join(', ')}`
        }
      ],
      temperature: 0.7,
      max_tokens: 500,
    });

    return response.choices[0].message.content;
  }

  private shouldAutoRespond(issue: any): boolean {
    // Cases where auto-response should be skipped
    const skipLabels = ['wontfix', 'duplicate', 'invalid'];
    if (issue.labels.some((l: any) => skipLabels.includes(l.name))) {
      return false;
    }

    // Don't auto-respond to Issues that already have comments
    if (issue.comments > 0) {
      return false;
    }

    return true;
  }
}
```

---

## 10. AI-Assisted Documentation Generation

### 10.1 Automated API Documentation Generation

```typescript
// src/api-doc-generator.ts
import OpenAI from 'openai';
import * as fs from 'fs';
import * as path from 'path';

export class APIDocGenerator {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async generateFromFile(filePath: string): Promise<string> {
    const code = fs.readFileSync(filePath, 'utf-8');
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are an API documentation generation expert. Generate detailed API documentation from code, including:

1. Module overview
2. Class/function list
3. Detailed description for each function:
   - Function description
   - Parameter description (type, required, default value)
   - Return value description
   - Exception description
   - Usage example
4. Type definition description
5. Constant description

Use Markdown format.`
        },
        {
          role: 'user',
          content: `File path: ${filePath}
Code content:
\`\`\`typescript
${code}
\`\`\``
        }
      ],
      temperature: 0.2,
      max_tokens: 4000,
    });

    return response.choices[0].message.content;
  }

  async generateFromDirectory(dirPath: string): Promise<void> {
    const files = this.getCodeFiles(dirPath);
    
    for (const file of files) {
      const doc = await this.generateFromFile(file);
      const docPath = file.replace(/\.(ts|js)$/, '.md');
      fs.writeFileSync(docPath, doc);
      console.log(`Generated documentation: ${docPath}`);
    }
  }

  private getCodeFiles(dirPath: string): string[] {
    const files: string[] = [];
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        files.push(...this.getCodeFiles(fullPath));
      } else if (entry.isFile() && /\.(ts|js)$/.test(entry.name)) {
        files.push(fullPath);
      }
    }

    return files;
  }
}
```

### 10.2 README Auto-Generation

```yaml
# .github/workflows/auto-readme.yml
name: Auto Generate README

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'package.json'

jobs:
  generate-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate README
        uses: your-org/ai-readme-generator@v1
        with:
          openai-key: ${{ secrets.OPENAI_API_KEY }}
          template: .github/readme-template.md
          output: README.md
          
      - name: Commit Changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add README.md
          git diff --staged --quiet || git commit -m "docs: auto-update README"
          git push
```

### 10.3 Changelog Auto-Generation

```typescript
// src/changelog-generator.ts
import OpenAI from 'openai';

export class ChangelogGenerator {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async generateFromCommits(commits: any[]): Promise<string> {
    const commitMessages = commits.map(c => `- ${c.message}`).join('\n');
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a changelog generation expert. Generate structured changelog from Git commit records.

Use the following categories:
- 🚀 New Features
- 🐛 Bug Fixes
- 📝 Documentation
- 🔧 Maintenance
- ⚡ Performance Improvements
- 🔒 Security
- 💥 Breaking Changes

Use concise descriptions for each change, including related Issue/PR numbers.`
        },
        {
          role: 'user',
          content: `Commit records:
${commitMessages}`
        }
      ],
      temperature: 0.3,
      max_tokens: 2000,
    });

    return response.choices[0].message.content;
  }
}
```

---

## 11. AI-Assisted Test Generation

### 11.1 Intelligent Test Case Generation

```typescript
// src/test-generator.ts
import OpenAI from 'openai';
import * as fs from 'fs';

export class TestGenerator {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async generateTests(filePath: string): Promise<string> {
    const code = fs.readFileSync(filePath, 'utf-8');
    const testFramework = this.detectTestFramework(filePath);
    
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a test generation expert. Generate comprehensive unit tests from code.

Test requirements:
1. Cover all public functions/methods
2. Test normal flow
3. Test boundary conditions
4. Test error handling
5. Use ${testFramework} test framework
6. Use AAA pattern (Arrange-Act-Assert)
7. Include descriptive test names
8. Mock external dependencies

Generated test code should be directly runnable.`
        },
        {
          role: 'user',
          content: `File path: ${filePath}
Test framework: ${testFramework}
Code content:
\`\`\`typescript
${code}
\`\`\``
        }
      ],
      temperature: 0.2,
      max_tokens: 4000,
    });

    return response.choices[0].message.content;
  }

  private detectTestFramework(filePath: string): string {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf-8'));
    
    if (packageJson.devDependencies?.jest || packageJson.dependencies?.jest) {
      return 'Jest';
    }
    if (packageJson.devDependencies?.vitest || packageJson.dependencies?.vitest) {
      return 'Vitest';
    }
    if (packageJson.devDependencies?.mocha || packageJson.dependencies?.mocha) {
      return 'Mocha';
    }
    
    return 'Jest'; // Default to Jest
  }
}
```

### 11.2 Test Coverage Analysis

```typescript
// src/coverage-analyzer.ts
import OpenAI from 'openai';

export class CoverageAnalyzer {
  private openai: OpenAI;

  constructor(apiKey: string) {
    this.openai = new OpenAI({ apiKey });
  }

  async analyzeCoverageGaps(coverageReport: any): Promise<string> {
    const response = await this.openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: `You are a test coverage analysis expert. Analyze the coverage report to find uncovered code paths
and suggest test cases that need to be added.

Return format:
1. Overall coverage summary
2. Uncovered critical paths
3. Suggested test case list
4. Priority ranking`
        },
        {
          role: 'user',
          content: `Coverage report:
${JSON.stringify(coverageReport, null, 2)}`
        }
      ],
      temperature: 0.3,
      max_tokens: 3000,
    });

    return response.choices[0].message.content;
  }
}
```

### 11.3 Test Generation Workflow

```yaml
# .github/workflows/ai-test-generation.yml
name: AI Test Generation

on:
  pull_request:
    types: [opened]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Get Changed Files
        id: changed-files
        uses: tj-actions/changed-files@v44
        
      - name: Generate Tests
        uses: your-org/ai-test-generator@v1
        with:
          files: ${{ steps.changed-files.outputs.all_changed_files }}
          openai-key: ${{ secrets.OPENAI_API_KEY }}
          
      - name: Run Generated Tests
        run: npm test
        
      - name: Update Coverage
        run: npm run test:coverage
        
      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const coverage = require('./coverage/coverage-summary.json');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## 📊 Test Coverage Report\n\n` +
                    `| Metric | Coverage |\n` +
                    `|--------|----------|\n` +
                    `| Statements | ${coverage.total.statements.pct}% |\n` +
                    `| Branches | ${coverage.total.branches.pct}% |\n` +
                    `| Functions | ${coverage.total.functions.pct}% |\n` +
                    `| Lines | ${coverage.total.lines.pct}% |\n`
            });
```

---

## 12. GitHub Next Experimental Features

### 12.1 GitHub Next Overview

GitHub Next is GitHub's **research and experimentation division**, focused on exploring the future of AI and software development.

**GitHub Next Projects**:

```
GitHub Next Research Projects:
├── Copilot Workspace
│   └── AI-native development environment
├── GitHub Models
│   └── AI Model-as-a-Service
├── Copilot for CLI
│   └── Terminal command AI assistant
├── Copilot for Docs
│   └── Documentation AI assistant
├── Copilot for Pull Requests
│   └── PR AI assistant
├── GitHub Blocks
│   └── Visual programming
├── Project Padawan
│   └── AI software engineering agent
└── Sketch-to-Code
    └── Sketch to code
```

### 12.2 Copilot for CLI

```bash
# Copilot for CLI usage examples

# Natural language to command
$ gh copilot suggest "find all large files in the current directory"
> find . -type f -size +100M

# Explain command
$ gh copilot explain "find . -name '*.js' -exec grep -l 'TODO' {} \;"
> This command does the following:
> 1. find . - Searches in the current directory and subdirectories
> 2. -name '*.js' - Only looks for .js files
> 3. -exec grep -l 'TODO' {} \; - Executes grep on each found file
>    -l only outputs filenames containing 'TODO'

# Fix command
$ gh copilot fix "git pus origin main"
> Did you mean: git push origin main?
> Possible corrections:
> 1. git push origin main (fix typo)
```

### 12.3 GitHub Blocks

GitHub Blocks is a **visual programming** environment that allows users to build applications by dragging and dropping components.

```
GitHub Blocks Features:
├── Data Blocks
│   ├── API Call Block
│   ├── Database Query Block
│   └── File Read Block
├── Processing Blocks
│   ├── Code Execution Block
│   ├── Data Transformation Block
│   └── Conditional Block
├── Output Blocks
│   ├── Display Block
│   ├── File Output Block
│   └── API Response Block
└── Connectors
    ├── Data Flow Connection
    └── Control Flow Connection
```

### 12.4 Project Padawan

Project Padawan is GitHub's **AI software engineering agent** project, aiming to create AI agents capable of independently completing complex software engineering tasks.

**Padawan Capabilities**:

```markdown
## Project Padawan Capabilities

### Code Understanding
- Understand the structure of entire codebases
- Track code dependencies
- Understand code intent and design patterns

### Task Execution
- Independently complete tasks based on Issue descriptions
- Automatically create branches, write code, submit PRs
- Respond to code review comments and modify code

### Learning Ability
- Learn from project history
- Adapt to project coding style
- Understand team workflows

### Collaboration
- Collaborate with human developers
- Explain decision-making process
- Accept feedback and improve
```

---

## 13. Impact of AI on Open Source Communities

### 13.1 Positive Impact

```markdown
## Positive Impact of AI on Open Source Communities

### 1. Lowering Contribution Barriers
- AI-assisted code understanding helps newcomers get started quickly
- Automatic documentation generation reduces learning curve
- Smart recommendation of "Good First Issues"

### 2. Improving Development Efficiency
- AI code completion accelerates development
- Automated code review reduces manual workload
- Intelligent bug fix suggestions

### 3. Improving Code Quality
- AI detects potential bugs and security vulnerabilities
- Automated test generation improves coverage
- Code style consistency checking

### 4. Enhancing Community Collaboration
- AI-assisted Issue classification and priority sorting
- Automatic translation breaks language barriers
- Smart matching of contributors and tasks
```

### 13.2 Challenges and Risks

```markdown
## Challenges of AI on Open Source Communities

### 1. Code Quality Risks
- AI-generated code may contain hidden bugs
- Over-reliance on AI may degrade developer skills
- AI may generate code that doesn't conform to project standards

### 2. Security Risks
- AI may generate code with security vulnerabilities
- Training data may contain malicious code
- AI tools may be used for malicious purposes

### 3. Community Governance Challenges
- How to effectively review the large volume of AI-generated PRs
- How to ensure the quality of AI contributions
- Copyright and licensing issues of AI-generated code

### 4. Ethical Issues
- Copyright issues of AI training data
- AI may exacerbate technological inequality
- AI may replace human developer jobs
```

### 13.3 Open Source Community Response Strategies

```markdown
## Response Strategies

### 1. Establish AI Code Review Mechanisms
- Develop review standards for AI-generated code
- Establish AI code quality checking processes
- Use AI to assist in reviewing AI-generated code

### 2. Improve Community Governance
- Update contribution guidelines to include rules for AI contributions
- Establish transparency requirements for AI contributions
- Develop community norms for AI tool usage

### 3. Invest in Education and Training
- Help developers learn to effectively use AI tools
- Emphasize that AI is an assistant tool, not a replacement
- Cultivate critical thinking, don't blindly trust AI

### 4. Technical Safeguards
- Establish automated testing and CI/CD processes
- Use multiple AI tools for cross-validation
- Maintain human control in critical decision-making
```

---

## 14. AI Toolchain for Chinese Developers

### 14.1 Domestic AI Programming Tools

```
AI Tools Available to Chinese Developers:
├── Code Assistants
│   ├── Tongyi Lingma (Alibaba Cloud)
│   ├── CodeGeeX (Zhipu AI)
│   ├── Wenxin Kuaima (Baidu)
│   ├── Doubao MarsCode (ByteDance)
│   └── Comate (Baidu)
├── AI Model Platforms
│   ├── Baidu Wenxin Yiyan API
│   ├── Alibaba Tongyi Qianwen API
│   ├── Zhipu AI API
│   ├── Moonshot Kimi API
│   └── DeepSeek API
├── AI Development Platforms
│   ├── Baidu PaddlePaddle
│   ├── Alibaba PAI
│   ├── Tencent TI Platform
│   └── Huawei ModelArts
└── AI Application Platforms
    ├── Coze (ByteDance)
    ├── Tongyi Qianwen Applications
    └── Wenxin Yiyan Applications
```

### 14.2 Tongyi Lingma Usage

```python
# Tongyi Lingma usage examples (VS Code plugin)

# 1. Code completion
# Input comments, automatically generate code
def calculate_fibonacci(n):
    # Calculate the nth Fibonacci number
    # Tongyi Lingma will automatically generate complete implementation
    
# 2. Code explanation
# Select code, right-click to select "Tongyi Lingma: Explain Code"
# Will generate detailed code explanation

# 3. Code optimization suggestions
# Select code, right-click to select "Tongyi Lingma: Optimize Code"
# Will provide optimization suggestions

# 4. Unit test generation
# Select function, right-click to select "Tongyi Lingma: Generate Unit Tests"
# Will automatically generate test cases
```

### 14.3 CodeGeeX Usage

```python
# CodeGeeX usage examples

# 1. Multi-language code generation
# Describe requirements in Chinese, generate Python code
# "Create a function to calculate the number of days between two dates"

# 2. Code translation
# Translate Python code to Java
# Select code, choose "Translate to Java"

# 3. Code comment generation
# Select code, choose "Generate Comments"
# Automatically generate Chinese and English comments

# 4. Code refactoring
# Select code, choose "Refactoring Suggestions"
# Provide refactoring solutions
```

### 14.4 Domestic AI API Usage

```python
# Using Baidu Wenxin Yiyan API
import requests

def call_wenxin(prompt, api_key, secret_key):
    # Get access_token
    token_url = "https://aip.baidubce.com/oauth/2.0/token"
    token_params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    token_response = requests.post(token_url, params=token_params)
    access_token = token_response.json()["access_token"]
    
    # Call Wenxin Yiyan API
    api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token={access_token}"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(api_url, json=payload)
    return response.json()["result"]

# Usage example
result = call_wenxin(
    "Explain what microservices architecture is",
    "your_api_key",
    "your_secret_key"
)
print(result)
```

```python
# Using Zhipu AI API
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your_api_key")

def call_glm4(prompt):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content

# Usage example
result = call_glm4("Implement a simple HTTP server in Python")
print(result)
```

### 14.5 Chinese Developer Best Practices

```markdown
## Chinese Developer AI Tool Best Practices

### 1. Tool Selection
- International projects: GitHub Copilot + GPT-4o
- Domestic projects: Tongyi Lingma + Tongyi Qianwen
- Enterprise projects: Choose domestic tools based on compliance requirements

### 2. Data Security
- Avoid uploading sensitive code to third-party AI services
- Use locally deployed AI models for sensitive code
- Comply with company data security policies

### 3. Code Quality
- Do not blindly accept AI-generated code
- Perform thorough code reviews
- Run complete test suites

### 4. Continuous Learning
- Learn best practices for using AI tools
- Stay updated on the latest developments in AI programming
- Develop the ability to collaborate with AI
```

### 14.6 Future Trends in AI Programming

```markdown
## Future Trends in AI Programming

### 1. Multimodal AI
- Support for images, voice, text, and other inputs
- Generate code directly from design mockups
- Voice-driven programming

### 2. Autonomous Agents
- AI capable of independently completing complex development tasks
- Automatic debugging and bug fixing
- Self-learning and improvement

### 3. Personalized AI
- Learn developer coding styles
- Adapt to specific project needs
- Provide personalized suggestions

### 4. Collaborative AI
- Multiple AI agents collaborating on tasks
- Deep collaboration between AI and human developers
- Cross-team AI collaboration

### 5. Domain-Specific AI
- AI programming assistants for specific domains
- Understanding domain-specific knowledge and standards
- Providing professional advice and solutions
```

---

## Summary

### Key Takeaways Review

1. **Copilot Workspace** is an AI-native development environment that integrates AI capabilities throughout the entire development workflow
2. **Agent Mode** can autonomously execute complex development tasks
3. **Copilot Extensions** allow developers to extend Copilot's capabilities
4. **GitHub Models** provides convenient access to AI models
5. **AI-assisted CI/CD** can automate code review, test generation, and documentation generation
6. **Chinese developers** have a rich selection of domestic AI tools to choose from
7. **AI's impact on open source communities** brings both positive effects and challenges

### Recommended Learning Path

```
Beginner Stage:
├── 1. Use GitHub Copilot basic features
├── 2. Learn Copilot Chat usage
└── 3. Try Copilot for CLI

Intermediate Stage:
├── 4. Learn Copilot Workspace usage
├── 5. Try Agent Mode
├── 6. Use GitHub Models API
└── 7. Build a simple Copilot Extension

Advanced Stage:
├── 8. Develop complex Copilot Extensions
├── 9. Build AI-assisted CI/CD workflows
├── 10. Implement custom AI code review systems
└── 11. Explore GitHub Next experimental features
```

### Recommended Resources

- [GitHub Copilot Official Documentation](https://docs.github.com/en/copilot)
- [GitHub Next Research Blog](https://githubnext.com/)
- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- [Copilot Extensions Development Guide](https://docs.github.com/en/copilot/building-copilot-extensions)

### Next Steps

After completing this tutorial, it is recommended to continue learning:
- **X13-real-world-project-case-studies.md**: Large-scale open source project management case studies
- **W7-copilot-advanced.md**: GitHub Copilot advanced usage tips
- **W8-copilot-extensions-dev.md**: Copilot Extensions development guide

---

> **Document Information**
> - Created: 2024
> - Last Updated: 2024
> - Version: v1.0
> - Author: GitHub Beginners Guide Writing Team

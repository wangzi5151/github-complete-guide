# GitHub Technical Writing Guide

> **Target Audience**: Chinese developers, technical documentation engineers, open source project maintainers
> **Estimated Reading Time**: 50 minutes
> **Prerequisites**: Basic Git/GitHub usage, Markdown basics

---

## Table of Contents

1. [Technical Writing Style Guide](#1-technical-writing-style-guide)
2. [Chinese Technical Documentation Typesetting Standards](#2-chinese-technical-documentation-typesetting-standards)
3. [Markdown Advanced Tips](#3-markdown-advanced-tips)
4. [AsciiDoc Introduction](#4-asciidoc-introduction)
5. [Static Documentation Sites](#5-static-documentation-sites)
6. [API Documentation Automation](#6-api-documentation-automation)
7. [Documentation Version Management Strategy](#7-documentation-version-management-strategy)
8. [Multilingual Documentation Management](#8-multilingual-documentation-management)
9. [Documentation Automated Testing](#9-documentation-automated-testing)
10. [GitHub Wiki Usage Guide](#10-github-wiki-usage-guide)
11. [GitHub Discussions as Knowledge Base](#11-github-discussions-as-knowledge-base)
12. [Technical Blog Writing](#12-technical-blog-writing)
13. [Documentation Contribution Workflow](#13-documentation-contribution-workflow)
14. [Chinese-English Mixed Typesetting Best Practices](#14-chinese-english-mixed-typesetting-best-practices)

---

## 1. Technical Writing Style Guide

### 1.1 Core Principles of Technical Writing

The goal of technical writing is **to help readers quickly understand and use technical content**. Unlike literary writing, technical writing emphasizes:

**Clarity**:
- Use simple and direct sentences
- Avoid ambiguity and vague expressions
- One sentence should express one idea

**Accuracy**:
- Technical details must be accurate
- Code examples must be runnable
- Version numbers, paths, and commands must be correct

**Conciseness**:
- Remove unnecessary modifiers
- Avoid repetitive information
- Use lists instead of long paragraphs

**Consistency**:
- Use unified terminology
- Maintain consistent formatting style
- Keep consistent document structure

### 1.2 Sentence Structure

**Use active voice**:
```markdown
# Not recommended
The configuration file is edited by the user.

# Recommended
Edit the configuration file.
```

**Use present tense**:
```markdown
# Not recommended
The system will return a JSON response.

# Recommended
The system returns a JSON response.
```

**Use second person (you)**:
```markdown
# Not recommended
Users should configure the environment.

# Recommended
You need to configure the environment variables.
```

### 1.3 Paragraph Writing

**Paragraph length**: 3-5 sentences is ideal, avoid exceeding 8 sentences

**Paragraph structure**:
1. Topic sentence: states the core content of the paragraph
2. Supporting sentences: provide details and explanations
3. Transition sentence: connects to the next paragraph (optional)

**Example**:
```markdown
GitHub Actions is a CI/CD service provided by GitHub. You can define workflows
in your repository, and they will automatically run tests and deploy when code
is pushed to specific branches. Workflows are defined using YAML format and
stored in the `.github/workflows` directory.
```

### 1.4 Terminology Management

Create a project Glossary:

```markdown
## Glossary

| Term | English | Definition |
|------|---------|------------|
| 仓库 | Repository | A container for storing code and resources |
| 分支 | Branch | An independent development line of code |
| 拉取请求 | Pull Request | A mechanism for requesting code merges |
| 工作流 | Workflow | A definition file for automated tasks |
```

### 1.5 Common Writing Errors

| Error Type | Incorrect Example | Correct Example |
|------------|-------------------|-----------------|
| Verbose | In this section, we will be discussing... | This section discusses... |
| Passive voice | Code is committed to the repository | Commit code to the repository |
| Vague | Some configurations may need modification | Modify the `timeout` field in `config.yml` |
| Colloquial | This feature is super great | This feature can improve development efficiency |
| Inconsistent terminology | Sometimes called "仓库", sometimes called "代码库" | Use "Repository" consistently |

---

## 2. Chinese Technical Documentation Typesetting Standards

### 2.1 Punctuation Standards

**Chinese punctuation**:
- Use full-width punctuation: ，。！？；：""''（）
- Do not use half-width punctuation: ,.!?;:""''()

**Special cases**:
- Use half-width punctuation in code
- Use half-width periods after English abbreviations (e.g., `e.g.`, `i.e.`)
- No space between numbers and units (e.g., `100MB`)

### 2.2 Spacing Standards

**Add space between Chinese and English**:
```markdown
# Not recommended
使用GitHub进行版本控制

# Recommended
使用 GitHub 进行版本控制
```

**Add space between numbers and Chinese**:
```markdown
# Not recommended
仓库有100个星标

# Recommended
仓库有 100 个星标
```

**No space before or after punctuation**:
```markdown
# Not recommended
使用 GitHub ，进行版本控制 。

# Recommended
使用 GitHub，进行版本控制。
```

**Exceptions**:
- Spacing in code blocks follows code conventions
- Preserve spaces between English words

### 2.3 Numbers and Units

**Numbers**:
- Generally use Arabic numerals: 3 steps, 10 files
- Use commas for large numbers: 1,000, 1,000,000
- Use symbols for percentages: 50% (not 50 percent)

**Units**:
- No space between unit and number: 100MB, 2GHz
- Use the International System of Units: KB, MB, GB, TB
- Time units: seconds, minutes, hours, days

### 2.4 Heading Standards

**Heading levels**:
- Level 1 heading (#): document title, only one per file
- Level 2 heading (##): major sections
- Level 3 heading (###): subsections
- Level 4 heading (####): detailed content
- It is not recommended to use level 5 or below headings

**Heading format**:
```markdown
# Document Title

## Level 1 Section

### Level 2 Section

#### Level 3 Section
```

**Heading capitalization**:
- Chinese headings: capitalize the first letter (e.g., "Git 基础教程")
- English headings: Title Case (e.g., "Getting Started with Git")
- Keep proper nouns as-is: GitHub, JavaScript, API

### 2.5 List Standards

**Ordered lists**: for steps that have a sequential order
```markdown
1. Clone the repository
2. Install dependencies
3. Start the service
```

**Unordered lists**: for parallel items
```markdown
- Advantage 1
- Advantage 2
- Advantage 3
```

**Nested lists**:
```markdown
- Frontend tech stack
  - React
  - Vue.js
  - Angular
- Backend tech stack
  - Node.js
  - Python
  - Go
```

---

## 3. Markdown Advanced Tips

### 3.1 Advanced Tables

**Alignment**:
```markdown
| Left aligned | Centered | Right aligned |
|:-------------|:--------:|--------------:|
| Content | Content | Content |
```

**Code in tables**:
```markdown
| Command | Description |
|---------|-------------|
| `git add` | Stage files |
| `git commit` | Commit changes |
| `git push` | Push code |
```

**Complex tables**:
```markdown
| Feature | Free | Pro | Enterprise |
|---------|:----:|:---:|:----------:|
| Private repositories | ✅ Unlimited | ✅ Unlimited | ✅ Unlimited |
| Collaborators | 3 users | Unlimited | Unlimited |
| CI/CD minutes | 2,000 | 3,000 | 50,000 |
| Storage | 500MB | 2GB | 50GB |
```

### 3.2 Advanced Code Blocks

**Code blocks with line numbers** (some platforms support):
```markdown
```python {.numberLines}
def hello():
    print("Hello, World!")

hello()
`` `
```

**Highlight specific lines** (some platforms support):
```markdown
```python {2,3}
def calculate_sum(a, b):
    result = a + b  # This line will be highlighted
    return result   # This line will also be highlighted
`` `
```

**Comments in code blocks**:
```python
# This is a Python function
def greet(name: str) -> str:
    """
    Generate a greeting
    
    Args:
        name: username
        
    Returns:
        Greeting string
    """
    return f"Hello, {name}!"
```

### 3.3 Collapsible Content

Use the `<details>` tag to create collapsible content:

```markdown
<details>
<summary>Click to expand detailed configuration</summary>

```yaml
server:
  host: localhost
  port: 8080
  debug: true

database:
  host: localhost
  port: 5432
  name: mydb
```

</details>
```

### 3.4 Alerts and Tips

GitHub supports the following alert syntax (GitHub Flavored Markdown):

```markdown
> [!NOTE]
> This is a note message.

> [!TIP]
> This is a tip message.

> [!IMPORTANT]
> This is important information.

> [!WARNING]
> This is a warning message.

> [!CAUTION]
> This is a caution message.
```

### 3.5 Mathematical Formulas

GitHub supports LaTeX mathematical formulas:

**Inline formulas**:
```markdown
The mass-energy equivalence $E = mc^2$ is the most famous formula in physics.
```

**Block formulas**:
```markdown
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$
```

**Matrices**:
```markdown
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$
```

### 3.6 Mermaid Diagrams

GitHub natively supports Mermaid diagrams:

**Flowchart**:
```markdown
```mermaid
graph TD
    A[Start] --> B{Is installed?}
    B -->|Yes| C[Configure environment]
    B -->|No| D[Install dependencies]
    D --> C
    C --> E[Run program]
    E --> F[End]
`` `
```

**Sequence diagram**:
```markdown
```mermaid
sequenceDiagram
    participant User as User
    participant Client as Client
    participant Server as Server
    
    User->>Client: Enter command
    Client->>Server: Send request
    Server-->>Client: Return response
    Client-->>User: Display result
`` `
```

**Gantt chart**:
```markdown
```mermaid
gantt
    title Project Plan
    dateFormat  YYYY-MM-DD
    section Design Phase
    Requirements Analysis  :done,    des1, 2024-01-01, 2024-01-15
    UI Design              :active,  des2, 2024-01-10, 2024-01-25
    section Development Phase
    Frontend Development   :         dev1, 2024-01-20, 2024-02-15
    Backend Development    :         dev2, 2024-01-25, 2024-02-20
`` `
```

### 3.7 Task Lists

```markdown
## Project TODO

- [x] Complete requirements analysis
- [x] Design database schema
- [ ] Implement user authentication
- [ ] Write unit tests
- [ ] Deploy to production
```

### 3.8 Footnotes

```markdown
GitHub is the world's largest code hosting platform[^1], with over 100 million developers[^2].

[^1]: GitHub official website https://github.com
[^2]: Statistics as of 2024
```

---

## 4. AsciiDoc Introduction

### 4.1 AsciiDoc Overview

AsciiDoc is a lightweight markup language that is more powerful than Markdown, particularly suitable for writing large technical documents.

**Key Features**:
- Supports complex document structures
- Built-in cross-references and indexing
- Supports conditional compilation
- Extensible macro system
- Generates HTML, PDF, EPUB and other formats

### 4.2 AsciiDoc vs Markdown Comparison

| Feature | Markdown | AsciiDoc |
|---------|----------|----------|
| Learning curve | Low | Medium |
| Table support | Basic | Advanced |
| Cross-references | Not supported | Native support |
| Conditional compilation | Not supported | Supported |
| Table of contents | Auto/Manual | Auto |
| Code blocks | Basic | Advanced (with callouts) |
| Use cases | Simple docs, README | Large docs, books |

### 4.3 AsciiDoc Basic Syntax

**Headings**:
```asciidoc
= Document Title
== Level 1 Section
=== Level 2 Section
==== Level 3 Section
```

**Paragraphs and line breaks**:
```asciidoc
This is the first paragraph.

This is the second paragraph.
Line breaks within a paragraph use +
forced line break.
```

**Lists**:
```asciidoc
* Unordered list item 1
* Unordered list item 2
** Nested item

. Ordered list item 1
. Ordered list item 2
.. Nested item
```

**Code blocks**:
```asciidoc
[source,python]
----
def hello():
    print("Hello, World!")
----
```

**Annotated code blocks**:
```asciidoc
[source,python]
----
def hello():  # <1>
    print("Hello, World!")  # <2>
----
<1> Function definition
<2> Print statement
```

**Tables**:
```asciidoc
[cols="1,2,1", options="header"]
|===
| Command
| Description
| Example

| git add
| Stage files
| `git add .`

| git commit
| Commit changes
| `git commit -m "message"`
|===
```

**Cross-references**:
```asciidoc
See the <<_installation>> section.

[[installation]]
== Installation Guide

This chapter describes how to install the software.
```

### 4.4 AsciiDoc Toolchain

**Asciidoctor**: The main AsciiDoc processor
```bash
# Install
gem install asciidoctor

# Convert to HTML
asciidoctor document.adoc

# Convert to PDF
asciidoctor-pdf document.adoc

# Convert to EPUB
asciidoctor-epub3 document.adoc
```

**Antora**: AsciiDoc documentation site generator
```bash
# Install
npm install -g @antora/cli @antora/site-generator-default

# Generate site
antora site.yml
```

### 4.5 When to Choose AsciiDoc

**Choose AsciiDoc**:
- Large documentation projects (over 100 pages)
- Need cross-references and indexing
- Need to generate PDF
- Technical book writing
- Enterprise-level documentation

**Choose Markdown**:
- Simple READMEs
- Blog posts
- Quick notes
- GitHub project documentation

---

## 5. Static Documentation Sites

### 5.1 Popular Static Documentation Site Tools

| Tool | Language | Features | Use Cases |
|------|----------|----------|-----------|
| MkDocs | Python | Easy to use, Material theme | Project documentation |
| Docusaurus | React | By Facebook, version management | Open source project docs |
| VitePress | Vue | Blazing fast build, Vue ecosystem | Vue project documentation |
| Hugo | Go | Blazing fast build, feature-rich | Blogs, documentation |
| Jekyll | Ruby | Native GitHub Pages support | Blogs |
| Sphinx | Python | Academic docs, reStructuredText | Python projects |

### 5.2 Getting Started with MkDocs

**Installation**:
```bash
pip install mkdocs
pip install mkdocs-material  # Material theme
```

**Initialize project**:
```bash
mkdocs new my-docs
cd my-docs
```

**Directory structure**:
```
my-docs/
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   └── api/
│       ├── overview.md
│       └── reference.md
└── mkdocs.yml
```

**Configuration file (mkdocs.yml)**:
```yaml
site_name: My Project Documentation
site_description: Project Documentation Site
site_url: https://example.com

theme:
  name: material
  language: zh
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.suggest
    - content.code.copy

nav:
  - Home: index.md
  - Quick Start: getting-started.md
  - API Documentation:
    - Overview: api/overview.md
    - Reference: api/reference.md

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```

**Local preview**:
```bash
mkdocs serve
# Visit http://localhost:8000
```

**Deploy to GitHub Pages**:
```bash
mkdocs gh-deploy
```

### 5.3 Getting Started with Docusaurus

**Initialize project**:
```bash
npx create-docusaurus@latest my-website classic
cd my-website
```

**Directory structure**:
```
my-website/
├── docs/
│   ├── intro.md
│   ├── tutorial-basics/
│   │   └── create-a-page.md
│   └── tutorial-extras/
│       └── translate-your-site.md
├── blog/
├── src/
│   ├── components/
│   └── css/
├── docusaurus.config.js
├── sidebars.js
└── package.json
```

**Configuration file (docusaurus.config.js)**:
```javascript
module.exports = {
  title: 'My Project Documentation',
  tagline: 'Project Documentation Site',
  url: 'https://example.com',
  baseUrl: '/',
  
  organizationName: 'your-org',
  projectName: 'your-project',
  
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en'],
  },
  
  themeConfig: {
    navbar: {
      title: 'My Project',
      items: [
        { type: 'doc', position: 'left', docId: 'intro', label: 'Docs' },
        { to: '/blog', label: 'Blog', position: 'left' },
        { type: 'localeDropdown', position: 'right' },
        { href: 'https://github.com/your-org/your-project', label: 'GitHub', position: 'right' },
      ],
    },
    
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Quick Start', to: '/docs/intro' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'GitHub', href: 'https://github.com/your-org/your-project' },
          ],
        },
      ],
    },
  },
};
```

**Run and build**:
```bash
# Local development
npm start

# Build
npm run build

# Deploy to GitHub Pages
GIT_USER=your-username npm run deploy
```

### 5.4 Getting Started with VitePress

**Installation**:
```bash
npm init vitepress
```

**Directory structure**:
```
docs/
├── .vitepress/
│   └── config.js
├── index.md
├── guide/
│   ├── getting-started.md
│   └── api.md
└── examples/
```

**Configuration file (.vitepress/config.js)**:
```javascript
export default {
  title: 'My Project Documentation',
  description: 'Project Documentation Site',
  
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'API', link: '/guide/api' },
    ],
    
    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Quick Start', link: '/guide/getting-started' },
            { text: 'API Reference', link: '/guide/api' },
          ],
        },
      ],
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-org/your-project' },
    ],
    
    search: {
      provider: 'local',
    },
  },
};
```

**Run and build**:
```bash
# Local development
npm run dev

# Build
npm run build

# Preview build result
npm run preview
```

### 5.5 Getting Started with Hugo

**Installation**:
```bash
# macOS
brew install hugo

# Linux
sudo apt install hugo

# Windows
choco install hugo
```

**Create site**:
```bash
hugo new site my-docs
cd my-docs
```

**Install theme**:
```bash
git init
git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
```

**Configuration file (hugo.toml)**:
```toml
baseURL = 'https://example.com/'
languageCode = 'zh-CN'
title = 'My Project Documentation'
theme = 'hugo-book'

[params]
  BookTheme = 'auto'
  BookToC = true
  BookSection = 'docs'
  BookRepo = 'https://github.com/your-org/your-project'

[menu]
  [[menu.after]]
    name = "GitHub"
    url = "https://github.com/your-org/your-project"
    weight = 10
```

**Create content**:
```bash
hugo new docs/getting-started.md
```

**Run and build**:
```bash
# Local development
hugo server -D

# Build
hugo
```

---

## 6. API Documentation Automation

### 6.1 API Documentation Tools Overview

| Tool | Features | Use Cases |
|------|----------|-----------|
| Swagger UI | Interactive docs, online testing | REST API |
| Redoc | Beautiful three-column layout | Production documentation |
| Stoplight Studio | Visual editor | API design |
| Readme.io | Commercial platform, collaboration | Enterprise API docs |
| Postman | API testing + documentation | API development |

### 6.2 OpenAPI Specification

OpenAPI (formerly Swagger) is the standard specification for describing REST APIs:

**OpenAPI 3.0 Example (YAML)**:
```yaml
openapi: 3.0.0
info:
  title: User Management API
  description: REST API documentation for user management system
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: Get user list
      description: Returns a list of all users
      operationId: getUsers
      tags:
        - User Management
      parameters:
        - name: page
          in: query
          description: Page number
          required: false
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          description: Items per page
          required: false
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successfully returned user list
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  total:
                    type: integer
        '401':
          description: Unauthorized
    
    post:
      summary: Create user
      description: Create a new user
      operationId: createUser
      tags:
        - User Management
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Invalid request parameters

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          description: User ID
          example: 1
        name:
          type: string
          description: Username
          example: "John Doe"
        email:
          type: string
          format: email
          description: Email address
          example: "johndoe@example.com"
        created_at:
          type: string
          format: date-time
          description: Creation time
    
    CreateUserRequest:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          description: Username
          example: "John Doe"
        email:
          type: string
          format: email
          description: Email address
          example: "johndoe@example.com"
```

### 6.3 Swagger UI Integration

**HTML integration**:
```html
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
  <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "/openapi.yaml",
      dom_id: '#swagger-ui',
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout"
    });
  </script>
</body>
</html>
```

**GitHub Pages integration**:
```yaml
# .github/workflows/api-docs.yml
name: Deploy API Docs

on:
  push:
    branches: [main]
    paths:
      - 'openapi.yaml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Build docs
        run: |
          npm install -g redoc-cli
          redoc-cli build openapi.yaml -o docs/api/index.html
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

### 6.4 Redoc Integration

Redoc provides a more beautiful three-column layout:

```bash
# Install
npm install -g redoc-cli

# Local preview
redoc-cli serve openapi.yaml

# Build static files
redoc-cli build openapi.yaml -o api-docs.html
```

**Custom configuration**:
```yaml
# redoc.yaml
theme:
  colors:
    primary:
      main: '#1976d2'
  typography:
    fontSize: '15px'
    fontFamily: 'Roboto, sans-serif'
  sidebar:
    width: '260px'
```

### 6.5 Auto-generate Documentation from Code Comments

**Python (using FastAPI)**:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="User Management API",
    description="REST API for user management system",
    version="1.0.0"
)

class User(BaseModel):
    """User model"""
    id: int
    name: str
    email: str

class CreateUserRequest(BaseModel):
    """Create user request"""
    name: str
    email: str

@app.get("/users", response_model=List[User], tags=["User Management"])
async def get_users(page: int = 1, limit: int = 20):
    """
    Get user list
    
    - **page**: Page number (default 1)
    - **limit**: Items per page (default 20)
    """
    # Implementation code
    pass

@app.post("/users", response_model=User, tags=["User Management"])
async def create_user(request: CreateUserRequest):
    """
    Create user
    
    Create a new user and return user information
    """
    # Implementation code
    pass
```

**Node.js (using Express + Swagger JSDoc)**:
```javascript
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const app = express();

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'User Management API',
      version: '1.0.0',
    },
  },
  apis: ['./routes/*.js'],
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

/**
 * @swagger
 * /users:
 *   get:
 *     summary: Get user list
 *     tags: [User Management]
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *         description: Page number
 *     responses:
 *       200:
 *         description: Success
 */
app.get('/users', (req, res) => {
  // Implementation code
});

app.listen(3000);
```

---

## 7. Documentation Version Management Strategy

### 7.1 Importance of Version Management

As projects iterate, documentation also needs version management:

- Users may be using different versions of the software
- APIs may change between versions
- Old version documentation needs to be preserved for reference

### 7.2 Docusaurus Version Management

Docusaurus has built-in version management:

```bash
# Create a new version
npm run docusaurus docs:version 2.0

# Directory structure changes
docs/           # Current development version (next)
versioned_docs/
  version-1.0/  # Version 1.0 documentation
  version-2.0/  # Version 2.0 documentation
versioned_sidebars/
  version-1.0-sidebars.json
  version-2.0-sidebars.json
```

**Configure version dropdown**:
```javascript
// docusaurus.config.js
module.exports = {
  themeConfig: {
    navbar: {
      items: [
        {
          type: 'docsVersionDropdown',
          position: 'right',
        },
      ],
    },
  },
};
```

### 7.3 MkDocs Version Management

Use the `mike` tool to manage MkDocs versions:

```bash
# Install
pip install mike

# Set default version
mike set-default latest

# Create new versions
mike deploy 1.0
mike deploy 2.0

# List all versions
mike list

# Set alias
mike deploy 2.0 latest
```

**Configure mkdocs.yml**:
```yaml
extra:
  version:
    provider: mike
```

### 7.4 Git Branch Strategy

**Branch naming conventions**:
```
main           # Main branch, latest documentation
docs/v1.0      # Version 1.0 documentation
docs/v2.0      # Version 2.0 documentation
docs/next       # Next version development documentation
```

**GitHub Actions auto-deployment**:
```yaml
name: Deploy Docs

on:
  push:
    branches:
      - main
      - 'docs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Determine version
        id: version
        run: |
          BRANCH=${GITHUB_REF#refs/heads/}
          if [ "$BRANCH" = "main" ]; then
            echo "version=latest" >> $GITHUB_OUTPUT
          else
            VERSION=${BRANCH#docs/}
            echo "version=$VERSION" >> $GITHUB_OUTPUT
          fi
      
      - name: Deploy
        run: |
          # Deploy to corresponding version directory
          echo "Deploying version ${{ steps.version.outputs.version }}"
```

### 7.5 Documentation Snapshots and Archiving

**Creating documentation snapshots**:
```bash
# Create snapshot directory
mkdir -p snapshots/v1.0.0

# Copy documentation
cp -r docs/* snapshots/v1.0.0/

# Commit snapshot
git add snapshots/v1.0.0
git commit -m "docs: snapshot v1.0.0"
git tag docs-v1.0.0
```

---

## 8. Multilingual Documentation Management

### 8.1 Multilingual Documentation Strategies

**Strategy 1: Separate directories**
```
docs/
├── en/
│   ├── getting-started.md
│   └── api/
├── zh/
│   ├── getting-started.md
│   └── api/
└── ja/
    ├── getting-started.md
    └── api/
```

**Strategy 2: File suffixes**
```
docs/
├── getting-started.md        # Default language
├── getting-started.zh.md     # Chinese
├── getting-started.ja.md     # Japanese
├── api/
│   ├── overview.md
│   ├── overview.zh.md
│   └── overview.ja.md
```

**Strategy 3: i18n framework**
```
docs/
├── getting-started.md
├── i18n/
│   ├── zh/
│   │   └── getting-started.md
│   └── ja/
│       └── getting-started.md
```

### 8.2 Docusaurus Multilingual Configuration

```javascript
// docusaurus.config.js
module.exports = {
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en', 'ja'],
    localeConfigs: {
      'zh-Hans': {
        label: '简体中文',
        htmlLang: 'zh-Hans',
      },
      en: {
        label: 'English',
      },
      ja: {
        label: '日本語',
      },
    },
  },
};
```

**Translation workflow**:
```bash
# Extract strings that need translation
npm run write-translations -- --locale zh-Hans

# Translation files are located at
# i18n/zh-Hans/docusaurus-plugin-content-docs/current/
# i18n/zh-Hans/docusaurus-theme-classic/
```

### 8.3 MkDocs Multilingual Configuration

Use the `mkdocs-static-i18n` plugin:

```yaml
# mkdocs.yml
plugins:
  - i18n:
      default_language: en
      languages:
        en:
          name: English
          build: true
        zh:
          name: 中文
          build: true
```

**Directory structure**:
```
docs/
├── index.md
├── getting-started.md
├── index.zh.md
├── getting-started.zh.md
```

### 8.4 Crowdin Integration

Crowdin is a professional translation management platform that supports GitHub integration:

**Configuration file (crowdin.yml)**:
```yaml
project_id_env: CROWDIN_PROJECT_ID
api_token_env: CROWDIN_PERSONAL_TOKEN

files:
  - source: /docs/**/*.md
    translation: /docs/**/%file_name%.%two_letters_code%.md
```

**GitHub Actions integration**:
```yaml
name: Crowdin

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  crowdin-upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Upload sources
        uses: crowdin/github-action@v1
        with:
          upload_sources: true
          download_translations: true
          config: crowdin.yml
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_PERSONAL_TOKEN }}
```

### 8.5 Translation Best Practices

1. **Maintain terminology consistency**: Create multilingual glossaries
2. **Avoid hardcoded strings**: Use i18n frameworks to manage text
3. **Provide language switching**: Add language selector to navigation bar
4. **Synchronize regularly**: Ensure translations stay in sync with source
5. **Community translation**: Encourage community contributions to translations

---

## 9. Documentation Automated Testing

### 9.1 Why Documentation Testing is Needed

Code examples in documentation may break due to:

- API changes
- Dependency version updates
- Configuration file changes
- Environment differences

### 9.2 Code Block Testing

**Python doctest**:
```python
def add(a, b):
    """
    Calculate the sum of two numbers
    
    >>> add(1, 2)
    3
    >>> add(-1, 1)
    0
    """
    return a + b

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

**Markdown code block testing** (using `markdown-test`):
```bash
# Install
npm install -g markdown-test

# Run tests
markdown-test docs/**/*.md
```

### 9.3 Link Checking

**Using markdown-link-check**:
```bash
# Install
npm install -g markdown-link-check

# Check a single file
markdown-link-check README.md

# Check a directory
find docs -name "*.md" -exec markdown-link-check {} \;
```

**GitHub Actions configuration**:
```yaml
name: Check Links

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          config-file: '.mlc-config.json'
```

**Configuration file (.mlc-config.json)**:
```json
{
  "retryOn429": true,
  "retryCount": 3,
  "aliveStatusCodes": [200, 206, 301, 302],
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    }
  ]
}
```

### 9.4 Spell Checking

**Using cspell**:
```bash
# Install
npm install -g cspell

# Check files
cspell "docs/**/*.md"

# Add custom words
cspell add words
```

**Configuration file (cspell.json)**:
```json
{
  "version": "0.2",
  "language": "en",
  "words": [
    "GitHub",
    "API",
    "CLI",
    "Docusaurus",
    "VitePress"
  ],
  "ignorePaths": [
    "node_modules",
    "package-lock.json"
  ]
}
```

### 9.5 Documentation CI/CD Pipeline

Complete documentation CI/CD pipeline:

```yaml
name: Docs CI

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check markdown
        uses: avto-dev/markdown-lint@v1
        with:
          args: './docs'
      
      - name: Check links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
      
      - name: Spell check
        run: npx cspell "docs/**/*.md"
  
  build:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build docs
        run: npm run docs:build
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: docs
          path: docs/dist
  
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: docs
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .
```

---

## 10. GitHub Wiki Usage Guide

### 10.1 Wiki Overview

GitHub Wiki is a documentation feature included with every repository, suitable for writing project documentation, knowledge bases, and tutorials.

**Features**:
- Independent Git repository
- Supports Markdown syntax
- Can be cloned and edited locally
- Supports sidebar navigation

### 10.2 Creating and Editing Wikis

**Enabling Wiki**:
1. Go to repository Settings
2. Check Wikis in the Features section
3. Click the Wiki tab to start creating

**Creating pages**:
1. Click "New Page"
2. Enter page title
3. Write content (Markdown format)
4. Click "Save Page"

### 10.3 Local Wiki Management

**Cloning Wiki**:
```bash
# Wiki URL format
git clone https://github.com/owner/repo.wiki.git

# Example
git clone https://github.com/octocat/Hello-World.wiki.git
```

**Local editing**:
```bash
cd repo.wiki.git

# Edit files
vim Home.md

# Commit changes
git add .
git commit -m "Update wiki"
git push
```

### 10.4 Wiki Sidebar

Edit the `_Sidebar.md` file to define the sidebar:

```markdown
## Table of Contents

* [Home](Home)
* [Getting Started](Getting-Started)
* [Installation](Installation)
  * [Windows](Installation-Windows)
  * [macOS](Installation-macOS)
  * [Linux](Installation-Linux)
* [API Reference](API-Reference)
* [FAQ](FAQ)
```

### 10.5 Wiki Footer

Edit the `_Footer.md` file to define the footer:

```markdown
---

**Project Links**
- [GitHub Repository](https://github.com/owner/repo)
- [Issue Tracker](https://github.com/owner/repo/issues)
- [Discussions](https://github.com/owner/repo/discussions)
```

### 10.6 Wiki Best Practices

1. **Clear structure**: Use sidebar to organize page hierarchy
2. **Interconnected links**: Add links between pages
3. **Regular maintenance**: Keep Wiki content in sync with project
4. **Local backup**: Regularly clone Wiki repository for backup
5. **Contribution guide**: Explain how to contribute Wiki content

### 10.7 Wiki Limitations

**Not supported**:
- Pull Request reviews
- Code reviews
- Version branches
- Complex directory structures

**Alternatives**:
- Documentation repository (docs/ directory)
- GitHub Pages
- External documentation platforms (e.g., Readme.io)

---

## 11. GitHub Discussions as Knowledge Base

### 11.1 Discussions Overview

GitHub Discussions is a discussion feature provided by GitHub, suitable for building community knowledge bases:

**Features**:
- Category-based discussion management
- Supports Q&A format
- Can mark best answers
- Supports voting and reactions

### 11.2 Enabling Discussions

1. Go to repository Settings
2. Check Discussions in the Features section
3. Click the Discussions tab to start configuration

### 11.3 Discussion Categories

Recommended categories:

| Category | Purpose | Format |
|----------|---------|--------|
| 📢 Announcements | Project announcements | Discussion |
| 💡 Ideas | Feature suggestions | Discussion |
| ❓ Q&A | Question answers | Q&A |
| 🐛 Bug Reports | Issue feedback | Discussion |
| 📖 Tutorials | Tutorial sharing | Discussion |
| 🎉 Show and Tell | Project showcase | Discussion |

### 11.4 Discussions Configuration

**Category configuration file**:
```yaml
# .github/DISCUSSION_TEMPLATE/announcement.yml
title: "📢 [Announcement] "
labels: ["announcement"]
body:
  - type: textarea
    id: content
    attributes:
      label: Announcement content
      description: Enter announcement content
    validations:
      required: true
```

**Q&A template**:
```yaml
# .github/DISCUSSION_TEMPLATE/q-and-a.yml
title: "❓ [Question] "
labels: ["question"]
body:
  - type: textarea
    id: description
    attributes:
      label: Question description
      description: Describe your question in detail
      placeholder: |
        1. What do you want to do?
        2. What have you tried?
        3. What is your expected result?
    validations:
      required: true
  
  - type: textarea
    id: environment
    attributes:
      label: Environment information
      description: Provide your environment information
      placeholder: |
        - Operating system:
        - Node.js version:
        - Package manager:
    validations:
      required: false
```

### 11.5 Discussions vs Issues

| Feature | Issues | Discussions |
|---------|--------|-------------|
| Purpose | Bug fixes, task tracking | Discussions, Q&A, ideas |
| Status | Open/Closed | Stateless |
| Best answer | Not supported | Supported |
| Voting | Not supported | Supported |
| Categories | Labels | Categories |
| Format | Single | Multiple (discussions, Q&A, polls, etc.) |

### 11.6 Converting Discussions to Issues

If a bug is found during discussion, it can be converted to an Issue:

1. Find the relevant reply in the Discussion
2. Click the "..." menu
3. Select "Transfer to issue"
4. Fill in Issue information

### 11.7 Discussions Best Practices

1. **Create templates**: Create templates for different types of discussions
2. **Clear categories**: Define the purpose of each category clearly
3. **Respond promptly**: Keep the community active
4. **Mark answers**: For Q&A categories, mark best answers promptly
5. **Link related items**: Create links between Discussions and Issues

---

## 12. Technical Blog Writing

### 12.1 GitHub Pages + Jekyll

**Jekyll Overview**:
Jekyll is a static site generator natively supported by GitHub Pages.

**Creating a blog**:
```bash
# Create new repository
# Repository name format: username.github.io

# Clone repository
git clone https://github.com/username/username.github.io.git
cd username.github.io

# Initialize Jekyll
jekyll new .
```

**Directory structure**:
```
username.github.io/
├── _posts/
│   └── 2024-01-01-my-first-post.md
├── _config.yml
├── index.md
└── about.md
```

**Configuration file (_config.yml)**:
```yaml
title: My Tech Blog
description: Sharing technical insights
url: https://username.github.io

theme: minima

plugins:
  - jekyll-feed
  - jekyll-seo-tag

social:
  github: username
  twitter: username
```

**Writing articles**:
```markdown
---
layout: post
title: "Git Workflow Best Practices"
date: 2024-01-01 12:00:00 +0800
categories: [Git, Tools]
tags: [git, workflow, best-practices]
---

## Why Git Workflow is Needed

Git workflow is the foundation of team collaboration...

## Common Git Workflows

### Git Flow

Git Flow is the most classic workflow...
```

### 12.2 GitHub Pages + Hugo

**Creating a Hugo blog**:
```bash
# Create new site
hugo new site blog
cd blog

# Install theme
git init
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

# Create post
hugo new posts/my-first-post.md
```

**Configuration file (hugo.toml)**:
```toml
baseURL = 'https://username.github.io/blog/'
languageCode = 'zh-CN'
title = 'My Tech Blog'
theme = 'PaperMod'

[params]
  author = "Your Name"
  description = "Sharing technical insights"
  defaultTheme = "auto"
  ShowReadingTime = true
  ShowShareButtons = true

[[menu.main]]
  name = "Home"
  url = "/"
  weight = 1

[[menu.main]]
  name = "Posts"
  url = "/posts/"
  weight = 2

[[menu.main]]
  name = "Tags"
  url = "/tags/"
  weight = 3

[[menu.main]]
  name = "About"
  url = "/about/"
  weight = 4
```

### 12.3 GitHub Actions Auto-deployment

**Jekyll deployment**:
```yaml
name: Deploy Jekyll

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      
      - name: Build
        run: bundle exec jekyll build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./_site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

**Hugo deployment**:
```yaml
name: Deploy Hugo

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0
      
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      
      - name: Build
        run: hugo --minify
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### 12.4 Technical Blog Writing Tips

**Article structure**:
```markdown
# Title

## Overview
Brief introduction to article content (2-3 sentences)

## Prerequisites
List what readers need to know

## Main Content
Step-by-step explanation with code examples

## Summary
Review key points, provide next steps

## References
List related links
```

**Code example principles**:
1. Complete and runnable
2. Include comments
3. Highlight key parts
4. Provide link to complete code repository

**SEO optimization**:
- Use descriptive titles
- Add keywords
- Use internal links
- Add image alt text
- Generate sitemap

---

## 13. Documentation Contribution Workflow

### 13.1 Documentation Contribution Flow

```
Fork repository
    ↓
Create branch
    ↓
Edit documentation
    ↓
Local preview
    ↓
Commit changes
    ↓
Create Pull Request
    ↓
Code review
    ↓
Merge and publish
```

### 13.2 Documentation Contribution Guide Template

Create `CONTRIBUTING.md` in the repository:

```markdown
# Contribution Guide

Thank you for contributing to this project!

## How to Contribute Documentation

### 1. Fork Repository

Click the "Fork" button in the upper right corner of the repository.

### 2. Clone Repository

```bash
git clone https://github.com/your-username/project.git
cd project
```

### 3. Create Branch

```bash
git checkout -b docs/your-topic
```

### 4. Edit Documentation

Use your preferred editor to edit the documentation.

### 5. Local Preview

```bash
# Install dependencies
npm install

# Local preview
npm run docs:dev
```

### 6. Commit Changes

```bash
git add .
git commit -m "docs: describe your changes"
```

### 7. Push and Create PR

```bash
git push origin docs/your-topic
```

Then create a Pull Request on GitHub.

## Documentation Standards

- Write in Chinese
- Follow [Chinese Technical Documentation Typesetting Standards](#chinese-technical-documentation-typesetting-standards)
- Code examples must be runnable
- Images should be stored in the `docs/assets` directory

## Feedback

If you have any questions, please ask in Discussions.
```

### 13.3 Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE/docs.md`:

```markdown
## Documentation Change Type

- [ ] New documentation
- [ ] Fix errors
- [ ] Update content
- [ ] Translation

## Changes

<!-- Describe your changes -->

## Related Issues

<!-- Related Issue number -->

## Checklist

- [ ] Documentation format is correct
- [ ] Code examples are runnable
- [ ] Links are valid
- [ ] Images display correctly
- [ ] Necessary explanations have been added

## Screenshots (if applicable)

<!-- Add screenshots -->
```

### 13.4 Code Review Best Practices

**As a reviewer**:
1. Check technical accuracy
2. Verify code examples
3. Check formatting and style
4. Provide constructive feedback
5. Respond promptly

**As a contributor**:
1. Preview changes
2. Self-check
3. Respond to review comments
4. Be patient
5. Learn and improve

### 13.5 Automated Contribution Pipeline

**GitHub Actions automated checks**:
```yaml
name: PR Docs Check

on:
  pull_request:
    paths:
      - 'docs/**'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check markdown
        uses: avto-dev/markdown-lint@v1
      
      - name: Check links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
      
      - name: Build preview
        run: |
          npm ci
          npm run docs:build
      
      - name: Comment preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '✅ Documentation preview build successful!'
            })
```

---

## 14. Chinese-English Mixed Typesetting Best Practices

Chinese-English mixed typesetting is one of the most common typesetting challenges in Chinese technical documentation. Since the technical field extensively uses English terms, how to properly handle English content in Chinese documents directly affects the professionalism and readability of the documentation.

### 14.1 Basic Rules

**Add space between Chinese and English**:
This is the most fundamental rule of Chinese-English mixed typesetting. A half-width space should be added between Chinese and English characters and numbers, which improves reading experience and avoids character sticking.

```markdown
# Recommended
使用 GitHub 进行版本控制
安装 Node.js 依赖
项目有 100 个 Star

# Not recommended
使用GitHub进行版本控制
安装Node.js依赖
项目有100个Star
```

Adding spaces is not just for aesthetics, but to improve readability. When English words are adjacent to Chinese characters, readers' eyes need to quickly switch language contexts, and spaces provide a visual buffer.

**Add space between numbers and Chinese**:
Spaces should also be added between numbers and Chinese characters, making numbers more prominent and easier to read.

```markdown
# Recommended
仓库有 100 个星标
3 个提交记录
版本号为 2.0.1

# Not recommended
仓库有100个星标
3个提交记录
版本号为2.0.1
```

**Full-width vs half-width punctuation**:
In Chinese context, use full-width punctuation; in English context, use half-width punctuation.

```markdown
# Recommended
这是一个示例，演示如何使用 GitHub。
请运行 `npm install` 命令。

# Not recommended
这是一个示例,演示如何使用GitHub.
请运行 `npm install` 命令
```

### 14.2 Punctuation Usage Standards

**Chinese punctuation**:
- Comma: ，(full-width)
- Period: 。(full-width)
- Colon: ：(full-width)
- Semicolon: ；(full-width)
- Question mark: ？(full-width)
- Exclamation mark: ！(full-width)
- Quotes: "" (full-width)
- Parentheses: （）(full-width)

**English punctuation**:
- Comma: , (half-width)
- Period: . (half-width)
- Colon: : (half-width)
- Semicolon: ; (half-width)
- Question mark: ? (half-width)
- Exclamation mark: ! (half-width)
- Quotes: "" (half-width)
- Parentheses: () (half-width)

**Mixed usage rules**:
When a sentence is primarily Chinese with English words or code, use Chinese punctuation:
```markdown
运行 `git commit` 命令，提交你的更改。
```

When a sentence is primarily English with Chinese explanations, use English punctuation:
```markdown
Use `git commit` to commit your changes.
```

### 14.3 Proper Noun Handling

**Keep as-is, do not translate**:
Technical proper nouns should remain in English and should not be translated. This is because:
1. Chinese translations of proper nouns may not be consistent
2. Developers are more familiar with the English terms
3. Easier to search and communicate

```markdown
# Recommended
使用 GitHub Actions 进行 CI/CD
配置 Docker 容器
运行 Kubernetes 集群

# Not recommended
使用 GitHub 动作进行持续集成/持续部署
配置 Docker 容器
运行 Kubernetes 集群
```

**Add annotations on first occurrence**:
For less common proper nouns, you can add Chinese annotations on first occurrence to help readers understand.

```markdown
持续集成（Continuous Integration，CI）is a development practice that requires developers to frequently integrate code into a shared repository.
```

**Common technical terminology reference table**:

| English Term | Chinese Term | Recommendation |
|--------------|--------------|----------------|
| Repository | 仓库 | English or Chinese |
| Branch | 分支 | English or Chinese |
| Pull Request | 拉取请求 | English (PR) |
| Issue | 问题/议题 | English |
| Fork | 复刻 | English |
| Clone | 克隆 | English |
| Commit | 提交 | English or Chinese |
| Push | 推送 | English or Chinese |
| Merge | 合并 | English or Chinese |
| Deploy | 部署 | Chinese |
| Build | 构建 | Chinese |
| Test | 测试 | Chinese |
| Debug | 调试 | Chinese |
| API | 接口 | English |
| SDK | 开发工具包 | English |
| IDE | 集成开发环境 | English |
| CLI | 命令行界面 | English |
| GUI | 图形用户界面 | English |
| URL | 网址 | English |
| HTTP | 超文本传输协议 | English |
| JSON | JavaScript 对象表示法 | English |
| YAML | YAML 格式 | English |
| Markdown | Markdown 格式 | English |
| Docker | Docker 容器 | English |
| Kubernetes | K8s | English |
| Git | Git 版本控制 | English |
| Node.js | Node.js 运行时 | English |
| React | React 框架 | English |
| Vue | Vue 框架 | English |
| Angular | Angular 框架 | English |
| TypeScript | TypeScript 语言 | English |
| JavaScript | JavaScript 语言 | English |
| Python | Python 语言 | English |
| Java | Java 语言 | English |
| Go | Go 语言 | English |
| Rust | Rust 语言 | English |

### 14.4 Code and Command Handling

**Use English punctuation in code**:
In code blocks or inline code, always use English punctuation.

```markdown
# Recommended
运行 `git commit -m "message"` 提交更改。
配置文件路径为 `/etc/config.yml`。

# Not recommended
运行 `git commit -m "message"` 提交更改。
配置文件路径为 `/etc/config.yml`。
```

**Use Chinese punctuation for command descriptions**:
When describing commands or code in Chinese, use Chinese punctuation.

```markdown
# Recommended
这个命令用于提交更改。参数 `-m` 用于指定提交信息。

# Not recommended
这个命令用于提交更改.参数 `-m` 用于指定提交信息.
```

**Language choice for code comments**:
Choose comment language based on project audience:
- For international developers: use English comments
- For Chinese developers: can use Chinese comments
- For open source projects: recommend English comments

```python
# English comments (for international developers)
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

# Chinese comments (for Chinese developers)
def calculate_sum(a, b):
    """计算两个数的和。"""
    return a + b
```

### 14.5 Typesetting Tool Recommendations

**Chinese typesetting check tools**:

1. **pangu.js**: Automatically add spaces between Chinese and English
   ```bash
   npm install -g pangu
   pangu --help
   ```

2. **lint-md**: Chinese Markdown typesetting check
   ```bash
   npm install -g lint-md
   lint-md docs/**/*.md
   ```

3. **zhlint**: Chinese typesetting formatting tool
   ```bash
   npm install -g zhlint
   zhlint --fix docs/**/*.md
   ```

**VS Code plugins**:
1. **Chinese Typography**: Automatically handle Chinese-English spacing
2. **Markdown Lint**: Markdown format checking
3. **Pangu Mark**: Automatically add Chinese-English spacing

**GitHub Actions integration**:
```yaml
name: Lint Markdown

on:
  push:
    paths:
      - '**/*.md'
  pull_request:
    paths:
      - '**/*.md'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run lint-md
        run: |
          npm install -g lint-md
          lint-md docs/**/*.md --config .lintmdrc.json
```

**lint-md configuration file (.lintmdrc.json)**:
```json
{
  "rules": {
    "no-empty-code": true,
    "no-empty-blockquote": true,
    "no-empty-list": true,
    "no-fullwidth-number": true,
    "no-space-in-inline-code": true,
    "no-trailing-punctuation": true,
    "no-long-code": {
      "length": 100,
      "exclude": ["code"]
    },
    "space-round-number": true,
    "space-round-letter": true,
    "space-round-alphabet": true
  }
}
```

### 14.6 Common Error Examples

| Error Type | Incorrect Example | Correct Example | Description |
|------------|-------------------|-----------------|-------------|
| Missing space | 使用GitHub进行版本控制 | 使用 GitHub 进行版本控制 | Add space between Chinese and English |
| Punctuation error | 这是示例. | 这是示例。 | Use full-width punctuation in Chinese context |
| Code punctuation | 运行 `npm install`。 | 运行 `npm install`。 | Use half-width punctuation in code |
| Over-translation | 拉取请求 | Pull Request | Keep proper nouns as-is |
| Format confusion | 运行`npm install`命令 | 运行 `npm install` 命令 | Add space before and after code |
| Number format | 仓库有100个星标 | 仓库有 100 个星标 | Add space before and after numbers |
| Mixed punctuation | 使用GitHub,进行版本控制 | 使用 GitHub，进行版本控制 | Use consistent full-width punctuation |
| Missing annotation | 使用 CI/CD | 使用 CI/CD（持续集成/持续部署） | Add annotation on first occurrence |

### 14.7 Typesetting Checklist

Before publishing documentation, use the following checklist:

**Basic format check**:
- [ ] Is there space between Chinese and English
- [ ] Is there space between numbers and Chinese
- [ ] Are punctuation marks correct (full-width/half-width)
- [ ] Are code block punctuation marks half-width
- [ ] Are proper nouns kept as-is

**Content check**:
- [ ] Is terminology usage consistent
- [ ] Are links valid
- [ ] Do images display correctly
- [ ] Are code examples runnable
- [ ] Are there any spelling errors

**Readability check**:
- [ ] Are paragraphs too long
- [ ] Are heading levels reasonable
- [ ] Are lists used appropriately
- [ ] Are there enough examples
- [ ] Are there necessary explanations

**Internationalization check**:
- [ ] Does English content need translation
- [ ] Do Chinese annotations need to be added
- [ ] Are the needs of readers from different language backgrounds considered
- [ ] Are multilingual versions provided

### 14.8 Best Practices Summary

**Core principles**:
1. **Consistency**: Maintain consistent typesetting style throughout the document
2. **Readability**: Typesetting should serve the content and improve reading experience
3. **Professionalism**: Technical documentation should reflect professional standards
4. **Internationalization**: Consider the needs of readers from different language backgrounds

**Specific recommendations**:
1. Create project typesetting standards documentation
2. Use automated tools to check typesetting
3. Pay attention to typesetting issues during code reviews
4. Regularly update typesetting standards
5. Collect reader feedback and improve

**Common questions**:

**Q**: Is it necessary to add spaces between Chinese and English?
**A**: Yes, this is a fundamental rule of Chinese-English mixed typesetting. Adding spaces improves readability and avoids character sticking.

**Q**: What punctuation should be used in Chinese comments in code?
**A**: Code comments usually use English punctuation because code editors and IDEs have better support for English punctuation. However, if the project is specifically targeted at Chinese developers, Chinese punctuation can also be used.

**Q**: Should proper nouns be translated?
**A**: Generally, no. Technical proper nouns should remain in English for easier communication and searching. You can add Chinese annotations on first occurrence.

**Q**: How to handle titles that mix Chinese and English?
**A**: Keep English proper nouns as-is in titles, and use Chinese for other parts. For example: "GitHub Actions 使用指南".

**Q**: Should numbers in documentation use Arabic or Chinese numerals?
**A**: Generally use Arabic numerals for easier reading. For example: "3 个步骤" instead of "三个步骤".

---

## 15. Technical Documentation Project in Practice

Technical documentation is not just an accessory to code; it is the bridge between developers and users. An excellent technical documentation project requires systematic planning, continuous maintenance, and constant optimization. This chapter will walk you through building a complete technical documentation system from scratch using practical examples.

### 15.1 Creating Project Documentation from Scratch

Assuming you are developing a command-line tool called `awesome-cli` and need to create a complete documentation system for it. We will go through the entire process step by step, from documentation planning to content writing to deployment.

**Step 1: Plan the documentation structure**

A good documentation structure is half the success. Before starting to write, carefully plan how the documentation will be organized:

```
awesome-cli-docs/
├── docs/
│   ├── index.md                 # Homepage
│   ├── getting-started.md       # Quick start
│   ├── installation.md          # Installation guide
│   ├── configuration.md         # Configuration guide
│   ├── commands/                # Command reference
│   │   ├── init.md
│   │   ├── build.md
│   │   └── deploy.md
│   ├── guides/                  # User guides
│   │   ├── basic-usage.md
│   │   ├── advanced-usage.md
│   │   └── best-practices.md
│   ├── api/                     # API documentation
│   │   ├── overview.md
│   │   └── reference.md
│   ├── faq.md                   # FAQ
│   └── changelog.md             # Changelog
├── mkdocs.yml
└── README.md
```

**Step 2: Write the homepage content**

The homepage is the first impression users get of the documentation, so it should introduce the project clearly and concisely:

```markdown
# Awesome CLI Documentation

Welcome to Awesome CLI! This is a powerful command-line tool that helps you quickly build and deploy applications.

## Features

- **Fast Build**: One-click project build, supporting multiple frameworks
- **Smart Deploy**: Auto-detect environment, one-click deploy to cloud
- **Plugin System**: Rich plugin ecosystem, unlimited extensibility
- **Cross-platform Support**: Supports Windows, macOS, and Linux

## Quick Start

```bash
# Install
npm install -g awesome-cli

# Initialize project
awesome-cli init my-project

# Build project
awesome-cli build

# Deploy project
awesome-cli deploy
```

## Get Help

- [Quick Start Guide](getting-started.md)
- [Command Reference](commands/init.md)
- [FAQ](faq.md)
- [GitHub Issues](https://github.com/your-username/awesome-cli/issues)
```

**Step 3: Write the quick start guide**

The quick start guide should help beginners get started within 5 minutes:

```markdown
# Quick Start

This guide will help you understand the basic usage of Awesome CLI in 5 minutes.

## Prerequisites

- Node.js 18 or higher
- npm 9 or higher
- Git

## Installation

Install globally using npm:

```bash
npm install -g awesome-cli
```

Verify installation:

```bash
awesome-cli --version
# Output: awesome-cli v1.0.0
```

## Create Your First Project

```bash
# Initialize project
awesome-cli init my-first-project

# Enter project directory
cd my-first-project

# View project structure
ls -la
```

The project structure is as follows:

```
my-first-project/
├── src/
│   └── index.js
├── tests/
│   └── index.test.js
├── package.json
├── awesome.config.js
└── README.md
```

## Build Project

```bash
awesome-cli build
```

After the build is complete, the build output will be generated in the `dist/` directory.

## Deploy Project

```bash
awesome-cli deploy
```

Follow the prompts to select a deployment environment and complete the deployment.

## Next Steps

- [Configuration Guide](configuration.md) - Learn how to configure the project
- [Command Reference](commands/init.md) - View all available commands
- [User Guide](guides/basic-usage.md) - Learn more about usage methods
```

### 15.2 Documentation Maintenance Workflow

Establish a workflow that keeps documentation in sync with code updates, ensuring documentation always stays consistent with code:

**GitHub Actions configuration**:
```yaml
name: Docs Update Reminder

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!docs/**'

jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - name: Check if docs need update
        uses: actions/github-script@v7
        with:
          script: |
            const { data: prs } = await github.rest.pulls.list({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'closed',
              sort: 'updated',
              direction: 'desc',
              per_page: 1
            });
            
            if (prs.length > 0) {
              const pr = prs[0];
              const { data: files } = await github.rest.pulls.listFiles({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: pr.number
              });
              
              const hasCodeChanges = files.some(f => 
                f.filename.startsWith('src/') && 
                !f.filename.startsWith('docs/')
              );
              
              if (hasCodeChanges) {
                await github.rest.issues.create({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  title: 'Reminder: Code changed, check if docs need updating',
                  body: `PR #${pr.number} modified code but did not update documentation.\n\nPlease check if the following need updating:\n- API documentation\n- Command reference\n- Configuration guide\n- Usage examples`,
                  labels: ['documentation']
                });
              }
            }
```

### 15.3 Documentation Quality Metrics

Establish a documentation quality assessment system to quantify documentation quality:

| Metric | Description | Target Value |
|--------|-------------|--------------|
| Coverage | Percentage of documented features | > 90% |
| Accuracy | Consistency between docs and actual functionality | 100% |
| Timeliness | Last documentation update time | < 30 days |
| Readability | Reading difficulty score | Below medium |
| Completeness | Completeness of required sections | 100% |
| Link validity | Percentage of valid links | > 95% |

**Automated check script**:
```bash
#!/bin/bash
# docs-quality-check.sh

echo "=== Documentation Quality Check Report ==="
echo ""

# Check file count
TOTAL_FILES=$(find docs -name "*.md" | wc -l)
echo "Total documentation files: $TOTAL_FILES"

# Check file size
TOTAL_SIZE=$(find docs -name "*.md" -exec wc -c {} + | tail -1 | awk '{print $1}')
echo "Total documentation size: $TOTAL_SIZE bytes"

# Check link validity
echo ""
echo "Checking link validity..."
broken_links=0
for file in docs/**/*.md; do
  while IFS= read -r line; do
    if [[ $line =~ \[.*\]\((http[s]?://[^)]+)\) ]]; then
      url="${BASH_REMATCH[1]}"
      status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
      if [ "$status" != "200" ]; then
        echo "  Broken link: $url (in $file)"
        ((broken_links++))
      fi
    fi
  done < "$file"
done
echo "Broken link count: $broken_links"

# Check code blocks
echo ""
echo "Checking code blocks..."
code_blocks=$(grep -r '```' docs --count | awk -F: '{sum+=$2} END {print sum}')
echo "Total code blocks: $((code_blocks / 2))"

echo ""
echo "=== Check complete ==="
```

### 15.4 Documentation Internationalization in Practice

Complete process for adding multilingual support to a project:

**Step 1: Extract translatable content**

```bash
# Use Docusaurus to extract translation strings
npm run write-translations -- --locale zh-Hans
```

**Step 2: Translate content files**

Directory structure:
```
i18n/
├── zh-Hans/
│   ├── docusaurus-plugin-content-docs/
│   │   └── current/
│   │       ├── getting-started.md
│   │       └── commands/
│   │           └── init.md
│   └── docusaurus-theme-classic/
│       ├── navbar.json
│       └── footer.json
└── en/
    └── docusaurus-plugin-content-docs/
        └── current/
            └── getting-started.md
```

**Step 3: Configure language switching**

```javascript
// docusaurus.config.js
module.exports = {
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en'],
    localeConfigs: {
      'zh-Hans': {
        label: '简体中文',
        direction: 'ltr',
        htmlLang: 'zh-Hans',
      },
      en: {
        label: 'English',
        direction: 'ltr',
        htmlLang: 'en-US',
      },
    },
  },
};
```

**Step 4: Automate translation workflow**

```yaml
# .github/workflows/translate.yml
name: Translation Sync

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - '!i18n/**'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect changes
        id: changes
        run: |
          git diff HEAD~1 --name-only | grep -v i18n | grep docs > changed_files.txt
          if [ -s changed_files.txt ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi
      
      - name: Create issue
        if: steps.changes.outputs.has_changes == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const changedFiles = fs.readFileSync('changed_files.txt', 'utf8');
            
            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Translation reminder: Documentation content updated',
              body: `The following documentation has been updated, please sync translations:\n\n\`\`\`\n${changedFiles}\n\`\`\`\n\nPlease update the corresponding translation files.`,
              labels: ['translation']
            });
```

### 15.5 Documentation Search Optimization

Tips to improve documentation search experience:

**Local search configuration (MkDocs)**:
```yaml
# mkdocs.yml
plugins:
  - search:
      lang: zh
      separator: '[\s\-\.]+'
```

**Algolia DocSearch integration**:
```javascript
// docusaurus.config.js
module.exports = {
  themeConfig: {
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'your-index',
      contextualSearch: true,
      searchPagePath: 'search',
    },
  },
};
```

**Search optimization recommendations**:
1. Add descriptive titles to each page
2. Use keyword-rich section headings
3. Add metadata descriptions
4. Establish clear documentation hierarchy
5. Use tags to categorize content

### 15.6 Documentation Performance Optimization

Performance optimization for large documentation sites:

**Image optimization**:
```markdown
<!-- Use WebP format -->
![Example image](./assets/example.webp)

<!-- Add size attributes -->
<img src="./assets/example.png" width="600" height="400" alt="Example image">

<!-- Use lazy loading -->
<img src="./assets/example.png" loading="lazy" alt="Example image">
```

**Code block optimization**:
```markdown
<!-- Show only key code -->
```python
# Key section
def important_function():
    pass
```

<!-- Put complete code in collapsible area -->
<details>
<summary>View complete code</summary>

```python
# Complete implementation
def important_function():
    # ... 100 lines of code
    pass
```

</details>
```

**Build optimization**:
```yaml
# GitHub Actions cache configuration
- name: Cache docs
  uses: actions/cache@v4
  with:
    path: |
      docs/.cache
      node_modules
    key: docs-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      docs-
```

### 15.7 Documentation Automated Testing

Code examples in documentation may break due to various reasons, such as API changes, dependency version updates, or environment differences. Establishing an automated testing mechanism can help discover and fix these issues in a timely manner, ensuring the accuracy and reliability of documentation.

**Testing strategy**:
1. Code block testing: Extract and execute code blocks from documentation
2. Link checking: Verify all external links are valid and accessible
3. Spell checking: Check for spelling errors and formatting issues in documentation
4. Format checking: Verify documentation format meets standards

**Complete testing pipeline**:
```yaml
# .github/workflows/docs-test.yml
name: Docs Testing

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Check markdown format
        run: |
          npm install -g markdownlint-cli
          markdownlint docs/**/*.md
      
      - name: Check links
        run: |
          npm install -g markdown-link-check
          find docs -name "*.md" -exec markdown-link-check {} \;
      
      - name: Spell check
        run: |
          npm install -g cspell
          cspell "docs/**/*.md"
      
      - name: Build docs
        run: npm run docs:build
```

### 15.8 Documentation Contribution Guide

Establish clear documentation contribution guidelines for the project to encourage community participation in documentation improvement. Good contribution guidelines can lower the barrier to participation and improve documentation quality:

```markdown
# Documentation Contribution Guide

Thank you for contributing to this project's documentation! Below are guidelines for participating in documentation improvement.

## How to Contribute

### Report Issues

If you find errors or unclear content in the documentation, please provide feedback through the following methods:
- Create a new issue in GitHub Issues
- Use the "Documentation Issue" label
- Describe the issue and suggested improvements in detail

### Submit Modifications

1. Fork the project repository to your account
2. Create a documentation branch: `git checkout -b docs/your-topic`
3. Modify documentation content and ensure correct formatting
4. Preview locally to confirm everything is correct, then commit
5. Create a Pull Request and describe the changes

### Documentation Standards

- Write in Chinese, keep the language concise and clear
- Follow Chinese-English mixed typesetting standards
- Code examples must be runnable and include comments
- Images should be stored in the `docs/assets` directory
- Add necessary comments and explanations

## Documentation Structure

```
docs/
├── index.md           # Homepage introduction
├── getting-started.md # Quick start guide
├── guides/            # Detailed user guides
├── api/               # API reference documentation
└── faq.md             # Frequently asked questions
```

## Local Development

```bash
# Install project dependencies
npm install

# Start local preview server
npm run docs:dev

# Build production documentation
npm run docs:build
```

## Contact

If you have any questions, please ask and discuss in GitHub Discussions.
```

---

## Appendix A: Recommended Tools List

| Category | Tool | Purpose |
|----------|------|---------|
| Editor | VS Code | Code and documentation editing |
| Editor | Typora | Markdown editing |
| Doc generation | MkDocs | Project documentation |
| Doc generation | Docusaurus | Open source project documentation |
| Doc generation | VitePress | Vue ecosystem documentation |
| Doc generation | Hugo | Blogs and documentation |
| API docs | Swagger UI | REST API documentation |
| API docs | Redoc | Beautiful API documentation |
| Typesetting check | lint-md | Chinese typesetting check |
| Typesetting check | zhlint | Chinese formatting |
| Link check | markdown-link-check | Link validity check |
| Spell check | cspell | Spell checking |
| Translation management | Crowdin | Multilingual translation platform |
| Version management | mike | MkDocs version management |

## Appendix B: Recommended Reading

- [Google Technical Writing Courses](https://developers.google.com/tech-writing)
- [Markdown Style Guide](https://www.markdownguide.org/)
- [Chinese Copywriting Guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Docusaurus Documentation](https://docusaurus.io/)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Hugo Documentation](https://gohugo.io/)

---

**Last Updated**: December 2024

**License**: This document is published under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

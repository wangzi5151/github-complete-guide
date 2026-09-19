# GitHub API and Webhooks Complete Guide

## Chapter 1: GitHub API Overview

### 1.1 REST API and GraphQL API Introduction

GitHub provides two API styles for developers: REST API and GraphQL API. Each API has its characteristics, suitable for different use scenarios. Understanding their differences and applicable scenarios is crucial for choosing the right API.

**REST API** is the earliest API style provided by GitHub, following RESTful architecture design principles. It uses multiple endpoints to access different resources, each endpoint corresponding to a specific URL. REST API uses standard HTTP methods (GET, POST, PATCH, PUT, DELETE) to perform different operations, and HTTP status codes to indicate operation results.

**GraphQL API** is the API style launched by GitHub in 2016, developed by Facebook. It uses a single endpoint (/graphql) to access all resources, and clients can precisely specify which data fields to fetch. GraphQL API uses query language to describe data requirements, can fetch multiple related resources in one request.

### 1.2 REST API vs GraphQL API Comparison

| Feature | REST API | GraphQL API |
|---------|----------|-------------|
| Query Method | Multiple endpoints | Single endpoint |
| Data Fetching | Fixed structure | On-demand fetching |
| Over-fetching | Possible | Not possible |
| Learning Difficulty | Low | Medium |
| Version Management | Simple | Built-in |
| Cache Support | Good | Needs additional configuration |
| Real-time Updates | Needs polling | Supports subscriptions |

**REST API Advantages**:
- Low learning curve, easy to get started
- Uses standard HTTP protocol, wide tool support
- Perfect cache mechanism, excellent performance
- Rich documentation, strong community support

**GraphQL API Advantages**:
- Precisely fetch needed data, avoid over-fetching
- Get multiple related resources in one request
- Strong type system, reduces errors
- Supports real-time subscriptions

### 1.3 API Version Control

GitHub API uses version control to manage API evolution:

```bash
# REST API version (via Accept header)
curl -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/octocat/Hello-World

# Specify API version
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/octocat/Hello-World

# Use preview features
curl -H "Accept: application/vnd.github.antiope-preview+json" \
  https://api.github.com/repos/octocat/Hello-World/check-runs
```

### 1.4 API Endpoint Structure

REST API endpoint structure follows this pattern:

```
https://api.github.com/{resource}
```

Common resource paths:
- `/users/{username}`: User information
- `/repos/{owner}/{repo}`: Repository information
- `/repos/{owner}/{repo}/issues`: Issue list
- `/repos/{owner}/{repo}/pulls`: Pull Request list
- `/repos/{owner}/{repo}/releases`: Release list
- `/orgs/{org}`: Organization information
- `/orgs/{org}/teams`: Team list

## Chapter 2: REST API Basic Usage

REST API is GitHub's most commonly used API style. This chapter will introduce in detail REST API's basic usage, including getting resources, creating resources, updating resources and deleting resources. Through this chapter's learning, developers can master basic skills of using REST API to interact with GitHub.

### 2.1 Get Repository Information

Getting repository information is one of the most common API calls. Through REST API, developers can get repository's detailed information, including repository name, description, star count, branch list, etc. This information can be used to build various tools and integration applications.

```bash
# Using curl
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/octocat/Hello-World

# Using gh CLI
gh api repos/octocat/Hello-World

# Using Python
import requests

response = requests.get(
    'https://api.github.com/repos/octocat/Hello-World',
    headers={'Authorization': 'token YOUR_TOKEN'}
)
repo = response.json()
print(f"Stars: {repo['stargazers_count']}")
```

### 2.2 Response Format

GitHub API returns JSON format response data. Response data contains resource's detailed information, developers can parse and use this information as needed. Understanding response data structure is crucial for correctly using API. Here is the repository information API's response example, containing commonly used fields.

```json
{
  "id": 1296269,
  "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
  "name": "Hello-World",
  "full_name": "octocat/Hello-World",
  "private": false,
  "owner": {
    "login": "octocat",
    "id": 583231,
    "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4"
  },
  "html_url": "https://github.com/octocat/Hello-World",
  "description": "This your first repo!",
  "fork": false,
  "stargazers_count": 2500,
  "watchers_count": 2500,
  "forks_count": 1500,
  "open_issues_count": 5,
  "default_branch": "main",
  "created_at": "2011-01-26T19:01:12Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### 2.3 Pagination

When returning results are many, GitHub API uses pagination mechanism. By default, each page returns 30 records, maximum can be set to 100. Developers need to understand pagination mechanism to fetch all data. GitHub API includes pagination information in response headers, developers can use this information to get next page data.

```bash
# REST API pagination
# First page
curl "https://api.github.com/repos/octocat/Hello-World/issues?page=1&per_page=100"

# Response header contains Link
# Link: <https://api.github.com/repos/octocat/Hello-World/issues?page=2>; rel="next",
#        <https://api.github.com/repos/octocat/Hello-World/issues?page=5>; rel="last"

# Use gh CLI to auto-handle pagination
gh api repos/octocat/Hello-World/issues --paginate

# Python pagination handling
import requests

def get_all_issues(owner, repo):
    issues = []
    page = 1
    while True:
        response = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/issues',
            params={'page': page, 'per_page': 100},
            headers={'Authorization': 'token YOUR_TOKEN'}
        )
        page_issues = response.json()
        if not page_issues:
            break
        issues.extend(page_issues)
        page += 1
    return issues
```

### 2.4 Filtering and Sorting

GitHub API supports rich filtering and sorting parameters, helping developers precisely fetch needed data. By using these parameters, can reduce unnecessary data transfer, improve API call efficiency. Different API endpoints support different filtering and sorting parameters, developers should check API documentation for specific supported parameters.

```bash
# Filter Issues
curl "https://api.github.com/repos/octocat/Hello-World/issues?state=open&labels=bug&sort=created&direction=desc"

# Filter PRs
curl "https://api.github.com/repos/octocat/Hello-World/pulls?state=open&base=main&head=octocat:feature"

# Search
curl "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc"

# Search Issues
curl "https://api.github.com/search/issues?q=repo:octocat/Hello-World+is:issue+is:open"
```

### 2.5 Create and Update Resources

Besides getting data, REST API can also be used to create and update resources. By sending POST, PATCH, PUT or DELETE requests, developers can manage various resources on GitHub. When creating and updating resources, need to provide corresponding data in request body. Here are the creating and updating Issues, comments and other resources examples.

```bash
# Create Issue
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/octocat/Hello-World/issues \
  -d '{"title":"Bug Report","body":"Description of the bug"}'

# Update Issue
curl -X PATCH \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/octocat/Hello-World/issues/1 \
  -d '{"state":"closed"}'

# Add comment
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/octocat/Hello-World/issues/1/comments \
  -d '{"body":"This is a comment"}'
```

## Chapter 3: Authentication Methods

Authentication is prerequisite for accessing GitHub API. GitHub supports various authentication methods, each suitable for different scenarios. Choosing appropriate authentication method is important for both security and convenience. This chapter will introduce in detail various authentication methods' characteristics and usage.

### 3.1 Personal Access Token (PAT)

Personal Access Token (PAT) is the simplest authentication method, suitable for personal scripts and CI/CD processes. PAT can replace password usage, provides same access permissions as password. Developers should create different PATs for different purposes, and set reasonable expiration time.

```bash
# Create PAT
# Settings → Developer settings → Personal access tokens

# Use PAT authentication
curl -H "Authorization: token ghp_xxxxxxxxxxxx" \
  https://api.github.com/user

# Or use Bearer
curl -H "Authorization: Bearer ghp_xxxxxxxxxxxx" \
  https://api.github.com/user

# gh CLI authentication
gh auth login
gh auth status
```

### 3.2 GitHub App Authentication

GitHub App is a more secure authentication method, suitable for integration applications and automation tools. GitHub App uses JWT (JSON Web Token) for authentication, token has short validity period (1 hour), higher security. GitHub App can be installed on repositories or organizations, with fine-grained permission control. Here is the using Python to implement GitHub App authentication example code.

```python
import jwt
import time
import requests

class GitHubApp:
    def __init__(self, app_id, private_key_path):
        self.app_id = app_id
        with open(private_key_path, 'r') as f:
            self.private_key = f.read()
    
    def get_jwt(self):
        now = int(time.time())
        payload = {
            'iat': now - 60,
            'exp': now + 600,
            'iss': self.app_id
        }
        return jwt.encode(payload, self.private_key, algorithm='RS256')
    
    def get_installation_token(self, installation_id):
        jwt_token = self.get_jwt()
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.post(
            f'https://api.github.com/app/installations/{installation_id}/access_tokens',
            headers=headers
        )
        return response.json()['token']
```

### 3.3 OAuth App Authentication

OAuth App is suitable for applications needing user authorization. Through OAuth flow, users can authorize applications to access specific resources of their GitHub account, without sharing passwords. OAuth App's authorization flow includes user authorization, getting authorization code, exchanging for access token, etc. Here is the OAuth authentication flow detailed explanation.

```bash
# 1. Create OAuth App
# Settings → Developer settings → OAuth Apps → New OAuth App

# 2. Get authorization code
# Redirect user to:
https://github.com/login/oauth/authorize?client_id=CLIENT_ID&redirect_uri=CALLBACK_URL&scope=repo

# 3. Exchange authorization code for Token
curl -X POST https://github.com/login/oauth/access_token \
  -H "Accept: application/json" \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "code=AUTHORIZATION_CODE"

# 4. Use Token
curl -H "Authorization: token ACCESS_TOKEN" \
  https://api.github.com/user
```

### 3.4 Authentication Method Comparison

Choosing appropriate authentication method requires considering multiple factors, including security, convenience, applicable scenarios, etc. Here is the various authentication methods detailed comparison, helping developers make choices based on actual needs. Generally, personal scripts and CI/CD use PAT, integration applications use GitHub App, third-party applications needing user authorization use OAuth App.

| Method | Applicable Scenario | Expiration | Permission Scope |
|--------|---------------------|------------|------------------|
| PAT | Personal scripts, CI/CD | Configurable expiration | User level |
| GitHub App | Integration applications, bots | 1 hour (renewable) | Installation level |
| OAuth App | Third-party applications | No expiration (revocable) | User authorization |
| GITHUB_TOKEN | GitHub Actions | During task | Repository level |

## Chapter 4: Common API Endpoint Examples

GitHub API provides rich endpoints, covering various GitHub features. This chapter will introduce most commonly used API endpoints, including users, repositories, Issues, Pull Requests, Actions and Releases. Through these examples, developers can quickly get started using GitHub API.

### 4.1 User Related API

User API is used to get user information, user's repositories, user's organizations, etc. Through these APIs, can build user profile pages, analyze user activities, etc. Here are the commonly used user API endpoint examples.

```bash
# Get current user info
gh api user

# Get specific user info
gh api users/{username}

# Get user's repositories
gh api users/{username}/repos

# Get user's organizations
gh api users/{username}/orgs

# Get user's Gists
gh api users/{username}/gists
```

### 4.2 Repository Related API

Repository API is used to manage repositories, including getting repository info, creating repository, deleting repository, getting branch list, etc. These APIs are foundation for building repository management tools. Here are the commonly used repository API endpoint examples.

```bash
# Get repository info
gh api repos/{owner}/{repo}

# Create repository
gh api user/repos -f name="new-repo" -f description="New repository"

# Delete repository
gh api -X DELETE repos/{owner}/{repo}

# Get repository languages
gh api repos/{owner}/{repo}/languages

# Get repository contributors
gh api repos/{owner}/{repo}/contributors

# Get repository tags
gh api repos/{owner}/{repo}/tags

# Get repository branches
gh api repos/{owner}/{repo}/branches
```

### 4.3 Issue Related API

Issue API is used to manage Issues, including creating, updating, closing Issues, and managing labels and comments. Issues are important tools for project management, through APIs can achieve automated Issue management. Here are the commonly used Issue API endpoint examples.

```bash
# List Issues
gh api repos/{owner}/{repo}/issues

# Create Issue
gh api repos/{owner}/{repo}/issues \
  -f title="Bug: Something broken" \
  -f body="Description of the bug" \
  -f 'labels[]="bug"' \
  -f 'assignees[]="username"'

# Update Issue
gh api -X PATCH repos/{owner}/{repo}/issues/{issue_number} \
  -f state="closed"

# Add comment
gh api repos/{owner}/{repo}/issues/{issue_number}/comments \
  -f body="This is a comment"

# Add label
gh api -X POST repos/{owner}/{repo}/issues/{issue_number}/labels \
  -f 'labels[]="enhancement"'

# Remove label
gh api -X DELETE repos/{owner}/{repo}/issues/{issue_number}/labels/{label_name}
```

### 4.4 Pull Request Related API

Pull Request API is used to manage Pull Requests, including creating, reviewing, merging PRs. Pull Requests are core functionality of code collaboration, through APIs can achieve automated code review and merge processes. Here are the commonly used Pull Request API endpoint examples.

```bash
# List PRs
gh api repos/{owner}/{repo}/pulls

# Create PR
gh api repos/{owner}/{repo}/pulls \
  -f title="New feature" \
  -f body="Description" \
  -f head="feature-branch" \
  -f base="main"

# Merge PR
gh api -X PUT repos/{owner}/{repo}/pulls/{pull_number}/merge

# Get PR file changes
gh api repos/{owner}/{repo}/pulls/{pull_number}/files

# Review PR
gh api -X POST repos/{owner}/{repo}/pulls/{pull_number}/reviews \
  -f event="APPROVE" \
  -f body="Looks good!"

# Get PR comments
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments
```

### 4.5 Actions Related API

Actions API is used to manage GitHub Actions, including viewing workflows, triggering runs, downloading logs, etc. Through Actions API, can achieve CI/CD process automation management. Here are the commonly used Actions API endpoint examples.

```bash
# List workflows
gh api repos/{owner}/{repo}/actions/workflows

# Trigger workflow
gh api -X POST repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches \
  -f ref="main"

# Get run list
gh api repos/{owner}/{repo}/actions/runs

# Download logs
gh api repos/{owner}/{repo}/actions/runs/{run_id}/logs

# Get artifacts
gh api repos/{owner}/{repo}/actions/runs/{run_id}/artifacts

# Cancel run
gh api -X POST repos/{owner}/{repo}/actions/runs/{run_id}/cancel
```

### 4.6 Releases Related API

Releases API is used to manage version releases, including creating, editing, deleting Releases, and uploading release assets. Version release is important part of software delivery, through APIs can achieve automated release process. Here are the commonly used Releases API endpoint examples.

```bash
# List Releases
gh api repos/{owner}/{repo}/releases

# Create Release
gh api repos/{owner}/{repo}/releases \
  -f tag_name="v1.0.0" \
  -f name="Release v1.0.0" \
  -f body="Release notes" \
  -f draft=false \
  -f prerelease=false

# Upload Release Asset
gh api repos/{owner}/{repo}/releases/{release_id}/assets \
  -X POST \
  -H "Content-Type: application/zip" \
  --data-binary "@release.zip" \
  -f name="release.zip"

# Delete Release
gh api -X DELETE repos/{owner}/{repo}/releases/{release_id}
```

## Chapter 5: GraphQL API Basics

GraphQL is a query language for APIs, developed and open-sourced by Facebook. GitHub launched GraphQL API in 2016, allowing clients to precisely specify which data to fetch. Compared to REST API, GraphQL API can reduce data transfer volume, improve query efficiency. This chapter will introduce GraphQL API basics and usage methods.

### 5.1 Query Syntax

GraphQL uses query language to describe data requirements. Query is a JSON format string, defining resources and fields to fetch. GraphQL queries support nesting, can fetch multiple related resources in one request. Here are the GraphQL query basic syntax examples.

```graphql
# Basic query
query {
  viewer {
    login
    name
    email
  }
}

# Query with parameters
query {
  repository(owner: "octocat", name: "Hello-World") {
    name
    description
    stargazerCount
    forkCount
  }
}

# Nested query
query {
  repository(owner: "octocat", name: "Hello-World") {
    issues(first: 10, states: OPEN) {
      nodes {
        title
        body
        author {
          login
        }
        createdAt
      }
    }
  }
}
```

### 5.2 Mutation Operations

Besides querying data, GraphQL also supports mutation operations. Mutations are used to create, update or delete resources. Mutation syntax is similar to queries, but uses `mutation` keyword. Here are the GraphQL mutation operation examples.

```graphql
# Create Issue
mutation {
  createIssue(input: {
    repositoryId: "REPO_ID"
    title: "Bug Report"
    body: "Description of the bug"
  }) {
    issue {
      number
      title
      url
    }
  }
}

# Add comment
mutation {
  addComment(input: {
    subjectId: "ISSUE_ID"
    body: "This is a comment"
  }) {
    commentEdge {
      node {
        body
        author {
          login
        }
      }
    }
  }
}
```

### 5.3 Use gh CLI for GraphQL

gh CLI is the simplest way to use GraphQL API. gh CLI has built-in authentication and formatting features, developers can directly use `gh api graphql` command to execute GraphQL queries. Here are the using gh CLI to execute GraphQL query examples.

```bash
# Basic query
gh api graphql -f query='
{
  viewer {
    login
    name
  }
}'

# Query with variables
gh api graphql -f query='
query($repo: String!) {
  repository(owner: "octocat", name: $repo) {
    stargazerCount
  }
}' -f repo="Hello-World"

# Complex query
gh api graphql -f query='
{
  viewer {
    repositories(first: 10, orderBy: {field: STARGAZERS, direction: DESC}) {
      nodes {
        name
        stargazerCount
        primaryLanguage {
          name
        }
      }
    }
  }
}'
```

### 5.4 GraphQL Pagination

GraphQL uses Cursor for pagination. Cursor is an opaque string, identifying position in list. By using cursors, can get next or previous page data. GraphQL's pagination model uses `pageInfo` object to describe pagination state, including whether has next page, whether has previous page, next page cursor, previous page cursor, etc.

```graphql
# Cursor pagination
query {
  repository(owner: "octocat", name: "Hello-World") {
    issues(first: 10, after: "Y3Vyc29yOnYyOpK5MjAyMy0wMS0wMVQwMDowMDowMFo=") {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        title
      }
    }
  }
}
```

### 5.5 GraphQL vs REST Selection Suggestions

Choosing whether to use GraphQL or REST API depends on specific use scenarios. Both API styles have advantages, developers should make choices based on actual needs. Here are the selection suggestions, helping developers make wise decisions.

**Use GraphQL Scenarios**:
- Need to fetch multiple related resources
- Only need partial fields, reduce data transfer
- Mobile applications, bandwidth limited
- Complex nested query requirements

**Use REST Scenarios**:
- Simple CRUD operations
- Need cache support
- File upload/download operations
- Webhook handling

## Chapter 6: Octokit Official SDK Usage

To simplify GitHub API usage, GitHub provides official SDK library Octokit. Octokit supports multiple programming languages, including JavaScript/TypeScript, Python, Go, etc. Using Octokit can avoid manually handling HTTP requests, authentication, pagination and other complex logic, letting developers focus on business logic. This chapter will introduce how to use Octokit to interact with GitHub API.

### 6.1 JavaScript/TypeScript Octokit

JavaScript/TypeScript is one of the most commonly used programming languages, Octokit provides complete JavaScript/TypeScript support. Through npm installing `@octokit/rest` package, can use Octokit in project. Here are the using JavaScript Octokit example code.

```bash
# Install
npm install @octokit/rest
```

```javascript
const { Octokit } = require("@octokit/rest");

// Initialize
const octokit = new Octokit({
  auth: "YOUR_TOKEN"
});

// Get repository info
async function getRepo() {
  const { data } = await octokit.repos.get({
    owner: "octocat",
    repo: "Hello-World"
  });
  console.log(`Stars: ${data.stargazers_count}`);
}

// Create Issue
async function createIssue() {
  const { data } = await octokit.issues.create({
    owner: "octocat",
    repo: "Hello-World",
    title: "Bug Report",
    body: "Description of the bug"
  });
  console.log(`Issue created: ${data.html_url}`);
}

// Use GraphQL
async function getRepoWithGraphQL() {
  const { data } = await octokit.graphql(`
    query {
      repository(owner: "octocat", name: "Hello-World") {
        stargazerCount
        issues(first: 10, states: OPEN) {
          nodes {
            title
          }
        }
      }
    }
  `);
  console.log(data);
}
```

### 6.2 Python PyGithub

Python is the preferred language for data science and automation script development. PyGithub is Python community's most popular GitHub API library, providing complete GitHub API encapsulation. Through pip installing PyGithub, can use in Python projects. Here are the using PyGithub example code.

```bash
# Install
pip install PyGithub
```

```python
from github import Github

# Initialize
g = Github("YOUR_TOKEN")

# Get repository
repo = g.get_repo("octocat/Hello-World")
print(f"Stars: {repo.stargazers_count}")

# Create Issue
issue = repo.create_issue(
    title="Bug Report",
    body="Description of the bug"
)
print(f"Issue created: {issue.html_url}")

# Get Issues
for issue in repo.get_issues(state="open"):
    print(f"#{issue.number}: {issue.title}")

# Create PR
pr = repo.create_pull(
    title="New feature",
    body="Description",
    head="feature-branch",
    base="main"
)
print(f"PR created: {pr.html_url}")
```

### 6.3 Go go-github

Go is a popular language for building high-performance server applications. go-github is Go community's GitHub API library, maintained by Google. go-github provides complete GitHub API encapsulation, supporting type-safe API calls. Here are the using go-github example code.

```go
package main

import (
    "context"
    "fmt"
    "github.com/google/go-github/v58/github"
    "golang.org/x/oauth2"
)

func main() {
    ctx := context.Background()
    ts := oauth2.StaticTokenSource(
        &oauth2.Token{AccessToken: "YOUR_TOKEN"},
    )
    tc := oauth2.NewClient(ctx, ts)
    client := github.NewClient(tc)

    // Get repository
    repo, _, err := client.Repositories.Get(ctx, "octocat", "Hello-World")
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("Stars: %d\n", repo.GetStargazersCount())

    // Create Issue
    issueRequest := &github.IssueRequest{
        Title: github.String("Bug Report"),
        Body:  github.String("Description of the bug"),
    }
    issue, _, err := client.Issues.Create(ctx, "octocat", "Hello-World", issueRequest)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("Issue created: %s\n", issue.GetHTMLURL())
}
```

### 6.4 Using gh CLI

gh CLI is GitHub's official command line tool, the simplest way to use GitHub API. gh CLI has built-in authentication, formatting, pagination features, developers don't need to handle complex API details. Here are the using gh CLI common command examples.

```bash
# Get repository info
gh api repos/{owner}/{repo}

# Create Issue
gh issue create --repo {owner}/{repo} --title "Bug" --body "Description"

# List PRs
gh pr list --repo {owner}/{repo}

# Trigger Action
gh workflow run workflow.yml --ref main

# GraphQL query
gh api graphql -f query='{ viewer { login } }'

# Format output
gh api repos/{owner}/{repo} --jq '.stargazers_count'
```

## Chapter 7: Webhooks Overview and Configuration

Webhook is GitHub's real-time event notification mechanism. By configuring Webhooks, when repository specific events occur, GitHub will send HTTP POST requests to specified URL. Webhook is foundation for building GitHub integration applications, can achieve automated event processing. This chapter will introduce Webhook's basic concepts and configuration methods.

### 7.1 What is Webhook

Webhook is an HTTP callback mechanism, when GitHub repository specific events occur, will send HTTP POST request to pre-configured URL. Compared to traditional polling methods, Webhook provides better real-time and higher efficiency event notification mechanism. Developers can process these events on receiving end, implementing various automation features.

Webhook's working principle: First configure Webhook in GitHub repository, specify URL to receive events and event types to monitor. When repository events occur (like code push, Issue creation, etc.), GitHub will send HTTP POST request to configured URL, request body contains event's detailed information. Receiving server processes request and returns HTTP 200 response, indicating event was successfully processed.

### 7.2 Webhook Advantages

Webhook has several notable advantages over traditional polling methods, making it the preferred solution for building real-time integration applications.

**Real-time**: Immediately notifies after event occurs, no need to wait for polling interval. This is very important for scenarios needing real-time response (like automatic deployment, instant notifications).

**Reduce Polling**: No need to periodically check API, save API call quota. GitHub API has rate limits, using Webhook can avoid unnecessary API calls.

**Save Resources**: Only sends requests when events occur, reduces server load. Polling method needs to periodically send requests, even when no new events will consume resources.

**Automation**: Can trigger automation processes, like deployment, notifications, code review, etc. Webhook is foundation for building CI/CD pipelines and automation tools.

### 7.3 Configure Webhook

Webhook can be configured through GitHub CLI or web interface. When configuring Webhook, need to specify URL to receive events, event types to monitor, content format, etc. Here are the using CLI to create and manage Webhook examples.

```bash
# Create Webhook using CLI
gh api repos/{owner}/{repo}/hooks \
  -X POST \
  -f '{
    "name": "web",
    "active": true,
    "events": ["push", "pull_request", "issues"],
    "config": {
      "url": "https://your-server.com/webhook",
      "content_type": "json",
      "secret": "your-webhook-secret",
      "insecure_ssl": "0"
    }
  }'

# View Webhook list
gh api repos/{owner}/{repo}/hooks

# Update Webhook
gh api -X PATCH repos/{owner}/{repo}/hooks/{hook_id} \
  -f '{
    "active": true,
    "events": ["push", "pull_request"]
  }'

# Delete Webhook
gh api -X DELETE repos/{owner}/{repo}/hooks/{hook_id}
```

### 7.4 Webhook Configuration Options

When configuring Webhook, need to understand each option's meaning and function. Reasonably configuring these options can ensure Webhook works correctly, while ensuring security. Here is the Webhook configuration options detailed explanation.

| Option | Description |
|--------|-------------|
| Payload URL | URL to receive events |
| Content type | application/json or application/x-www-form-urlencoded |
| Secret | Key for verifying signature |
| SSL verification | Whether to verify SSL certificate |
| Active | Whether to enable |
| Events | Trigger event list |

### 7.5 Webhook Event List

GitHub supports various Webhook events, covering various repository activities. Developers can choose to monitor specific event types based on needs. Here are the commonly used Webhook event types and their trigger timing detailed explanation.

| Event | Trigger Timing |
|-------|----------------|
| push | Code pushed to repository |
| pull_request | PR created, updated, merged, closed |
| issues | Issue created, updated, closed, reopened |
| issue_comment | Comment on Issue or PR |
| release | Release published, edited, deleted |
| create | Branch or tag created |
| delete | Branch or tag deleted |
| fork | Repository forked |
| watch | Repository starred |
| workflow_run | GitHub Actions run completed |
| workflow_job | GitHub Actions Job status change |
| check_run | Check Run status change |
| check_suite | Check Suite status change |
| deployment | Deployment created |
| deployment_status | Deployment status change |
| gollum | Wiki page edited |
| member | Collaborator added or removed |
| membership | Team member added or removed |
| organization | Organization settings change |
| page_build | GitHub Pages build completed |
| project | Project created, updated, deleted |
| project_card | Project Card created, updated, deleted |
| project_column | Project Column created, updated, deleted |
| public | Repository changed from private to public |
| pull_request_review | PR review submitted |
| pull_request_review_comment | PR review comment |
| repository | Repository created, deleted, archived |
| status | Commit status change |
| team | Team created, updated, deleted |
| team_add | Team added repository access |

## Chapter 8: Webhook Event Types Details

Each Webhook event type has its specific data structure and trigger conditions. Understanding event's detailed structure is crucial for correctly processing Webhook events. This chapter will introduce in detail several commonly used event types' data structures and processing methods.

### 8.1 Push Event

Push event triggers when code is pushed to repository. This is one of the most commonly used Webhook events, often used to trigger CI/CD pipelines, send notifications, etc. Push event contains pushed branch, commit information, pusher details. Here is the Push event's data structure example.

```json
{
  "ref": "refs/heads/main",
  "before": "0000000000000000000000000000000000000000",
  "after": "1234567890abcdef1234567890abcdef12345678",
  "repository": {
    "id": 1296269,
    "name": "Hello-World",
    "full_name": "octocat/Hello-World"
  },
  "pusher": {
    "name": "octocat",
    "email": "octocat@github.com"
  },
  "commits": [
    {
      "id": "1234567890abcdef1234567890abcdef12345678",
      "message": "Fix bug",
      "timestamp": "2023-01-01T00:00:00Z",
      "author": {
        "name": "octocat",
        "email": "octocat@github.com"
      }
    }
  ]
}
```

### 8.2 Pull Request Event

Pull Request event triggers when PR status changes. PR event's `action` field identifies specific change type, such as `opened` (created), `closed` (closed), `merged` (merged), `reviewed` (reviewed), etc. By monitoring PR events, can achieve automated code review, merge notifications, etc. Here is the PR event's data structure example.

```json
{
  "action": "opened",
  "number": 42,
  "pull_request": {
    "id": 123456,
    "number": 42,
    "title": "New feature",
    "body": "Description of the feature",
    "state": "open",
    "user": {
      "login": "octocat"
    },
    "head": {
      "ref": "feature-branch",
      "sha": "abc123"
    },
    "base": {
      "ref": "main",
      "sha": "def456"
    }
  }
}
```

### 8.3 Issue Event

Issue event triggers when Issue status changes. Issue event's `action` field identifies specific change type, such as `opened` (created), `closed` (closed), `reopened` (reopened), `edited` (edited), etc. By monitoring Issue events, can achieve automated Issue management, notifications, etc. Here is the Issue event's data structure example.

```json
{
  "action": "opened",
  "issue": {
    "id": 123456,
    "number": 1,
    "title": "Bug: Something broken",
    "body": "Description of the bug",
    "state": "open",
    "user": {
      "login": "octocat"
    },
    "labels": [
      {
        "name": "bug",
        "color": "fc2929"
      }
    ]
  }
}
```

### 8.4 Workflow Run Event

Workflow Run event triggers when GitHub Actions run completes. By monitoring Workflow Run events, can achieve CI/CD process monitoring and notifications. For example, when workflow fails send alert notification, when workflow succeeds trigger subsequent process. Here is the Workflow Run event's data structure example.

```json
{
  "action": "completed",
  "workflow_run": {
    "id": 123456,
    "name": "CI",
    "head_branch": "main",
    "head_sha": "abc123",
    "status": "completed",
    "conclusion": "success",
    "workflow_id": 789,
    "run_number": 42,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:05:00Z"
  }
}
```

## Chapter 9: Webhook Security (Signature Verification)

Webhook security is key to building reliable integration applications. If Webhook requests are not verified, attackers may forge Webhook requests, triggering unauthorized operations. GitHub uses HMAC-SHA256 algorithm to sign Webhook requests, developers should verify signatures on receiving end, ensuring requests indeed come from GitHub.

### 9.1 Why Signature Verification is Needed

Signature verification is foundation of Webhook security. By verifying signatures, can ensure the following points: First, request indeed comes from GitHub, not forged. Second, request has not been tampered with during transmission. Finally, prevent replay attacks (attackers intercepting legitimate requests and resending). Developers should always verify Webhook signatures, don't skip this security step.

### 9.2 Signature Generation Algorithm

GitHub uses HMAC-SHA256 algorithm to generate signatures. HMAC (Hash-based Message Authentication Code) is a hash-based message authentication code, using key to perform hash calculation on message. GitHub uses configured Webhook Secret as key, performs HMAC-SHA256 calculation on request body, generates signature and appends to request header. Signature is passed through `X-Hub-Signature-256` header, format is `sha256=signature_value`.

```
X-Hub-Signature-256: sha256=abc123...
```

### 9.3 Signature Verification Examples

Signature verification implementation varies by programming language, but basic principle is same: use Webhook Secret to perform HMAC-SHA256 calculation on request body, then compare with signature in request header. Comparison should use constant-time comparison function (like Python's `hmac.compare_digest`) to prevent timing attacks. Here are the several commonly used languages' signature verification implementations.

**Python Verification**:

```python
import hmac
import hashlib

def verify_signature(payload_body, secret_token, signature_header):
    """Verify GitHub Webhook signature"""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        secret_token.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

# Flask example
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = "your-secret"

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, WEBHOOK_SECRET, signature):
        abort(401)
    
    payload = request.json
    # Process Webhook event
    return 'OK', 200
```

**Node.js Verification**:

```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  const digest = 'sha256=' + hmac.update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(digest)
  );
}

// Express example
const express = require('express');
const app = express();
const WEBHOOK_SECRET = 'your-secret';

app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-hub-signature-256'];
  if (!verifySignature(req.body, signature, WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }
  
  const payload = JSON.parse(req.body);
  // Process Webhook event
  res.status(200).send('OK');
});
```

**Go Verification**:

```go
package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "io"
    "net/http"
)

func verifySignature(payload []byte, signature, secret string) bool {
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write(payload)
    expectedMAC := hex.EncodeToString(mac.Sum(nil))
    expectedSignature := "sha256=" + expectedMAC
    return hmac.Equal([]byte(signature), []byte(expectedSignature))
}

func webhookHandler(w http.ResponseWriter, r *http.Request) {
    payload, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading body", http.StatusBadRequest)
        return
    }
    
    signature := r.Header.Get("X-Hub-Signature-256")
    if !verifySignature(payload, signature, "your-secret") {
        http.Error(w, "Invalid signature", http.StatusUnauthorized)
        return
    }
    
    // Process Webhook event
    w.WriteHeader(http.StatusOK)
}
```

### 9.4 Security Best Practices

Webhook security is not only about verifying signatures, includes multiple aspects of security measures. Here are the Webhook security best practices, developers should strictly follow when building integration applications. These best practices can help developers avoid common security risks, ensure Webhook service's security and reliability.

1. **Always verify signatures**: Don't skip signature verification step
2. **Use constant-time comparison**: Prevent timing attacks, use `hmac.compare_digest` etc. functions
3. **Use HTTPS**: Ensure data not eavesdropped during transmission
4. **Protect Secret**: Don't hardcode in code, use environment variables
5. **Restrict IP whitelist**: Only allow GitHub's IP ranges to access

## Chapter 10: Practice: Build GitHub Integration Application

This chapter will through several actual cases, show how to use GitHub API and Webhooks to build integration applications. These cases cover common usage scenarios, including automatic code review, Issue auto-labeling, deployment notifications, etc. Through learning these cases, developers can master basic skills for building GitHub integration applications.

### 10.1 Example: Automatic Code Review Bot

Automatic code review bot is a common GitHub integration application. When Pull Request is created, bot automatically analyzes code changes, detects potential issues (like security vulnerabilities, code style problems, etc.), and adds review comments on PR. Here are the using Python Flask to build automatic code review bot example. This bot detects sensitive information and TODO comments in code, and adds corresponding comments on PR.

```python
from flask import Flask, request
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

def verify_signature(payload, signature):
    if not signature:
        return False
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected, signature)

def review_code(owner, repo, pr_number):
    """Auto review code"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get PR files
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    files = response.json()
    
    comments = []
    for file in files:
        filename = file['filename']
        patch = file.get('patch', '')
        
        # Simple code review rules
        if 'password' in patch.lower() or 'secret' in patch.lower():
            comments.append({
                'path': filename,
                'position': 1,
                'body': 'Warning: Possible sensitive information detected.'
            })
        
        if 'TODO' in patch:
            comments.append({
                'path': filename,
                'position': 1,
                'body': 'Note: TODO comment found. Please track this task.'
            })
    
    # Submit review comments
    if comments:
        review_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
        review_data = {
            'event': 'COMMENT',
            'body': 'Automated code review by Bot',
            'comments': comments
        }
        requests.post(review_url, json=review_data, headers=headers)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Invalid signature', 401
    
    payload = request.json
    
    if payload.get('action') == 'opened' and 'pull_request' in payload:
        pr = payload['pull_request']
        owner = payload['repository']['owner']['login']
        repo = payload['repository']['name']
        pr_number = pr['number']
        
        review_code(owner, repo, pr_number)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
```

### 10.2 Example: Issue Auto-labeling Bot

Issue auto-labeling bot can automatically add labels based on Issue's title and content. This helps Issue classification and management, improving project management efficiency. Here are the using Python Flask to build Issue auto-labeling bot example. This bot analyzes Issue's title and content, automatically adds corresponding labels (like bug, enhancement, documentation, etc.) based on keywords.

```python
from flask import Flask, request
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

def verify_signature(payload, signature):
    if not signature:
        return False
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected, signature)

def analyze_issue(title, body):
    """Analyze Issue content and return labels"""
    labels = []
    
    # Detect Bug
    if any(word in title.lower() for word in ['bug', 'error', 'crash', 'broken']):
        labels.append('bug')
    
    # Detect Feature Request
    if any(word in title.lower() for word in ['feature', 'request', 'enhancement']):
        labels.append('enhancement')
    
    # Detect Documentation
    if any(word in title.lower() for word in ['doc', 'documentation', 'readme']):
        labels.append('documentation')
    
    # Detect Priority
    if any(word in title.lower() for word in ['urgent', 'critical', 'blocker']):
        labels.append('priority: high')
    
    return labels

def add_labels(owner, repo, issue_number, labels):
    """Add labels to Issue"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels'
    requests.post(url, json={'labels': labels}, headers=headers)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Invalid signature', 401
    
    payload = request.json
    
    if payload.get('action') == 'opened' and 'issue' in payload:
        issue = payload['issue']
        owner = payload['repository']['owner']['login']
        repo = payload['repository']['name']
        
        title = issue['title']
        body = issue.get('body', '')
        issue_number = issue['number']
        
        labels = analyze_issue(title, body)
        if labels:
            add_labels(owner, repo, issue_number, labels)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
```

### 10.3 Example: Deployment Notification Bot

Deployment notification bot can send notifications when CI/CD process completes. This helps team understand deployment status, timely discover and handle deployment issues. Here are the using Python Flask to build deployment notification bot example. This bot monitors GitHub Actions' workflow_run event, when workflow completes, sends notification messages to Slack.

```python
from flask import Flask, request
import hmac
import hashlib
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

def verify_signature(payload, signature):
    if not signature:
        return False
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected, signature)

def send_slack_message(message):
    """Send Slack notification"""
    requests.post(SLACK_WEBHOOK_URL, json={'text': message})

def handle_workflow_run(payload):
    """Handle workflow_run event"""
    workflow_run = payload['workflow_run']
    
    status = workflow_run['status']
    conclusion = workflow_run.get('conclusion', 'in_progress')
    name = workflow_run['name']
    branch = workflow_run['head_branch']
    url = workflow_run['html_url']
    
    if status == 'completed':
        if conclusion == 'success':
            emoji = '✅'
            message = f"{emoji} {name} succeeded on {branch}"
        elif conclusion == 'failure':
            emoji = '❌'
            message = f"{emoji} {name} failed on {branch}"
        else:
            emoji = '⚠️'
            message = f"{emoji} {name} {conclusion} on {branch}"
        
        message += f"\n<{url}|View details>"
        send_slack_message(message)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Invalid signature', 401
    
    payload = request.json
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'workflow_run':
        handle_workflow_run(payload)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
```

## Chapter 11: API Rate Limits and Optimization

GitHub has rate limits for API calls, to prevent abuse and ensure service stability. Understanding rate limit rules and taking optimization measures is crucial for building reliable integration applications. This chapter will introduce rate limit rules, checking methods and optimization strategies.

### 11.1 Rate Limit Rules

GitHub API's rate limits vary by authentication method. Unauthenticated requests have lowest rate limits, GitHub App has highest rate limits. Developers should choose appropriate authentication method based on actual needs, and reasonably plan API calls. Here are the different authentication methods' rate limit details.

| Authentication Method | Core Limit | Search Limit | GraphQL Points |
|-----------------------|------------|--------------|----------------|
| Unauthenticated | 60/hour | 10/minute | N/A |
| PAT | 5000/hour | 30/minute | 5000/hour |
| GitHub App | 15000/hour | 30/minute | 5000/hour |
| GITHUB_TOKEN | 1000/hour | 30/minute | 1000/hour |

### 11.2 Check Rate Limits

Developers can check current rate limit status through API. Rate limit information includes total limit, used count, remaining count and reset time. By monitoring this information, can avoid exceeding rate limits. Here are the checking rate limit methods.

```bash
# View current limits
gh api /rate_limit

# Response example
{
  "resources": {
    "core": {
      "limit": 5000,
      "used": 123,
      "remaining": 4877,
      "reset": 1609459200
    },
    "search": {
      "limit": 30,
      "used": 5,
      "remaining": 25,
      "reset": 1609459260
    },
    "graphql": {
      "limit": 5000,
      "used": 100,
      "remaining": 4900,
      "reset": 1609459200
    }
  }
}
```

### 11.3 Handle Rate Limits

When API calls exceed rate limits, GitHub returns 403 status code. Developers should handle rate limits in code, when encountering rate limits, wait a period of time then retry. Here are the handling rate limits Python example code, it automatically detects rate limits and waits for reset time.

```python
import requests
import time

def github_api_call(url, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    while True:
        response = requests.get(url, headers=headers)
        
        # Check rate limit
        remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        
        if remaining == 0:
            # Wait for reset
            wait_time = reset_time - time.time() + 1
            if wait_time > 0:
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and 'rate limit' in response.text.lower():
            time.sleep(60)
            continue
        else:
            response.raise_for_status()
```

### 11.4 Optimization Strategies

To reduce API call count and improve efficiency, developers can adopt various optimization strategies. These strategies can help applications complete more work within rate limits, while improving response speed and user experience. Here are the commonly used API call optimization strategies.

**Use Conditional Requests**:

```bash
# Use ETag
curl -H "If-None-Match: \"abc123\"" \
  https://api.github.com/repos/octocat/Hello-World

# Use Last-Modified
curl -H "If-Modified-Since: Wed, 01 Jan 2023 00:00:00 GMT" \
  https://api.github.com/repos/octocat/Hello-World
```

**Use GraphQL to Reduce Requests**:

```graphql
# Get multiple resources in one request
query {
  repository(owner: "octocat", name: "Hello-World") {
    issues(first: 100) {
      nodes {
        title
        comments(first: 10) {
          nodes {
            body
          }
        }
      }
    }
    pullRequests(first: 100) {
      nodes {
        title
        reviews(first: 10) {
          nodes {
            body
          }
        }
      }
    }
  }
}
```

**Use Webhook Instead of Polling**:

```python
# Bad practice: polling
while True:
    issues = get_issues()
    process_issues(issues)
    time.sleep(60)

# Good practice: use Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    issue = request.json['issue']
    process_issue(issue)
    return 'OK', 200
```

**Cache Responses**:

```python
import requests_cache

# Install: pip install requests-cache
requests_cache.install_cache('github_cache', expire_after=300)

# Now all requests will be cached
response = requests.get('https://api.github.com/repos/octocat/Hello-World')
```

## Chapter 12: GitHub App vs OAuth App Comparison

GitHub App and OAuth App are two different application types, suitable for different use scenarios. Understanding their differences is crucial for choosing appropriate application type. This chapter will compare in detail both application types' characteristics and applicable scenarios.

### 12.1 Core Differences

GitHub App and OAuth App have significant differences in identity model, permission model, rate limits, etc. GitHub App runs with independent identity, has its own permissions; OAuth App runs with user identity, inherits user's permissions. These differences determine their applicable scenarios.

| Feature | GitHub App | OAuth App |
|---------|------------|-----------|
| Identity | Independent identity | User identity |
| Installation | Installed on repository/organization | User authorization |
| Permissions | Fine-grained permissions | User scope permissions |
| Rate Limit | 15000/hour | 5000/hour |
| Webhook | Bound to installation | Needs separate configuration |
| Recommended Scenario | Integration applications | User authorization applications |

### 12.2 GitHub App Advantages

GitHub App is more modern application type, has several advantages. These advantages make GitHub App the preferred for building integration applications. Here are the GitHub App's main advantages, developers should consider these factors when choosing application type.

**Fine-grained Permissions**: GitHub App can precisely configure needed permissions, only request necessary access. This is more secure than OAuth App's user scope permissions.

**Independent Identity**: GitHub App runs with independent identity, doesn't depend on user account. This makes application's behavior more predictable, easier to manage.

**Higher Quota**: GitHub App's API rate limit is 15000 times/hour, three times higher than OAuth App's 5000 times/hour.

**Installation-level Tokens**: GitHub App uses short-lived installation tokens (1 hour), more secure than long-lived OAuth tokens.

**Organization-level Control**: Organization administrators can control GitHub App installation, can restrict which repositories can install applications.

### 12.3 OAuth App Advantages

OAuth App is traditional application type, although in certain aspects not as good as GitHub App, still has its unique advantages. In some scenarios, OAuth App may be better choice. Here are the OAuth App's main advantages.

**User Identity**: OAuth App executes operations with user identity, can access all resources user has permission to.

**Simple Integration**: OAuth App's integration process is relatively simple, suitable for scenarios needing user authorization.

**Broad Support**: OAuth App supports all GitHub features, no GitHub App's some limitations.

**Long-term Tokens**: OAuth tokens have no expiration time (unless manually revoked), suitable for scenarios needing long-term access.

### 12.4 Selection Suggestions

Choosing whether to use GitHub App or OAuth App depends on specific use scenarios. Developers should consider application's needs, security requirements and user experience factors to make choices. Here are the selection suggestions, helping developers make wise decisions.

**Choose GitHub App**:
- Building GitHub integration applications
- Need fine-grained permission control
- Need high API quota
- Organization-level integration

**Choose OAuth App**:
- Need to operate with user identity
- Simple user authorization scenarios
- Need to access user-specific data
- Traditional third-party applications

### 12.5 Create GitHub App

Creating GitHub App requires completing in GitHub settings. Creation process needs configuring application's basic information, permissions, Webhooks, etc. Here are the creating GitHub App detailed steps, developers should follow these steps to complete application creation and configuration.

```bash
# 1. Visit Settings → Developer settings → GitHub Apps → New GitHub App

# 2. Configure basic info
# - App name: My Integration
# - Homepage URL: https://example.com
# - Callback URL: https://example.com/callback

# 3. Configure permissions
# Repository permissions:
#   - Issues: Read & Write
#   - Pull requests: Read & Write
#   - Contents: Read-only

# 4. Configure events
# - Issues
# - Pull request

# 5. Generate private key

# 6. Install to repository/organization
```

### 12.6 Use GitHub App

Using GitHub App requires implementing JWT authentication and installation token retrieval. Here are the using Python to implement GitHub App authentication complete example code. This example shows how to generate JWT, get installation token, and use installation token to call API. Developers can build their own GitHub App applications based on this example.

```python
import jwt
import time
import requests

class GitHubApp:
    def __init__(self, app_id, private_key_path):
        self.app_id = app_id
        with open(private_key_path, 'r') as f:
            self.private_key = f.read()
    
    def get_jwt(self):
        now = int(time.time())
        payload = {
            'iat': now - 60,
            'exp': now + 600,
            'iss': self.app_id
        }
        return jwt.encode(payload, self.private_key, algorithm='RS256')
    
    def get_installation_token(self, installation_id):
        jwt_token = self.get_jwt()
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.post(
            f'https://api.github.com/app/installations/{installation_id}/access_tokens',
            headers=headers
        )
        return response.json()['token']
    
    def api_call(self, method, url, installation_id, **kwargs):
        token = self.get_installation_token(installation_id)
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        return requests.request(method, url, headers=headers, **kwargs)

# Usage example
app = GitHubApp('APP_ID', 'private-key.pem')
token = app.get_installation_token('INSTALLATION_ID')
response = app.api_call('GET', 'https://api.github.com/repos/octocat/Hello-World', 'INSTALLATION_ID')
```

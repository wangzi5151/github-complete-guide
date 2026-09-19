# Exercise 33: GitHub API Integration

## Objective

Learn how to use the GitHub API to automate and extend GitHub functionality.

## Prerequisites

- A GitHub account
- Familiarity with REST API basics
- Basic programming skills

## Steps

### 1. Understanding the GitHub API

The GitHub API is a RESTful API that allows you to access GitHub functionality programmatically.

**API Versions**:
- REST API v3: Legacy API with comprehensive features
- GraphQL API v4: More flexible, can fetch multiple resources in a single request

**Authentication Methods**:
- Personal Access Token (PAT)
- GitHub App
- OAuth App

### 2. Creating a Personal Access Token

**Steps to Create**:

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select the token type
4. Choose permission scopes
5. Click "Generate token"

**Permission Scopes**:
- `repo`: Repository access
- `admin:org`: Organization management
- `admin:repo_hook`: Webhook management
- `user`: User information
- `workflow`: GitHub Actions

### 3. Using the REST API

**Example: Get User Information**:

```bash
# Using curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/users/octocat

# Using Python
import requests

headers = {
    'Authorization': f'Bearer {YOUR_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get('https://api.github.com/users/octocat', headers=headers)
print(response.json())
```

**Example: Get Repository List**:

```bash
# Using curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/user/repos

# Using Python
import requests

headers = {
    'Authorization': f'Bearer {YOUR_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get('https://api.github.com/user/repos', headers=headers)
for repo in response.json():
    print(repo['name'])
```

**Example: Create an Issue**:

```bash
# Using curl
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo/issues \
  -d '{"title":"New Issue","body":"This is a new issue"}'

# Using Python
import requests

headers = {
    'Authorization': f'Bearer {YOUR_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

data = {
    'title': 'New Issue',
    'body': 'This is a new issue'
}

response = requests.post(
    'https://api.github.com/repos/owner/repo/issues',
    headers=headers,
    json=data
)
print(response.json())
```

### 4. Using the GraphQL API

**Example: Get User Information**:

```bash
# Using curl
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/graphql \
  -d '{"query":"query { viewer { login name email } }"}'

# Using Python
import requests

headers = {
    'Authorization': f'Bearer {YOUR_TOKEN}',
    'Content-Type': 'application/json'
}

query = '''
query {
  viewer {
    login
    name
    email
  }
}
'''

response = requests.post(
    'https://api.github.com/graphql',
    headers=headers,
    json={'query': query}
)
print(response.json())
```

**Example: Get Repository Information**:

```bash
# Using Python
import requests

headers = {
    'Authorization': f'Bearer {YOUR_TOKEN}',
    'Content-Type': 'application/json'
}

query = '''
query {
  repository(owner: "octocat", name: "Hello-World") {
    name
    description
    stargazerCount
    forkCount
    issues(first: 5) {
      nodes {
        title
        body
      }
    }
  }
}
'''

response = requests.post(
    'https://api.github.com/graphql',
    headers=headers,
    json={'query': query}
)
print(response.json())
```

### 5. Using GitHub CLI

**Example: Call the API Using GitHub CLI**:

```bash
# Get user information
gh api users/octocat

# Get repository list
gh api user/repos

# Create an Issue
gh api repos/owner/repo/issues -f title="New Issue" -f body="This is a new issue"

# Using GraphQL
gh api graphql -f query='query { viewer { login name email } }'
```

### 6. Using Webhooks

**Creating a Webhook**:

1. Go to the repository settings
2. Click "Webhooks"
3. Click "Add webhook"
4. Configure the Webhook

**Webhook Events**:
- `push`: Code push
- `pull_request`: Pull Request events
- `issues`: Issue events
- `release`: Release events

**Example: Handling a Webhook**:

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

WEBHOOK_SECRET = 'your-webhook-secret'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return 'Invalid signature', 403
    
    # Handle event
    event = request.headers.get('X-GitHub-Event')
    payload = request.json()
    
    if event == 'push':
        handle_push(payload)
    elif event == 'pull_request':
        handle_pull_request(payload)
    elif event == 'issues':
        handle_issues(payload)
    
    return 'OK', 200

def verify_signature(payload, signature):
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

def handle_push(payload):
    print(f"Push to {payload['repository']['full_name']}")
    print(f"Commits: {len(payload['commits'])}")

def handle_pull_request(payload):
    action = payload['action']
    pr = payload['pull_request']
    print(f"PR {action}: {pr['title']}")

def handle_issues(payload):
    action = payload['action']
    issue = payload['issue']
    print(f"Issue {action}: {issue['title']}")

if __name__ == '__main__':
    app.run(port=5000)
```

### 7. Using GitHub Apps

**Creating a GitHub App**:

1. Go to [GitHub Developer Settings](https://github.com/settings/apps)
2. Click "New GitHub App"
3. Configure the App
4. Generate a private key

**Example: Using a GitHub App**:

```python
import jwt
import time
import requests

# Configuration
APP_ID = 'your-app-id'
PRIVATE_KEY = open('private-key.pem', 'r').read()

# Generate JWT
def generate_jwt():
    now = int(time.time())
    payload = {
        'iat': now - 60,
        'exp': now + 600,
        'iss': APP_ID
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')

# Get installation token
def get_installation_token(installation_id):
    jwt_token = generate_jwt()
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )
    
    return response.json()['token']

# Use installation token
def use_installation_token(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        'https://api.github.com/installation/repositories',
        headers=headers
    )
    
    return response.json()
```

### 8. Using OAuth

**OAuth Flow**:

1. Redirect the user to the GitHub authorization page
2. After the user authorizes, GitHub redirects back to your application
3. Your application obtains an access token

**Example: OAuth Flow**:

```python
from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/login')
def login():
    return redirect(
        f'https://github.com/login/oauth/authorize'
        f'?client_id={CLIENT_ID}'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope=repo,user'
    )

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Get access token
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        json={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        },
        headers={'Accept': 'application/json'}
    )
    
    token = response.json()['access_token']
    session['token'] = token
    
    return redirect('/profile')

@app.route('/profile')
def profile():
    token = session.get('token')
    if not token:
        return redirect('/login')
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get('https://api.github.com/user', headers=headers)
    user = response.json()
    
    return f"Hello, {user['login']}!"

if __name__ == '__main__':
    app.run(port=5000)
```

### 9. Automating with the GitHub API

**Example: Auto-merge Dependabot PRs**:

```python
import requests

def auto_merge_dependabot_prs(token, owner, repo):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get PR list
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls',
        headers=headers
    )
    
    prs = response.json()
    
    for pr in prs:
        # Check if it is a Dependabot PR
        if pr['user']['login'] == 'dependabot[bot]':
            # Check if CI passed
            if check_ci_status(token, owner, repo, pr['number']):
                # Merge the PR
                merge_pr(token, owner, repo, pr['number'])

def check_ci_status(token, owner, repo, pr_number):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews',
        headers=headers
    )
    
    reviews = response.json()
    return any(r['state'] == 'APPROVED' for r in reviews)

def merge_pr(token, owner, repo, pr_number):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.put(
        f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge',
        headers=headers,
        json={'merge_method': 'squash'}
    )
    
    return response.json()
```

### 10. Reporting with the GitHub API

**Example: Generate a Contribution Report**:

```python
import requests
from datetime import datetime, timedelta

def generate_contribution_report(token, owner, repo, days=30):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get commits
    commits = get_commits(token, owner, repo, start_date, end_date)
    
    # Get PRs
    prs = get_pull_requests(token, owner, repo, start_date, end_date)
    
    # Get Issues
    issues = get_issues(token, owner, repo, start_date, end_date)
    
    # Generate report
    report = f"""
    # Contribution Report
    
    **Date Range**: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
    
    ## Statistics
    
    - Commits: {len(commits)}
    - Pull Requests: {len(prs)}
    - Issues: {len(issues)}
    
    ## Active Contributors
    
    {get_active_contributors(commits, prs, issues)}
    """
    
    return report

def get_commits(token, owner, repo, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/commits',
        headers=headers,
        params={
            'since': start_date.isoformat(),
            'until': end_date.isoformat(),
            'per_page': 100
        }
    )
    
    return response.json()

def get_pull_requests(token, owner, repo, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls',
        headers=headers,
        params={
            'state': 'all',
            'sort': 'created',
            'direction': 'desc',
            'per_page': 100
        }
    )
    
    return [pr for pr in response.json() 
            if start_date.isoformat() <= pr['created_at'] <= end_date.isoformat()]

def get_issues(token, owner, repo, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/issues',
        headers=headers,
        params={
            'state': 'all',
            'sort': 'created',
            'direction': 'desc',
            'per_page': 100
        }
    )
    
    return [issue for issue in response.json() 
            if start_date.isoformat() <= issue['created_at'] <= end_date.isoformat()]

def get_active_contributors(commits, prs, issues):
    contributors = {}
    
    for commit in commits:
        author = commit['commit']['author']['name']
        contributors[author] = contributors.get(author, 0) + 1
    
    for pr in prs:
        author = pr['user']['login']
        contributors[author] = contributors.get(author, 0) + 1
    
    for issue in issues:
        author = issue['user']['login']
        contributors[author] = contributors.get(author, 0) + 1
    
    # Sort by contribution count
    sorted_contributors = sorted(contributors.items(), key=lambda x: x[1], reverse=True)
    
    return '\n'.join([f"- {name}: {count} contributions" for name, count in sorted_contributors[:10]])
```

## Challenges

1. **Challenge 1**: Create a script that automatically creates Issues
2. **Challenge 2**: Create a script that automatically merges Dependabot PRs
3. **Challenge 3**: Create a script that generates contribution reports
4. **Challenge 4**: Create a server that automatically handles Webhooks
5. **Challenge 5**: Create a GitHub App to automate repository management

## Reflection

1. What are some use cases for the GitHub API?
2. How can you protect GitHub API access tokens?
3. How should you handle GitHub API rate limits?
4. How do you choose between the REST API and the GraphQL API?

## Related Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [GitHub CLI Documentation](https://cli.github.com/)
- [GitHub Webhooks Documentation](https://docs.github.com/en/webhooks)
- [GitHub Apps Documentation](https://docs.github.com/en/apps)

---

**Previous: [Exercise 32: GitHub Actions Matrix Strategy](exercise-32-github-actions-matrix.md) | Next: [Exercise 34: GitHub Security Best Practices](exercise-34-github-security-best-practices.md)**

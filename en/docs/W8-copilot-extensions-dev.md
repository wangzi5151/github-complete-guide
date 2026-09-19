# GitHub Copilot Extensions Development

## What is a Copilot Extension?

Copilot Extensions allow you to build custom AI assistants that integrate into Copilot's workflow.

## Architecture Overview

```
User → GitHub Copilot → Your Extension API → External Service
```

## Creating an Extension

### 1. Register a GitHub App

```bash
# Visit https://github.com/settings/apps/new
# Configure:
# - GitHub Copilot: Send replies → Enable
# - Webhook URL: Your API address
# - Permissions: Code search, repository read
```

### 2. Create an API Service

```python
# app.py
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

GITHUB_SECRET = "your-webhook-secret"

@app.route("/copilot", methods=["POST"])
def copilot_handler():
    # Verify signature
    signature = request.headers["X-Hub-Signature-256"]
    expected = "sha256=" + hmac.new(
        GITHUB_SECRET.encode(),
        request.data,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        return jsonify({"error": "Invalid signature"}), 401
    
    payload = request.json
    
    # Handle request
    prompt = payload.get("prompt", "")
    context = payload.get("context", {})
    
    # Generate response
    response = generate_response(prompt, context)
    
    return jsonify({
        "choices": [{
            "message": {
                "content": response
            }
        }]
    })

def generate_response(prompt, context):
    """Your AI logic"""
    # You can call any external API here
    # For example: database queries, API calls, document search, etc.
    return f"Based on your request: {prompt}"

if __name__ == "__main__":
    app.run(port=8080)
```

### 3. Configure the Extension

```json
{
  "name": "my-extension",
  "description": "Custom Copilot Extension",
  "hooks": {
    "copilot": "/copilot"
  },
  "permissions": {
    "repository": ["read"],
    "codespaces": ["read"]
  }
}
```

## Use Cases

### 1. Internal Document Search

```python
@app.route("/copilot", methods=["POST"])
def search_docs():
    prompt = request.json["prompt"]
    
    # Search internal documents
    results = search_internal_docs(prompt)
    
    # Return relevant document snippets
    return jsonify({
        "choices": [{
            "message": {
                "content": format_doc_results(results)
            }
        }]
    })
```

### 2. Database Query

```python
@app.route("/copilot", methods=["POST"])
def query_database():
    prompt = request.json["prompt"]
    
    # Parse natural language query
    sql = natural_to_sql(prompt)
    
    # Execute query
    results = db.execute(sql)
    
    return jsonify({
        "choices": [{
            "message": {
                "content": format_query_results(results)
            }
        }]
    })
```

### 3. API Integration

```python
@app.route("/copilot", methods=["POST"])
def integrate_api():
    prompt = request.json["prompt"]
    
    # Call external API
    if "weather" in prompt:
        city = extract_city(prompt)
        weather = get_weather(city)
        return format_weather(weather)
    
    if "exchange rate" in prompt:
        currencies = extract_currencies(prompt)
        rate = get_exchange_rate(currencies)
        return format_rate(rate)
```

### 4. CI/CD Operations

```python
@app.route("/copilot", methods=["POST"])
def cicd_operations():
    prompt = request.json["prompt"]
    context = request.json["context"]
    
    if "deploy" in prompt:
        # Trigger deployment
        deployment = trigger_deployment(context["repo"])
        return f"Deployment triggered: {deployment.url}"
    
    if "rollback" in prompt:
        # Execute rollback
        rollback = execute_rollback(context["repo"])
        return f"Rolled back to version: {rollback.version}"
```

## Deployment

### Deploy with Vercel

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

### Deploy with Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
```

## Best Practices

1. **Fast Response**: Keep response time < 3 seconds
2. **Clear Output**: Use Markdown to format output
3. **Error Handling**: Provide useful error messages
4. **Logging**: Log requests and responses for debugging
5. **Rate Limiting**: Prevent API abuse

## Related Resources

- [Copilot Extensions Documentation](https://docs.github.com/en/copilot/extensions)
- [GitHub App Creation](https://docs.github.com/en/apps/creating-github-apps)
- [Webhook Development](https://docs.github.com/en/webhooks)

---

**Previous: [GitHub Copilot Advanced Features](W7-copilot-advanced.md) | Next: [GitHub Actions Advanced Usage](W9-actions-advanced.md)**

# Exercise 27: Testing AI Models with GitHub Models

## Learning Objectives

After completing this exercise, you will be able to:

- Understand the concept and purpose of GitHub Models
- Call various AI models using the GitHub Models API
- Compare the performance and output quality of different models
- Build simple applications based on AI models
- Learn best practices for model evaluation and selection

## Prerequisites

- Have a GitHub account
- Have Python 3.10+ or Node.js 18+ installed
- Basic knowledge of API calls
- Understanding of JSON data format

## Background Knowledge

### What are GitHub Models

GitHub Models is an AI model testing platform provided by GitHub that allows developers to:

1. **Test AI models for free**: Experience various large language models without paying
2. **Compare different models**: Test multiple models' outputs on the same platform
3. **Rapid prototyping**: Use the API to quickly build AI application prototypes
4. **Integrate into workflows**: Integrate models into GitHub Actions and applications

### Supported Model Types

GitHub Models offers multiple models for testing:

- **Language models**: GPT-4, Claude, Llama, etc.
- **Embedding models**: For text vectorization
- **Image models**: For image generation and understanding
- **Multimodal models**: Support text and image input

---

## Exercise Steps

### Part 1: Setting Up GitHub Models Access

#### Step 1: Get a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Select permissions: `read:user` and `models:read`
4. Generate and save the token

```bash
# Set environment variable
export GITHUB_TOKEN="your_github_token_here"
```

#### Step 2: Install Required Dependencies

**Python Environment:**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install openai requests python-dotenv
```

**Node.js Environment:**

```bash
# Initialize project
mkdir github-models-demo && cd github-models-demo
npm init -y

# Install dependencies
npm install openai dotenv
```

### Part 2: Using Python to Call GitHub Models

#### Step 3: Create a Basic Call Script

Create file `basic_call.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure GitHub Models client
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

def call_model(model_name, messages, temperature=0.7, max_tokens=1000):
    """
    Call the specified AI model
    
    Args:
        model_name: Model name
        messages: List of messages
        temperature: Temperature parameter (controls randomness)
        max_tokens: Maximum number of tokens to generate
    
    Returns:
        Model response text
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=0.95,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Call failed: {str(e)}"

# Test the call
if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer questions in English."},
        {"role": "user", "content": "What is GitHub Actions?"}
    ]
    
    response = call_model("gpt-4o-mini", messages)
    print("Model response:")
    print(response)
```

#### Step 4: Create Environment Configuration File

Create file `.env`:

```
GITHUB_TOKEN=your_github_token_here
```

Create file `.gitignore`:

```
.env
venv/
node_modules/
__pycache__/
```

#### Step 5: Run the Basic Call

```bash
python basic_call.py
```

Expected output:

```
Model response:
GitHub Actions is a continuous integration and continuous deployment (CI/CD) platform provided by GitHub. It allows developers to automate software development workflows, including building, testing, and deploying tasks.

Key features:
1. Event-triggered: Can automatically run when push, pull request, issue, and other events occur
2. YAML configuration: Uses YAML files to define workflows
3. Matrix builds: Supports parallel testing across multiple operating systems and language versions
4. Marketplace sharing: Actions can be shared and reused through GitHub Marketplace
5. Free tier: Free for public repositories, with free tier available for private repositories
```

### Part 3: Comparing Different Models

#### Step 6: Create a Model Comparison Script

Create file `compare_models.py`:

```python
import os
import time
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

# List of available models
AVAILABLE_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "Meta-Llama-3.1-405B-Instruct",
    "Meta-Llama-3.1-70B-Instruct",
    "Mistral-large",
    "Phi-3-medium-4k-instruct",
]

def compare_models(
    prompt: str,
    models: List[str] = None,
    system_prompt: str = "You are a helpful assistant. Answer questions in English.",
) -> Dict[str, Any]:
    """
    Compare multiple models' responses to the same prompt
    
    Args:
        prompt: User prompt
        models: List of models to compare
        system_prompt: System prompt
    
    Returns:
        Dictionary containing each model's response
    """
    if models is None:
        models = AVAILABLE_MODELS[:3]  # Compare first 3 models by default
    
    results = {}
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    
    for model in models:
        print(f"\nTesting model: {model}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            
            elapsed_time = time.time() - start_time
            content = response.choices[0].message.content
            
            results[model] = {
                "response": content,
                "time": round(elapsed_time, 2),
                "tokens": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens,
                },
                "success": True,
            }
            
            print(f"Response time: {elapsed_time:.2f}s")
            print(f"Tokens used: {response.usage.total_tokens}")
            print(f"Response preview: {content[:200]}...")
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            results[model] = {
                "response": None,
                "time": round(elapsed_time, 2),
                "error": str(e),
                "success": False,
            }
            print(f"Error: {str(e)}")
    
    return results

def format_comparison_report(results: Dict[str, Any]) -> str:
    """Generate comparison report"""
    report = "# Model Comparison Report\n\n"
    
    # Performance summary
    report += "## Performance Summary\n\n"
    report += "| Model | Response Time | Tokens | Status |\n"
    report += "|-------|---------------|--------|--------|\n"
    
    for model, data in results.items():
        status = "✅ Success" if data["success"] else "❌ Failed"
        time_str = f"{data['time']}s"
        tokens = data.get("tokens", {}).get("total", "N/A")
        report += f"| {model} | {time_str} | {tokens} | {status} |\n"
    
    # Detailed responses
    report += "\n## Detailed Responses\n\n"
    for model, data in results.items():
        report += f"### {model}\n\n"
        if data["success"]:
            report += f"{data['response']}\n\n"
        else:
            report += f"Error: {data.get('error', 'Unknown error')}\n\n"
        report += "---\n\n"
    
    return report

# Main program
if __name__ == "__main__":
    test_prompt = "Explain the relationship between machine learning, deep learning, and artificial intelligence in simple terms."
    
    print("=" * 60)
    print("GitHub Models Comparison Test")
    print("=" * 60)
    print(f"\nTest prompt: {test_prompt}\n")
    
    results = compare_models(test_prompt)
    
    # Generate report
    report = format_comparison_report(results)
    
    # Save report
    with open("model_comparison_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("Comparison report saved to model_comparison_report.md")
    print("=" * 60)
    
    # Save raw data
    with open("model_comparison_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("Raw data saved to model_comparison_data.json")
```

#### Step 7: Run Model Comparison

```bash
python compare_models.py
```

### Part 4: Building a Simple AI Application

#### Step 8: Create a Code Review Assistant

Create file `code_reviewer.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

class CodeReviewer:
    """AI Code Review Assistant"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.system_prompt = """You are a professional code review expert. Your task is to:
1. Check for potential issues and bugs in the code
2. Evaluate code readability and maintainability
3. Provide improvement suggestions
4. Check for security vulnerabilities
5. Offer performance optimization suggestions

Please respond in English and output in the following format:
- Critical Issues (must fix)
- Suggested Improvements (recommended fixes)
- Code Style (optional optimizations)
- Overall Assessment
"""
    
    def review_code(
        self,
        code: str,
        language: str = "python",
        context: Optional[str] = None,
    ) -> str:
        """
        Review code
        
        Args:
            code: Code to review
            language: Programming language
            context: Additional context information
        
        Returns:
            Review result
        """
        user_message = f"Please review the following {language} code:\n\n```{language}\n{code}\n```"
        
        if context:
            user_message += f"\n\nContext: {context}"
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Low temperature for more consistent output
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Review failed: {str(e)}"
    
    def suggest_fixes(self, code: str, issues: str) -> str:
        """
        Provide fix suggestions based on discovered issues
        
        Args:
            code: Original code
            issues: Description of discovered issues
        
        Returns:
            Fixed code
        """
        messages = [
            {
                "role": "system",
                "content": "You are a code fix expert. Based on the provided issue description, provide the complete fixed code.",
            },
            {
                "role": "user",
                "content": f"Original code:\n```python\n{code}\n```\n\nDiscovered issues:\n{issues}\n\nPlease provide the complete fixed code.",
            },
        ]
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Fix suggestion failed: {str(e)}"


# Example usage
if __name__ == "__main__":
    reviewer = CodeReviewer()
    
    # Sample code
    sample_code = '''
def get_user_data(user_id):
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def process_data(data):
    if data != None:
        result = data[0] + data[1]
        return result
    else:
        return 0

class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
        print("User added: " + str(user))
    
    def get_all_users(self):
        return self.users
'''
    
    print("=" * 60)
    print("AI Code Review Assistant")
    print("=" * 60)
    
    # Review code
    print("\nReviewing code...\n")
    review_result = reviewer.review_code(sample_code, "python", "This is a user management module")
    print(review_result)
    
    print("\n" + "=" * 60)
    print("Getting fix suggestions...")
    print("=" * 60)
    
    # Get fix suggestions
    fix_suggestion = reviewer.suggest_fixes(sample_code, review_result)
    print(f"\n{fix_suggestion}")
```

#### Step 9: Create a Text Summarization Tool

Create file `text_summarizer.py`:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

class TextSummarizer:
    """AI Text Summarization Tool"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    
    def summarize(
        self,
        text: str,
        max_length: int = 200,
        style: str = "concise",
    ) -> str:
        """
        Generate text summary
        
        Args:
            text: Original text
            max_length: Maximum summary length (in words)
            style: Summary style ('concise', 'detailed', 'bullet_points')
        
        Returns:
            Generated summary
        """
        style_prompts = {
            "concise": f"Summarize the following content concisely, no more than {max_length} words:",
            "detailed": f"Summarize the following content in detail, including key information, no more than {max_length} words:",
            "bullet_points": f"Summarize the following content in bullet point format, each point concise and clear:",
        }
        
        system_prompt = style_prompts.get(style, style_prompts["concise"])
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=500,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Summary generation failed: {str(e)}"
    
    def extract_key_points(self, text: str) -> list:
        """
        Extract key points from text
        
        Args:
            text: Original text
        
        Returns:
            List of key points
        """
        messages = [
            {
                "role": "system",
                "content": "Extract key points from the text, one per line, prefixed with '-'.",
            },
            {"role": "user", "content": text},
        ]
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500,
            )
            points = response.choices[0].message.content.strip().split("\n")
            return [p.strip("- ").strip() for p in points if p.strip()]
        except Exception as e:
            return [f"Extraction failed: {str(e)}"]


# Example usage
if __name__ == "__main__":
    summarizer = TextSummarizer()
    
    sample_text = """
    GitHub Actions is a continuous integration and continuous deployment (CI/CD) service provided by GitHub.
    It allows developers to automate software development workflows, including building, testing, packaging, releasing, and deploying tasks.
    
    GitHub Actions uses YAML syntax to define workflow files, which are stored in the repository's
    .github/workflows directory. Each workflow consists of one or more jobs,
    and each job contains a series of steps.
    
    Workflows can be automatically triggered when specific events occur, such as code pushes to the repository,
    pull request creation, scheduled tasks, etc. Developers can also manually trigger workflows.
    
    GitHub Actions provides a rich set of built-in Actions, and community-shared Actions can be
    obtained through the GitHub Marketplace. This greatly simplifies CI/CD pipeline configuration.
    
    Additionally, GitHub Actions supports matrix builds, which can run tests in parallel
    across multiple operating systems and language versions, ensuring code compatibility.
    """
    
    print("=" * 60)
    print("AI Text Summarization Tool")
    print("=" * 60)
    
    # Generate summaries in different styles
    print("\n1. Concise Summary:")
    print("-" * 40)
    print(summarizer.summarize(sample_text, max_length=100, style="concise"))
    
    print("\n2. Detailed Summary:")
    print("-" * 40)
    print(summarizer.summarize(sample_text, max_length=200, style="detailed"))
    
    print("\n3. Bullet Points:")
    print("-" * 40)
    print(summarizer.summarize(sample_text, style="bullet_points"))
    
    print("\n4. Key Points Extraction:")
    print("-" * 40)
    key_points = summarizer.extract_key_points(sample_text)
    for i, point in enumerate(key_points, 1):
        print(f"{i}. {point}")
```

### Part 5: Using GitHub Models in GitHub Actions

#### Step 10: Create a Workflow Using GitHub Models

Create file `.github/workflows/ai-review.yml`:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install openai requests PyGithub
      
      - name: Get PR changes
        id: changes
        uses: actions/github-script@v7
        with:
          script: |
            const { data: files } = await github.rest.pulls.listFiles({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
            });
            
            const changes = files
              .filter(f => f.status !== 'removed')
              .map(f => ({
                filename: f.filename,
                patch: f.patch || '',
              }))
              .slice(0, 10);  // Limit to max 10 files
            
            core.setOutput('changes', JSON.stringify(changes));
      
      - name: AI Code Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python << 'EOF'
          import os
          import json
          from openai import OpenAI
          
          client = OpenAI(
              base_url="https://models.inference.ai.azure.com",
              api_key=os.getenv("GITHUB_TOKEN"),
          )
          
          changes = json.loads('${{ steps.changes.outputs.changes }}')
          
          reviews = []
          for change in changes:
              if not change['patch']:
                  continue
              
              messages = [
                  {
                      "role": "system",
                      "content": "You are a code review expert. Briefly point out issues in the code in English, no more than 50 words per issue. If there are no issues, reply 'Code looks good'."
                  },
                  {
                      "role": "user",
                      "content": f"File: {change['filename']}\n\nChanges:\n{change['patch']}"
                  }
              ]
              
              try:
                  response = client.chat.completions.create(
                      model="gpt-4o-mini",
                      messages=messages,
                      temperature=0.3,
                      max_tokens=500,
                  )
                  review = response.choices[0].message.content
                  reviews.append(f"**{change['filename']}**:\n{review}")
              except Exception as e:
                  reviews.append(f"**{change['filename']}**: Review failed - {str(e)}")
          
          # Output results
          with open('review_result.md', 'w') as f:
              f.write("## AI Code Review Results\n\n")
              f.write("\n\n---\n\n".join(reviews))
          
          EOF
      
      - name: Post review comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review_result.md', 'utf8');
            
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review,
            });
```

---

## Verifying Exercise Results

### Checklist

After completing the exercise, verify the following:

- [ ] Successfully configured GitHub Token
- [ ] Able to call the GitHub Models API
- [ ] Model comparison script runs normally and generates reports
- [ ] Code review assistant can analyze code
- [ ] Text summarization tool can generate summaries
- [ ] GitHub Actions workflow can automatically review PRs

### Verification Commands

```bash
# Test API connection
python -c "
from openai import OpenAI
import os
client = OpenAI(base_url='https://models.inference.ai.azure.com', api_key=os.getenv('GITHUB_TOKEN'))
response = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': 'Hello'}], max_tokens=10)
print('API connection successful:', response.choices[0].message.content)
"

# Run model comparison
python compare_models.py

# Check the generated report
cat model_comparison_report.md
```

---

## Advanced Challenges

### Challenge 1: Build a Multilingual Translation Assistant

Create a tool that supports translation between multiple languages:

```python
class TranslationAssistant:
    def translate(self, text, source_lang, target_lang):
        # Implement translation functionality
        pass
    
    def detect_language(self, text):
        # Implement language detection
        pass
```

### Challenge 2: Implement a Conversational AI Assistant

Create an assistant that supports multi-turn conversations:

```python
class ConversationalAssistant:
    def __init__(self):
        self.conversation_history = []
    
    def chat(self, message):
        # Maintain conversation history
        # Call model to generate response
        # Return response and update history
        pass
    
    def clear_history(self):
        self.conversation_history = []
```

### Challenge 3: Create a Documentation Generator

Use AI to automatically generate API documentation:

```python
def generate_api_docs(code):
    """
    Automatically generate API documentation from code
    """
    # Parse code structure
    # Generate documentation
    # Format output
    pass
```

### Challenge 4: Implement a Sentiment Analysis Tool

Create a tool that analyzes text sentiment:

```python
class SentimentAnalyzer:
    def analyze(self, text):
        """
        Analyze text sentiment
        Returns: {
            'sentiment': 'positive' | 'negative' | 'neutral',
            'confidence': 0.95,
            'keywords': ['keyword1', 'keyword2']
        }
        """
        pass
```

---

## Prompt Engineering Best Practices

### Basic Structure of Prompts

Prompt engineering is a core skill for using large language models. A good prompt typically contains several components: the system prompt defines the model's role and behavioral rules, such as specifying the model as a code review expert or technical documentation translator. The user prompt contains the specific task description and input data. Context information provides the model with necessary background knowledge to better understand the task. Output format requirements explicitly specify the desired output structure, such as using tables, lists, or specific markup languages.

### Prompt Optimization Techniques

There are several key techniques for improving model output quality. First, be specific in instructions and avoid vague descriptions, for example, change "write an article" to "introduce GitHub Actions core concepts in 300 words for beginners". Second, provide examples by giving input-output example pairs in the prompt to help the model learn the expected format and style. Third, use step-by-step thinking for complex tasks, guiding the model to reason step by step rather than providing answers directly. Fourth, role assignment by specifying a professional role for the model can significantly improve output professionalism and consistency. Fifth, constraint conditions by clearly specifying output length, language, style, and other limitations.

### Model Selection Guide

Different models are suitable for different task scenarios. For simple text classification and information extraction tasks, small models like GPT-4o-mini are sufficient, offering fast response times and low costs. For complex reasoning and creative writing tasks, it's recommended to use large models like GPT-4o or Claude. For code generation and code review tasks, models trained on code data should be selected. For multilingual tasks, models that support the target languages should be chosen. In practice, it's recommended to first use small models for prototype validation, then consider upgrading to large models only after confirming effectiveness.

### Token Management and Cost Control

When using large language models, token consumption directly impacts costs. Input tokens include the total length of system prompts, user prompts, and context information. Output tokens are the length of the model's generated response. To optimize costs, you can take the following measures: streamline system prompts by removing redundant descriptions. Control output length by using the `max_tokens` parameter to limit generation length. Use context window management by keeping only the most recent few rounds of conversation history. For structured output tasks, using JSON mode can reduce ineffective formatted text. For batch processing tasks, merge requests to reduce the number of API calls.

### Error Handling and Retry Strategies

Calling AI models in production environments requires robust error handling mechanisms. Common error types include rate limit errors, service unavailable errors, context length exceeded errors, and content filtering errors. For rate limit errors, it's recommended to use exponential backoff strategy for retries. For service unavailable errors, you can configure multiple models as fallback options. For context length exceeded, you need to implement automatic truncation or summarization mechanisms. For content filtering errors, you need to adjust input content or modify prompts. It's recommended to implement unified error handling middleware to centrally manage error handling logic for all model calls.

### Evaluation Metrics System

Establishing a scientific model evaluation system is crucial for selecting and optimizing models. Common evaluation metrics include accuracy metrics that measure the correctness of model output. Relevance metrics that measure how well model output matches user needs. Fluency metrics that measure the language quality of model output. Safety metrics that measure whether model output contains harmful or inappropriate content. Efficiency metrics include response time, token consumption, and concurrent processing capability. It's recommended to build an evaluation dataset containing various types of test cases and conduct regular benchmark testing of models.

### Data Privacy and Security

When using AI models, data privacy and security are issues that require special attention. Do not include sensitive personal information, trade secrets, or credential data in prompts. Understand the model provider's data usage policies and confirm whether input data will be used for model training. For enterprise application scenarios, it's recommended to use enterprise-level API services, which typically provide stricter data protection commitments. Implement data anonymization mechanisms to anonymize sensitive information before sending to models. Regularly review model usage logs to ensure no sensitive data leakage.

### Trade-offs Between Local and Cloud Models

Choosing between deploying models locally or using cloud APIs requires considering multiple factors. Advantages of local deployment include data staying within the local network, no network latency, no call costs, and complete controllability. Advantages of cloud APIs include no need to manage infrastructure, continuous model updates, support for larger-scale concurrency, and no need to invest in GPU hardware costs. For development and testing phases, it's recommended to use cloud APIs for rapid validation. For sensitive data processing in production environments, consider local deployment. A hybrid architecture is also an option, routing non-sensitive tasks to cloud APIs and using local models for sensitive tasks.

---

## Frequently Asked Questions

### Q1: Does GitHub Models have usage limits?

Yes, GitHub Models has rate limits:
- Per-minute request limits
- Daily request limits
- Specific limits depend on your GitHub plan

### Q2: How to choose the right model?

Consider the following when choosing a model:
- **Task type**: Use small models for simple tasks, large models for complex tasks
- **Response speed**: Small models are generally faster
- **Cost**: Large models consume more tokens
- **Quality**: Compare different models on test data

### Q3: How to handle API call failures?

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_model_with_retry(client, model, messages):
    return client.chat.completions.create(model=model, messages=messages)
```

### Q4: How to optimize model call costs?

1. Use caching to avoid redundant calls
2. Choose the appropriate model size
3. Limit output token count
4. Batch process requests

---

## Further Reading

- [GitHub Models Official Documentation](https://docs.github.com/en/github-models)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Prompt Engineering Guide](https://docs.github.com/en/github-models/prototyping-with-ai-models)

---

## Exercise Summary

Through this exercise, you have learned to:

1. ✅ Configure GitHub Models access
2. ✅ Use Python to call the GitHub Models API
3. ✅ Compare the performance and output quality of different models
4. ✅ Build a code review assistant and text summarization tool
5. ✅ Integrate AI models into GitHub Actions

GitHub Models provides developers with a convenient AI model testing platform. It's recommended to experiment with different models and prompts to find the solution that best fits your use case.

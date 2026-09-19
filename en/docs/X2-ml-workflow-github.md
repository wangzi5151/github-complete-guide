# Machine Learning Workflow on GitHub

> This document is aimed at Chinese developers, providing a comprehensive introduction to building efficient machine learning development workflows on GitHub.

---

## Table of Contents

1. [GitHub + Jupyter Notebook Collaboration](#1-github--jupyter-notebook-collaboration)
2. [GitHub Models Usage Guide](#2-github-models-usage-guide)
3. [ML Project Structure Best Practices](#3-ml-project-structure-best-practices)
4. [DVC Data Version Control](#4-dvc-data-version-control)
5. [ML Pipeline and GitHub Actions Integration](#5-ml-pipeline-and-github-actions-integration)
6. [Model Registration and Deployment](#6-model-registration-and-deployment)
7. [MLflow and GitHub Integration](#7-mlflow-and-github-integration)
8. [Hugging Face + GitHub Workflow](#8-hugging-face--github-workflow)
9. [GPU Runner and Self-Hosted Runner](#9-gpu-runner-and-self-hosted-runner)
10. [ML Project CI/CD Best Practices](#10-ml-project-cicd-best-practices)
11. [Large Model Project Management](#11-large-model-project-management)
12. [AI Safety and Responsible AI Development](#12-ai-safety-and-responsible-ai-development)
13. [Domestic ML Developer Toolchain](#13-domestic-ml-developer-toolchain)

---

## 1. GitHub + Jupyter Notebook Collaboration

### 1.1 Version Control Challenges with Jupyter Notebooks

Jupyter Notebooks (.ipynb files) are essentially JSON-formatted files containing code, outputs, metadata, and other information. Using Git directly for version control can encounter some issues:

```text
Common issues:
1. Output results (such as images, large blocks of text) cause files to become too large
2. Disordered execution order makes diffs difficult to read
3. Frequent metadata changes produce noise
4. Merge conflicts are hard to resolve
```

### 1.2 Configuring Git to Optimize Notebook Version Control

```bash
# Create .gitattributes file in the project root directory
*.ipynb filter=strip-notebook-output

# Configure Git filter
git config --global filter.strip-notebook-output.clean 'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR'
git config --global filter.strip-notebook-output.smudge cat
git config --global filter.strip-notebook-output.required true
```

```bash
# Use nbstripout tool (recommended)
pip install nbstripout

# Enable in the project
nbstripout --install

# .gitattributes auto-generated:
*.ipynb filter=strip-notebook-output
*.ipynb diff=ipynb
```

### 1.3 Notebook-Friendly Project Structure

```
ml-project/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_evaluation.ipynb
│   └── 05_inference.ipynb
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── dataset.py
│   │   └── preprocessing.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   └── custom_model.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   └── callbacks.py
│   └── utils/
│       ├── __init__.py
│       ├── metrics.py
│       └── visualization.py
├── configs/
│   ├── train_config.yaml
│   └── model_config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── models/
│   └── checkpoints/
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

### 1.4 Using ReviewNB for Notebook Review

```text
ReviewNB is GitHub's Notebook code review tool:

Features:
- Visual Notebook diff
- Line-level comments
- Rendered charts and outputs
- Integration with GitHub PRs

Installation:
1. Visit reviewnb.com
2. Install the GitHub App
3. Enable in repository settings

Usage:
- Automatically displays Notebook diff when creating a PR
- Can add comments on specific cells
- Supports viewing historical versions
```

### 1.5 JupyterLab Git Extension

```bash
# Install JupyterLab Git extension
pip install jupyterlab-git

# Configure JupyterLab
jupyter labextension install @jupyterlab/git

# Use in JupyterLab
# A Git icon will appear in the left sidebar
# Supports commit, push, pull and other operations
# Supports viewing diffs and history
```

---

## 2. GitHub Models Usage Guide

### 2.1 What Are GitHub Models

GitHub Models is an AI model testing platform provided by GitHub, allowing developers to test and evaluate various AI models directly on GitHub.

```text
Supported model categories:
1. Language Models (LLM)
   - GPT-4o, GPT-4o mini
   - Claude 3.5 Sonnet, Claude 3 Haiku
   - Llama 3.1, Mistral Large

2. Embedding Models
   - OpenAI text-embedding-3-small
   - Cohere embed-v3

3. Image Models
   - DALL-E 3
   - Stable Diffusion

4. Audio Models
   - Whisper (Speech Recognition)
   - TTS (Text-to-Speech)
```

### 2.2 Testing Models with GitHub Models

```text
Access method:
1. Visit github.com/marketplace/models
2. Select the model you want to test
3. Enter prompts in the Playground
4. View model responses

Playground features:
- Adjust model parameters (temperature, top_p, etc.)
- Compare responses from multiple models
- Save and share prompt templates
- View API call examples
```

### 2.3 Using GitHub Models via API

```python
# Using OpenAI SDK to call GitHub Models
from openai import OpenAI

# Initialize client (using GitHub Token)
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="your-github-token"
)

# Call GPT-4o model
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Please explain what machine learning is?"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

```python
# Using Azure AI SDK
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential("your-github-token")
)

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful AI assistant."),
        UserMessage(content="Please explain what deep learning is?")
    ],
    model="gpt-4o"
)

print(response.choices[0].message.content)
```

### 2.4 Model Evaluation and Comparison

```python
# Model evaluation script
import json
from openai import OpenAI

def evaluate_model(client, model_name, test_cases):
    """Evaluate model performance on test cases"""
    results = []
    
    for case in test_cases:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": case["system_prompt"]},
                {"role": "user", "content": case["input"]}
            ],
            temperature=0.0  # Use deterministic output
        )
        
        output = response.choices[0].message.content
        results.append({
            "input": case["input"],
            "expected": case["expected"],
            "actual": output,
            "correct": case["expected"].lower() in output.lower()
        })
    
    accuracy = sum(1 for r in results if r["correct"]) / len(results)
    return {
        "model": model_name,
        "accuracy": accuracy,
        "results": results
    }

# Test cases
test_cases = [
    {
        "input": "What is gradient descent?",
        "expected": "optimization algorithm",
        "system_prompt": "Answer in one sentence"
    },
    {
        "input": "What is overfitting?",
        "expected": "generalization ability",
        "system_prompt": "Answer in one sentence"
    }
]

# Compare multiple models
models = ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet"]
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="your-github-token"
)

for model in models:
    result = evaluate_model(client, model, test_cases)
    print(f"{model}: {result['accuracy']:.2%} accuracy")
```

---

## 3. ML Project Structure Best Practices

### 3.1 Standard Project Structure

```text
ml-project/
├── .github/
│   ├── workflows/
│   │   ├── train.yml         # Training pipeline
│   │   ├── evaluate.yml      # Evaluation pipeline
│   │   └── deploy.yml        # Deployment pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── CODEOWNERS
├── configs/
│   ├── data_config.yaml      # Data configuration
│   ├── model_config.yaml     # Model configuration
│   ├── train_config.yaml     # Training configuration
│   └── eval_config.yaml      # Evaluation configuration
├── data/
│   ├── raw/                  # Raw data (not committed to Git)
│   ├── processed/            # Processed data
│   └── features/             # Feature data
├── docs/
│   ├── data_dictionary.md    # Data dictionary
│   ├── model_card.md         # Model card
│   └── experiments.md        # Experiment records
├── models/
│   ├── checkpoints/          # Model checkpoints
│   └── final/                # Final model
├── notebooks/
│   ├── exploration/          # Exploratory analysis
│   ├── training/             # Training experiments
│   └── evaluation/           # Evaluation analysis
├── scripts/
│   ├── data_download.py      # Data download script
│   ├── preprocess.py         # Data preprocessing
│   ├── train.py              # Training script
│   ├── evaluate.py           # Evaluation script
│   └── predict.py            # Inference script
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── dataset.py        # Dataset class
│   │   ├── dataloader.py     # Data loader
│   │   └── transforms.py     # Data transformations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # Base model class
│   │   ├── layers.py         # Custom layers
│   │   └── architectures.py  # Model architectures
│   ├── training/
│   │   ├── __init__.py
│   │   ├── trainer.py        # Trainer
│   │   ├── losses.py         # Loss functions
│   │   └── optimizers.py     # Optimizers
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py        # Evaluation metrics
│   │   └── evaluator.py      # Evaluator
│   └── utils/
│       ├── __init__.py
│       ├── io.py             # I/O utilities
│       ├── logging.py        # Logging utilities
│       └── visualization.py  # Visualization utilities
├── tests/
│   ├── unit/
│   │   ├── test_data.py
│   │   ├── test_models.py
│   │   └── test_training.py
│   └── integration/
│       └── test_pipeline.py
├── .dvc/                     # DVC configuration
├── .env.example              # Environment variable template
├── .gitignore
├── .pre-commit-config.yaml
├── dvc.yaml                  # DVC pipeline
├── Makefile                  # Common commands
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md                 # Project documentation
```

### 3.2 Configuration Management

```yaml
# configs/train_config.yaml
project:
  name: "my-ml-project"
  version: "1.0.0"
  description: "Project description"

data:
  train_path: "data/processed/train.parquet"
  val_path: "data/processed/val.parquet"
  test_path: "data/processed/test.parquet"
  batch_size: 32
  num_workers: 4

model:
  architecture: "transformer"
  hidden_size: 768
  num_layers: 12
  num_heads: 12
  dropout: 0.1

training:
  epochs: 100
  learning_rate: 0.0001
  weight_decay: 0.01
  warmup_steps: 1000
  gradient_clip: 1.0
  save_every: 10
  eval_every: 5

logging:
  level: "INFO"
  wandb_project: "my-ml-project"
  log_dir: "logs/"
```

```python
# src/utils/config.py
from dataclasses import dataclass
from typing import Optional
import yaml
from pathlib import Path

@dataclass
class DataConfig:
    train_path: str
    val_path: str
    test_path: str
    batch_size: int = 32
    num_workers: int = 4

@dataclass
class ModelConfig:
    architecture: str
    hidden_size: int = 768
    num_layers: int = 12
    num_heads: int = 12
    dropout: float = 0.1

@dataclass
class TrainingConfig:
    epochs: int = 100
    learning_rate: float = 1e-4
    weight_decay: float = 0.01
    warmup_steps: int = 1000
    gradient_clip: float = 1.0

@dataclass
class Config:
    project: dict
    data: DataConfig
    model: ModelConfig
    training: TrainingConfig
    
    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        """Load configuration from YAML file"""
        with open(path) as f:
            config_dict = yaml.safe_load(f)
        
        return cls(
            project=config_dict["project"],
            data=DataConfig(**config_dict["data"]),
            model=ModelConfig(**config_dict["model"]),
            training=TrainingConfig(**config_dict["training"])
        )
    
    def save(self, path: str):
        """Save configuration to YAML file"""
        with open(path, "w") as f:
            yaml.dump(self.__dict__, f, default_flow_style=False)
```

### 3.3 Makefile for Managing Common Commands

```makefile
# Makefile
.PHONY: setup data train evaluate clean

# Install dependencies
setup:
	pip install -r requirements.txt
	pre-commit install

# Download and process data
data:
	python scripts/data_download.py
	python scripts/preprocess.py

# Train model
train:
	python scripts/train.py --config configs/train_config.yaml

# Evaluate model
evaluate:
	python scripts/evaluate.py --config configs/eval_config.yaml

# Run tests
test:
	pytest tests/ -v

# Code quality checks
lint:
	ruff check src/ scripts/ tests/
	mypy src/

# Clean generated files
clean:
	rm -rf data/processed/
	rm -rf models/checkpoints/*
	rm -rf logs/*

# Full pipeline
all: setup data train evaluate

# DVC commands
dvc-repro:
	dvc repro

dvc-push:
	dvc push

dvc-pull:
	dvc pull
```

---

## 4. DVC Data Version Control

### 4.1 What Is DVC

DVC (Data Version Control) is an open-source data version control tool specifically designed for machine learning projects. It solves the problem of versioning data and model files in ML projects.

```text
DVC core features:
1. Data version control: Manage data like Git manages code
2. Pipeline management: Define and reproduce ML pipelines
3. Experiment management: Track and compare experiment results
4. Remote storage: Support for multiple cloud storage backends
5. Model registry: Manage model versions and metadata
```

### 4.2 DVC Installation and Configuration

```bash
# Install DVC
pip install dvc

# Install specific storage backends
pip install dvc-s3      # AWS S3
pip install dvc-gs      # Google Cloud Storage
pip install dvc-azure   # Azure Blob Storage
pip install dvc-oss     # Alibaba Cloud OSS

# Initialize DVC
cd my-ml-project
dvc init

# Configure remote storage (using S3 as example)
dvc remote add -d storage s3://my-bucket/dvc-store
dvc remote modify storage access_key_id YOUR_ACCESS_KEY
dvc remote modify storage secret_access_key YOUR_SECRET_KEY

# Configure Alibaba Cloud OSS
dvc remote add -d oss-storage oss://my-bucket/dvc-store
dvc remote modify oss-storage oss_key_id YOUR_KEY_ID
dvc remote modify oss-storage oss_key_secret YOUR_KEY_SECRET
dvc remote modify oss-storage oss_endpoint oss-cn-hangzhou.aliyuncs.com
```

### 4.3 Data Version Control Practices

```bash
# Add data files to DVC tracking
dvc add data/raw/train.csv
dvc add data/raw/test.csv

# This will create .dvc files
# data/raw/train.csv.dvc
# data/raw/test.csv.dvc

# Commit DVC files to Git
git add data/raw/*.dvc .gitignore
git commit -m "Add training and test data"

# Push data to remote storage
dvc push

# Pull data
dvc pull

# View data version history
dvc dag
git log --oneline

# Switch to a specific version
git checkout v1.0
dvc checkout
```

### 4.4 DVC Pipeline Definition

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python scripts/preprocess.py --config configs/data_config.yaml
    deps:
      - data/raw/
      - scripts/preprocess.py
      - configs/data_config.yaml
    outs:
      - data/processed/train.parquet
      - data/processed/val.parquet
      - data/processed/test.parquet
    metrics:
      - data_stats.json:
          cache: false

  train:
    cmd: python scripts/train.py --config configs/train_config.yaml
    deps:
      - data/processed/
      - src/models/
      - src/training/
      - configs/train_config.yaml
    outs:
      - models/checkpoints/best_model.pt
    metrics:
      - train_metrics.json:
          cache: false
    plots:
      - logs/train_loss.csv:
          x: step
          y: loss

  evaluate:
    cmd: python scripts/evaluate.py --config configs/eval_config.yaml
    deps:
      - models/checkpoints/best_model.pt
      - data/processed/test.parquet
      - scripts/evaluate.py
    metrics:
      - eval_metrics.json:
          cache: false
    plots:
      - logs/confusion_matrix.png
      - logs/roc_curve.png
```

### 4.5 Experiment Management

```bash
# Run experiment
dvc exp run

# View experiment history
dvc exp show

# Compare experiments
dvc exp diff

# Create new experiment (modify parameters)
dvc exp run -S train_config.yaml:training.learning_rate=0.001
dvc exp run -S train_config.yaml:training.batch_size=64

# Name experiment
dvc exp run --name "lr-0.001-bs-64"

# Apply experiment results
dvc exp apply exp-name

# Remove experiment
dvc exp remove exp-name
```

---

## 5. ML Pipeline and GitHub Actions Integration

### 5.1 Training Pipeline Automation

```yaml
# .github/workflows/train.yml
name: ML Training Pipeline

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'configs/**'
      - 'scripts/**'
      - 'data/**/*.dvc'
  workflow_dispatch:
    inputs:
      epochs:
        description: 'Number of epochs'
        default: '100'
      learning_rate:
        description: 'Learning rate'
        default: '0.0001'

jobs:
  prepare-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Setup DVC
        uses: iterative/setup-dvc@v1
        with:
          version: '3.x'
          
      - name: Pull data
        run: dvc pull
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          
      - name: Prepare data
        run: python scripts/preprocess.py --config configs/data_config.yaml
        
      - name: Upload processed data
        uses: actions/upload-artifact@v4
        with:
          name: processed-data
          path: data/processed/

  train-model:
    needs: prepare-data
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Download processed data
        uses: actions/download-artifact@v4
        with:
          name: processed-data
          path: data/processed/
          
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Train model
        run: |
          python scripts/train.py \
            --config configs/train_config.yaml \
            --epochs ${{ github.event.inputs.epochs || '100' }} \
            --learning-rate ${{ github.event.inputs.learning_rate || '0.0001' }}
            
      - name: Upload model
        uses: actions/upload-artifact@v4
        with:
          name: trained-model
          path: models/checkpoints/best_model.pt

  evaluate-model:
    needs: train-model
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: models/checkpoints/
          
      - name: Download processed data
        uses: actions/download-artifact@v4
        with:
          name: processed-data
          path: data/processed/
          
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Evaluate model
        run: python scripts/evaluate.py --config configs/eval_config.yaml
        
      - name: Upload evaluation results
        uses: actions/upload-artifact@v4
        with:
          name: evaluation-results
          path: eval_metrics.json

  register-model:
    needs: evaluate-model
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
          path: models/checkpoints/
          
      - name: Download evaluation results
        uses: actions/download-artifact@v4
        with:
          name: evaluation-results
          
      - name: Register model
        run: |
          python scripts/register_model.py \
            --model-path models/checkpoints/best_model.pt \
            --metrics eval_metrics.json \
            --version ${{ github.sha }}
```

### 5.2 Model Evaluation Pipeline

```yaml
# .github/workflows/evaluate.yml
name: Model Evaluation

on:
  pull_request:
    paths:
      - 'src/models/**'
      - 'configs/model_config.yaml'
  schedule:
    - cron: '0 0 * * 0'  # Run every Sunday

jobs:
  evaluate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        dataset: ['test', 'validation', 'holdout']
        
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Pull data and model
        run: |
          dvc pull data/processed/${{ matrix.dataset }}.parquet
          dvc pull models/checkpoints/best_model.pt
          
      - name: Run evaluation
        run: |
          python scripts/evaluate.py \
            --dataset ${{ matrix.dataset }} \
            --output results/
            
      - name: Compare with baseline
        run: |
          python scripts/compare_results.py \
            --current results/metrics.json \
            --baseline baseline_metrics.json
            
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const metrics = JSON.parse(fs.readFileSync('results/metrics.json', 'utf8'));
            const body = `## Model Evaluation Results (${{ matrix.dataset }})
            
            | Metric | Value | Baseline | Change |
            |------|-----|------|------|
            | Accuracy | ${metrics.accuracy} | - | - |
            | F1 Score | ${metrics.f1} | - | - |
            | AUC-ROC | ${metrics.auc_roc} | - | - |
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

---

## 6. Model Registration and Deployment

### 6.1 GitHub Container Registry Model Registration

```python
# scripts/register_model.py
import argparse
import json
import datetime
from pathlib import Path
import hashlib

class ModelRegistry:
    def __init__(self, registry_path: str = "models/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        
    def register_model(
        self,
        model_path: str,
        metrics: dict,
        version: str,
        description: str = "",
        tags: list[str] = None
    ) -> dict:
        """Register model to the model registry"""
        model_path = Path(model_path)
        
        # Compute hash of the model file
        model_hash = self._compute_hash(model_path)
        
        # Create model metadata
        metadata = {
            "version": version,
            "registered_at": datetime.datetime.now().isoformat(),
            "model_path": str(model_path),
            "model_hash": model_hash,
            "metrics": metrics,
            "description": description,
            "tags": tags or [],
            "framework": "pytorch",  # or tensorflow, onnx, etc.
            "input_format": "tensor",
            "output_format": "class_probabilities"
        }
        
        # Save metadata
        version_dir = self.registry_path / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        with open(version_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Create latest symlink
        latest_link = self.registry_path / "latest"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(version_dir)
        
        print(f"Model registered: {version}")
        return metadata
        
    def get_model_info(self, version: str) -> dict:
        """Get model information"""
        metadata_path = self.registry_path / version / "metadata.json"
        with open(metadata_path) as f:
            return json.load(f)
            
    def list_models(self) -> list[dict]:
        """List all registered models"""
        models = []
        for version_dir in self.registry_path.iterdir():
            if version_dir.is_dir() and version_dir.name != "latest":
                metadata_path = version_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path) as f:
                        models.append(json.load(f))
        return sorted(models, key=lambda x: x["registered_at"], reverse=True)
        
    def _compute_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file"""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Register model to the model registry")
    parser.add_argument("--model-path", required=True, help="Model file path")
    parser.add_argument("--metrics", required=True, help="Evaluation metrics JSON file")
    parser.add_argument("--version", required=True, help="Model version")
    parser.add_argument("--description", default="", help="Model description")
    
    args = parser.parse_args()
    
    # Load evaluation metrics
    with open(args.metrics) as f:
        metrics = json.load(f)
        
    # Register model
    registry = ModelRegistry()
    metadata = registry.register_model(
        model_path=args.model_path,
        metrics=metrics,
        version=args.version,
        description=args.description
    )
    
    print(json.dumps(metadata, indent=2))
```

### 6.2 Model Deployment to GitHub Packages

```yaml
# .github/workflows/deploy-model.yml
name: Deploy Model to GitHub Packages

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Build and push model image
        run: |
          # Create Docker image containing the model
          docker build \
            --tag ghcr.io/${{ github.repository }}/model:${{ github.ref_name }} \
            --tag ghcr.io/${{ github.repository }}/model:latest \
            --build-arg MODEL_VERSION=${{ github.ref_name }} \
            .
          docker push ghcr.io/${{ github.repository }}/model:${{ github.ref_name }}
          docker push ghcr.io/${{ github.repository }}/model:latest
```

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model code
COPY src/ src/
COPY models/ models/
COPY scripts/ scripts/

# Copy model files
ARG MODEL_VERSION
COPY models/checkpoints/best_model.pt /app/models/best_model.pt

# Copy inference script
COPY scripts/serve.py /app/serve.py

# Expose port
EXPOSE 8000

# Start inference service
CMD ["python", "serve.py", "--model-path", "/app/models/best_model.pt"]
```

---

## 7. MLflow and GitHub Integration

### 7.1 MLflow Configuration

```python
# src/training/trainer_with_mlflow.py
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
import torch
from pathlib import Path

class MLflowTrainer:
    def __init__(self, config):
        self.config = config
        
        # Configure MLflow
        mlflow.set_tracking_uri(config.mlflow_tracking_uri)
        mlflow.set_experiment(config.experiment_name)
        
        self.client = MlflowClient()
        
    def train(self, model, train_loader, val_loader):
        """Train model and log to MLflow"""
        with mlflow.start_run(run_name=self.config.run_name) as run:
            # Log parameters
            mlflow.log_params({
                "learning_rate": self.config.learning_rate,
                "batch_size": self.config.batch_size,
                "epochs": self.config.epochs,
                "optimizer": self.config.optimizer,
                "model_architecture": self.config.model_architecture
            })
            
            # Training loop
            for epoch in range(self.config.epochs):
                train_loss = self._train_epoch(model, train_loader)
                val_loss, val_metrics = self._validate(model, val_loader)
                
                # Log metrics
                mlflow.log_metrics({
                    "train_loss": train_loss,
                    "val_loss": val_loss,
                    **val_metrics
                }, step=epoch)
                
                # Save checkpoint
                if epoch % self.config.save_every == 0:
                    checkpoint_path = f"checkpoints/model_epoch_{epoch}.pt"
                    torch.save(model.state_dict(), checkpoint_path)
                    mlflow.log_artifact(checkpoint_path)
                    
            # Save final model
            mlflow.pytorch.log_model(
                model,
                "model",
                registered_model_name=self.config.model_name
            )
            
            # Log model card
            mlflow.log_artifact("docs/model_card.md")
            
            return run.info.run_id
            
    def _train_epoch(self, model, train_loader):
        """Train for one epoch"""
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            loss = self._compute_loss(model, batch)
            loss.backward()
            self._optimizer.step()
            self._optimizer.zero_grad()
            total_loss += loss.item()
            
        return total_loss / len(train_loader)
        
    def _validate(self, model, val_loader):
        """Validate model"""
        model.eval()
        total_loss = 0
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for batch in val_loader:
                loss, predictions, targets = self._compute_validation(model, batch)
                total_loss += loss.item()
                all_predictions.extend(predictions)
                all_targets.extend(targets)
                
        # Compute evaluation metrics
        metrics = self._compute_metrics(all_predictions, all_targets)
        
        return total_loss / len(val_loader), metrics
```

### 7.2 MLflow and GitHub Actions Integration

```yaml
# .github/workflows/train-with-mlflow.yml
name: Train with MLflow Tracking

on:
  push:
    branches: [main]

jobs:
  train:
    runs-on: ubuntu-latest
    
    services:
      mlflow:
        image: ghcr.io/mlflow/mlflow:v2.x
        ports:
          - 5000:5000
        options: >-
          --health-cmd "curl -f http://localhost:5000/health || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install mlflow boto3
          
      - name: Configure MLflow
        run: |
          mlflow server \
            --backend-store-uri sqlite:///mlflow.db \
            --default-artifact-root ./mlruns \
            --host 0.0.0.0 \
            --port 5000 &
          sleep 5
          
      - name: Train model
        env:
          MLFLOW_TRACKING_URI: http://localhost:5000
        run: |
          python scripts/train.py \
            --config configs/train_config.yaml \
            --mlflow-tracking-uri http://localhost:5000
            
      - name: Upload MLflow artifacts
        uses: actions/upload-artifact@v4
        with:
          name: mlflow-runs
          path: mlruns/
          
      - name: Deploy model to MLflow Registry
        if: github.ref == 'refs/heads/main'
        env:
          MLFLOW_TRACKING_URI: http://localhost:5000
        run: |
          python scripts/register_to_mlflow.py \
            --model-name "production-model" \
            --stage "Production"
```

---

## 8. Hugging Face + GitHub Workflow

### 8.1 Hugging Face Hub Integration

```python
# src/models/huggingface_integration.py
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import HfApi, HfFolder, Repository
import torch

class HuggingFaceIntegration:
    def __init__(self, repo_name: str, token: str = None):
        self.repo_name = repo_name
        self.api = HfApi()
        self.token = token or HfFolder.get_token()
        
    def push_model(self, model, tokenizer, commit_message: str = "Update model"):
        """Push model to Hugging Face Hub"""
        # Save model and tokenizer
        model.save_pretrained("temp_model")
        tokenizer.save_pretrained("temp_model")
        
        # Push to Hub
        self.api.upload_folder(
            folder_path="temp_model",
            repo_id=self.repo_name,
            token=self.token,
            commit_message=commit_message
        )
        
    def load_model(self):
        """Load model from Hugging Face Hub"""
        model = AutoModel.from_pretrained(self.repo_name)
        tokenizer = AutoTokenizer.from_pretrained(self.repo_name)
        return model, tokenizer
        
    def create_model_card(self, model_card_content: str):
        """Create model card"""
        with open("README.md", "w") as f:
            f.write(model_card_content)
            
        self.api.upload_file(
            path_or_fileobj="README.md",
            path_in_repo="README.md",
            repo_id=self.repo_name,
            token=self.token,
            commit_message="Update model card"
        )
```

### 8.2 GitHub Actions Auto-Push to Hugging Face

```yaml
# .github/workflows/push-to-huggingface.yml
name: Push Model to Hugging Face

on:
  push:
    tags:
      - 'model-v*'

jobs:
  push-model:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install transformers huggingface_hub
          
      - name: Pull trained model
        run: dvc pull models/checkpoints/
        
      - name: Push to Hugging Face
        env:
          HUGGING_FACE_HUB_TOKEN: ${{ secrets.HUGGING_FACE_HUB_TOKEN }}
        run: |
          python scripts/push_to_huggingface.py \
            --model-path models/checkpoints/best_model.pt \
            --repo-name ${{ secrets.HF_REPO_NAME }} \
            --version ${{ github.ref_name }}
```

### 8.3 Using Hugging Face Spaces to Showcase Models

```yaml
# .github/workflows/deploy-to-spaces.yml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches: [main]
    paths:
      - 'app/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r app/requirements.txt
        
      - name: Deploy to Spaces
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          huggingface-cli login --token $HF_TOKEN
          git clone https://huggingface.co/spaces/${{ secrets.HF_SPACE_NAME }} space_repo
          cp -r app/* space_repo/
          cd space_repo
          git add .
          git commit -m "Deploy from GitHub Actions"
          git push
```

---

## 9. GPU Runner and Self-Hosted Runner

### 9.1 GitHub GPU Runner Configuration

```yaml
# Using GitHub-provided GPU Runner
jobs:
  train-gpu:
    runs-on: ubuntu-latest-gpu  # GPU Runner provided by GitHub
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install CUDA dependencies
        run: |
          pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
          
      - name: Verify GPU
        run: |
          python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}')"
          
      - name: Train model
        run: |
          python scripts/train.py --config configs/train_config.yaml --device cuda
```

### 9.2 Self-Hosted GPU Runner Setup

```yaml
# .github/workflows/self-hosted-gpu.yml
name: Train on Self-Hosted GPU

on:
  push:
    branches: [main]

jobs:
  train:
    runs-on: [self-hosted, gpu, linux]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup environment
        run: |
          source /opt/conda/etc/profile.d/conda.sh
          conda activate ml-project
          
      - name: Pull data
        run: dvc pull
        
      - name: Train with GPU
        env:
          CUDA_VISIBLE_DEVICES: "0,1"
        run: |
          python scripts/train.py \
            --config configs/train_config.yaml \
            --device cuda \
            --num-gpus 2
            
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: training-results
          path: |
            models/checkpoints/
            logs/
```

### 9.3 Self-Hosted Runner Installation Script

```bash
#!/bin/bash
# setup-gpu-runner.sh

# Install necessary software
sudo apt-get update
sudo apt-get install -y \
    curl \
    git \
    jq \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Install NVIDIA driver (if not present)
if ! command -v nvidia-smi &> /dev/null; then
    sudo apt-get install -y nvidia-driver-535
    sudo reboot
fi

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Download GitHub Actions Runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/latest/download/actions-runner-linux-x64.tar.gz
tar xzf actions-runner-linux-x64.tar.gz

# Configure Runner
./config.sh \
    --url https://github.com/YOUR_ORG/YOUR_REPO \
    --token YOUR_TOKEN \
    --labels gpu,self-hosted,linux \
    --name gpu-runner-01

# Install as service
sudo ./svc.sh install
sudo ./svc.sh start
```

---

## 10. ML Project CI/CD Best Practices

### 10.1 Code Quality Checks

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install linters
        run: |
          pip install ruff mypy pytest pytest-cov
          
      - name: Run Ruff
        run: ruff check src/ scripts/ tests/
        
      - name: Run MyPy
        run: mypy src/ --ignore-missing-imports
        
      - name: Run tests
        run: pytest tests/ -v --cov=src --cov-report=xml
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### 10.2 Data Validation

```yaml
# .github/workflows/data-validation.yml
name: Data Validation

on:
  push:
    paths:
      - 'data/**/*.dvc'
      - 'scripts/preprocess.py'

jobs:
  validate-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: pip install -r requirements.txt great_expectations
        
      - name: Pull data
        run: dvc pull
        
      - name: Validate data quality
        run: |
          python scripts/validate_data.py \
            --data-path data/raw/ \
            --expectations configs/data_expectations.json
            
      - name: Generate data report
        run: |
          python scripts/generate_data_report.py \
            --output data_report.html
            
      - name: Upload data report
        uses: actions/upload-artifact@v4
        with:
          name: data-report
          path: data_report.html
```

### 10.3 Model Performance Testing

```python
# tests/test_model_performance.py
import pytest
import torch
from src.models import load_model
from src.evaluation import ModelEvaluator

class TestModelPerformance:
    """Model performance tests"""
    
    @pytest.fixture
    def model(self):
        """Load test model"""
        return load_model("models/checkpoints/best_model.pt")
        
    @pytest.fixture
    def test_data(self):
        """Load test data"""
        return load_test_data("data/processed/test.parquet")
        
    def test_accuracy_threshold(self, model, test_data):
        """Test if accuracy meets the threshold"""
        evaluator = ModelEvaluator(model)
        metrics = evaluator.evaluate(test_data)
        
        assert metrics["accuracy"] >= 0.95, \
            f"Accuracy {metrics['accuracy']:.4f} is below threshold 0.95"
            
    def test_inference_latency(self, model, test_data):
        """Test inference latency"""
        sample_input = test_data[0]["input"]
        
        # Warmup
        for _ in range(10):
            model(sample_input)
            
        # Measure latency
        import time
        latencies = []
        for _ in range(100):
            start = time.time()
            model(sample_input)
            latencies.append(time.time() - start)
            
        avg_latency = sum(latencies) / len(latencies)
        p99_latency = sorted(latencies)[98]
        
        assert avg_latency < 0.05, \
            f"Average latency {avg_latency:.4f}s exceeds threshold 0.05s"
        assert p99_latency < 0.1, \
            f"P99 latency {p99_latency:.4f}s exceeds threshold 0.1s"
            
    def test_model_size(self, model):
        """Test model size"""
        model_size = sum(p.numel() for p in model.parameters()) * 4 / 1024 / 1024  # MB
        
        assert model_size < 500, \
            f"Model size {model_size:.2f}MB exceeds threshold 500MB"
            
    def test_memory_usage(self, model, test_data):
        """Test memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Batch inference
        for batch in test_data.batches(batch_size=32):
            model(batch["input"])
            
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        assert memory_increase < 2000, \
            f"Memory usage increase {memory_increase:.2f}MB exceeds threshold 2000MB"
```

### 10.4 Complete CI/CD Pipeline

```yaml
# .github/workflows/ml-cicd.yml
name: ML CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Stage 1: Code quality checks
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint and test
        run: |
          pip install ruff pytest
          ruff check .
          pytest tests/unit/ -v

  # Stage 2: Data validation
  data-validation:
    runs-on: ubuntu-latest
    needs: code-quality
    steps:
      - uses: actions/checkout@v4
      - name: Validate data
        run: python scripts/validate_data.py

  # Stage 3: Training
  training:
    runs-on: ubuntu-latest-gpu
    needs: data-validation
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Train model
        run: python scripts/train.py --config configs/train_config.yaml
      - name: Upload model
        uses: actions/upload-artifact@v4
        with:
          name: trained-model
          path: models/checkpoints/

  # Stage 4: Evaluation
  evaluation:
    runs-on: ubuntu-latest
    needs: training
    steps:
      - uses: actions/checkout@v4
      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model
      - name: Evaluate model
        run: python scripts/evaluate.py
      - name: Performance tests
        run: pytest tests/performance/ -v

  # Stage 5: Deployment
  deploy:
    runs-on: ubuntu-latest
    needs: evaluation
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy model
        run: python scripts/deploy.py
```

---

## 11. Large Model Project Management

### 11.1 Special Challenges of Large Model Projects

```text
Special characteristics of large model projects (such as LLM fine-tuning):

1. Large data scale
   - Training data may reach TB level
   - Requires efficient data processing pipelines
   - Data version management is more complex

2. High computational resource requirements
   - Requires multi-GPU training
   - Training time may span several days
   - Cost control is important

3. Model version management
   - Model files may reach tens of GB
   - Requires specialized storage solutions
   - Version traceability is important

4. Experiment management
   - Requires tracking large numbers of hyperparameters
   - Experiment comparison analysis is complex
   - Requires automated tool support
```

### 11.2 Large Model Project Structure

```text
llm-project/
├── data/
│   ├── raw/                  # Raw data
│   ├── processed/            # Processed data
│   ├── tokenized/            # Tokenized data
│   └── cache/                # Cached data
├── models/
│   ├── base/                 # Base model
│   ├── finetuned/            # Fine-tuned model
│   └── merged/               # Merged model
├── configs/
│   ├── lora_config.yaml      # LoRA configuration
│   ├── training_config.yaml  # Training configuration
│   └── inference_config.yaml # Inference configuration
├── scripts/
│   ├── prepare_dataset.py    # Data preparation
│   ├── finetune.py           # Fine-tuning script
│   ├── merge_adapters.py     # Merge LoRA weights
│   ├── evaluate.py           # Evaluation script
│   └── serve.py              # Inference service
├── src/
│   ├── data/
│   │   ├── dataset.py        # Dataset class
│   │   └── collator.py       # Data collator
│   ├── models/
│   │   ├── lora.py           # LoRA implementation
│   │   └── quantization.py   # Quantization tools
│   └── training/
│       ├── trainer.py        # Trainer
│       └── callbacks.py      # Callbacks
├── docker/
│   ├── Dockerfile.train      # Training container
│   └── Dockerfile.serve      # Inference container
└── README.md
```

### 11.3 Fine-Tuning Large Models with LoRA

```python
# scripts/finetune.py
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
import torch

def finetune_with_lora(config):
    """Fine-tune large model using LoRA"""
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        torch_dtype=torch.float16,
        device_map="auto",
        load_in_4bit=True  # 4-bit quantization
    )
    
    tokenizer = AutoTokenizer.from_pretrained(config.base_model)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Prepare model
    model = prepare_model_for_kbit_training(model)
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=config.lora_r,  # rank
        lora_alpha=config.lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation,
        learning_rate=config.learning_rate,
        weight_decay=0.01,
        warmup_steps=100,
        logging_steps=10,
        save_steps=500,
        evaluation_strategy="steps",
        eval_steps=500,
        fp16=True,
        optim="paged_adamw_8bit",
        lr_scheduler_type="cosine",
        max_grad_norm=0.3
    )
    
    # Create trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",
        max_seq_length=config.max_seq_length,
        packing=True
    )
    
    # Start training
    trainer.train()
    
    # Save LoRA weights
    model.save_pretrained(config.output_dir)
    
    return model

if __name__ == "__main__":
    from src.utils.config import Config
    config = Config.from_yaml("configs/training_config.yaml")
    finetune_with_lora(config)
```

### 11.4 GitHub Actions Large Model Training Pipeline

```yaml
# .github/workflows/llm-finetune.yml
name: LLM Fine-tuning

on:
  workflow_dispatch:
    inputs:
      base_model:
        description: 'Base model name'
        default: 'meta-llama/Llama-2-7b-hf'
      lora_r:
        description: 'LoRA rank'
        default: '16'
      epochs:
        description: 'Number of epochs'
        default: '3'

jobs:
  finetune:
    runs-on: [self-hosted, gpu, a100]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup environment
        run: |
          source /opt/conda/etc/profile.d/conda.sh
          conda activate llm-project
          
      - name: Pull data
        run: dvc pull data/tokenized/
        
      - name: Fine-tune model
        env:
          WANDB_API_KEY: ${{ secrets.WANDB_API_KEY }}
          HUGGING_FACE_HUB_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python scripts/finetune.py \
            --base-model ${{ github.event.inputs.base_model }} \
            --lora-r ${{ github.event.inputs.lora_r }} \
            --epochs ${{ github.event.inputs.epochs }} \
            --output-dir models/finetuned/
            
      - name: Merge LoRA weights
        run: |
          python scripts/merge_adapters.py \
            --base-model ${{ github.event.inputs.base_model }} \
            --adapter-path models/finetuned/ \
            --output-path models/merged/
            
      - name: Evaluate model
        run: |
          python scripts/evaluate.py \
            --model-path models/merged/ \
            --output eval_results.json
            
      - name: Push to Hugging Face
        if: success()
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python scripts/push_to_huggingface.py \
            --model-path models/merged/ \
            --repo-name ${{ secrets.HF_REPO_NAME }}
```

---

## 12. AI Safety and Responsible AI Development

### 12.1 AI Safety Checklist

```text
AI Safety Checklist:

1. Data Security
   □ Is the data source legally compliant
   □ Does it contain personal privacy information
   □ Has the data been anonymized
   □ Is the data stored in encrypted form

2. Model Security
   □ Has the model undergone adversarial testing
   □ Is there a backdoor attack risk
   □ Are model outputs filtered
   □ Is there a model watermarking mechanism

3. Deployment Security
   □ Does the API have access control
   □ Is there request rate limiting
   □ Is there input validation
   □ Is there monitoring and alerting

4. Compliance
   □ Does it comply with relevant regulations (such as the "Interim Measures for the Management of Generative Artificial Intelligence Services")
   □ Are there user agreements and privacy policies
   □ Is there a content moderation mechanism
   □ Is there a complaint handling process
```

### 12.2 Model Fairness Testing

```python
# src/evaluation/fairness.py
import numpy as np
from collections import defaultdict

class FairnessEvaluator:
    """Model fairness evaluator"""
    
    def __init__(self, model, protected_attributes: list[str]):
        self.model = model
        self.protected_attributes = protected_attributes
        
    def evaluate(self, dataset) -> dict:
        """Evaluate model fairness"""
        results = {}
        
        for attr in self.protected_attributes:
            # Group by protected attribute
            groups = self._group_by_attribute(dataset, attr)
            
            # Compute performance metrics for each group
            group_metrics = {}
            for group_name, group_data in groups.items():
                predictions = self.model.predict(group_data["features"])
                metrics = self._compute_metrics(predictions, group_data["labels"])
                group_metrics[group_name] = metrics
                
            # Compute fairness metrics
            results[attr] = {
                "group_metrics": group_metrics,
                "demographic_parity": self._demographic_parity(group_metrics),
                "equalized_odds": self._equalized_odds(group_metrics),
                "disparate_impact": self._disparate_impact(group_metrics)
            }
            
        return results
        
    def _demographic_parity(self, group_metrics: dict) -> float:
        """Demographic parity"""
        positive_rates = {}
        for group, metrics in group_metrics.items():
            positive_rates[group] = metrics["positive_rate"]
            
        max_rate = max(positive_rates.values())
        min_rate = min(positive_rates.values())
        
        return min_rate / max_rate if max_rate > 0 else 1.0
        
    def _equalized_odds(self, group_metrics: dict) -> float:
        """Equalized odds"""
        tpr_values = []
        fpr_values = []
        
        for group, metrics in group_metrics.items():
            tpr_values.append(metrics["true_positive_rate"])
            fpr_values.append(metrics["false_positive_rate"])
            
        tpr_diff = max(tpr_values) - min(tpr_values)
        fpr_diff = max(fpr_values) - min(fpr_values)
        
        return 1.0 - (tpr_diff + fpr_diff) / 2
        
    def _disparate_impact(self, group_metrics: dict) -> float:
        """Disparate impact ratio"""
        positive_rates = {}
        for group, metrics in group_metrics.items():
            positive_rates[group] = metrics["positive_rate"]
            
        rates = list(positive_rates.values())
        return min(rates) / max(rates) if max(rates) > 0 else 1.0
        
    def _group_by_attribute(self, dataset, attribute: str) -> dict:
        """Group data by attribute"""
        groups = defaultdict(lambda: {"features": [], "labels": []})
        
        for sample in dataset:
            group = sample[attribute]
            groups[group]["features"].append(sample["features"])
            groups[group]["labels"].append(sample["label"])
            
        return dict(groups)
        
    def _compute_metrics(self, predictions, labels) -> dict:
        """Compute evaluation metrics"""
        predictions = np.array(predictions)
        labels = np.array(labels)
        
        positive_rate = np.mean(predictions == 1)
        true_positive_rate = np.mean(predictions[labels == 1] == 1)
        false_positive_rate = np.mean(predictions[labels == 0] == 1)
        accuracy = np.mean(predictions == labels)
        
        return {
            "positive_rate": positive_rate,
            "true_positive_rate": true_positive_rate,
            "false_positive_rate": false_positive_rate,
            "accuracy": accuracy
        }
```

### 12.3 Content Safety Filtering

```python
# src/safety/content_filter.py
import re
from typing import Optional

class ContentSafetyFilter:
    """Content safety filter"""
    
    def __init__(self):
        # Sensitive word library (example, should use a more comprehensive library in practice)
        self.blocked_patterns = [
            r"(violence|bloody|pornographic)",
            r"(discrimination|hatred|insult)",
            r"(illegal|crime|terrorism)",
            r"(politically_sensitive_word1|politically_sensitive_word2)"
        ]
        
        # Compile regular expressions
        self.compiled_patterns = [re.compile(p) for p in self.blocked_patterns]
        
    def check(self, text: str) -> tuple[bool, Optional[str]]:
        """Check if text is safe
        
        Returns:
            (is_safe, reason): whether it is safe, and reason if unsafe
        """
        for pattern in self.compiled_patterns:
            match = pattern.search(text)
            if match:
                return False, f"Contains sensitive content: {match.group()}"
                
        return True, None
        
    def filter(self, text: str) -> str:
        """Filter sensitive content from text"""
        filtered_text = text
        
        for pattern in self.compiled_patterns:
            filtered_text = pattern.sub("***", filtered_text)
            
        return filtered_text
        
    def check_model_output(self, output: str, input_text: str = "") -> dict:
        """Check if model output is safe"""
        is_safe, reason = self.check(output)
        
        result = {
            "is_safe": is_safe,
            "original_output": output,
            "filtered_output": self.filter(output) if not is_safe else output
        }
        
        if reason:
            result["reason"] = reason
            
        return result
```

### 12.4 GitHub Actions Safety Check

```yaml
# .github/workflows/ai-safety.yml
name: AI Safety Check

on:
  pull_request:
    branches: [main]

jobs:
  safety-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install safety bandit
          
      - name: Check dependencies for vulnerabilities
        run: safety check
        
      - name: Run security linter
        run: bandit -r src/ -f json -o security_report.json || true
        
      - name: Run fairness tests
        run: pytest tests/fairness/ -v
        
      - name: Run safety tests
        run: pytest tests/safety/ -v
        
      - name: Upload security report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security_report.json
```

---

## 13. Domestic ML Developer Toolchain

### 13.1 Domestic Cloud Service Provider ML Platforms

```text
Major domestic ML platforms:

1. Alibaba Cloud - PAI (Platform for AI)
   - Advantages: Comprehensive features, integrated with Alibaba Cloud ecosystem
   - Use cases: Enterprise-level ML projects
   - URL: https://pai.console.aliyun.com/

2. Tencent Cloud - TI Platform
   - Advantages: Good integration with Tencent ecosystem
   - Use cases: AI applications in gaming and social sectors
   - URL: https://cloud.tencent.com/product/ti

3. Huawei Cloud - ModelArts
   - Advantages: Supports Ascend chips, domestic production
   - Use cases: Government and enterprise customers, domestic production requirements
   - URL: https://www.huaweicloud.com/product/modelarts.html

4. Baidu Intelligent Cloud - BML
   - Advantages: Pre-built Baidu AI capabilities
   - Use cases: NLP, CV domain applications
   - URL: https://cloud.baidu.com/product/bml

5. ByteDance - Volcano Engine
   - Advantages: Accumulated ML experience from ByteDance internally
   - Use cases: Recommendation systems, content understanding
   - URL: https://www.volcengine.com/product/ml-platform
```

### 13.2 Domestic MLOps Tools

```text
MLOps Tool Comparison:

1. MLflow (Open-source, International)
   - Advantages: Active community, comprehensive features
   - Disadvantages: Limited Chinese documentation, requires self-deployment
   - Suitable for: Teams with strong technical capabilities

2. Kubeflow (Open-source, International)
   - Advantages: Kubernetes-native, highly scalable
   - Disadvantages: Complex deployment, steep learning curve
   - Suitable for: Large-scale ML platforms

3. AutoDL (Domestic)
   - Advantages: Affordable GPU rental, simple operation
   - Disadvantages: Relatively simple features
   - Suitable for: Individual developers, small teams

4. QuDong Cloud (Domestic)
   - Advantages: Rich GPU resources, cost-effective
   - Disadvantages: Features still being improved
   - Suitable for: Teams needing GPU resources
```

### 13.3 Domestic Data Storage Solutions

```python
# Data storage configuration examples

# Alibaba Cloud OSS
import oss2

def setup_aliyun_oss():
    """Configure Alibaba Cloud OSS"""
    auth = oss2.Auth('your-access-key-id', 'your-access-key-secret')
    bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'your-bucket-name')
    
    # Upload file
    bucket.put_object('data/train.csv', open('data/train.csv', 'rb'))
    
    # Download file
    bucket.get_object_to_file('data/train.csv', 'downloaded_train.csv')

# Tencent Cloud COS
from qcloud_cos import CosConfig, CosS3Client

def setup_tencent_cos():
    """Configure Tencent Cloud COS"""
    config = CosConfig(
        Region='ap-guangzhou',
        SecretId='your-secret-id',
        SecretKey='your-secret-key'
    )
    client = CosS3Client(config)
    
    # Upload file
    client.upload_file(
        Bucket='your-bucket-name',
        Key='data/train.csv',
        LocalFilePath='data/train.csv'
    )

# Huawei Cloud OBS
from obs import ObsClient

def setup_huawei_obs():
    """Configure Huawei Cloud OBS"""
    client = ObsClient(
        access_key_id='your-access-key-id',
        secret_access_key='your-secret-access-key',
        server='https://obs.cn-hangzhou.myhuaweicloud.com'
    )
    
    # Upload file
    client.putFile(
        bucketName='your-bucket-name',
        objectKey='data/train.csv',
        file_path='data/train.csv'
    )
```

### 13.4 DVC Domestic Storage Configuration

```bash
# Configure Alibaba Cloud OSS as DVC remote storage
dvc remote add -d myremote oss://my-bucket/dvc-store
dvc remote modify myremote oss_key_id YOUR_KEY_ID
dvc remote modify myremote oss_key_secret YOUR_KEY_SECRET
dvc remote modify myremote oss_endpoint oss-cn-hangzhou.aliyuncs.com

# Configure Tencent Cloud COS
pip install dvc-cos
dvc remote add -d myremote cos://my-bucket/dvc-store
dvc remote modify myremote cos_secret_id YOUR_SECRET_ID
dvc remote modify myremote cos_secret_key YOUR_SECRET_KEY
dvc remote modify myremote cos_region ap-guangzhou

# Configure Huawei Cloud OBS
pip install dvc-obs
dvc remote add -d myremote obs://my-bucket/dvc-store
dvc remote modify myremote obs_access_key_id YOUR_KEY_ID
dvc remote modify myremote obs_secret_access_key YOUR_SECRET_KEY
dvc remote modify myremote obs_endpoint obs.cn-hangzhou.myhuaweicloud.com
```

### 13.5 Domestic ML Development Best Practices

```text
Domestic ML development recommendations:

1. Network optimization
   - Use domestic mirror sources (Tsinghua, Alibaba Cloud)
   - Prioritize storing model files in domestic storage
   - Use CDN to accelerate data transfer

2. Compliance
   - Comply with the "Data Security Law"
   - Comply with the "Personal Information Protection Law"
   - Comply with the "Interim Measures for the Management of Generative Artificial Intelligence Services"
   - Conduct cross-border data security assessments

3. Cost control
   - Choose appropriate GPU instances
   - Use Spot instances to reduce costs
   - Plan training tasks rationally

4. Team collaboration
   - Use Chinese documentation
   - Establish internal knowledge base
   - Regular technical sharing
```

```python
# Configure domestic pip mirror source
# ~/.pip/pip.conf
"""
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
"""

# Configure domestic Hugging Face mirror
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# Download model using mirror
from transformers import AutoModel

model = AutoModel.from_pretrained("bert-base-chinese")
```

### 13.6 Makefile Domestic Optimization Configuration

```makefile
# Makefile - Domestic optimized version

# Configure mirror source
.PHONY: setup-mirrors
setup-mirrors:
	pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
	pip config set install.trusted-host mirrors.aliyun.com
	echo "export HF_ENDPOINT=https://hf-mirror.com" >> ~/.bashrc

# Install dependencies (using domestic mirror)
.PHONY: install
install:
	pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Download model (using mirror)
.PHONY: download-model
download-model:
	HF_ENDPOINT=https://hf-mirror.com python scripts/download_model.py

# Configure DVC remote storage (Alibaba Cloud OSS)
.PHONY: setup-dvc
setup-dvc:
	dvc remote add -d myremote oss://my-bucket/dvc-store
	dvc remote modify myremote oss_key_id $(OSS_KEY_ID)
	dvc remote modify myremote oss_key_secret $(OSS_KEY_SECRET)
	dvc remote modify myremote oss_endpoint oss-cn-hangzhou.aliyuncs.com

# Train (using domestic W&B alternative)
.PHONY: train
train:
	python scripts/train.py --config configs/train_config.yaml --tracker none
```

---

## Conclusion

The machine learning workflow on GitHub has formed a complete ecosystem, from data version control to model deployment, from experiment management to CI/CD automation, with mature tools and best practices available for reference.

**Key Takeaways:**

1. **Version Control**: Use Git + DVC to manage code, data, and models
2. **Experiment Management**: Use MLflow or Weights & Biases to track experiments
3. **Automation**: Use GitHub Actions to build ML pipelines
4. **Collaboration**: Use GitHub's collaboration features (Issues, PR, Code Review)
5. **Deployment**: Use GitHub Packages and Container Registry to deploy models
6. **Security**: Follow AI safety best practices

**Next Steps:**

- Choose an ML tool stack that suits your project
- Establish a standardized project structure
- Configure CI/CD pipelines
- Establish experiment management workflows
- Pay attention to AI safety and compliance

---

> **Document Version:** v1.0  
> **Last Updated:** 2025  
> **Author:** GitHub Chinese Developer Community

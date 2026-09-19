# Exercise 30: Terraform + GitHub Actions Infrastructure Automation

## Learning Objectives

After completing this exercise, you will be able to:

- Understand the concepts and advantages of Infrastructure as Code (IaC)
- Write basic Terraform configuration files
- Use GitHub Actions to automate infrastructure deployment
- Manage infrastructure across multiple environments (development, staging, production)
- Implement version control and auditing for infrastructure

## Prerequisites

- A GitHub repository
- A cloud service account (AWS, Azure, or GCP)
- Understanding of basic cloud service concepts
- Completion of the GitHub Actions basics exercise

## Background Knowledge

### What is Infrastructure as Code

Infrastructure as Code (IaC) is a method of managing and configuring infrastructure through code:

1. **Declarative Configuration**: Define the desired infrastructure state
2. **Version Control**: Store configuration code in a version control system
3. **Automated Deployment**: Automatically create and update infrastructure through tools
4. **Repeatability**: Ensure consistency across environments

### Introduction to Terraform

Terraform is an Infrastructure as Code tool developed by HashiCorp:

- **Multi-Cloud Support**: Supports major cloud platforms such as AWS, Azure, GCP
- **State Management**: Tracks the current state of infrastructure
- **Plan and Apply**: Preview changes before executing them
- **Modular**: Supports code reuse and organization

### GitHub Actions Integration

GitHub Actions can be combined with Terraform to achieve:

- Automated infrastructure deployment
- Automatic planning on Pull Requests
- Multi-environment management
- Security scanning and compliance checks

---

## Exercise Steps

### Part 1: Terraform Basic Configuration

#### Step 1: Install Terraform

**macOS:**

```bash
# Using Homebrew
brew install terraform

# Or using tfenv version manager
brew install tfenv
tfenv install 1.7.0
tfenv use 1.7.0
```

**Linux:**

```bash
# Download Terraform
wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip

# Extract
unzip terraform_1.7.0_linux_amd64.zip

# Move to PATH
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
```

**Windows:**

```bash
# Using Chocolatey
choco install terraform

# Or using Scoop
scoop install terraform

# Or using tfenv
scoop install tfenv
tfenv install 1.7.0
tfenv use 1.7.0
```

#### Step 2: Create Project Directory Structure

```bash
# Create project structure
mkdir -p terraform-github-demo/{environments/{dev,staging,prod},modules/network,scripts}

# View directory structure
tree terraform-github-demo/
```

Expected output:

```
terraform-github-demo/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── modules/
│   └── network/
└── scripts/
```

#### Step 3: Create Basic Terraform Configuration

Create file `terraform-github-demo/main.tf`:

```hcl
# Configure Terraform provider
terraform {
  required_version = ">= 1.7.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Remote state storage (recommended)
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Configure AWS provider
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
      Repository  = var.repository
    }
  }
}

# Define variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "my-project"
}

variable "repository" {
  description = "GitHub repository URL"
  type        = string
  default     = "github.com/username/repo"
}

# Output values
output "environment" {
  description = "Current environment"
  value       = var.environment
}

output "region" {
  description = "AWS region"
  value       = var.aws_region
}
```

#### Step 4: Create Network Module

Create file `terraform-github-demo/modules/network/main.tf`:

```hcl
# Network module - Create VPC and subnets

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "private_subnet_cidrs" {
  description = "List of private subnet CIDRs"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "List of public subnet CIDRs"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# Create VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.environment}-vpc"
  }
}

# Create internet gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.environment}-igw"
  }
}

# Create public subnets
resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.environment}-public-subnet-${count.index + 1}"
    Tier = "Public"
  }
}

# Create private subnets
resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.environment}-private-subnet-${count.index + 1}"
    Tier = "Private"
  }
}

# Create public subnet route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.environment}-public-rt"
  }
}

# Associate public subnets with route table
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Output values
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

#### Step 5: Create Environment Configuration

Create file `terraform-github-demo/environments/dev/main.tf`:

```hcl
# Development environment configuration

terraform {
  required_version = ">= 1.7.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Development environment state file
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      Environment = "dev"
      Project     = "my-project"
      ManagedBy   = "Terraform"
    }
  }
}

# Invoke the network module
module "network" {
  source = "../../modules/network"
  
  environment = "dev"
  vpc_cidr    = "10.0.0.0/16"
  
  availability_zones    = ["us-east-1a", "us-east-1b"]
  private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet_cidrs  = ["10.0.101.0/24", "10.0.102.0/24"]
}

# Output values
output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}
```

Create file `terraform-github-demo/environments/dev/terraform.tfvars`:

```hcl
# Development environment variables
aws_region   = "us-east-1"
environment  = "dev"
project_name = "my-project"
```

#### Step 6: Create Production Environment Configuration

Create file `terraform-github-demo/environments/prod/main.tf`:

```hcl
# Production environment configuration

terraform {
  required_version = ">= 1.7.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Production environment state file
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      Environment = "prod"
      Project     = "my-project"
      ManagedBy   = "Terraform"
    }
  }
}

# Invoke the network module
module "network" {
  source = "../../modules/network"
  
  environment = "prod"
  vpc_cidr    = "10.1.0.0/16"
  
  availability_zones    = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnet_cidrs = ["10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]
  public_subnet_cidrs  = ["10.1.101.0/24", "10.1.102.0/24", "10.1.103.0/24"]
}

# Output values
output "vpc_id" {
  value = module.network.vpc_id
}

output "public_subnet_ids" {
  value = module.network.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.network.private_subnet_ids
}
```

### Part 2: GitHub Actions Integration

#### Step 7: Create Terraform Plan Workflow

Create file `.github/workflows/terraform-plan.yml`:

```yaml
name: Terraform Plan

on:
  pull_request:
    branches: [main]
    paths:
      - 'terraform-github-demo/**'
      - '.github/workflows/terraform-*'

permissions:
  contents: read
  pull-requests: write
  id-token: write

env:
  TF_VERSION: '1.7.0'
  AWS_REGION: 'us-east-1'

jobs:
  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Terraform format check
        run: terraform fmt -check -recursive
        working-directory: terraform-github-demo
      
      - name: Terraform init
        run: terraform init
        working-directory: terraform-github-demo/environments/${{ matrix.environment }}
      
      - name: Terraform validate
        run: terraform validate
        working-directory: terraform-github-demo/environments/${{ matrix.environment }}
      
      - name: Terraform plan
        id: plan
        run: |
          terraform plan -no-color -out=tfplan
        working-directory: terraform-github-demo/environments/${{ matrix.environment }}
        continue-on-error: true
      
      - name: Generate plan output
        run: |
          terraform show -no-color tfplan > plan_output.txt
        working-directory: terraform-github-demo/environments/${{ matrix.environment }}
      
      - name: Add PR comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const planOutput = fs.readFileSync(
              `terraform-github-demo/environments/${{ matrix.environment }}/plan_output.txt`,
              'utf8'
            );
            
            const environment = '${{ matrix.environment }}';
            const planStatus = '${{ steps.plan.outcome }}';
            const emoji = planStatus === 'success' ? '✅' : '❌';
            
            const body = `## ${emoji} Terraform Plan - ${environment}
            
            \`\`\`
            ${planOutput.substring(0, 60000)}
            \`\`\`
            
            **Status:** ${planStatus}
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
      
      - name: Check plan result
        if: steps.plan.outcome == 'failure'
        run: exit 1
```

#### Step 8: Create Terraform Apply Workflow

Create file `.github/workflows/terraform-apply.yml`:

```yaml
name: Terraform Apply

on:
  push:
    branches: [main]
    paths:
      - 'terraform-github-demo/**'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod
      action:
        description: 'Action to execute'
        required: true
        type: choice
        options:
          - plan
          - apply
          - destroy

permissions:
  contents: read
  id-token: write

env:
  TF_VERSION: '1.7.0'
  AWS_REGION: 'us-east-1'

jobs:
  terraform-apply:
    name: Terraform Apply
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'dev' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Determine environment
        id: env
        run: |
          if [ "${{ github.event_name }}" = "workflow_dispatch" ]; then
            echo "environment=${{ github.event.inputs.environment }}" >> $GITHUB_OUTPUT
          else
            echo "environment=dev" >> $GITHUB_OUTPUT
          fi
      
      - name: Terraform init
        run: terraform init
        working-directory: terraform-github-demo/environments/${{ steps.env.outputs.environment }}
      
      - name: Terraform plan
        run: terraform plan -out=tfplan
        working-directory: terraform-github-demo/environments/${{ steps.env.outputs.environment }}
      
      - name: Terraform apply
        if: |
          (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
          (github.event_name == 'workflow_dispatch' && github.event.inputs.action == 'apply')
        run: terraform apply -auto-approve tfplan
        working-directory: terraform-github-demo/environments/${{ steps.env.outputs.environment }}
      
      - name: Terraform destroy
        if: github.event_name == 'workflow_dispatch' && github.event.inputs.action == 'destroy'
        run: terraform destroy -auto-approve
        working-directory: terraform-github-demo/environments/${{ steps.env.outputs.environment }}
      
      - name: Output result
        run: |
          echo "Environment: ${{ steps.env.outputs.environment }}"
          echo "Operation completed"
```

#### Step 9: Create Multi-Environment Deployment Workflow

Create file `.github/workflows/terraform-multi-env.yml`:

```yaml
name: Terraform Multi-Environment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Select environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod
      action:
        description: 'Action to execute'
        required: true
        type: choice
        options:
          - plan
          - apply
          - destroy

permissions:
  contents: read
  id-token: write

env:
  TF_VERSION: '1.7.0'

jobs:
  # Approval job (required for production)
  approval:
    name: Approval Required
    runs-on: ubuntu-latest
    if: github.event.inputs.environment == 'prod'
    environment: production-approval
    
    steps:
      - name: Wait for approval
        run: echo "Production deployment has been approved"

  # Terraform job
  terraform:
    name: Terraform ${{ github.event.inputs.action }}
    runs-on: ubuntu-latest
    needs: [approval]
    if: always() && (needs.approval.result == 'success' || github.event.inputs.environment != 'prod')
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: 'us-east-1'
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ env.TF_VERSION }}
      
      - name: Terraform init
        run: terraform init
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Terraform plan
        id: plan
        run: terraform plan -no-color -out=tfplan
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Terraform apply
        if: github.event.inputs.action == 'apply'
        run: terraform apply -auto-approve tfplan
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Terraform destroy
        if: github.event.inputs.action == 'destroy'
        run: terraform destroy -auto-approve
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Generate report
        if: always()
        run: |
          echo "# Terraform Deployment Report" > report.md
          echo "" >> report.md
          echo "## Environment: ${{ github.event.inputs.environment }}" >> report.md
          echo "## Action: ${{ github.event.inputs.action }}" >> report.md
          echo "## Status: ${{ job.status }}" >> report.md
          echo "## Time: $(date)" >> report.md
      
      - name: Upload report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: terraform-report-${{ github.event.inputs.environment }}
          path: report.md
```

### Part 3: Advanced Configuration

#### Step 10: Create Terraform Backend Configuration

Create file `terraform-github-demo/backend/main.tf`:

```hcl
# Backend resource creation (needs to be created manually first)

provider "aws" {
  region = "us-east-1"
}

# S3 bucket for storing state
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket"
  
  lifecycle {
    prevent_destroy = true
  }
  
  tags = {
    Name        = "Terraform State Bucket"
    Environment = "shared"
    ManagedBy   = "Terraform"
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  tags = {
    Name        = "Terraform Lock Table"
    Environment = "shared"
    ManagedBy   = "Terraform"
  }
}

# Output values
output "s3_bucket_name" {
  description = "State bucket name"
  value       = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  description = "Lock table name"
  value       = aws_dynamodb_table.terraform_locks.name
}
```

#### Step 11: Create Security Scan Workflow

Create file `.github/workflows/terraform-security.yml`:

```yaml
name: Terraform Security Scan

on:
  pull_request:
    branches: [main]
    paths:
      - 'terraform-github-demo/**'

permissions:
  contents: read
  pull-requests: write

jobs:
  tfsec:
    name: tfsec Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run tfsec
        uses: aquasecurity/tfsec-action@v1.0.3
        with:
          working_directory: terraform-github-demo
          soft_fail: true
      
      - name: Upload tfsec SARIF report
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: tfsec.sarif
  
  checkov:
    name: Checkov Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform-github-demo
          soft_fail: true
          output_format: sarif
          output_file_path: checkov.sarif
      
      - name: Upload Checkov SARIF report
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: checkov.sarif
  
  infracost:
    name: Infracost Estimate
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Infracost
        uses: infracost/actions/setup@v2
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
      
      - name: Generate cost estimate
        run: |
          infracost breakdown --path terraform-github-demo/environments/dev \
            --format json \
            --out-file infracost.json
      
      - name: Add PR comment
        uses: infracost/actions/comment@v2
        with:
          path: infracost.json
          behavior: update
```

#### Step 12: Create State Management Workflow

Create file `.github/workflows/terraform-state.yml`:

```yaml
name: Terraform State Management

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - dev
          - staging
          - prod
      action:
        description: 'Action'
        required: true
        type: choice
        options:
          - list
          - show
          - mv
          - rm
          - import
      resource:
        description: 'Resource address (for mv/rm/import)'
        required: false
        type: string
      target:
        description: 'Target address (for mv)'
        required: false
        type: string

permissions:
  contents: read
  id-token: write

jobs:
  state-management:
    name: State Management
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: 'us-east-1'
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: '1.7.0'
      
      - name: Terraform init
        run: terraform init
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: List resources
        if: github.event.inputs.action == 'list'
        run: terraform state list
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Show resource
        if: github.event.inputs.action == 'show'
        run: terraform state show "${{ github.event.inputs.resource }}"
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Move resource
        if: github.event.inputs.action == 'mv'
        run: |
          terraform state mv \
            "${{ github.event.inputs.resource }}" \
            "${{ github.event.inputs.target }}"
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Remove resource
        if: github.event.inputs.action == 'rm'
        run: terraform state rm "${{ github.event.inputs.resource }}"
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
      
      - name: Import resource
        if: github.event.inputs.action == 'import'
        run: |
          terraform import \
            "${{ github.event.inputs.resource }}" \
            "${{ github.event.inputs.target }}"
        working-directory: terraform-github-demo/environments/${{ github.event.inputs.environment }}
```

### Part 4: Utility Scripts

#### Step 13: Create Initialization Script

Create file `terraform-github-demo/scripts/init.sh`:

```bash
#!/bin/bash

# Terraform initialization script

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print help information
show_help() {
    echo "Terraform Initialization Tool"
    echo ""
    echo "Usage: $0 [options] <environment>"
    echo ""
    echo "Environments:"
    echo "  dev      - Development environment"
    echo "  staging  - Staging environment"
    echo "  prod     - Production environment"
    echo ""
    echo "Options:"
    echo "  -h, --help   Show help information"
    echo "  -f, --force  Force reinitialization"
}

# Initialize environment
init_environment() {
    local env=$1
    local force=$2
    
    echo -e "${GREEN}=== Initializing ${env} environment ===${NC}"
    echo ""
    
    # Check environment directory
    if [ ! -d "environments/${env}" ]; then
        echo -e "${RED}Error: Environment directory does not exist: environments/${env}${NC}"
        exit 1
    fi
    
    # Enter environment directory
    cd "environments/${env}"
    
    # Check if force initialization is needed
    if [ "$force" = "true" ] && [ -d ".terraform" ]; then
        echo -e "${YELLOW}Clearing existing Terraform state...${NC}"
        rm -rf .terraform .terraform.lock.hcl
    fi
    
    # Initialize Terraform
    echo "Initializing Terraform..."
    terraform init
    
    # Validate configuration
    echo ""
    echo "Validating configuration..."
    terraform validate
    
    # Format check
    echo ""
    echo "Checking code format..."
    terraform fmt -check
    
    echo ""
    echo -e "${GREEN}Initialization complete!${NC}"
    
    # Show workspace information
    echo ""
    echo "Current workspace:"
    terraform workspace list
    
    # Return to original directory
    cd ../..
}

# Main logic
FORCE=false
ENV=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        dev|staging|prod)
            ENV=$1
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

if [ -z "$ENV" ]; then
    echo -e "${RED}Error: Please specify an environment${NC}"
    show_help
    exit 1
fi

init_environment "$ENV" "$FORCE"
```

#### Step 14: Create Deployment Script

Create file `terraform-github-demo/scripts/deploy.sh`:

```bash
#!/bin/bash

# Terraform deployment script

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Print help information
show_help() {
    echo "Terraform Deployment Tool"
    echo ""
    echo "Usage: $0 [options] <environment> <action>"
    echo ""
    echo "Environments:"
    echo "  dev      - Development environment"
    echo "  staging  - Staging environment"
    echo "  prod     - Production environment"
    echo ""
    echo "Actions:"
    echo "  plan     - View change plan"
    echo "  apply    - Apply changes"
    echo "  destroy  - Destroy resources"
    echo "  output   - Show outputs"
    echo ""
    echo "Options:"
    echo "  -h, --help         Show help information"
    echo "  -y, --auto-approve Auto-confirm"
    echo "  -var-file=FILE     Specify variable file"
}

# Deployment function
deploy() {
    local env=$1
    local action=$2
    local auto_approve=$3
    local var_file=$4
    
    echo -e "${GREEN}=== ${env} environment - ${action} ===${NC}"
    echo ""
    
    # Check environment directory
    if [ ! -d "environments/${env}" ]; then
        echo -e "${RED}Error: Environment directory does not exist: environments/${env}${NC}"
        exit 1
    fi
    
    # Enter environment directory
    cd "environments/${env}"
    
    # Build command arguments
    local cmd_args=""
    if [ -n "$var_file" ]; then
        cmd_args="-var-file=${var_file}"
    fi
    
    # Execute action
    case $action in
        plan)
            echo "Generating change plan..."
            terraform plan $cmd_args
            ;;
        apply)
            echo "Applying changes..."
            if [ "$auto_approve" = "true" ]; then
                terraform apply -auto-approve $cmd_args
            else
                terraform apply $cmd_args
            fi
            ;;
        destroy)
            echo -e "${YELLOW}Warning: About to destroy all resources!${NC}"
            if [ "$auto_approve" = "true" ]; then
                terraform destroy -auto-approve $cmd_args
            else
                terraform destroy $cmd_args
            fi
            ;;
        output)
            echo "Output values:"
            terraform output
            ;;
        *)
            echo -e "${RED}Unknown action: $action${NC}"
            exit 1
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}Operation completed!${NC}"
    
    # Return to original directory
    cd ../..
}

# Main logic
AUTO_APPROVE=false
VAR_FILE=""
ENV=""
ACTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -y|--auto-approve)
            AUTO_APPROVE=true
            shift
            ;;
        -var-file=*)
            VAR_FILE="${1#*=}"
            shift
            ;;
        dev|staging|prod)
            ENV=$1
            shift
            ;;
        plan|apply|destroy|output)
            ACTION=$1
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

if [ -z "$ENV" ] || [ -z "$ACTION" ]; then
    echo -e "${RED}Error: Please specify environment and action${NC}"
    show_help
    exit 1
fi

deploy "$ENV" "$ACTION" "$AUTO_APPROVE" "$VAR_FILE"
```

#### Step 15: Create Terraform Documentation Generation Script

Create file `terraform-github-demo/scripts/generate-docs.sh`:

```bash
#!/bin/bash

# Terraform documentation generation script

set -e

# Color definitions
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}=== Generating Terraform Documentation ===${NC}"
echo ""

# Check if terraform-docs is installed
if ! command -v terraform-docs &> /dev/null; then
    echo "Installing terraform-docs..."
    
    # Detect operating system
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install terraform-docs
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -sSLo terraform-docs.tar.gz https://github.com/terraform-docs/terraform-docs/releases/download/v0.16.0/terraform-docs-v0.16.0-linux-amd64.tar.gz
        tar -xzf terraform-docs.tar.gz
        sudo mv terraform-docs /usr/local/bin/
        rm terraform-docs.tar.gz
    fi
fi

# Generate module documentation
echo "Generating module documentation..."
for module_dir in modules/*/; do
    if [ -d "$module_dir" ]; then
        module_name=$(basename "$module_dir")
        echo "  - ${module_name}"
        
        # Generate Markdown documentation
        terraform-docs markdown table "${module_dir}" > "${module_dir}/README.md"
    fi
done

# Generate environment documentation
echo ""
echo "Generating environment documentation..."
for env_dir in environments/*/; do
    if [ -d "$env_dir" ]; then
        env_name=$(basename "$env_dir")
        echo "  - ${env_name}"
        
        # Generate Markdown documentation
        terraform-docs markdown table "${env_dir}" > "${env_dir}/README.md"
    fi
done

# Generate main README
echo ""
echo "Generating main README..."
cat > README.md << 'EOF'
# Terraform GitHub Demo

This project demonstrates how to use Terraform and GitHub Actions to manage cloud infrastructure.

## Project Structure

```
.
├── environments/          # Environment configurations
│   ├── dev/              # Development environment
│   ├── staging/          # Staging environment
│   └── prod/             # Production environment
├── modules/              # Reusable modules
│   └── network/          # Network module
├── scripts/              # Utility scripts
└── .github/workflows/    # GitHub Actions workflows
```

## Quick Start

### Initialize Environment

```bash
# Initialize development environment
./scripts/init.sh dev

# Initialize staging environment
./scripts/init.sh staging

# Initialize production environment
./scripts/init.sh prod
```

### Deploy Resources

```bash
# View change plan
./scripts/deploy.sh dev plan

# Apply changes
./scripts/deploy.sh dev apply

# Destroy resources
./scripts/deploy.sh dev destroy
```

### Generate Documentation

```bash
./scripts/generate-docs.sh
```

## GitHub Actions Workflows

- `terraform-plan.yml` - Automatic planning on PR
- `terraform-apply.yml` - Automatic deployment after merge
- `terraform-multi-env.yml` - Multi-environment deployment
- `terraform-security.yml` - Security scanning
- `terraform-state.yml` - State management

## Best Practices

1. Use remote state storage
2. Enable state locking
3. Use variable files to manage environment differences
4. Review change plans in PRs
5. Use GitHub Environments to protect production
6. Run security scans regularly

## Security Considerations

- Never hardcode credentials in code
- Use GitHub Secrets to store sensitive information
- Enable state encryption
- Restrict IAM permissions
- Audit infrastructure changes regularly
EOF

echo ""
echo -e "${GREEN}Documentation generation complete!${NC}"
```

```bash
# Make scripts executable
chmod +x terraform-github-demo/scripts/*.sh
```

---

## Verify Exercise Results

### Checklist

After completing the exercise, verify the following:

- [ ] Terraform is installed correctly
- [ ] Project directory structure is created
- [ ] Terraform configuration file syntax is correct
- [ ] GitHub Actions workflows are created
- [ ] Script files are executable

### Verification Commands

```bash
# Check Terraform installation
terraform version

# Validate configuration files
cd terraform-github-demo/environments/dev
terraform init -backend=false
terraform validate
terraform fmt -check

# Check workflow syntax
actionlint .github/workflows/terraform-*.yml

# Check scripts
bash -n terraform-github-demo/scripts/init.sh
bash -n terraform-github-demo/scripts/deploy.sh
```

---

## Advanced Challenges

### Challenge 1: Implement Terraform Cloud Integration

Use Terraform Cloud instead of S3 backend:

```hcl
terraform {
  cloud {
    organization = "your-org"
    
    workspaces {
      name = "my-project-dev"
    }
  }
}
```

### Challenge 2: Create a Custom Terraform Provider

Develop a simple Terraform Provider:

```go
package main

import (
    "github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
    "github.com/hashicorp/terraform-plugin-sdk/v2/plugin"
)

func main() {
    plugin.Serve(&plugin.ServeOpts{
        ProviderFunc: func() *schema.Provider {
            return Provider()
        },
    })
}
```

### Challenge 3: Implement Infrastructure Drift Detection

Create a workflow that periodically detects infrastructure drift:

```yaml
name: Drift Detection

on:
  schedule:
    - cron: '0 8 * * 1'  # Every Monday at 8am

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Detect drift
        run: |
          terraform plan -detailed-exitcode
          if [ $? -eq 2 ]; then
            echo "Infrastructure drift detected!"
            exit 1
          fi
```

### Challenge 4: Implement Cost Optimization Recommendations

Use Infracost to analyze and provide cost optimization recommendations:

```yaml
- name: Cost optimization analysis
  run: |
    infracost diff --path terraform-github-demo/environments/dev \
      --format json \
      --out-file infracost-diff.json
    
    # Analyze cost changes
    python scripts/analyze-cost.py infracost-diff.json
```

---

## Frequently Asked Questions

### Q1: How to handle Terraform state conflicts?

```bash
# View current lock
terraform force-unlock <LOCK_ID>

# Or use DynamoDB to automatically unlock
aws dynamodb delete-item \
  --table-name terraform-locks \
  --key '{"LockID":{"S":"<LOCK_ID>"}}'
```

### Q2: How to safely delete resources?

```bash
# First view resources to be deleted
terraform plan -destroy

# Selectively delete using -target
terraform destroy -target=aws_instance.example

# Or remove resources from code and apply
terraform apply
```

### Q3: How to roll back Terraform changes?

```bash
# Roll back code using Git
git revert <commit-hash>

# Reapply
terraform apply

# Or manually modify state
terraform state mv aws_instance.old aws_instance.new
```

### Q4: How to optimize Terraform execution speed?

1. Use the `-parallelism` parameter to increase parallelism
2. Use `-refresh=false` to skip state refresh
3. Use `-target` to only process specific resources
4. Use Terraform Cloud's remote execution
5. Use module caching

---

## In-Depth Analysis of Terraform Core Concepts

### The Importance of State Management

Terraform's state file is the core of all infrastructure management. The state file records the current state of all resources managed by Terraform, including resource attributes, dependencies, and unique identifiers. When executing the `terraform plan` command, Terraform compares the desired state defined in the configuration files with the current state recorded in the state file, calculating the change operations that need to be executed. If the state file is lost or corrupted, Terraform will be unable to properly manage infrastructure, potentially leading to duplicate resource creation or unintended deletion.

Remote state storage is the foundation of team collaboration. Storing the state file in remote services such as S3, Azure Blob Storage, or Terraform Cloud ensures that all team members use the same state file. State locking prevents conflicts caused by multiple people modifying the state simultaneously, with DynamoDB tables used to implement state locking in AWS environments. State encryption ensures that sensitive information is not leaked, with S3 supporting server-side encryption using KMS. State version control allows rolling back to previous state versions, enabling quick recovery when issues arise.

### Workspace Strategies

Terraform workspaces are a mechanism for managing multiple environments within the same configuration. Each workspace has an independent state file, using the same configuration to create different environment instances. Workspaces are suitable for scenarios with small environment differences, such as development, staging, and production environments using the same resource configuration with only different scales and parameters.

However, for scenarios with significant environment differences, directory isolation is recommended. Each environment uses an independent configuration directory, allowing for completely different resource configurations and parameters. Directory isolation offers greater flexibility, enabling independent optimization and customization for different environments. In this exercise, we adopted the directory isolation approach, with each environment having its own configuration directory and state file.

### Modular Design Principles

Good modular design can significantly improve Terraform code maintainability and reusability. Modules should follow the single responsibility principle, with each module responsible for managing one type of resource. Module interfaces should be concise and clear, with input variables and output values having clear descriptions and type definitions. Modules should include reasonable default values to reduce the configuration burden on callers. Modules should support parameterization, controlling resource scale, names, and other attributes through variables.

Module version management is also important. It is recommended to use Git tags to manage module versions, with semantic versioning indicating the nature of changes. Maintain a changelog in the module repository, recording the changes in each version. Module users can specify the module version to use through version constraints, avoiding unexpected breaking changes.

### Plan and Apply Workflow

Terraform's plan and apply process is the key to ensuring safe infrastructure changes. Before executing `terraform apply`, you should first run `terraform plan` to view the change plan. The change plan lists all operations to be executed, including resource creation, modification, and deletion. Carefully review the change plan to confirm all changes are as expected. Pay special attention to operations marked for destruction to ensure important resources are not accidentally deleted.

In CI/CD workflows, `terraform plan` can be automatically executed during the Pull Request phase, with the change plan added as a comment to the PR. Reviewers can view the change plan and confirm whether the changes are reasonable. After merging the PR, `terraform apply` is automatically executed to apply the changes. This workflow ensures all infrastructure changes go through review, reducing the risk of operational errors.

### Variable Management Best Practices

Terraform's variable management directly affects configuration flexibility and maintainability. Using variable files can separate environment-specific parameters from general configurations. Each environment can have its own variable file, such as `dev.tfvars`, `staging.tfvars`, and `prod.tfvars`. Variable files should not contain sensitive information; sensitive information should be passed through environment variables or key management services.

Variable validation rules can be specified at definition time to ensure input values meet expectations. For example, environment variables can be restricted to only `dev`, `staging`, or `prod`. Instance types can be limited to a specific list of values. Port ranges can be restricted to valid ranges. Variable validation can catch configuration errors during the planning phase, avoiding discovery of problems during the apply phase.

### Output Value Design

Terraform output values are used to expose resource attributes for external use. Output values can be used for information transfer between modules, such as a network module outputting subnet IDs and a compute module using those subnet IDs to create instances. Output values can also be used in CI/CD workflows, such as outputting load balancer DNS names for subsequent health checks. Output values should have clear descriptions explaining the meaning and purpose of the output. Sensitive output values should be marked as `sensitive = true` to prevent leakage in logs.

### Provider Configuration

Terraform providers are plugins that interact with cloud service APIs. Provider version constraints should be explicitly specified to avoid using untested versions. Default tags can be configured at the provider level to ensure all resources have unified tags. Multi-provider configuration allows managing resources across multiple regions or accounts in the same configuration. Provider authentication information should be passed through environment variables or configuration files, not hardcoded in configuration.

### Lifecycle Management

Terraform lifecycle rules can control resource creation, update, and deletion behavior. The `create_before_destroy` rule creates a new resource before deleting the old one during replacement, avoiding service disruption. The `prevent_destroy` rule prevents important resources from being accidentally deleted, such as databases and state storage buckets. The `ignore_changes` rule ignores changes to specific attributes, preventing external modifications from triggering unnecessary updates. Proper use of lifecycle rules can improve infrastructure stability and security.

### Secret Management

Managing secrets in Terraform requires special caution. Never hardcode passwords, keys, or other sensitive information in configuration files or variable files. Use secret management services such as AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault to store sensitive information. Retrieve secret values at runtime through data sources rather than storing them in the state file. If secrets must be stored in the state file, ensure the storage location has appropriate access control and encryption protection. Regularly rotate secret values to reduce leakage risk.

### Disaster Recovery Planning

Infrastructure disaster recovery planning is essential for production environments. Regularly back up state files to ensure recovery is possible if the state file is corrupted. Document all manually configured resources that are not managed by Terraform and need separate backup. Establish an infrastructure rebuild process to quickly reconstruct the entire environment in case of disaster. Conduct regular disaster recovery drills to verify the effectiveness of recovery processes. Use infrastructure version control to quickly roll back to previously known good states.

### Performance Optimization

Terraform execution for large infrastructure may take considerable time. Use the `-parallelism` parameter to increase the parallelism of resource creation, with a default value of 10 that can be increased as appropriate based on cloud service limits. Use `-refresh=false` to skip state refresh, saving time when the state file is already up to date. Use the `-target` parameter to only process specific resources, avoiding execution of full plan and apply during debugging. Split large configurations into multiple independent state files to reduce the number of resources managed by each state file. Use Terraform Cloud's remote execution capability, leveraging its caching and parallelism features to improve execution efficiency.

### Code Review Checklist

Establishing a Terraform configuration code review checklist can improve code quality. Review content includes security checks, confirming no hardcoded credentials and overly permissive permissions. Resource naming checks, confirming resource names follow naming conventions and are descriptive. Tag checks, confirming all resources have necessary tags. Variable checks, confirming variables have clear descriptions and reasonable default values. Output checks, confirming output values have clear descriptions and sensitive values are marked. Lifecycle checks, confirming lifecycle rules are used appropriately. Dependency checks, confirming dependencies between resources are correct. Format checks, confirming code format conforms to Terraform standards.

---

## Further Reading

- [Terraform Official Documentation](https://developer.hashicorp.com/terraform/docs)
- [GitHub Actions Integration with Terraform](https://learn.hashicorp.com/tutorials/terraform/github-actions)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Infracost Documentation](https://www.infracost.io/docs/)

---

## Exercise Summary

Through this exercise, you have learned:

1. ✅ Understanding the concept of Infrastructure as Code
2. ✅ Writing Terraform configuration files
3. ✅ Creating reusable Terraform modules
4. ✅ Automating deployment with GitHub Actions
5. ✅ Managing multi-environment infrastructure
6. ✅ Implementing security scanning and cost estimation

The combination of Terraform and GitHub Actions is an important practice in modern DevOps. It is recommended to adopt this approach gradually in real projects, starting from the development environment and expanding to production.

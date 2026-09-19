# Terraform IaC + GitHub Practical Guide

> This tutorial is designed for Chinese developers, systematically explaining how to use Terraform to implement Infrastructure as Code (IaC), and deeply integrate with GitHub Actions to achieve automated infrastructure management.

---

## Table of Contents

1. [Infrastructure as Code Concepts](#1-infrastructure-as-code-concepts)
2. [Terraform Basic Syntax and Providers](#2-terraform-basic-syntax-and-providers)
3. [Terraform + GitHub Actions CI/CD](#3-terraform--github-actions-cicd)
4. [Terraform State Management (Remote Backend)](#4-terraform-state-management-remote-backend)
5. [Terraform Modular Development](#5-terraform-modular-development)
6. [Terraform and GitHub Provider](#6-terraform-and-github-provider)
7. [Deploying GitHub Actions Runner to Cloud Providers](#7-deploying-github-actions-runner-to-cloud-providers)
8. [Multi-Environment Terraform Management](#8-multi-environment-terraform-management)
9. [Terraform Security Scanning](#9-terraform-security-scanning)
10. [Terratest Testing Framework](#10-terratest-testing-framework)
11. [OpenTofu vs Terraform](#11-opentofu-vs-terraform)
12. [Domestic Cloud Provider Terraform Providers](#12-domestic-cloud-provider-terraform-providers)
13. [IaC Best Practices](#13-iac-best-practices)

---

## 1. Infrastructure as Code Concepts

### 1.1 What is IaC

Infrastructure as Code (IaC) is a method of defining and managing infrastructure using code. With IaC, developers can declaratively describe cloud resources (such as servers, databases, networks, etc.) and manage these configurations through version control systems.

### 1.2 Core Advantages of IaC

| Advantage | Description |
|-----------|-------------|
| **Version Control** | Infrastructure changes have complete Git history |
| **Repeatability** | The same code produces the same infrastructure |
| **Automation** | Reduces manual operations and human errors |
| **Documentation** | Code itself serves as the best documentation |
| **Collaboration** | Team members can review infrastructure changes through PRs |
| **Cost Management** | Clear tracking of resource creation and destruction |

### 1.3 Declarative vs Imperative

```hcl
// Declarative (Terraform) - Describes desired state
resource "alicloud_instance" "web" {
  instance_name = "web-server"
  image_id      = "ubuntu_22_04_x64_20G_alibase_20240101.vhd"
  instance_type = "ecs.g6.large"
}
```

```bash
# Imperative (CLI) - Describes operational steps
aliyun ecs CreateInstance --RegionId cn-hangzhou --InstanceName web-server
aliyun ecs StartInstance --InstanceId i-xxx
```

### 1.4 Comparison of Mainstream IaC Tools

| Tool | Type | Language | State Management | Use Case |
|------|------|----------|------------------|----------|
| **Terraform** | General | HCL | Remote | Multi-cloud environments |
| **OpenTofu** | General | HCL | Remote | Open-source Terraform alternative |
| **Pulumi** | General | Multi-language | Remote | Preference for programming languages |
| **AWS CDK** | AWS-specific | Multi-language | CloudFormation | Deep AWS users |
| **CloudFormation** | AWS-specific | JSON/YAML | AWS-managed | Deep AWS users |
| **Ansible** | Configuration Management | YAML | None | Config management + simple IaC |

### 1.5 Terraform Ecosystem

```
Terraform Ecosystem
├── Terraform Core     # Core engine
├── Providers          # Cloud provider plugins (Alibaba Cloud, Tencent Cloud, AWS, etc.)
├── Modules            # Reusable configuration modules
├── Registry           # Public module and provider repository
├── Cloud              # Terraform Cloud/Enterprise (remote state management)
├── Sentinel           # Policy as Code
└── CDKTF              # Using programming languages to write Terraform
```

---

## 2. Terraform Basic Syntax and Providers

### 2.1 Installing Terraform

```bash
# Linux
wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip
unzip terraform_1.7.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
terraform version

# macOS
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Using domestic mirrors (recommended)
# Set environment variables
export TF_RELEASES_MIRROR=https://mirrors.tencent.com/terraform/
# Or
export TF_RELEASES_MIRROR=https://releases.hashicorp.mirrors.ustc.edu.cn/
```

### 2.2 HCL Basic Syntax

```hcl
# Variable definition
variable "region" {
  description = "Cloud provider region"
  type        = string
  default     = "cn-hangzhou"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "my-app"
  }
}

# Local variables
locals {
  common_tags = merge(var.tags, {
    ManagedBy = "terraform"
    Repository = "my-org/my-infra"
  })
  
  name_prefix = "${var.project}-${var.environment}"
}

# Outputs
output "instance_ids" {
  description = "Instance ID list"
  value       = alicloud_instance.web[*].id
}

output "load_balancer_ip" {
  description = "Load balancer IP"
  value       = alicloud_slb.this.address
}
```

### 2.3 Alibaba Cloud Provider Configuration

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.220"
    }
  }
}

provider "alicloud" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
  
  # Or use environment variables
  # ALICLOUD_ACCESS_KEY
  # ALICLOUD_SECRET_KEY
  # ALICLOUD_REGION
}

# Create VPC
resource "alicloud_vpc" "main" {
  vpc_name   = "${local.name_prefix}-vpc"
  cidr_block = "172.16.0.0/12"
  
  tags = local.common_tags
}

# Create VSwitch
resource "alicloud_vswitch" "main" {
  count        = 2
  vpc_id       = alicloud_vpc.main.id
  cidr_block   = cidrsubnet(alicloud_vpc.main.cidr_block, 8, count.index)
  zone_id      = data.alicloud_zones.available.zones[count.index].id
  vswitch_name = "${local.name_prefix}-vsw-${count.index}"
  
  tags = local.common_tags
}

# Create Security Group
resource "alicloud_security_group" "web" {
  name   = "${local.name_prefix}-web-sg"
  vpc_id = alicloud_vpc.main.id
  
  tags = local.common_tags
}

resource "alicloud_security_group_rule" "allow_http" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "80/80"
  security_group_id = alicloud_security_group.web.id
  cidr_ip           = "0.0.0.0/0"
}

# Create ECS instances
resource "alicloud_instance" "web" {
  count                = var.instance_count
  instance_name        = "${local.name_prefix}-web-${count.index}"
  host_name            = "web-${count.index}"
  image_id             = data.alicloud_images.ubuntu.images[0].id
  instance_type        = "ecs.g6.large"
  security_groups      = [alicloud_security_group.web.id]
  vswitch_id           = alicloud_vswitch.main[count.index % 2].id
  system_disk_category = "cloud_essd"
  system_disk_size     = 40
  
  tags = local.common_tags
}

# Data sources
data "alicloud_zones" "available" {
  available_resource_creation = "VSwitch"
}

data "alicloud_images" "ubuntu" {
  most_recent = true
  owners      = "system"
  name_regex  = "^ubuntu_22"
}
```

### 2.4 Tencent Cloud Provider Configuration

```hcl
terraform {
  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = "~> 1.81"
    }
  }
}

provider "tencentcloud" {
  region     = "ap-guangzhou"
  secret_id  = var.secret_id
  secret_key = var.secret_key
}

# Create VPC
resource "tencentcloud_vpc" "main" {
  name       = "${local.name_prefix}-vpc"
  cidr_block = "172.16.0.0/12"
}

# Create Subnet
resource "tencentcloud_subnet" "main" {
  name              = "${local.name_prefix}-subnet"
  vpc_id            = tencentcloud_vpc.main.id
  cidr_block        = "172.16.0.0/24"
  availability_zone = "ap-guangzhou-3"
}

# Create CVM Instance
resource "tencentcloud_instance" "web" {
  instance_name     = "${local.name_prefix}-web"
  availability_zone = "ap-guangzhou-3"
  image_id          = "img-2lr9q49h"
  instance_type     = "SA2.MEDIUM4"
  system_disk_type  = "CLOUD_SSD"
  system_disk_size  = 50
  vpc_id            = tencentcloud_vpc.main.id
  subnet_id         = tencentcloud_subnet.main.id
}
```

### 2.5 AWS Provider Configuration (China Region)

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "cn-northwest-1"  # Ningxia Region
  # Or "cn-north-1"  # Beijing Region
  
  # Use environment variables or shared credentials
  # AWS_ACCESS_KEY_ID
  # AWS_SECRET_ACCESS_KEY
}

# Create VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}

# Create Subnet
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${local.name_prefix}-public-${count.index}"
  }
}
```

---

## 3. Terraform + GitHub Actions CI/CD

### 3.1 Basic Workflow

```yaml
name: Terraform CI/CD

on:
  push:
    branches: [main]
    paths:
    - 'terraform/**'
  pull_request:
    branches: [main]
    paths:
    - 'terraform/**'

env:
  TF_DIR: terraform
  TF_VERSION: 1.7.0

jobs:
  terraform-plan:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Configure credentials
      run: |
        cat > backend.tf << 'EOF'
        terraform {
          backend "oss" {
            bucket = "my-terraform-state"
            prefix = "my-project"
            region = "cn-hangzhou"
          }
        }
        EOF
    
    - name: Terraform Init
      run: terraform init
      working-directory: ${{ env.TF_DIR }}
    
    - name: Terraform Format Check
      run: terraform fmt -check -recursive
      working-directory: ${{ env.TF_DIR }}
    
    - name: Terraform Validate
      run: terraform validate
      working-directory: ${{ env.TF_DIR }}
    
    - name: Terraform Plan
      id: plan
      run: |
        terraform plan -no-color -out=tfplan 2>&1 | tee plan_output.txt
      working-directory: ${{ env.TF_DIR }}
      env:
        ALICLOUD_ACCESS_KEY: ${{ secrets.ALICLOUD_ACCESS_KEY }}
        ALICLOUD_SECRET_KEY: ${{ secrets.ALICLOUD_SECRET_KEY }}
        ALICLOUD_REGION: cn-hangzhou
    
    - name: Comment PR with Plan
      uses: actions/github-script@v7
      with:
        script: |
          const fs = require('fs');
          const plan = fs.readFileSync('${{ env.TF_DIR }}/plan_output.txt', 'utf8');
          const truncated = plan.length > 60000 ? plan.substring(0, 60000) + '\n... (truncated)' : plan;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## Terraform Plan Output
          
          \`\`\`hcl
          ${truncated}
          \`\`\`
          
          *Triggered by: @${{ github.actor }}, Commit: \`${{ github.sha }}\`*`
          });

  terraform-apply:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Terraform Init
      run: terraform init
      working-directory: ${{ env.TF_DIR }}
      env:
        ALICLOUD_ACCESS_KEY: ${{ secrets.ALICLOUD_ACCESS_KEY }}
        ALICLOUD_SECRET_KEY: ${{ secrets.ALICLOUD_SECRET_KEY }}
    
    - name: Terraform Apply
      run: |
        terraform apply -auto-approve
      working-directory: ${{ env.TF_DIR }}
      env:
        ALICLOUD_ACCESS_KEY: ${{ secrets.ALICLOUD_ACCESS_KEY }}
        ALICLOUD_SECRET_KEY: ${{ secrets.ALICLOUD_SECRET_KEY }}
        ALICLOUD_REGION: cn-hangzhou
```

### 3.2 Using OIDC Authentication (Recommended)

```yaml
name: Terraform with OIDC

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  id-token: write
  contents: read
  pull-requests: write

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Configure Alibaba Cloud OIDC
      run: |
        # Get GitHub OIDC Token
        OIDC_TOKEN=$(curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
          "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=sts.aliyuncs.com" | jq -r '.value')
        
        # Use STS Assume Role
        STS_RESPONSE=$(aliyun sts AssumeRoleWithOIDC \
          --RoleArn "acs:ram::123456789:role/terraform-role" \
          --OIDCProviderArn "acs:ram::123456789:oidc-provider/github" \
          --OIDCToken "$OIDC_TOKEN" \
          --RoleSessionName "github-actions")
        
        # Set environment variables
        echo "ALICLOUD_ACCESS_KEY=$(echo $STS_RESPONSE | jq -r '.Credentials.AccessKeyId')" >> $GITHUB_ENV
        echo "ALICLOUD_SECRET_KEY=$(echo $STS_RESPONSE | jq -r '.Credentials.AccessKeySecret')" >> $GITHUB_ENV
        echo "ALICLOUD_SECURITY_TOKEN=$(echo $STS_RESPONSE | jq -r '.Credentials.SecurityToken')" >> $GITHUB_ENV
    
    - name: Terraform Init & Apply
      run: |
        terraform init
        terraform plan -out=tfplan
        terraform apply tfplan
      working-directory: terraform
```

### 3.3 Complete CI/CD Pipeline

```yaml
name: Terraform Full Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # Stage 1: Code quality check
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Terraform Format Check
      uses: hashicorp/setup-terraform@v3
    
    - name: Check formatting
      run: terraform fmt -check -recursive
      working-directory: terraform
    
    - name: TFLint
      uses: terraform-linters/setup-tflint@v4
      run: |
        tflint --init
        tflint --recursive
      working-directory: terraform
    
    - name: tfsec Security Scan
      uses: aquasecurity/tfsec-action@v1.0.3
      with:
        working_directory: terraform
    
    - name: Checkov Scan
      uses: bridgecrewio/checkov-action@v12
      with:
        directory: terraform
        framework: terraform

  # Stage 2: Plan
  plan:
    needs: quality
    runs-on: ubuntu-latest
    outputs:
      has_changes: ${{ steps.plan.outputs.has_changes }}
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Terraform Init
      run: terraform init
      working-directory: terraform
    
    - name: Terraform Plan
      id: plan
      run: |
        terraform plan -no-color -detailed-exitcode -out=tfplan 2>&1 | tee plan.txt
        if [ $? -eq 2 ]; then
          echo "has_changes=true" >> $GITHUB_OUTPUT
        else
          echo "has_changes=false" >> $GITHUB_OUTPUT
        fi
      working-directory: terraform
    
    - name: Upload Plan Artifact
      if: steps.plan.outputs.has_changes == 'true'
      uses: actions/upload-artifact@v4
      with:
        name: tfplan
        path: terraform/tfplan
        retention-days: 5

  # Stage 3: Apply (main branch only)
  apply:
    needs: plan
    if: github.ref == 'refs/heads/main' && needs.plan.outputs.has_changes == 'true'
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Download Plan Artifact
      uses: actions/download-artifact@v4
      with:
        name: tfplan
        path: terraform
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Terraform Init
      run: terraform init
      working-directory: terraform
    
    - name: Terraform Apply
      run: terraform apply -auto-approve tfplan
      working-directory: terraform
```

---

## 4. Terraform State Management (Remote Backend)

### 4.1 Why Remote State is Needed

Problems with local state files:
- Cannot collaborate with multiple people
- Easy to lose
- Cannot implement state locking

### 4.2 Alibaba Cloud OSS Backend

```hcl
# backend.tf
terraform {
  backend "oss" {
    bucket              = "my-terraform-state"
    prefix              = "my-project/production"
    region              = "cn-hangzhou"
    encrypt             = true
    tablestore_endpoint = "https://tf-state-lock.cn-hangzhou.ots.aliyuncs.com"
    tablestore_table    = "terraform_lock"
  }
}
```

**Creating OSS Bucket and TableStore:**

```hcl
# Manually create storage backend resources first
provider "alicloud" {
  region = "cn-hangzhou"
}

# OSS Bucket
resource "alicloud_oss_bucket" "terraform_state" {
  bucket = "my-terraform-state"
  acl    = "private"
  
  versioning {
    status = "Enabled"
  }
  
  server_side_encryption_rule {
    sse_algorithm = "AES256"
  }
  
  lifecycle {
    prevent_destroy = true
  }
}

# TableStore (for state locking)
resource "alicloud_ots_table" "terraform_lock" {
  instance_name = "terraform-state-lock"
  table_name    = "terraform_lock"
  
  primary_key {
    name = "LockID"
    type = "String"
  }
  
  time_to_live = -1
  max_version  = 1
}
```

### 4.3 Tencent Cloud COS Backend

```hcl
terraform {
  backend "cos" {
    region = "ap-guangzhou"
    bucket = "my-terraform-state-1250000000"
    prefix = "my-project/production"
    
    encrypt = true
  }
}
```

### 4.4 AWS S3 Backend (China Region)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "my-project/production/terraform.tfstate"
    region         = "cn-northwest-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
    
    # China region requires special configuration
    endpoints {
      s3 = "https://s3.cn-northwest-1.amazonaws.com.cn"
    }
  }
}
```

### 4.5 Managing State with GitHub Actions

```yaml
# Securely managing state in GitHub Actions
name: Terraform State Management

on:
  workflow_dispatch:
    inputs:
      action:
        description: 'Action to perform'
        required: true
        type: choice
        options:
        - list
        - show
        - import
        - remove

jobs:
  state:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Terraform Init
      run: terraform init
      working-directory: terraform
    
    - name: List Resources
      if: inputs.action == 'list'
      run: terraform state list
      working-directory: terraform
    
    - name: Show Resource
      if: inputs.action == 'show'
      run: terraform state show ${{ github.event.inputs.resource }}
      working-directory: terraform
```

### 4.6 State Migration

```bash
# Migrate from local to remote Backend
# 1. Configure remote Backend
# 2. Run terraform init
# 3. Terraform will ask whether to migrate state

terraform init
# Output:
# Initializing the backend...
# Do you want to copy existing state to the new backend?
#   Pre-existing state was found while migrating the previous backend to the
#   newly configured backend. Do you want to copy this state to the new
#   backend? Enter "yes" to copy and "no" to start with an empty state.
#   Enter a value: yes
```

---

## 5. Terraform Modular Development

### 5.1 Module Structure

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── ecs/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
└── slb/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

### 5.2 VPC Module Example

```hcl
# modules/vpc/main.tf
resource "alicloud_vpc" "this" {
  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block
  
  tags = merge(var.tags, {
    Name = var.vpc_name
  })
}

resource "alicloud_vswitch" "this" {
  count        = length(var.availability_zones)
  vpc_id       = alicloud_vpc.this.id
  cidr_block   = cidrsubnet(var.cidr_block, 8, count.index)
  zone_id      = var.availability_zones[count.index]
  vswitch_name = "${var.vpc_name}-vsw-${count.index}"
  
  tags = merge(var.tags, {
    Name = "${var.vpc_name}-vsw-${count.index}"
  })
}

resource "alicloud_nat_gateway" "this" {
  count              = var.enable_nat_gateway ? 1 : 0
  vpc_id             = alicloud_vpc.this.id
  nat_gateway_name   = "${var.vpc_name}-nat"
  payment_type       = "PayAsYouGo"
  vswitch_id         = alicloud_vswitch.this[0].id
  nat_type           = "Enhanced"
}
```

```hcl
# modules/vpc/variables.tf
variable "vpc_name" {
  description = "VPC name"
  type        = string
}

variable "cidr_block" {
  description = "VPC CIDR"
  type        = string
  default     = "172.16.0.0/12"
}

variable "availability_zones" {
  description = "Availability zone list"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Whether to create NAT gateway"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = alicloud_vpc.this.id
}

output "vswitch_ids" {
  description = "VSwitch ID list"
  value       = alicloud_vswitch.this[*].id
}

output "nat_gateway_id" {
  description = "NAT Gateway ID"
  value       = var.enable_nat_gateway ? alicloud_nat_gateway.this[0].id : null
}
```

### 5.3 Using Modules

```hcl
# environments/production/main.tf
module "vpc" {
  source = "../../modules/vpc"
  
  vpc_name           = "production-vpc"
  cidr_block         = "172.16.0.0/12"
  availability_zones = ["cn-hangzhou-h", "cn-hangzhou-i"]
  enable_nat_gateway = true
  
  tags = local.common_tags
}

module "ecs_cluster" {
  source = "../../modules/ecs"
  
  cluster_name       = "production-cluster"
  vpc_id             = module.vpc.vpc_id
  vswitch_ids        = module.vpc.vswitch_ids
  instance_type      = "ecs.g6.large"
  instance_count     = 3
  
  tags = local.common_tags
}

module "load_balancer" {
  source = "../../modules/slb"
  
  slb_name           = "production-slb"
  vpc_id             = module.vpc.vpc_id
  vswitch_id         = module.vpc.vswitch_ids[0]
  backend_server_ids = module.ecs_cluster.instance_ids
  
  tags = local.common_tags
}
```

### 5.4 Module Version Management

```hcl
# Using Git repository as module source
module "vpc" {
  source = "git::https://github.com/my-org/terraform-modules.git//vpc?ref=v1.2.0"
}

# Using Terraform Registry
module "vpc" {
  source  = "terraform-alicloud-modules/vpc/alicloud"
  version = "~> 1.0"
}

# Using local path (during development)
module "vpc" {
  source = "../../modules/vpc"
}
```

### 5.5 Module Testing and Documentation

```hcl
# modules/vpc/tests/vpc_test.go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestVpcModule(t *testing.T) {
	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../",
		Vars: map[string]interface{}{
			"vpc_name":           "test-vpc",
			"cidr_block":         "10.0.0.0/16",
			"availability_zones": []string{"cn-hangzhou-h"},
		},
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	vpcId := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcId)
}
```

---

## 6. Terraform and GitHub Provider

### 6.1 Configuring GitHub Provider

```hcl
terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}

provider "github" {
  owner = "my-org"
  token = var.github_token
}
```

### 6.2 Managing GitHub Repositories

```hcl
# Create repository
resource "github_repository" "app" {
  name        = "my-app"
  description = "My application repository"
  visibility  = "private"
  
  has_issues   = true
  has_projects = true
  has_wiki     = false
  
  auto_init          = true
  gitignore_template = "Go"
  license_template   = "mit"
  
  # Branch protection
  # Note: Requires separate github_branch_protection resource
}

# Branch protection rules
resource "github_branch_protection" "main" {
  repository_id = github_repository.app.node_id
  pattern       = "main"
  
  enforce_admins = true
  
  required_pull_request_reviews {
    required_approving_review_count = 2
    dismiss_stale_reviews          = true
    require_code_owner_reviews     = true
  }
  
  required_status_checks {
    strict   = true
    contexts = ["ci/build", "ci/test"]
  }
  
  restrict_pushes {
    blocks_creations = true
    push_allowances  = ["my-org/admins"]
  }
}
```

### 6.3 Managing GitHub Secrets

```hcl
# Repository Secrets
resource "github_actions_secret" "alicloud_access_key" {
  repository      = github_repository.app.name
  secret_name     = "ALICLOUD_ACCESS_KEY"
  plaintext_value = var.alicloud_access_key
}

resource "github_actions_secret" "alicloud_secret_key" {
  repository      = github_repository.app.name
  secret_name     = "ALICLOUD_SECRET_KEY"
  plaintext_value = var.alicloud_secret_key
}

# Environment Secrets
resource "github_repository_environment" "production" {
  repository  = github_repository.app.name
  environment = "production"
  
  reviewers {
    users = [data.github_user.admin.id]
  }
  
  deployment_branch_policy {
    protected_branches     = true
    custom_branch_policies = false
  }
}

resource "github_actions_environment_secret" "kubeconfig" {
  repository      = github_repository.app.name
  environment     = github_repository_environment.production.environment
  secret_name     = "KUBECONFIG"
  plaintext_value = base64encode(var.kubeconfig)
}
```

### 6.4 Managing GitHub Teams

```hcl
# Create teams
resource "github_team" "developers" {
  name        = "developers"
  description = "Development team"
  privacy     = "closed"
}

resource "github_team" "devops" {
  name        = "devops"
  description = "DevOps team"
  privacy     = "closed"
}

# Team members
resource "github_team_members" "developers" {
  team_id = github_team.developers.id
  
  members {
    username = "developer1"
    role     = "member"
  }
  
  members {
    username = "developer2"
    role     = "member"
  }
}

# Team repository permissions
resource "github_team_repository" "developers" {
  team_id    = github_team.developers.id
  repository = github_repository.app.name
  permission = "push"
}

resource "github_team_repository" "devops" {
  team_id    = github_team.devops.id
  repository = github_repository.app.name
  permission = "admin"
}
```

### 6.5 Managing GitHub Actions Workflows

```hcl
# Using GitHub Actions variables
resource "github_actions_variable" "environment" {
  repository    = github_repository.app.name
  variable_name = "DEPLOY_ENVIRONMENT"
  value         = "production"
}

# Organization-level Secrets
resource "github_actions_organization_secret" "shared_token" {
  secret_name     = "SHARED_TOKEN"
  visibility      = "selected"
  plaintext_value = var.shared_token
  
  selected_repository_ids = [
    github_repository.app.repo_id
  ]
}
```

---

## 7. Deploying GitHub Actions Runner to Cloud Providers

### 7.1 Self-Hosted Runner Overview

Advantages of self-hosted runners:
- Access to internal network resources
- Customizable runtime environment
- No GitHub-hosted limitations
- Controllable costs

### 7.2 Alibaba Cloud ECS Runner

```hcl
# modules/github-runner/main.tf
resource "alicloud_instance" "runner" {
  count             = var.runner_count
  instance_name     = "${var.runner_name}-${count.index}"
  image_id          = data.alicloud_images.ubuntu.images[0].id
  instance_type     = var.instance_type
  security_groups   = [alicloud_security_group.runner.id]
  vswitch_id        = var.vswitch_id
  system_disk_category = "cloud_essd"
  system_disk_size  = 100
  
  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    github_token = var.github_token
    runner_name  = "${var.runner_name}-${count.index}"
    repo_url     = var.repo_url
    labels       = var.runner_labels
  }))
  
  tags = merge(var.tags, {
    Name = "${var.runner_name}-${count.index}"
    Role = "github-runner"
  })
}

resource "alicloud_security_group" "runner" {
  name   = "${var.runner_name}-sg"
  vpc_id = var.vpc_id
}

# Allow HTTPS egress (communication with GitHub)
resource "alicloud_security_group_rule" "allow_https_out" {
  type              = "egress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "443/443"
  security_group_id = alicloud_security_group.runner.id
  cidr_ip           = "0.0.0.0/0"
}
```

```bash
#!/bin/bash
# modules/github-runner/userdata.sh
set -e

# Install dependencies
apt-get update
apt-get install -y curl jq

# Create runner user
useradd -m -s /bin/bash runner
usermod -aG sudo runner

# Download GitHub Actions Runner
RUNNER_VERSION="2.311.0"
cd /home/runner
curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L \
  https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
tar xzf actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
rm actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

# Configure Runner
chown -R runner:runner /home/runner
su - runner -c "./config.sh \
  --url ${repo_url} \
  --token ${github_token} \
  --name ${runner_name} \
  --labels ${labels} \
  --work _work \
  --unattended"

# Install as service
./svc.sh install runner
./svc.sh start
```

### 7.3 Alibaba Cloud ACK Runner (K8s Deployment)

```hcl
# Using Actions Runner Controller (ARC)
resource "helm_release" "arc" {
  name       = "actions-runner-controller"
  repository = "https://actions-runner-controller.github.io/actions-runner-controller"
  chart      = "actions-runner-controller"
  namespace  = "arc-systems"
  create_namespace = true
  
  set {
    name  = "authSecret.create"
    value = "true"
  }
  
  set {
    name  = "authSecret.github_token"
    value = var.github_token
  }
}
```

```yaml
# Runner deployment configuration
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: github-runner
  namespace: arc-systems
spec:
  replicas: 3
  template:
    spec:
      repository: my-org/my-repo
      labels:
        - self-hosted
        - linux
        - x64
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "2"
          memory: "4Gi"
```

### 7.4 Tencent Cloud CVM Runner

```hcl
resource "tencentcloud_instance" "runner" {
  count             = var.runner_count
  instance_name     = "github-runner-${count.index}"
  availability_zone = "ap-guangzhou-3"
  image_id          = "img-2lr9q49h"
  instance_type     = "SA2.MEDIUM4"
  system_disk_type  = "CLOUD_SSD"
  system_disk_size  = 100
  
  user_data = base64encode(templatefile("${path.module}/userdata.sh", {
    github_token = var.github_token
    runner_name  = "github-runner-${count.index}"
    repo_url     = var.repo_url
  }))
}
```

### 7.5 Runner Auto Scaling

```hcl
# Using ARC's RunnerSet for auto scaling
resource "kubernetes_manifest" "runner_set" {
  manifest = {
    apiVersion = "actions.summerwind.dev/v1alpha1"
    kind       = "RunnerSet"
    metadata = {
      name      = "github-runner"
      namespace = "arc-systems"
    }
    spec = {
      replicas = 2
      repository = "my-org/my-repo"
      labels = ["self-hosted", "linux"]
      
      # Auto scaling based on queue length
      # Requires configuring HorizontalRunnerAutoscaler
    }
  }
}

resource "kubernetes_manifest" "autoscaler" {
  manifest = {
    apiVersion = "actions.summerwind.dev/v1alpha1"
    kind       = "HorizontalRunnerAutoscaler"
    metadata = {
      name      = "github-runner-autoscaler"
      namespace = "arc-systems"
    }
    spec = {
      scaleTargetRef = {
        kind = "RunnerSet"
        name = "github-runner"
      }
      minReplicas = 1
      maxReplicas = 10
      scaleMetrics = [
        {
          type = "TotalNumberOfQueuedAndInProgressWorkflowRuns"
          repositoryNames = ["my-repo"]
        }
      ]
    }
  }
}
```

---

## 8. Multi-Environment Terraform Management

### 8.1 Directory Structure Approach

```
terraform/
├── modules/                  # Shared modules
│   ├── vpc/
│   ├── ecs/
│   └── slb/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars
│       └── backend.tf
└── README.md
```

**Environment Configuration Example:**

```hcl
# environments/dev/terraform.tfvars
environment    = "development"
region         = "cn-hangzhou"
instance_type  = "ecs.g6.large"
instance_count = 1
enable_monitoring = false

# environments/production/terraform.tfvars
environment    = "production"
region         = "cn-hangzhou"
instance_type  = "ecs.g6.2xlarge"
instance_count = 5
enable_monitoring = true
```

### 8.2 Terraform Workspace Approach

```bash
# Create workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new production

# Switch workspaces
terraform workspace select production

# List workspaces
terraform workspace list

# Show current workspace
terraform workspace show
```

```hcl
# Using workspace to differentiate environments
locals {
  env = terraform.workspace
  
  instance_type = {
    dev      = "ecs.g6.large"
    staging  = "ecs.g6.xlarge"
    production = "ecs.g6.2xlarge"
  }
  
  instance_count = {
    dev      = 1
    staging  = 2
    production = 5
  }
}

resource "alicloud_instance" "web" {
  count         = local.instance_count[local.env]
  instance_type = local.instance_type[local.env]
  # ...
}
```

### 8.3 Terragrunt Approach

```hcl
# terragrunt.hcl (root configuration)
remote_state {
  backend = "oss"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket = "my-terraform-state"
    prefix = "${path_relative_to_include()}/terraform.tfstate"
    region = "cn-hangzhou"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents = <<EOF
provider "alicloud" {
  region = var.region
}
EOF
}
```

```hcl
# environments/production/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/vpc"
}

inputs = {
  vpc_name           = "production-vpc"
  cidr_block         = "172.16.0.0/12"
  availability_zones = ["cn-hangzhou-h", "cn-hangzhou-i"]
  enable_nat_gateway = true
}
```

### 8.4 GitHub Actions Multi-Environment Deployment

```yaml
name: Terraform Multi-Environment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, production]
        include:
        - environment: dev
          auto_approve: true
        - environment: staging
          auto_approve: true
        - environment: production
          auto_approve: false
    
    environment: ${{ matrix.environment }}
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Terraform Init
      run: terraform init
      working-directory: terraform/environments/${{ matrix.environment }}
    
    - name: Terraform Plan
      run: terraform plan -out=tfplan
      working-directory: terraform/environments/${{ matrix.environment }}
    
    - name: Terraform Apply
      if: matrix.auto_approve && github.ref == 'refs/heads/main'
      run: terraform apply -auto-approve tfplan
      working-directory: terraform/environments/${{ matrix.environment }}
    
    - name: Manual Approval Required
      if: !matrix.auto_approve && github.ref == 'refs/heads/main'
      uses: trstringer/manual-approval@v1
      with:
        secret: ${{ secrets.GITHUB_TOKEN }}
        approvers: my-org/admins
```

---

## 9. Terraform Security Scanning

### 9.1 tfsec

```yaml
# Using tfsec in GitHub Actions
- name: Run tfsec
  uses: aquasecurity/tfsec-action@v1.0.3
  with:
    working_directory: terraform
    soft_fail: false
    format: json
    output: tfsec-results.json

- name: Upload tfsec results
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: tfsec-results.sarif
```

**tfsec Configuration File:**

```yaml
# .tfsec/config.yml
minimum_severity: MEDIUM
exclude:
  - aws-vpc-no-public-ingress-sgr  # Exclude specific rules
  - alicloud-ecs-no-public-ingress-sgr
```

### 9.2 Checkov

```yaml
# Using Checkov in GitHub Actions
- name: Run Checkov
  uses: bridgecrewio/checkov-action@v12
  with:
    directory: terraform
    framework: terraform
    output_format: json
    output_file_path: checkov-results.json
    soft_fail: false
    skip_check: CKV_AWS_18  # Skip specific checks
```

**Checkov Configuration File:**

```yaml
# .checkov.yml
framework:
- terraform
directory:
- terraform
skip-check:
- CKV_AWS_18  # S3 access logs
- CKV_ALI_1   # Alibaba Cloud specific checks
```

### 9.3 TFLint

```yaml
# Installing and running TFLint
- name: Setup TFLint
  uses: terraform-linters/setup-tflint@v4

- name: Run TFLint
  run: |
    tflint --init
    tflint --recursive --format json > tflint-results.json
  working-directory: terraform
```

**TFLint Configuration:**

```hcl
# .tflint.hcl
plugin "alicloud" {
  enabled = true
  version = "0.25.0"
  source  = "github.com/terraform-linters/tflint-ruleset-alicloud"
}

rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}

rule "terraform_documented_variables" {
  enabled = true
}

rule "terraform_documented_outputs" {
  enabled = true
}
```

### 9.4 Comprehensive Security Scanning Workflow

```yaml
name: Terraform Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run tfsec
      uses: aquasecurity/tfsec-action@v1.0.3
      with:
        working_directory: terraform
    
    - name: Run Checkov
      uses: bridgecrewio/checkov-action@v12
      with:
        directory: terraform
    
    - name: Setup TFLint
      uses: terraform-linters/setup-tflint@v4
    
    - name: Run TFLint
      run: |
        tflint --init
        tflint --recursive
      working-directory: terraform
    
    - name: Terraform Validate
      run: |
        terraform init -backend=false
        terraform validate
      working-directory: terraform
```

---

## 10. Terratest Testing Framework

### 10.1 Terratest Introduction

Terratest is a Go testing framework developed by Gruntwork for writing automated tests for infrastructure.

### 10.2 Installation

```bash
# Initialize Go module
cd test
go mod init github.com/my-org/terraform-tests
go mod tidy

# Install dependencies
go get github.com/gruntwork-io/terratest
go get github.com/stretchr/testify
```

### 10.3 VPC Module Testing

```go
// test/vpc_test.go
package test

import (
	"testing"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestVpcModule(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"vpc_name":           "test-vpc",
			"cidr_block":         "10.0.0.0/16",
			"availability_zones": []string{"cn-hangzhou-h"},
		},
		PlanFilePath: "tfplan",
	})

	defer terraform.Destroy(t, terraformOptions)

	terraform.InitAndApply(t, terraformOptions)

	// Validate outputs
	vpcId := terraform.Output(t, terraformOptions, "vpc_id")
	assert.NotEmpty(t, vpcId)

	vswitchIds := terraform.OutputList(t, terraformOptions, "vswitch_ids")
	require.Len(t, vswitchIds, 1)
	assert.NotEmpty(t, vswitchIds[0])
}

func TestVpcWithNatGateway(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../modules/vpc",
		Vars: map[string]interface{}{
			"vpc_name":           "test-vpc-nat",
			"cidr_block":         "10.1.0.0/16",
			"availability_zones": []string{"cn-hangzhou-h", "cn-hangzhou-i"},
			"enable_nat_gateway": true,
		},
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	natGatewayId := terraform.Output(t, terraformOptions, "nat_gateway_id")
	assert.NotEmpty(t, natGatewayId)
}
```

### 10.4 ECS Module Testing

```go
// test/ecs_test.go
package test

import (
	"testing"
	"fmt"
	http_helper "github.com/gruntwork-io/terratest/modules/http-helper"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestEcsModule(t *testing.T) {
	t.Parallel()

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		TerraformDir: "../modules/ecs",
		Vars: map[string]interface{}{
			"cluster_name":   "test-cluster",
			"vpc_id":         "vpc-xxx",       // Use actual VPC ID
			"vswitch_ids":    []string{"vsw-xxx"},
			"instance_type":  "ecs.g6.large",
			"instance_count": 2,
		},
	})

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Validate instance count
	instanceIds := terraform.OutputList(t, terraformOptions, "instance_ids")
	assert.Len(t, instanceIds, 2)

	// Validate instance accessibility
	publicIp := terraform.Output(t, terraformOptions, "public_ip")
	url := fmt.Sprintf("http://%s", publicIp)
	http_helper.HttpGet(t, url, nil, 200, "Welcome")
}
```

### 10.5 Integration Test Workflow

```yaml
name: Terraform Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Go
      uses: actions/setup-go@v5
      with:
        go-version: '1.22'
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v3
    
    - name: Run Tests
      run: |
        cd test
        go test -v -timeout 30m ./...
      env:
        ALICLOUD_ACCESS_KEY: ${{ secrets.ALICLOUD_ACCESS_KEY }}
        ALICLOUD_SECRET_KEY: ${{ secrets.ALICLOUD_SECRET_KEY }}
        ALICLOUD_REGION: cn-hangzhou
```

---

## 11. OpenTofu vs Terraform

### 11.1 Background

In 2023, HashiCorp changed Terraform's license from MPL 2.0 to BSL 1.1, which prompted the community to create OpenTofu as an open-source alternative.

### 11.2 Comparison

| Feature | Terraform | OpenTofu |
|---------|-----------|----------|
| License | BSL 1.1 | MPL 2.0 |
| Maintainer | HashiCorp | Linux Foundation |
| Compatibility | Original | Highly compatible |
| Module Registry | Terraform Registry | OpenTofu Registry |
| State Encryption | Not supported | Supported |
| Community | Larger | Growing |

### 11.3 Migrating to OpenTofu

```bash
# Install OpenTofu
curl -fsSL https://get.opentofu.org/install-opentofu.sh | bash

# Or use Homebrew
brew install opentofu

# Migration steps
# 1. Backup current state
cp terraform.tfstate terraform.tfstate.backup

# 2. Initialize OpenTofu (compatible with existing configurations)
tofu init

# 3. Verify state
tofu plan

# 4. After confirming, use tofu command instead of terraform
tofu apply
```

### 11.4 Using OpenTofu in GitHub Actions

```yaml
name: OpenTofu CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  tofu:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup OpenTofu
      uses: opentofu/setup-opentofu@v1
      with:
        tofu_version: '1.6.0'
    
    - name: Tofu Init
      run: tofu init
      working-directory: terraform
    
    - name: Tofu Plan
      run: tofu plan
      working-directory: terraform
    
    - name: Tofu Apply
      if: github.ref == 'refs/heads/main'
      run: tofu apply -auto-approve
      working-directory: terraform
```

### 11.5 OpenTofu Exclusive Features

```hcl
# OpenTofu supports state encryption
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "terraform.tfstate"
    region = "cn-hangzhou"
    
    # OpenTofu exclusive: state encryption
    encryption {
      key_provider "pbkdf2" "my_key" {
        passphrase = var.encryption_passphrase
      }
      
      state {
        method = method.aes_gcm.my_key
      }
    }
  }
}
```

---

## 12. Domestic Cloud Provider Terraform Providers

### 12.1 Alibaba Cloud Provider

```hcl
# Alibaba Cloud Provider
terraform {
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.220"
    }
  }
}

# Common resources
resource "alicloud_vpc" "main" { }
resource "alicloud_vswitch" "main" { }
resource "alicloud_instance" "main" { }
resource "alicloud_slb_load_balancer" "main" { }
resource "alicloud_db_instance" "main" { }
resource "alicloud_redis_instance" "main" { }
resource "alicloud_oss_bucket" "main" { }
resource "alicloud_cs_managed_kubernetes" "main" { }
resource "alicloud_cdn_domain_new" "main" { }
resource "alicloud_dns_record" "main" { }
```

### 12.2 Tencent Cloud Provider

```hcl
# Tencent Cloud Provider
terraform {
  required_providers {
    tencentcloud = {
      source  = "tencentcloudstack/tencentcloud"
      version = "~> 1.81"
    }
  }
}

# Common resources
resource "tencentcloud_vpc" "main" { }
resource "tencentcloud_subnet" "main" { }
resource "tencentcloud_instance" "main" { }
resource "tencentcloud_clb_instance" "main" { }
resource "tencentcloud_mysql_instance" "main" { }
resource "tencentcloud_redis_instance" "main" { }
resource "tencentcloud_cos_bucket" "main" { }
resource "tencentcloud_kubernetes_cluster" "main" { }
resource "tencentcloud_cdn_domain" "main" { }
resource "tencentcloud_dns_record" "main" { }
```

### 12.3 Huawei Cloud Provider

```hcl
# Huawei Cloud Provider
terraform {
  required_providers {
    huaweicloud = {
      source  = "huaweicloud/huaweicloud"
      version = "~> 1.60"
    }
  }
}

# Common resources
resource "huaweicloud_vpc_v1" "main" { }
resource "huaweicloud_vpc_subnet_v1" "main" { }
resource "huaweicloud_compute_instance_v2" "main" { }
resource "huaweicloud_lb_loadbalancer_v2" "main" { }
resource "huaweicloud_rds_instance_v3" "main" { }
resource "huaweicloud_redis_instance" "main" { }
resource "huaweicloud_obs_bucket" "main" { }
resource "huaweicloud_cce_cluster" "main" { }
resource "huaweicloud_cdn_domain" "main" { }
resource "huaweicloud_dns_recordset_v2" "main" { }
```

### 12.4 Multi-Cloud Provider Configuration

```hcl
# Managing multiple cloud providers simultaneously
provider "alicloud" {
  alias  = "hangzhou"
  region = "cn-hangzhou"
}

provider "alicloud" {
  alias  = "shanghai"
  region = "cn-shanghai"
}

provider "tencentcloud" {
  alias  = "guangzhou"
  region = "ap-guangzhou"
}

provider "huaweicloud" {
  alias  = "beijing"
  region = "cn-north-4"
}

# Alibaba Cloud Hangzhou resources
resource "alicloud_vpc" "hangzhou" {
  provider   = alicloud.hangzhou
  vpc_name   = "hangzhou-vpc"
  cidr_block = "172.16.0.0/12"
}

# Tencent Cloud Guangzhou resources
resource "tencentcloud_vpc" "guangzhou" {
  provider   = tencentcloud.guangzhou
  name       = "guangzhou-vpc"
  cidr_block = "10.0.0.0/16"
}
```

### 12.5 Domestic Provider Resource Comparison Table

| Resource Type | Alibaba Cloud | Tencent Cloud | Huawei Cloud |
|---------------|---------------|---------------|--------------|
| VPC | `alicloud_vpc` | `tencentcloud_vpc` | `huaweicloud_vpc_v1` |
| Subnet | `alicloud_vswitch` | `tencentcloud_subnet` | `huaweicloud_vpc_subnet_v1` |
| Cloud Server | `alicloud_instance` | `tencentcloud_instance` | `huaweicloud_compute_instance_v2` |
| Load Balancer | `alicloud_slb_load_balancer` | `tencentcloud_clb_instance` | `huaweicloud_lb_loadbalancer_v2` |
| RDS | `alicloud_db_instance` | `tencentcloud_mysql_instance` | `huaweicloud_rds_instance_v3` |
| Redis | `alicloud_redis_instance` | `tencentcloud_redis_instance` | `huaweicloud_redis_instance` |
| OSS/COS/OBS | `alicloud_oss_bucket` | `tencentcloud_cos_bucket` | `huaweicloud_obs_bucket` |
| K8s | `alicloud_cs_managed_kubernetes` | `tencentcloud_kubernetes_cluster` | `huaweicloud_cce_cluster` |
| CDN | `alicloud_cdn_domain_new` | `tencentcloud_cdn_domain` | `huaweicloud_cdn_domain` |
| DNS | `alicloud_dns_record` | `tencentcloud_dns_record` | `huaweicloud_dns_recordset_v2` |

---

## 13. IaC Best Practices

### 13.1 Code Organization

```
terraform/
├── modules/                    # Reusable modules
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── monitoring/
├── environments/               # Environment configurations
│   ├── dev/
│   ├── staging/
│   └── production/
├── global/                     # Global resources
│   ├── iam/
│   ├── dns/
│   └── terraform.tfstate.d/
└── scripts/                    # Helper scripts
    ├── init-backend.sh
    └── migrate-state.sh
```

### 13.2 Naming Conventions

```hcl
# Resource naming convention
# Format: {project}-{environment}-{component}-{resource_type}

# Example
resource "alicloud_vpc" "main" {
  vpc_name = "myapp-production-vpc"
}

resource "alicloud_instance" "web" {
  instance_name = "myapp-production-web-01"
}

# Tagging convention
locals {
  common_tags = {
    Project     = "myapp"
    Environment = "production"
    ManagedBy   = "terraform"
    Team        = "platform"
    CostCenter  = "engineering"
  }
}
```

### 13.3 Version Locking

```hcl
# Using exact versions
terraform {
  required_version = "= 1.7.0"
  
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "= 1.220.0"
    }
  }
}

# Or using version constraints
terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  
  required_providers {
    alicloud = {
      source  = "aliyun/alicloud"
      version = "~> 1.220"  # Allows 1.220.x patch versions
    }
  }
}
```

### 13.4 State Management Best Practices

```hcl
# 1. Use remote Backend
terraform {
  backend "oss" {
    bucket = "my-terraform-state"
    prefix = "my-project"
  }
}

# 2. Enable state encryption
terraform {
  backend "s3" {
    bucket  = "my-terraform-state"
    key     = "terraform.tfstate"
    encrypt = true
  }
}

# 3. Use state locking
# Alibaba Cloud: Use TableStore
# AWS: Use DynamoDB
# Tencent Cloud: COS automatic locking
```

### 13.5 Security Best Practices

```hcl
# 1. Do not hardcode sensitive information in code
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Mark as sensitive
}

# 2. Use Secret Manager
resource "alicloud_kms_secret" "db_password" {
  secret_name = "db-password"
  secret_data = var.db_password
}

# 3. Principle of least privilege
# Create a dedicated RAM role for Terraform, granting only necessary permissions

# 4. Use OIDC authentication
# Avoid using long-term AccessKey
```

### 13.6 CI/CD Best Practices

```yaml
# 1. Auto Plan on PR
# 2. Auto Apply after merge
# 3. Use environment approval
# 4. Save Plan artifacts
# 5. Add security scanning

name: Terraform Best Practices

on:
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
    # Format check
    - name: Terraform Format
      run: terraform fmt -check -recursive
    
    # Security scan
    - name: Security Scan
      uses: aquasecurity/tfsec-action@v1.0.3
    
    # Lint check
    - name: TFLint
      run: tflint --recursive
    
    # Plan
    - name: Terraform Plan
      run: terraform plan -out=tfplan
    
    # Comment on PR
    - name: Comment Plan
      uses: actions/github-script@v7
```

### 13.7 Documentation Best Practices

```hcl
# 1. Add description to every variable
variable "instance_type" {
  description = "ECS instance type, recommended to use ecs.g6 series"
  type        = string
  default     = "ecs.g6.large"
}

# 2. Add description to every output
output "vpc_id" {
  description = "Created VPC ID, for reference by other modules"
  value       = alicloud_vpc.main.id
}

# 3. Document modules using README
# modules/vpc/README.md

# 4. Use terraform-docs to auto-generate documentation
```

### 13.8 Cost Optimization

```hcl
# 1. Use preemptible/spot instances
resource "alicloud_instance" "spot" {
  spot_strategy    = "SpotAsPriceGo"
  spot_price_limit = "0.5"
}

# 2. Auto scaling
resource "alicloud_ess_scaling_group" "main" {
  min_size = 1
  max_size = 10
}

# 3. Resource tags for cost tracking
locals {
  cost_tags = {
    CostCenter = "engineering"
    Team       = "platform"
  }
}

# 4. Use terraform-cost-estimation
# https://github.com/infracost/infracost
```

### 13.9 Rollback Strategy

```bash
# 1. Use version control rollback
git revert <commit-hash>
git push

# 2. Use state rollback
terraform state pull > terraform.tfstate.backup
terraform apply -target=resource.name

# 3. Use Terraform Cloud/Enterprise versioned state

# 4. Maintain sufficient state history
```

---

## Appendix: Complete Project Example

```
my-terraform-project/
├── .github/
│   └── workflows/
│       ├── terraform-plan.yml
│       ├── terraform-apply.yml
│       └── terraform-destroy.yml
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── ecs/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   └── rds/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── README.md
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   └── ...
│   └── production/
│       └── ...
├── tests/
│   ├── go.mod
│   ├── go.sum
│   └── vpc_test.go
├── scripts/
│   ├── init-backend.sh
│   └── setup-credentials.sh
├── .tfsec/
│   └── config.yml
├── .tflint.hcl
├── .gitignore
└── README.md
```

**.gitignore File:**

```gitignore
# Terraform
*.tfstate
*.tfstate.backup
*.tfstate.*.backup
.terraform/
.terraform.lock.hcl
crash.log
crash.*.log
*.tfvars
!*.tfvars.example
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraformrc
terraform.rc

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Summary

This tutorial provides a detailed guide to Terraform IaC integration with GitHub, covering:

- **IaC Concepts**: Core principles and advantages of Infrastructure as Code
- **Terraform Basics**: HCL syntax, provider configuration, core resources
- **CI/CD Integration**: GitHub Actions automated Plan/Apply workflows
- **State Management**: Remote backends, state locking, encrypted storage
- **Modular Development**: Reusable module design, version management, testing
- **GitHub Provider**: Managing GitHub resources with Terraform
- **Runner Deployment**: Cloud deployment solutions for self-hosted runners
- **Multi-Environment Management**: Directory structures, Workspaces, Terragrunt approaches
- **Security Scanning**: tfsec, Checkov, TFLint toolchain
- **Terratest**: Infrastructure automated testing framework
- **OpenTofu**: Open-source alternative to Terraform
- **Domestic Cloud Providers**: Detailed guide to Alibaba Cloud, Tencent Cloud, Huawei Cloud providers
- **Best Practices**: Code organization, naming conventions, security, cost optimization

With these practices, Chinese developers can build efficient, secure, and maintainable Infrastructure as Code systems.

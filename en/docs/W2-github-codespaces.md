# GitHub Codespaces Complete Guide

## 1. GitHub Codespaces Overview and Pricing

### 1.1 What is GitHub Codespaces

GitHub Codespaces is a cloud-based development environment service provided by GitHub. Built on the Visual Studio Code infrastructure, it allows developers to connect directly from a browser or local VS Code to a full development container running in the cloud. Each Codespace is essentially a virtual machine hosted on Microsoft Azure cloud infrastructure, pre-installed with a complete Linux operating system, commonly used development toolchains, and user-customized runtime environments. Developers don't need to install any SDKs, compilers, or databases on their local machines — just a browser is needed to start writing, building, testing, and debugging code.

The core concept of Codespaces is Environment as Code. Traditional development environment setup often takes hours or even days to install dependencies, configure paths, and debug version compatibility issues. Codespaces incorporates the entire development environment definition into version control through the `devcontainer.json` configuration file, enabling any team member to get a completely consistent development experience on any device. This not only dramatically reduces the onboarding cost for new members but also completely eliminates the classic "it works on my machine" problem.

### 1.2 Core Advantages in Detail

| Advantage Dimension | Description |
|---------------------|-------------|
| **Zero-Config Startup** | From opening a repository to entering an editable IDE interface, typically only 10-30 seconds |
| **Environment Consistency** | All team members share the same OS, runtime, toolchain, and extension configurations |
| **Device Independence** | Supports professional development on low-performance devices like Chromebooks, iPads, and Android tablets |
| **Elastic Computing Power** | Choose from 2-core / 4-core / 8-core / 16-core / 32-core CPUs, with memory from 8GB to 64GB |
| **Security Isolation** | Each Codespace runs in an isolated virtual machine, completely separated from others |
| **Deep Git Integration** | Automatically uses GitHub authentication, no need to configure SSH keys or personal access tokens |

### 1.3 Pricing Model in Detail

GitHub Codespaces is billed by the **core-hour** unit, which is the number of CPU cores multiplied by usage hours.

| Plan | Monthly Free Allowance | 2-Core Machine Usable Hours | Overage Cost (per core-hour) |
|------|----------------------|---------------------------|------------------------------|
| **Free** | 120 core-hours | ~60 hours | $0.18 |
| **Pro** | 180 core-hours | ~90 hours | $0.18 |
| **Team** | 180 core-hours/user | ~90 hours/user | $0.08 |
| **Enterprise** | Customizable | Customizable | Negotiable |

**Billing Example:**

Assuming you use a 4-core CPU machine configuration, working 4 hours per day:

- Daily consumption: 4 cores × 4 hours = 16 core-hours
- Monthly consumption (22 working days): 16 × 22 = 352 core-hours
- Free plan allowance: 120 core-hours
- Overage cost: (352 - 120) × $0.18 = $41.76

> **Important Note:** Codespaces does not continue billing after it stops running, but storage costs still accumulate. Default storage costs are $0.07/GB/month, included in the free allowance. Each Codespace has 15GB of storage by default.

---

## 2. Creating and Managing Codespaces

### 2.1 Creating from the GitHub Web Interface

The simplest way to create is directly from the GitHub repository page:

1. Open any GitHub repository page (e.g., `https://github.com/microsoft/vscode`)
2. Click the green **Code** button at the top of the page
3. Switch to the **Codespaces** tab
4. Click **Create codespace on main** (creates on the main branch by default)

GitHub will automatically select a suitable machine configuration for you (usually 2 cores), then start building the development container. The first creation may take 1-3 minutes to pull images and install dependencies, while subsequent startups will be much faster (usually 10-30 seconds) because the images are cached.

After creation, the browser will automatically redirect to a complete VS Code Web interface where you can run commands directly in the terminal, write code, and install extensions — almost identical to local VS Code.

### 2.2 Customizing Machine Configuration

When creating a Codespace, you can click the **Machine type** dropdown to select different machine specifications:

| Machine Type | CPU Cores | Memory | Storage | Use Case |
|--------------|-----------|--------|---------|----------|
| 2-core | 2 vCPU | 8 GB | 32 GB | Light editing, documentation |
| 4-core | 4 vCPU | 16 GB | 32 GB | Small to medium project development |
| 8-core | 8 vCPU | 32 GB | 64 GB | Large projects, compilation and building |
| 16-core | 16 vCPU | 32 GB | 64 GB | High-performance computing, CI simulation |
| 32-core | 32 vCPU | 64 GB | 128 GB | Extra-large projects, performance testing |

### 2.3 Creating from VS Code Desktop

If you prefer using the local VS Code desktop version, you can install the GitHub Codespaces extension:

1. Open VS Code and go to the Extensions marketplace
2. Search for and install the **GitHub Codespaces** extension (published by GitHub)
3. After installation, press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the command palette
4. Type `Codespaces: Create New Codespace`
5. Select the repository and branch
6. Choose the machine configuration
7. VS Code will automatically connect to the remote Codespace

The advantage of this approach is that you can use all features of the local VS Code, including custom themes, keybinding, and local extensions.

### 2.4 Creating from GitHub CLI

```bash
# Install GitHub CLI (if not installed)
# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# Ubuntu/Debian
sudo apt install gh

# Login to GitHub
gh auth login

# Create Codespace (default configuration)
gh codespace create --repo owner/repo-name

# Specify branch and machine configuration
gh codespace create --repo owner/repo-name --branch dev --machine 4-core

# List all Codespaces
gh codespace list

# View details of a specific Codespace
gh codespace view --codespace codespace-name
```

### 2.5 Managing Codespace Lifecycle

Each Codespace has the following states:

- **Running:** Actively consuming core-hours, accessible via browser or VS Code
- **Stopped:** Not consuming core-hours, but storage is still billed
- **Deleted:** All data permanently removed, no longer billed

```bash
# Stop Codespace
gh codespace stop --codespace codespace-name

# Start a stopped Codespace
gh codespace start --codespace codespace-name

# Delete Codespace (irreversible)
gh codespace delete --codespace codespace-name

# Batch delete all stopped Codespaces
gh codespace list --json name,state | jq -r '.[] | select(.state=="Available") | .name' | xargs -I {} gh codespace delete -c {}
```

**Auto-Stop Policy:** GitHub automatically stops a Codespace after 30 minutes of inactivity by default. You can modify this timeout in Settings → Codespaces, with selectable ranges from 5 minutes to 240 minutes. Setting an appropriate timeout can effectively avoid unnecessary costs from forgetting to close Codespaces.

---

## 3. Dev Container Configuration (devcontainer.json)

### 3.1 What is devcontainer.json

`devcontainer.json` is the core configuration file of the Dev Container Specification. It defines the image to use when Codespace starts, the tools to install, the extensions to configure, the ports to forward, and various initialization scripts. This file is typically placed in the `.devcontainer/` folder at the project root.

When you create a Codespace, GitHub first checks if a `devcontainer.json` file exists in the repository. If it exists, the development container is built according to its definition; if not, a default generic development container image is used.

### 3.2 Complete Configuration Fields Explained

Here is a `devcontainer.json` example containing all commonly used fields:

```json
{
  "name": "My Full-Stack Project Development Environment",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",

  "forwardPorts": [3000, 5432, 8080],
  "portsAttributes": {
    "3000": {
      "label": "Frontend Application",
      "onAutoForward": "openBrowser",
      "visibility": "public"
    },
    "5432": {
      "label": "PostgreSQL Database",
      "onAutoForward": "notify",
      "visibility": "private"
    },
    "8080": {
      "label": "Backend API",
      "onAutoForward": "silent",
      "visibility": "public"
    }
  },

  "postCreateCommand": "npm install && npm run db:migrate",
  "postStartCommand": "echo 'Environment Ready!'",
  "postAttachCommand": "git pull",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next",
        "bradlc.vscode-tailwindcss",
        "prisma.prisma"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2,
        "terminal.integrated.defaultProfile.linux": "zsh"
      }
    }
  },

  "remoteUser": "vscode",
  "containerUser": "vscode",

  "mounts": [
    "source=${localEnv:HOME}/.gitconfig,target=/home/vscode/.gitconfig,type=bind,readonly"
  ],

  "containerEnv": {
    "NODE_ENV": "development",
    "DATABASE_URL": "postgresql://localhost:5432/mydb"
  },

  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/node:1": { "version": "20" }
  },

  "runArgs": ["--memory=4g", "--cpus=2"],

  "hostRequirements": {
    "cpus": 4,
    "memory": "8gb",
    "storage": "32gb"
  }
}
```

### 3.3 Common Base Images Reference

| Image Name | Use Case | Included Content |
|------------|----------|-----------------|
| `mcr.microsoft.com/devcontainers/javascript-node:20` | Node.js projects | Node.js 20, npm, yarn, Git |
| `mcr.microsoft.com/devcontainers/python:3.12` | Python projects | Python 3.12, pip, Git |
| `mcr.microsoft.com/devcontainers/java:17` | Java projects | JDK 17, Gradle, Maven, Git |
| `mcr.microsoft.com/devcontainers/go:1.22` | Go projects | Go 1.22, Git |
| `mcr.microsoft.com/devcontainers/rust:1` | Rust projects | Rust toolchain, Git |
| `mcr.microsoft.com/devcontainers/cpp:debian-12` | C/C++ projects | GCC, CMake, Git |
| `mcr.microsoft.com/devcontainers/dotnet:8.0` | .NET projects | .NET 8.0 SDK, Git |
| `mcr.microsoft.com/devcontainers/universal:2` | General purpose | Multi-language support |

### 3.4 Lifecycle Command Execution Order

devcontainer.json contains four lifecycle hook commands that execute in the following order:

1. **`onCreateCommand`:** Runs only when the container is first created (installing global packages, system-level dependencies)
2. **`postCreateCommand`:** Runs after container creation (installing project dependencies, database migrations)
3. **`postStartCommand`:** Runs each time the container starts (pulling latest code, starting services)
4. **`postAttachCommand`:** Runs each time VS Code connects to the container (displaying welcome messages)

```json
{
  "onCreateCommand": "npm install -g typescript nodemon",
  "postCreateCommand": "npm install && cp .env.example .env",
  "postStartCommand": "git fetch --all",
  "postAttachCommand": "echo 'Hello! Welcome to the development environment!'"
}
```

### 3.5 Using Dev Container Features

Features are pre-packaged development tool installation units that can be combined like building blocks:

```json
{
  "image": "mcr.microsoft.com/devcontainers/base:debian-12",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20",
      "nodeGypDependencies": true
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12",
      "installTools": true
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {
      "dockerDashComposeVersion": "v2"
    },
    "ghcr.io/devcontainers/features/github-cli:1": {
      "version": "latest"
    },
    "ghcr.io/devcontainers/features/terraform:1": {},
    "ghcr.io/devcontainers/features/kubernetes-helm:1": {}
  }
}
```

Common Features repository: `https://github.com/devcontainers/features`

---

## 4. Custom Development Containers (Dockerfile)

### 4.1 When You Need a Custom Dockerfile

When pre-built base images cannot meet your requirements, you need to write a custom Dockerfile. Common scenarios include:

- Needing to install specific versions of system-level dependencies (e.g., specific versions of OpenSSL, libcurl, etc.)
- Needing to configure special environment variables or system services
- Needing to install proprietary tools not available in Features
- Needing to deeply customize the system (e.g., modifying kernel parameters, installing drivers, etc.)

### 4.2 Basic Dockerfile Example

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/javascript-node:20

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
       postgresql-client \
       redis-tools \
       imagemagick \
       ffmpeg \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages
RUN npm install -g \
    pnpm \
    turbo \
    prisma \
    @nestjs/cli

# Install Rust toolchain (for certain Node.js native module compilation)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Configure zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Switch back to non-root user
USER vscode
```

### 4.3 Referencing Dockerfile in devcontainer.json

```json
{
  "name": "Custom Development Environment",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".",
    "args": {
      "NODE_VERSION": "20"
    }
  },
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

### 4.4 Multi-Stage Build Example

For complex projects, you can use multi-stage builds to optimize image size:

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/base:debian-12 AS base

# Stage 1: Install build tools
FROM base AS build-tools
RUN apt-get update && apt-get -y install build-essential cmake ninja-build

# Stage 2: Final image
FROM base
COPY --from=build-tools /usr/bin/cmake /usr/bin/cmake
COPY --from=build-tools /usr/bin/ninja /usr/bin/ninja

# Install project-specific dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
       libssl-dev \
       libsqlite3-dev \
       libcurl4-openssl-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
```

### 4.5 Docker Compose Integration

For projects requiring multiple services (such as databases, caches, message queues), you can use Docker Compose:

```yaml
# .devcontainer/docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    network_mode: service:db

  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

The corresponding `devcontainer.json`:

```json
{
  "name": "Full-Stack Development Environment",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [3000, 5432, 6379],
  "postCreateCommand": "npm install && npm run db:migrate",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-vscode.vscode-json",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg"
      ]
    }
  }
}
```

---

## 5. Port Forwarding and Web Preview

### 5.1 Port Forwarding Mechanism

Codespaces' port forwarding feature allows you to access services running in remote containers. When an application inside the container listens on a certain port, Codespaces automatically maps that port to a URL accessible through the browser.

Port forwarding has three visibility levels:

| Visibility | Description | Access Method |
|------------|-------------|---------------|
| **private** | Only the creator can access | Requires GitHub login |
| **org** | Members of the same organization can access | Requires GitHub login |
| **public** | Anyone can access | No login required |

### 5.2 Automatic Port Detection

When Codespaces detects that a service inside the container has started listening on a port, it automatically forwards that port. You may see a prompt like the following in the terminal:

```
Forwarding port 3000 to public URL https://your-codespace-name-3000.app.github.dev
```

### 5.3 Port Configuration Example

```json
{
  "forwardPorts": [3000, 5432, 8080],
  "portsAttributes": {
    "3000": {
      "label": "Frontend Development Server",
      "onAutoForward": "openBrowser",
      "visibility": "public"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "notify",
      "visibility": "private"
    },
    "8080": {
      "label": "API Server",
      "onAutoForward": "silent",
      "visibility": "org"
    }
  },
  "otherPortsAttributes": {
    "onAutoForward": "silent",
    "visibility": "private"
  }
}
```

### 5.4 Web Preview Feature

Codespaces provides a built-in Web preview feature that allows you to view the running web application directly in a panel next to the IDE, without opening a new browser tab.

How to use:

1. Right-click on a port → **Preview in Editor**
2. Or use the command palette: `Ports: Preview in Editor`
3. The preview panel will appear on the right side of the editor and can be resized

### 5.5 HTTPS and Custom Domains

All port-forwarded URLs automatically support HTTPS, in the following format:

```
https://<codespace-name>-<port>.app.github.dev
```

This is very useful for development scenarios requiring HTTPS (such as Service Workers, Web Crypto API, OAuth callbacks, etc.), without needing additional SSL certificate configuration.

---

## 6. VS Code and Codespaces Integration

### 6.1 VS Code Web Version

When you open a Codespace in a browser, you're using the VS Code Web version (based on vscode.dev architecture). It supports almost all features of the desktop VS Code, including:

- Full IntelliSense (code completion, type checking, go-to-definition)
- Integrated terminal (complete Linux shell environment)
- Debugger (supports remote debugging for Node.js, Python, Go, and other languages)
- Git integration (source control panel, commit, push, pull)
- Extension marketplace (most extensions are compatible with the web version)

### 6.2 VS Code Desktop Connection

After installing the **GitHub Codespaces** extension, you can connect to a remote Codespace from the desktop VS Code:

1. Open VS Code
2. Click the remote connection icon in the lower-left corner (or press `Ctrl+Shift+P` and type `Codespaces`)
3. Select **Codespaces: Connect to Codespace**
4. Select the Codespace to connect to from the list

The advantage of the desktop version is better performance, local filesystem access, and more extension support.

### 6.3 Settings Sync

Codespaces automatically integrates with VS Code's Settings Sync feature. The themes, keybindings, code snippets, and extensions you configure in your local VS Code are automatically synced to the Codespace. This means you don't need to reconfigure personal preferences in each new Codespace.

To enable Settings Sync:

1. Press `Ctrl+Shift+P` in VS Code
2. Type `Settings Sync: Turn On`
3. Login to your GitHub account
4. Select the settings items to sync

### 6.4 Keyboard Shortcut Mapping

When using VS Code in a browser, certain shortcuts may be intercepted by the browser (e.g., `Ctrl+W` closes the tab). Codespaces provides keyboard shortcut mapping functionality:

1. Press `Ctrl+Shift+P` to open the command palette
2. Type `Preferences: Open Keyboard Shortcuts (JSON)`
3. Add custom mappings

Or enable the **Codespaces: Keyboard Layout** option directly in the Codespace settings.

---

## 7. JetBrains Gateway Integration

### 7.1 Overview

In addition to VS Code, GitHub Codespaces also supports JetBrains IDEs, including IntelliJ IDEA, PyCharm, WebStorm, GoLand, PhpStorm, and others. This is implemented through JetBrains Gateway (gateway client).

### 7.2 Connection Steps

1. Download and install [JetBrains Gateway](https://www.jetbrains.com/remote-development/gateway/)
2. Open JetBrains Gateway and select **GitHub Codespaces** as the connection type
3. Login to your GitHub account
4. Select the Codespace to connect to from the list
5. Choose the JetBrains IDE to use (e.g., IntelliJ IDEA Ultimate)
6. Gateway will automatically download and configure the remote IDE backend
7. After the connection is established, you will see the familiar JetBrains IDE interface

### 7.3 Important Notes

- JetBrains IDE remote development requires larger machine configurations (recommended at least 4 cores and 16GB)
- On first connection, Gateway needs to install JetBrains Backend on the remote server, which may take several minutes
- Some plugins that require local filesystem access may not be compatible with remote development mode
- JetBrains' free Community Edition does not support remote development; a Professional license is required

---

## 8. GitHub CLI Managing Codespaces

### 8.1 Common Commands Quick Reference

```bash
# Create Codespace
gh codespace create --repo owner/repo --branch main --machine 4-core

# List all Codespaces
gh codespace list
gh codespace list --json name,state,machine,frozenAt

# Connect to Codespace (via SSH)
gh codespace ssh

# Connect to Codespace (via VS Code desktop)
gh codespace code

# View Codespace details
gh codespace view --codespace my-codespace

# Stop Codespace
gh codespace stop --codespace my-codespace

# Start Codespace
gh codespace start --codespace my-codespace

# Delete Codespace
gh codespace delete --codespace my-codespace

# Execute command in Codespace
gh codespace ssh --command "npm test"

# Forward port
gh codespace ports forward 3000:3000 --codespace my-codespace

# List port forwarding
gh codespace ports list --codespace my-codespace

# Edit Codespace machine configuration
gh codespace edit --codespace my-codespace --machine 8-core

# View Codespace logs
gh codespace logs --codespace my-codespace
```

### 8.2 Batch Management Script

```bash
#!/bin/bash
# Stop all running Codespaces
echo "Stopping all running Codespaces..."
gh codespace list --json name,state -q '.[] | select(.state=="Available") | .name' | while read name; do
    echo "Stopping: $name"
    gh codespace stop --codespace "$name"
done
echo "Done!"

# Delete all Codespaces that have been stopped for more than 7 days
echo "Cleaning up long-unused Codespaces..."
gh codespace list --json name,frozenAt -q '.[] | select(.frozenAt != null) | .name' | while read name; do
    echo "Deleting: $name"
    gh codespace delete --codespace "$name" --force
done
```

### 8.3 Advanced SSH Usage

```bash
# Configure SSH alias
gh codespace ssh --config >> ~/.ssh/config

# Transfer files using scp
gh codespace scp -r ./local-dir :/workspaces/repo/remote-dir

# Sync files using rsync
gh codespace ssh -- rsync -avz /workspaces/repo/ ./backup/
```

---

## 9. Codespaces Secrets Configuration

### 9.1 Purpose of Secrets

Secrets are used to store sensitive information such as API keys, database passwords, access tokens, and more. They are stored in encrypted form and do not appear in Codespace environment variable logs or get committed to Git repositories.

### 9.2 Configuring Secrets

**Via the web interface:**

1. Go to the repository or organization **Settings** → **Codespaces**
2. In the **Secrets** section, click **New repository secret** or **New organization secret**
3. Enter the Secret name and value
4. Select which Codespaces can access the Secret (optional)

**Via GitHub CLI:**

```bash
# Add repository-level Secret
gh secret set API_KEY --body "your-secret-value" --repo owner/repo

# Add organization-level Secret
gh secret set ORG_API_KEY --body "your-secret-value" --org my-org

# Read Secret from file
gh secret set GOOGLE_CREDENTIALS --body "$(cat credentials.json)" --repo owner/repo

# List all Secrets
gh secret list --repo owner/repo

# Delete Secret
gh secret delete OLD_API_KEY --repo owner/repo
```

### 9.3 Using Secrets in Codespace

Secrets are automatically injected as environment variables:

```bash
# Use in terminal
echo $API_KEY

# Use in Node.js
console.log(process.env.API_KEY);

# Use in Python
import os
api_key = os.environ.get('API_KEY')

# Reference in .env file (not recommended to write Secrets to files)
# It's recommended to use environment variables directly
```

### 9.4 Secret Best Practices

- Use meaningful names, like `STRIPE_SECRET_KEY` instead of `KEY1`
- Use different Secrets for different environments (development, testing, production)
- Rotate Secrets regularly
- Use organization-level Secrets for cross-repository sharing
- Don't print Secrets in commands like `postCreateCommand`

---

## 10. Team Codespaces Management

### 10.1 Organization-Level Configuration

Organization administrators can configure Codespaces usage policies in organization settings:

1. Go to the organization **Settings** → **Codespaces**
2. Configure the following policies:
   - **Permission Policy:** Who can create Codespaces
   - **Machine Type Restrictions:** Maximum machine configuration allowed
   - **Region Restrictions:** Allowed Azure regions
   - **Timeout Policy:** Mandatory maximum idle timeout
   - **Retention Policy:** Maximum retention days for Codespaces

### 10.2 Cost Management

Organizations can set spending limits for Codespaces:

1. Go to the organization **Settings** → **Billing and plans**
2. Set a monthly spending limit in the **Codespaces** section
3. Configure behavior when the limit is reached (notification, block new Codespace creation)

### 10.3 Sharing Codespace Configuration

By committing `devcontainer.json` in the repository, ensure all team members use the same development environment:

```
.github/
└── devcontainer/
    ├── devcontainer.json      # Main configuration
    ├── Dockerfile              # Custom image
    ├── docker-compose.yml      # Multi-service configuration
    ├── setup.sh                # Initialization script
    └── README.md               # Environment documentation
```

---

## 11. Prebuild Configuration (Prebuilds)

### 11.1 What are Prebuilds

Prebuilds is a mechanism provided by GitHub to accelerate Codespace startup. It pre-builds and caches development container images. When a user creates a Codespace, it directly uses the cached image, reducing startup time from minutes to seconds.

### 11.2 Configuring Prebuilds

1. Go to the repository **Settings** → **Codespaces** → **Prebuilds**
2. Click **New prebuild configuration**
3. Configure the following options:
   - **Branch:** Select the branch to prebuild (usually main)
   - **Region:** Select the geographic region for prebuilds
   - **Machine Type:** Select the machine configuration for prebuilds
   - **Trigger Events:** Select when to trigger prebuilds (push, schedule, etc.)

### 11.3 Prebuilds Configuration Example

```json
{
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "onCreateCommand": "npm install -g pnpm turbo",
  "postCreateCommand": "pnpm install && pnpm build",
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

### 11.4 Prebuilds Cost

Prebuilds themselves do not incur additional charges, but they consume storage space (for caching images). It's recommended to configure Prebuilds only for frequently used branches to avoid unnecessary storage overhead.

### 11.5 Relationship Between Prebuilds and Actions

Prebuilds actually use GitHub Actions to build container images. You need to ensure your repository has sufficient Actions minutes to support Prebuilds. If your repository is public, Actions minutes are unlimited; for private repositories, you need to obtain the appropriate minutes based on your plan.

---

## 12. Cost Control and Optimization

### 12.1 Cost Optimization Strategies

**Choose the right machine configuration:**

- Use 2 cores for daily coding
- Temporarily upgrade to 4 or 8 cores when compilation and building is needed
- Downgrade back to 2 cores after completion

**Set appropriate timeout values:**

```json
{
  "settings": {
    "codespaces.prebuildRetentionPeriodDays": 7,
    "codespaces.idleTimeout": 30,
    "codespaces.defaultIdleTimeout": 60
  }
}
```

**Use scheduled stopping:**

```bash
# Set auto-stop after 2 hours
gh codespace edit --codespace my-codespace --idle-timeout 120
```

### 12.2 Monitoring Usage

1. Go to **Settings** → **Billing and plans** → **Codespaces**
2. View the current month's core-hours used
3. Set spending limit alerts

```bash
# View current billing cycle usage
gh api /user/settings/billing/codespaces
```

### 12.3 Freeze and Dormancy

Codespaces automatically stops (freezes) after idle timeout. A stopped Codespace:

- Does not consume core-hours (computation costs)
- Still consumes storage space ($0.07/GB/month)
- Retained for up to 30 days (Free plan) or 90 days (paid plans)

### 12.4 Practical Tips for Saving Costs

1. **Use Prebuilds:** Reduce build time during each creation, indirectly saving core-hours
2. **Create on demand:** Don't long-term retain unused Codespaces
3. **Batch operations:** Use CLI scripts to batch stop or delete Codespaces
4. **Use branches wisely:** Create different Codespaces for different development tasks, delete them promptly after completion
5. **Take advantage of free allowance:** Plan usage time wisely to fully utilize the monthly free core-hours

---

## 13. Codespaces and GitHub Copilot Integration

### 13.1 Enabling GitHub Copilot

GitHub Copilot is available by default in Codespaces (requires a Copilot subscription). Enabling steps:

1. Ensure your GitHub account has a Copilot subscription (Individual $10/month, Business $19/user/month)
2. After creating a Codespace, the Copilot extension is automatically installed and activated
3. Start writing code in the editor, and Copilot will automatically provide suggestions

### 13.2 Copilot Chat

Copilot Chat is an AI conversation feature that can be used directly in Codespaces:

1. Press `Ctrl+Shift+I` to open the Copilot Chat panel
2. Enter your question or request
3. Copilot will provide answers based on your code context

Common commands:
- `/explain` - Explain selected code
- `/fix` - Fix issues in code
- `/test` - Generate tests for code
- `/doc` - Generate documentation for code

### 13.3 Copilot's Codespaces Advantage

Unique advantages of using Copilot in Codespaces:

- **Enhanced Context Awareness:** Copilot can access the entire project code, not just the currently open file
- **Terminal Integration:** Use Copilot in the terminal to generate shell commands
- **PR Description Generation:** Combined with GitHub CLI, Copilot can automatically generate PR descriptions and commit messages

---

## 14. Network Optimization for Chinese Developers Using Codespaces

### 14.1 Network Latency Issues

Because Codespaces servers are located overseas (mainly US and European Azure data centers), Chinese developers may encounter the following issues:

- Slow image pulling when creating Codespaces
- High latency in terminal operations
- Slow file synchronization speed
- Slow loading of port-forwarded Web previews

### 14.2 Optimization Strategies

**Use a proxy:**

Configure proxy in devcontainer.json:

```json
{
  "containerEnv": {
    "HTTP_PROXY": "http://your-proxy:port",
    "HTTPS_PROXY": "http://your-proxy:port",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}
```

**Use domestic mirror sources:**

```json
{
  "postCreateCommand": "npm config set registry https://registry.npmmirror.com && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"
}
```

**Use domestic mirrors in Dockerfile:**

```dockerfile
FROM mcr.microsoft.com/devcontainers/javascript-node:20

# Use Tsinghua npm mirror
RUN npm config set registry https://registry.npmmirror.com

# Use Alibaba Cloud Maven mirror (Java projects)
RUN mkdir -p ~/.m2 && echo '<settings><mirrors><mirror><id>aliyun</id><url>https://maven.aliyun.com/repository/public</url><mirrorOf>central</mirrorOf></mirror></mirrors></settings>' > ~/.m2/settings.xml
```

### 14.3 Choosing the Right Region

When creating a Codespace, you can select the closest region:

- **East US:** Default region, relatively good for China
- **West Europe:** Slightly higher latency, but sometimes more stable
- **Southeast Asia:** Closest physical distance, but not always available

### 14.4 Combining Local Development and Codespaces

For poor network conditions, it's recommended to:

1. Use Codespaces for environment setup and dependency installation
2. Use VS Code desktop's Remote - SSH feature to connect to the Codespace
3. Use Settings Sync to keep local and remote environments consistent
4. For large file operations, use GitHub CLI's `codespace scp` command

---

## 15. Practical Examples

### 15.1 Full-Stack Web Application Development

**Project Structure:**

```
my-fullstack-app/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   └── Dockerfile
├── frontend/
│   ├── package.json
│   └── src/
├── backend/
│   ├── package.json
│   └── src/
└── docker-compose.yml
```

**devcontainer.json Configuration:**

```json
{
  "name": "Full-Stack Development Environment",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [3000, 5432, 8080],
  "portsAttributes": {
    "3000": { "label": "Frontend" },
    "8080": { "label": "Backend API" }
  },
  "postCreateCommand": "cd frontend && npm install && cd ../backend && npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next"
      ]
    }
  }
}
```

### 15.2 Python Data Science Project

**devcontainer.json Configuration:**

```json
{
  "name": "Data Science Environment",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/node:1": {}
  },
  "postCreateCommand": "pip install -r requirements.txt && jupyter notebook --generate-config",
  "forwardPorts": [8888],
  "portsAttributes": {
    "8888": { "label": "Jupyter Notebook" }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "ms-python.vscode-pylance"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  }
}
```

### 15.3 Open Source Project Contribution Environment

When contributing code to open source projects, Codespaces is the most convenient way:

```bash
# 1. Create Codespace after forking repository
gh codespace create --repo your-fork/repo-name

# 2. Create feature branch in Codespace
gh codespace ssh --command "git checkout -b feature/my-feature"

# 3. Develop and test
gh codespace ssh --command "npm test"

# 4. Commit and push
gh codespace ssh --command "git add . && git commit -m 'feat: add new feature' && git push origin feature/my-feature"

# 5. Create Pull Request
gh codespace ssh --command "gh pr create --title 'feat: add new feature' --body 'Description of changes'"
```

### 15.4 Teaching and Training Environment

Codespaces is excellent for programming education and training:

```json
{
  "name": "Programming Introductory Course",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "postCreateCommand": "echo 'Welcome to the programming course!' && python --version && node --version",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "dbaeumer.vscode-eslint",
        "formulahendry.code-runner"
      ],
      "settings": {
        "terminal.integrated.defaultProfile.linux": "bash"
      }
    }
  }
}
```

Teachers can place course materials and exercise code in a repository, and students only need to click one button to get a complete learning environment, without spending time configuring local development environments.

---

## 16. Advanced Codespaces Tips and Tricks

### 16.1 Using GPG Signed Commits

Configuring GPG signing in Codespaces ensures your commits are authenticated. First, generate or import a GPG key in the Codespace:

```bash
# Check if GPG key already exists
gpg --list-secret-keys --keyid-format=long

# If no key exists, generate a new one
gpg --full-generate-key

# Get key ID
gpg --list-secret-keys --keyid-format=long
# Output example: sec   rsa4096/ABC123DEF456 2024-01-01 [SC]

# Configure Git to use this key
git config --global user.signingkey ABC123DEF456
git config --global commit.gpgsign true

# Export public key to add to GitHub account settings
gpg --armor --export ABC123DEF456
```

Add the exported public key to GitHub's Settings → SSH and GPG keys → New GPG key, and all subsequent commits in the Codespace will be automatically signed.

### 16.2 Multi-Repository Workspace

Work on multiple related repositories simultaneously in a single Codespace:

```json
{
  "name": "Multi-Repository Workspace",
  "image": "mcr.microsoft.com/devcontainers/base:debian-12",
  "postCreateCommand": "git clone https://github.com/company/shared-lib.git /workspaces/shared-lib && git clone https://github.com/company/utils.git /workspaces/utils",
  "customizations": {
    "vscode": {
      "folders": [
        { "path": "/workspaces/main-project" },
        { "path": "/workspaces/shared-lib" },
        { "path": "/workspaces/utils" }
      ]
    }
  }
}
```

### 16.3 Database Connection and Management

Connect to remote databases or use local databases in a Codespace:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/postgres:1": {
      "version": "16"
    }
  },
  "postCreateCommand": "sudo service postgresql start && psql -c \"CREATE USER devuser WITH PASSWORD 'devpass';\" && psql -c \"CREATE DATABASE myapp OWNER devuser;\"",
  "customizations": {
    "vscode": {
      "extensions": [
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg",
        "cweijan.vscode-postgresql-client2"
      ]
    }
  }
}
```

### 16.4 Using Codespace for Code Review

Codespaces are excellent for code review, allowing you to test others' code changes in an isolated environment:

1. Open the PR page
2. Click the "Open in Codespace" button (if Prebuild is configured, it will start quickly)
3. Run tests, build the project, and verify functionality in the Codespace
4. After completing the review, submit review comments directly in the Codespace

### 16.5 Environment Variables and Configuration Files

Best practices for managing environment variables in a Codespace:

```bash
# Create .env file in Codespace (don't commit to repository)
cp .env.example .env

# Edit environment variables
vim .env

# Ensure .env is in .gitignore
echo ".env" >> .gitignore
```

For sensitive information, it's strongly recommended to use Codespaces Secrets instead of .env files:

```bash
# Set Secrets via CLI
gh secret set DATABASE_URL --body "postgresql://user:pass@host:5432/db" --repo owner/repo

# Use in Codespace
echo $DATABASE_URL
```

### 16.6 Performance Monitoring and Debugging

Monitor Codespace resource usage:

```bash
# View CPU and memory usage
htop

# View disk usage
df -h

# View network connections
ss -tuln

# View processes
ps aux

# Clean up unnecessary files to free space
sudo apt-get clean
rm -rf ~/.cache/pip
rm -rf ~/.npm/_cacache
docker system prune -f  # If using Docker
```

### 16.7 Offline Work and Network Recovery

While Codespaces relies on network connectivity, you can take measures to handle network instability:

```bash
# Pre-cache dependencies
npm install  # node_modules will be cached after installation
pip install -r requirements.txt  # pip packages will be cached

# Use Git's offline mode
git config --global transfer.fsckObjects true
git config --global fetch.prune true

# Regularly commit local changes
git add . && git commit -m "WIP: local changes"
```

### 16.8 Custom Shell Environment

Configure personalized shell environments to improve development efficiency:

```json
{
  "postCreateCommand": "sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git clone https://github.com/zsh-users/zsh-syntax-highlighting ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
  "customizations": {
    "vscode": {
      "settings": {
        "terminal.integrated.defaultProfile.linux": "zsh",
        "terminal.integrated.profiles.linux": {
          "zsh": {
            "path": "/bin/zsh"
          }
        }
      }
    }
  }
}
```

### 16.9 Using GitHub Copilot Terminal Integration

Use Copilot directly in the Codespace terminal to generate commands:

```bash
# Press Ctrl+I in the terminal to invoke Copilot
# Enter a natural language description, and Copilot will generate the corresponding command

# Example:
# "List all files larger than 100MB"
# Copilot generates: find . -type f -size +100M -exec ls -lh {} \;
```

### 16.10 Snapshots and Recovery

Although Codespace automatically saves state, manually creating snapshots is a better practice:

```bash
# Create Git stash to save current work state
git stash save "WIP: feature-x implementation"

# View all stashes
git stash list

# Restore stash
git stash pop

# Create backup branch
git checkout -b backup/2024-01-15
git push origin backup/2024-01-15
git checkout main
```

---

## 17. Frequently Asked Questions (FAQ)

### Q1: What is the difference between Codespace and GitHub Dev Environment?

GitHub Codespaces is a complete cloud development environment providing virtual machine-level isolation and a full Linux environment. GitHub Dev Environment (accessed via github.dev) is a lightweight browser-based code editor that runs VS Code directly in the browser without a backend virtual machine, suitable for quick browsing and light editing.

### Q2: Is data in Codespace safe?

Codespace data is stored on Microsoft Azure cloud infrastructure using encrypted storage. Each Codespace runs in an isolated virtual machine, completely separated from other users' Codespaces. However, it's recommended not to store highly sensitive data in Codespaces and to use Secrets for managing sensitive information.

### Q3: How to handle Git conflicts in Codespace?

When multiple collaborators modify the same Codespace simultaneously, Git conflicts may occur. The solution is:

```bash
# View conflicting files
git status

# Commit after resolving conflicts
git add .
git commit -m "resolve: merge conflict"
```

### Q4: Does Codespace support GPU?

Currently, GitHub Codespaces does not support GPU acceleration. If you need GPU computing (such as machine learning training), it's recommended to use Google Colab, AWS SageMaker, or other cloud services that support GPUs.

### Q5: How to use a private npm registry in Codespace?

```json
{
  "postCreateCommand": "echo '//npm.pkg.github.com/:_authToken=${NPM_TOKEN}' > ~/.npmrc",
  "containerEnv": {
    "NPM_TOKEN": "${localEnv:NPM_TOKEN}"
  }
}
```

Or use Codespaces Secrets to store NPM_TOKEN.

### Q6: What to do if Codespace runs out of storage?

```bash
# View disk usage details
du -sh /* | sort -rh | head -20

# Clean apt cache
sudo apt-get clean
sudo apt-get autoremove

# Clean npm cache
npm cache clean --force

# Clean pip cache
pip cache purge

# Clean Docker (if used)
docker system prune -a -f

# Delete old log files
sudo journalctl --vacuum-time=7d
```

### Q7: How to auto-run an application after Codespace creation?

Use `postStartCommand` in `devcontainer.json`:

```json
{
  "postStartCommand": "npm run dev &",
  "forwardPorts": [3000],
  "portsAttributes": {
    "3000": {
      "label": "Development Server",
      "onAutoForward": "openBrowser"
    }
  }
}
```

### Q8: How to use custom CA certificates in Codespace?

```json
{
  "postCreateCommand": "sudo cp /path/to/custom-ca.crt /usr/local/share/ca-certificates/ && sudo update-ca-certificates",
  "containerEnv": {
    "NODE_EXTRA_CA_CERTS": "/usr/local/share/ca-certificates/custom-ca.crt"
  }
}
```

### Q9: How long can a Codespace be used?

Codespaces are retained for a certain time after being stopped. The free plan retains them for 30 days, and paid plans for 90 days. After the retention period, the Codespace is automatically deleted. Running Codespaces have no time limit, but continue to incur costs.

### Q10: How to use Docker in Codespace?

Codespaces supports Docker, but you need to enable the Docker-in-Docker feature in devcontainer.json:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  }
}
```

Once enabled, you can run docker build, docker run, and other commands in the Codespace, just like in a local environment.

### Q11: How to upload local files to Codespace?

You can use GitHub CLI's scp command:

```bash
# Upload a single file
gh codespace scp ./local-file.txt :/workspaces/repo/remote-file.txt

# Upload an entire directory
gh codespace scp -r ./local-dir :/workspaces/repo/remote-dir

# Download file to local
gh codespace scp :/workspaces/repo/remote-file.txt ./local-file.txt
```

### Q12: How to run background services in Codespace?

Use postStartCommand to automatically run background services when the Codespace starts:

```json
{
  "postStartCommand": "npm run dev &",
  "forwardPorts": [3000]
}
```

Or use the nohup command:

```bash
nohup npm run dev > /tmp/dev-server.log 2>&1 &
```

### Q13: Which operating systems does Codespace support?

Currently, Codespaces only supports Linux operating systems (based on Ubuntu or Debian). Windows and macOS are not supported. However, you can use Wine in a Codespace to run some Windows programs.

### Q14: How to use databases in Codespace?

Codespaces supports multiple databases, which can be installed via Features or Docker Compose:

```json
{
  "features": {
    "ghcr.io/devcontainers/features/postgres:1": {},
    "ghcr.io/devcontainers/features/redis:1": {},
    "ghcr.io/devcontainers/features/mongodb:1": {}
  }
}
```

### Q15: How to share a Codespace with team members?

You can create shared Codespace configurations through organization settings. Commit devcontainer.json files in the repository to ensure all team members use the same development environment. You can also share sensitive configurations through Codespace Secrets.

### Q16: Does Codespace support Git LFS?

Yes, Codespaces fully supports Git LFS (Large File Storage). If your project uses Git LFS, the Codespace will automatically download LFS files. For large files, it's recommended to configure shallow cloning in devcontainer.json to speed up startup.

### Q17: How to do remote debugging in Codespace?

VS Code supports remote debugging. You can configure launch.json in the Codespace, then map the debugging port to local through port forwarding. For Node.js applications, you can directly use VS Code's built-in debugger to connect to the running process.

### Q18: Is the Codespace's network egress IP fixed?

No. The Codespace's egress IP may change. If your service requires IP whitelisting, it's recommended to use a fixed proxy service or VPN solution.

### Q19: How to use private Docker images in Codespace?

You can configure Docker registry authentication in devcontainer.json. First, store Docker credentials as a Codespace Secret, then authenticate during container startup. You can also use cloud services like Azure Container Registry to host private images.

### Q20: Does Codespace support WebSocket connections?

Yes, Codespaces fully supports WebSocket connections. The port forwarding service automatically handles WebSocket upgrade requests. This is important for real-time applications (such as chat applications, online games, real-time data push, etc.).

### Q21: How to use GitHub Copilot in Codespace?

GitHub Copilot is available by default in Codespaces without additional configuration. Just ensure your GitHub account has a Copilot plan subscription. When writing code in the editor, Copilot will automatically provide suggestions. You can also use Copilot Chat for conversational programming.

### Q22: What is Codespace's data backup strategy?

It's recommended to regularly push important data to remote repositories. For stateful services like databases, you can configure periodic backup scripts. Data is retained after Codespace is stopped but cannot be recovered after deletion, so important data should always have remote backups.

---

## 18. Future Development of Codespaces

GitHub Codespaces is rapidly evolving, and future updates may include:

1. **GPU Support:** Providing GPU acceleration for machine learning and data science projects
2. **More Operating Systems:** Supporting Windows and macOS development environments
3. **Better Offline Support:** Reducing dependency on network connectivity
4. **More Granular Permission Control:** Allowing finer access control
5. **More IDE Integration:** Supporting editors like Vim and Neovim
6. **Lower Latency:** Deploying data centers in more regions worldwide to reduce latency
7. **Better Collaboration Features:** Real-time multi-user editing and debugging
8. **Smarter Resource Management:** Automatically adjusting resource configurations based on usage patterns

As a developer, staying aware of these development trends can help you better plan your development environment strategy and fully leverage the advantages of cloud-based development.

## 19. Appendix: Common Commands Quick Reference

### 19.1 GitHub CLI Commands

| Command | Description |
|---------|-------------|
| `gh codespace create` | Create a new Codespace |
| `gh codespace list` | List all Codespaces |
| `gh codespace delete` | Delete a specified Codespace |
| `gh codespace start` | Start a stopped Codespace |
| `gh codespace stop` | Stop a running Codespace |
| `gh codespace ssh` | Connect to Codespace via SSH |
| `gh codespace code` | Open Codespace in VS Code desktop |
| `gh codespace ports forward` | Forward ports |
| `gh codespace ports list` | List port forwarding |
| `gh codespace edit` | Modify Codespace configuration |
| `gh codespace logs` | View Codespace logs |
| `gh codespace scp` | Transfer files between local and Codespace |

### 19.2 Common devcontainer.json Configuration

| Configuration Item | Description | Example |
|--------------------|-------------|---------|
| `name` | Container name | `"My Development Environment"` |
| `image` | Base image | `"mcr.microsoft.com/devcontainers/javascript-node:20"` |
| `build.dockerfile` | Custom Dockerfile | `"Dockerfile"` |
| `forwardPorts` | Ports to forward | `[3000, 8080]` |
| `postCreateCommand` | Command to run after creation | `"npm install"` |
| `postStartCommand` | Command to run after startup | `"npm run dev &"` |
| `customizations.vscode.extensions` | VS Code extensions | `["dbaeumer.vscode-eslint"]` |
| `customizations.vscode.settings` | VS Code settings | `{"editor.formatOnSave": true}` |
| `features` | Dev container features | `{"ghcr.io/devcontainers/features/node:1": {}}` |
| `containerEnv` | Environment variables | `{"NODE_ENV": "development"}` |
| `remoteUser` | Remote user | `"vscode"` |
| `hostRequirements` | Host requirements | `{"cpus": 4, "memory": "8gb"}` |

### 19.3 Common Features List

| Feature | Description |
|---------|-------------|
| `ghcr.io/devcontainers/features/node:1` | Node.js runtime |
| `ghcr.io/devcontainers/features/python:1` | Python runtime |
| `ghcr.io/devcontainers/features/go:1` | Go runtime |
| `ghcr.io/devcontainers/features/rust:1` | Rust toolchain |
| `ghcr.io/devcontainers/features/java:1` | Java runtime |
| `ghcr.io/devcontainers/features/docker-in-docker:2` | Docker support |
| `ghcr.io/devcontainers/features/github-cli:1` | GitHub CLI |
| `ghcr.io/devcontainers/features/terraform:1` | Terraform |
| `ghcr.io/devcontainers/features/kubernetes-helm:1` | Kubernetes and Helm |
| `ghcr.io/devcontainers/features/git:1` | Git configuration |

### 19.4 Quick Solutions to Common Problems

| Problem | Solution |
|---------|----------|
| Slow Codespace startup | Use Prebuilds or select a closer region |
| Port not accessible | Check port visibility settings |
| Extension incompatible | Check if the extension supports web VS Code |
| Insufficient disk space | Clean cache and temporary files |
| Network connection issues | Check proxy configuration or use domestic mirrors |
| Submodule not initialized | Run `git submodule update --init` |
| Environment variable not effective | Restart Codespace or reload terminal |
| Dependency installation failed | Check network connection or use mirror sources |
| Terminal not accepting input | Refresh page or reconnect |
| Code completion not working | Check if language server is running |
| Git operation failed | Check GitHub authentication status |
| Build timeout | Upgrade machine configuration or optimize build scripts |
| Insufficient memory | Upgrade to a machine with more memory |
| Cannot push to remote | Check permissions and authentication configuration |
| Port conflict | Modify application listening port or stop conflicting services |

### 19.5 Development Environment Configuration Template Library

Here are some devcontainer.json templates for common project types:

**React + Node.js Full-Stack Project:**

```json
{
  "name": "React Full-Stack Project",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "forwardPorts": [3000, 5173],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss"
      ]
    }
  }
}
```

**Python Django Project:**

```json
{
  "name": "Django Project",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "forwardPorts": [8000],
  "postCreateCommand": "pip install -r requirements.txt && python manage.py migrate",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  }
}
```

**Go Microservice Project:**

```json
{
  "name": "Go Microservice",
  "image": "mcr.microsoft.com/devcontainers/go:1.22",
  "forwardPorts": [8080],
  "postCreateCommand": "go mod download",
  "customizations": {
    "vscode": {
      "extensions": [
        "golang.go"
      ]
    }
  }
}
```

**Rust Systems Programming Project:**

```json
{
  "name": "Rust Project",
  "image": "mcr.microsoft.com/devcontainers/rust:1",
  "forwardPorts": [8000],
  "postCreateCommand": "cargo build",
  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer"
      ]
    }
  }
}
```

---

## Summary

GitHub Codespaces is a powerful cloud development tool that completely solves pain points of environment configuration by codifying development environments, dramatically improving team collaboration efficiency. For Chinese developers, while there are certain network latency issues, reasonable configuration and optimization strategies allow you to fully leverage its advantages.

Key takeaways:

1. **Environment as Code:** Use `devcontainer.json` to define reproducible development environments, ensuring team consistency
2. **Flexible Configuration:** Choose appropriate machine configurations, tools, and extensions based on project requirements
3. **Cost Control:** Set appropriate timeouts, promptly delete unused Codespaces, and fully utilize free allowances
4. **Team Collaboration:** Implement secure team development through organization settings and Secrets management
5. **Performance Optimization:** Use Prebuilds to speed up startup, use domestic mirror sources to optimize download speeds
6. **Security Practices:** Use GPG signing, Secrets to manage sensitive information, and be mindful of data security
7. **Advanced Techniques:** Multi-repository workspaces, database management, Copilot integration, and more to improve development efficiency

Whether you're an individual developer or collaborating in a team, Codespaces provides a consistent, efficient, and secure development environment. Combined with GitHub Copilot's AI-assisted programming capabilities, Codespaces is redefining the way modern software development works.

For beginners, it's recommended to start with the following steps:

1. Choose a simple open source repository and create your first Codespace
2. Familiarize yourself with the basic operations of VS Code Web and terminal usage
3. Try modifying `devcontainer.json` to customize the development environment
4. Use GitHub CLI to manage your Codespace
5. Create `devcontainer.json` configuration for your own projects
6. Explore advanced features like Prebuilds, Secrets, and more

Through continuous practice and exploration, you'll be able to fully leverage Codespaces' powerful features, improve development efficiency, and enjoy the convenience of cloud-based development.

---

**Previous: [GitHub Packages Introduction](J-github-packages.md) | Next: [GitHub Mobile Introduction](K-github-mobile.md)**

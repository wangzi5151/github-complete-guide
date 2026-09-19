# Exercise 23: Developing with GitHub Codespaces

## Learning Objectives

Through this exercise, you will master the following skills:

- Understand how GitHub Codespaces works
- Create and configure Codespaces
- Develop using VS Code in the browser
- Create and customize devcontainer configurations
- Manage the lifecycle of Codespaces
- Share development environment configurations within a team

## Prerequisites

- A GitHub account
- Understanding of GitHub Codespaces usage quotas (free users receive a certain number of hours per month)
- Basic Git operation knowledge
- Basic understanding of Docker concepts (optional, but helpful)

## Part 1: Understanding GitHub Codespaces

### What is GitHub Codespaces?

GitHub Codespaces is a cloud-based development environment that provides the following capabilities:

1. **Ready to use**: Spin up a complete development environment in seconds
2. **Consistent configuration**: Team members use the same development environment configuration
3. **Cloud-based execution**: Code runs in the cloud, so your local machine doesn't need to be high-end
4. **Pre-configured environment**: Pre-installed with common development tools and runtimes
5. **Seamless integration**: Deep integration with GitHub repositories

### Use Cases

Codespaces is particularly well-suited for the following scenarios:

- Quickly starting new project development without local environment setup
- Contributing to open source projects without local environment conflicts
- Seamlessly switching development environments across different devices
- Ensuring team members use consistent development environments
- Quickly running and testing code during code reviews

## Part 2: Creating Your First Codespace

In this section, you will create a GitHub Codespace and experience the convenience of cloud-based development firsthand. The process of creating a Codespace is very simple and intuitive. GitHub provides multiple ways to create one, including from the repository page, from the command line, and from existing templates. Regardless of which method you choose, GitHub will allocate a complete development environment for you in the cloud, which includes all the tools and dependencies your project requires. After creation, you can access VS Code in the browser directly, or connect remotely to your Codespace through a local VS Code client. The entire process typically takes only a few minutes, which is a significant time and effort savings compared to traditional local development environment setup.

### Step 1: Create from a GitHub Repository

1. Open your GitHub repository page
2. Click the green "Code" button
3. Switch to the "Codespaces" tab
4. Click "Create codespace on main"

```
Repository Page Layout:
┌─────────────────────────────────────┐
│ [Code] [Issues] [Pull requests] ... │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────┐                        │
│  │ Code ▼  │  ← Click here          │
│  └─────────┘                        │
│  ┌─────────────────────────────┐    │
│  │ Local │ GitHub Codespaces │  │    │
│  │       │ ───────────────── │  │    │
│  │       │ Create on main    │  │    │
│  │       │ ───────────────── │  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### Step 2: Wait for Codespace to Start

After creating the Codespace, GitHub will execute the following steps:

1. Allocate a cloud virtual machine
2. Clone your repository code
3. Install development tools based on the configuration
4. Launch VS Code in the browser

This process typically takes 30 seconds to 2 minutes.

### Step 3: Familiarize Yourself with the VS Code Web Interface

After the Codespace starts, you will see the familiar VS Code interface:

```
┌────────┬──────────────────────────────────────────┐
│        │  explorer  │  editor area                │
│ File   │  ┌───────┐ │  ┌──────────────────────┐   │
│ Explo- │  │ File  │ │  │  Code Editor Area     │   │
│ rer    │  │ Tree  │ │  │                      │   │
│        │  └───────┘ │  └──────────────────────┘   │
│        │            │                              │
│        │            │  ┌──────────────────────┐   │
│        │            │  │  Terminal/Output Area │   │
│        │            │  └──────────────────────┘   │
├────────┴────────────┴──────────────────────────────┤
│ Status Bar: Shows connection status, branch info, etc. │
└─────────────────────────────────────────────────────┘
```

### Step 4: Run Commands in the Terminal

In the Codespace terminal, you can run commands just like you would locally. Codespace provides a complete terminal environment, supporting common shell commands and development tools. You can install dependencies, run tests, start services, execute scripts, and more in the terminal. Since Codespace runs in a cloud Linux environment, you should be aware of some differences from a local environment. For example, file paths may differ from your local operating system, and some system-level operations may require specific permissions. Additionally, the Codespace terminal supports multi-tab and split-screen functionality, making it convenient to run multiple commands simultaneously or view different output:

```bash
# View current directory
pwd
# Output: /workspaces/your-repo-name

# View file list
ls -la

# View Git status
git status

# Install project dependencies (using Node.js project as an example)
npm install

# Run the project
npm start

# Run tests
npm test
```

### Step 5: Edit and Commit Code

Modify and commit code in the Codespace:

```bash
# Create a new branch
git checkout -b feature/new-feature

# Edit files (modify directly in the editor)
# ...

# View changes
git diff

# Commit changes
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature
```

## Part 3: Configuring devcontainer

Development Container configuration is one of the core features of GitHub Codespaces. By using development container configurations, you can define your entire development environment as code, which means you can manage your development environment configuration just like you manage application code. This approach brings many benefits: first, it ensures that every developer on the team uses exactly the same development environment, avoiding the "it works on my machine" problem; second, new team members can set up their development environment in minutes without spending a lot of time on manual configuration; finally, development environment configurations can be version-controlled, and any environment changes can be reviewed through the code review process to ensure quality.

### What is devcontainer?

`devcontainer` is a JSON configuration file that defines the Codespace development environment. It is located at `.devcontainer/devcontainer.json`. This configuration file can specify the base image, development tools to install, VS Code extensions, port forwarding rules, environment variables, and project initialization commands. When the Codespace starts, the system reads this configuration file and configures the development environment according to its definitions. The devcontainer specification is an open standard jointly defined by Microsoft and GitHub, and can be used not only in GitHub Codespaces but also in VS Code's remote container development feature. This means you can use the same containerized environment during local development, ensuring consistency of the development environment.

### Step 1: Create a Basic Configuration

Create a devcontainer configuration in the project root directory:

```bash
# Create .devcontainer directory
mkdir -p .devcontainer

# Create configuration file
touch .devcontainer/devcontainer.json
```

### Step 2: Write a Node.js Project Configuration

For Node.js projects, use the following configuration:

```json
{
  "name": "Node.js Development Environment",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "forwardPorts": [3000, 5000, 8080],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next",
        "GitHub.copilot"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": "explicit"
        }
      }
    }
  }
}
```

### Step 3: Write a Python Project Configuration

For Python projects, use the following configuration:

```json
{
  "name": "Python Development Environment",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/common-utils:2": {}
  },
  "forwardPorts": [5000, 8000, 8080],
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "GitHub.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "[python]": {
          "editor.defaultFormatter": "ms-python.black-formatter",
          "editor.formatOnSave": true
        }
      }
    }
  }
}
```

### Step 4: Write a Multi-Language Project Configuration

For projects requiring multiple language runtimes:

```json
{
  "name": "Full Stack Development Environment",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.12"
    },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [3000, 5000, 8000],
  "postCreateCommand": "bash .devcontainer/setup.sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-python.python",
        "ms-azuretools.vscode-docker",
        "GitHub.copilot"
      ]
    }
  }
}
```

Then create the setup script:

```bash
#!/bin/bash
# .devcontainer/setup.sh

echo "Setting up development environment..."

# Install frontend dependencies
if [ -f "frontend/package.json" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Install backend dependencies
if [ -f "backend/requirements.txt" ]; then
    echo "Installing backend dependencies..."
    cd backend && pip install -r requirements.txt && cd ..
fi

# Install Git hooks
if [ -f ".husky/install.sh" ]; then
    echo "Installing Git hooks..."
    bash .husky/install.sh
fi

echo "Setup complete!"
```

## Part 4: Customizing Containers with Dockerfile

Although devcontainer provides rich pre-built images and feature modules, sometimes your project may require more specialized environment configurations. In such cases, you can use a Dockerfile to fully customize your development container. With a Dockerfile, you can precisely control every software package, every environment variable, and every system configuration installed in the container. This approach gives you maximum flexibility to meet any complex development environment requirements. For example, if your project needs specific versions of database drivers, specialized compilation toolchains, or custom security configurations, using a Dockerfile is the best choice. Note that when writing Dockerfiles, you should follow best practices, including using multi-stage builds, minimizing image layers, and leveraging caching effectively, to ensure fast and efficient container builds.

### Step 1: Create a Dockerfile

When you need finer-grained control over the development environment configuration, a Dockerfile provides maximum flexibility. You can define all configurations from the OS level to the application level in a Dockerfile, including system package installation, programming language runtime configuration, development tool installation, and various environment variable settings. Here is an example Dockerfile for a multi-language development environment:

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install Python 3.12
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI
RUN curl -fsSL https://get.docker.com | sh

# Install common development tools
RUN npm install -g \
    typescript \
    ts-node \
    nodemon \
    prettier \
    eslint

# Set Git configuration
RUN git config --global core.autocrlf input \
    && git config --global pull.rebase true

# Create non-root user (optional)
ARG USERNAME=vscode
RUN groupadd --gid 1000 ${USERNAME} \
    && useradd --uid 1000 --gid ${USERNAME} -m ${USERNAME}
```

### Step 2: Update devcontainer.json to Use the Dockerfile

```json
{
  "name": "Custom Development Environment",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "remoteUser": "vscode",
  "customizations": {
    "vscode": {
      "extensions": [
        "GitHub.copilot"
      ]
    }
  }
}
```

## Part 5: Managing Codespace Lifecycle

Understanding how to effectively manage the Codespace lifecycle is important for controlling costs and improving work efficiency. Each Codespace has its own running state, including available, stopped, and deleted. When a Codespace is running, it consumes your usage quota; when a Codespace is stopped, no charges are incurred, but the data within it is preserved. You need to manage Codespace states reasonably based on actual usage, stopping them promptly when not in use to save costs, and deleting them when no longer needed to release resources. GitHub provides an auto-stop feature that automatically stops Codespaces after a period of idleness, which is an excellent cost-saving practice.

### Viewing Your Codespaces

Manage your Codespaces through the GitHub CLI:

```bash
# List all Codespaces
gh codespace list

# Example output:
# NAME                          DISPLAY NAME      REPOSITORY             BRANCH   STATE
# owner-repo-abc123             owner/repo        owner/repo             main     Available
# owner-another-def456          owner/another     owner/another          dev      Shutdown
```

### Connecting to an Existing Codespace

```bash
# Connect to Codespace using SSH
gh codespace ssh

# Specify Codespace name
gh codespace ssh --codespace owner-repo-abc123

# Use port forwarding
gh codespace ssh --codespace owner-repo-abc123 -- -L 3000:localhost:3000
```

### Managing Port Forwarding

```bash
# Set up Codespace port forwarding
gh codespace ports forward 3000:3000 --codespace owner-repo-abc123

# View current port status
gh codespace ports list --codespace owner-repo-abc123
```

### Stopping and Deleting a Codespace

```bash
# Stop a Codespace
gh codespace stop --codespace owner-repo-abc123

# Delete a Codespace
gh codespace delete --codespace owner-repo-abc123

# Delete all Codespaces
gh codespace delete --all
```

### Managing via the Web

Visit https://github.com/codespaces to manage all your Codespaces on the web.

## Part 6: Port Forwarding and Web Application Preview

Port forwarding is a powerful feature provided by Codespaces that allows you to run web application services in the cloud and access them locally through your browser. When you start a development server in a Codespace, the Codespace automatically detects the port the service is listening on and forwards it to a URL accessible via browser. This is extremely useful for frontend development, backend development, and full-stack development. You can preview your code changes in real time, just as smoothly as local development. Additionally, you can set ports to be publicly visible, allowing you to share preview links with team members or customers so they can experience your application features in advance. This is very convenient for design reviews, feature demonstrations, or remote collaboration.

### Step 1: Start a Web Application

Start your web application in the Codespace:

```bash
# Start the development server
npm run dev
# Assume the server runs on http://localhost:3000
```

### Step 2: Access the Application

After starting the server, the Codespace will automatically detect the port and forward it. You will see a notification; click "Open in Browser" to access the application in your browser.

You can also manually configure port forwarding:

1. Open the "PORTS" tab at the bottom of the terminal
2. Click "Forward a Port"
3. Enter the port number (e.g., 3000)
4. Select visibility (Private or Public)

### Step 3: Share Preview Links

After setting a port to Public, you can share the link with others to preview your application:

1. Find the corresponding port in the PORTS tab
2. Right-click and select "Port Visibility" → "Public"
3. Copy the link address and share it with others

## Part 7: Advanced Challenges

After completing the basic Codespace usage, you can try the following advanced challenges to deepen your mastery of Codespaces' advanced features. These challenges will help you create more comprehensive development environment configurations, meet complex project requirements, and learn how to share development environment configurations with team members. Through these practices, you will be able to fully leverage the capabilities of Codespaces to build an efficient and consistent development experience.

### Challenge 1: Create a Complete devcontainer Configuration for an Existing Project

Choose one of your own projects and create a complete development environment configuration:

```json
{
  "name": "My Project Dev Environment",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": { "version": "20" },
    "ghcr.io/devcontainers/features/python:1": { "version": "3.12" },
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "forwardPorts": [3000, 5432, 6379],
  "postCreateCommand": "bash .devcontainer/setup.sh",
  "postAttachCommand": "echo 'Welcome to the dev environment!'",
  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "ms-python.python",
        "ms-azuretools.vscode-docker",
        "GitHub.copilot",
        "eamodio.gitlens"
      ],
      "settings": {
        "files.autoSave": "afterDelay",
        "editor.formatOnSave": true
      }
    }
  }
}
```

### Challenge 2: Configure Database Services

Use Docker Compose to configure database services needed for development:

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
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: devdb

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres-data:
```

Corresponding `devcontainer.json`:

```json
{
  "name": "Project with Database",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [5432, 6379],
  "postCreateCommand": "npm install && npm run db:migrate",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker",
        "mtxr.sqltools",
        "mtxr.sqltools-driver-pg"
      ]
    }
  }
}
```

### Challenge 3: Configure Team-Shared Codespace Prebuilds

Configure prebuilds in the repository settings to speed up Codespace creation:

1. Go to repository Settings → Codespaces
2. Click "Add prebuild configuration"
3. Select a branch (usually main)
4. Configure region and instance type
5. Save the configuration

Prebuilds automatically update when code is pushed, so team members can use the prebuilt environment directly when creating a Codespace, without waiting for dependency installation. Prebuilds are especially useful for large projects, where dependency installation and environment configuration can take a long time. By using prebuilds, team members can spin up a fully configured development environment in seconds, significantly improving development efficiency. Additionally, prebuilds can reduce network bandwidth consumption, since dependency packages only need to be downloaded once instead of individually by each team member.

## Verification Checklist

After completing the exercise, please confirm the following:

- [ ] Successfully created a Codespace
- [ ] Able to edit and run code in the Codespace
- [ ] Created a basic `devcontainer.json` configuration
- [ ] Understand how to manage the Codespace lifecycle
- [ ] Configured port forwarding and can preview web applications
- [ ] Understand how to manage Codespaces via CLI

## Frequently Asked Questions

### Q1: Are Codespaces free?

GitHub provides free users with a certain amount of free quota each month (currently 120 core hours/month). Pro users receive more quota. Usage beyond the quota is billed based on consumption.

### Q2: How can I reduce Codespaces usage costs?

- Stop your Codespace promptly when not in use
- Set a shorter auto-stop timeout
- Use a smaller machine type
- Use prebuilds to reduce startup time

### Q3: Will data in my Codespace be preserved?

Data in a Codespace is preserved for the duration of the Codespace's existence. If a Codespace is deleted, any unpushed code will be lost. It is recommended to frequently push code to the remote repository.

## Summary

Through this exercise, you learned how to use GitHub Codespaces for cloud-based development. Codespaces provides a consistent and convenient development environment, particularly suitable for team collaboration and open source contributions. Through devcontainer configuration, you can codify your development environment, ensuring every team member uses the same environment. In practice, it is recommended to include devcontainer configuration in version control, maintaining and updating it alongside your project code. This way, when the project's tech stack or dependencies change, the development environment will also automatically update, avoiding various issues caused by environment inconsistencies. Meanwhile, making good use of Codespaces' prebuild feature can significantly reduce environment startup time and improve team development efficiency. As cloud development technology continues to mature, GitHub Codespaces will become the preferred development environment solution for more and more development teams. Mastering this skill will bring new opportunities to your career development.

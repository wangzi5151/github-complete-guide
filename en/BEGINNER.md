# 🎯 GitHub Beginner Learning Path

> A GitHub learning roadmap tailored for developers. Pick your starting point based on your skill level and progress step by step—from complete beginner to advanced practitioner, with clear goals and companion tutorials at every stage.

---

## 📊 Where Do You Stand?

Not sure where to begin? Take one minute for a self-assessment:

| Question | If your answer is "No" |
|------|-------------------|
| Do you know what version control is? | 👉 Start from **Level 1** |
| Can you use `git add` and `git commit` locally? | 👉 Start from **Level 2** |
| Can you create a repository on GitHub and push code? | 👉 Start from **Level 3** |
| Have you used Pull Requests and Code Review? | 👉 Start from **Level 4** |
| Have you set up automated workflows with GitHub Actions? | 👉 Start from **Level 5** |
| Are you familiar with advanced tools like Copilot, K8s, and Terraform? | 👉 Go to **Level 6** |

> 💡 **Tip**: Even if you already have some experience, we recommend quickly skimming the earlier levels to fill in any gaps. Many seemingly simple concepts will pay off handsomely once you understand them deeply.

---

## 🗺️ Learning Path Overview

```
Level 1 ──→ Level 2 ──→ Level 3 ──→ Level 4 ──→ Level 5 ──→ Level 6
 Absolute     Git          GitHub       Team          CI/CD         Advanced
 Beginner     Operations   Basics       Collaboration Automation    Topics
 1-2 days     3-5 days     1 week       1-2 weeks     1-2 weeks     Ongoing
```

---

## Level 1: Complete Beginner — What Are Git and GitHub?

**🎯 Goal**: Understand the core concepts of version control, register a GitHub account, and set up your Git environment

**⏱️ Estimated Time**: 1-2 days

**📋 Prerequisites**: No programming experience required—just a computer and a passion to learn

### What You'll Learn

- What version control is and why every developer needs it
- The differences and connections between Git and GitHub
- How to register a GitHub account and complete basic setup
- How to install and configure Git on your own computer

### 📖 Tutorial List

| No. | Tutorial | Description |
|------|------|------|
| 0 | [Preface](docs/00-preface.md) | Learn about this tutorial's purpose, target audience, and how to use it, so you can plan a sensible study schedule |
| 1 | [What Is Version Control](docs/00-what-is-version-control.md) | Understand version control from scratch and why it dramatically boosts development efficiency and team collaboration |
| 2 | [What Is GitHub](docs/01-what-is-github.md) | Learn about GitHub's core features, ecosystem, and its important place in modern software development |
| 3 | [Git Installation Guide](docs/00-git-installation-guide.md) | A detailed, illustrated guide to installing Git on Windows, macOS, and Linux |
| 4 | [Install Git](docs/02-install-git.md) | More installation details and solutions to common installation issues, so your Git environment runs smoothly |
| 5 | [GitHub Signup Guide](docs/00-github-signup-guide.md) | A hands-on guide to registering a GitHub account, including email verification and profile setup |
| 6 | [Sign Up for GitHub](docs/03-signup-github.md) | Precautions and FAQs during registration to help you take your first step smoothly |

### ✅ Completion Criteria

- [ ] Can explain "what version control is" in your own words
- [ ] Can distinguish Git (a tool) from GitHub (a platform)
- [ ] Successfully installed Git on your computer (running `git --version` shows a version number)
- [ ] Successfully registered and logged into a GitHub account

### 🇨🇳 Special Notes for Users in China

If you use GitHub from a network environment in China, we recommend reading these in advance:

- [China Acceleration Guide](docs/Q-china-acceleration.md) — Configure mirror sources and proxies to improve access speed
- [China Direct Access Guide](docs/Q2-china-direct-access.md) — Multiple solutions to network issues when accessing GitHub from China

---

## Level 2: Learn Basic Git Operations

**🎯 Goal**: Master Git's core operations and manage code versions independently on your local machine

**⏱️ Estimated Time**: 3-5 days

**📋 Prerequisites**: Complete Level 1; Git is installed and configured

### What You'll Learn

- Git's core working principles (the concepts of working directory, staging area, and repository)
- How to create a repository, stage files, and commit changes
- How to view commit history and file differences
- How to use branches for parallel development
- How to merge branches and resolve code conflicts
- How to undo mistaken operations

### 📖 Tutorial List

| No. | Tutorial | Description |
|------|------|------|
| 7 | [SSH Keys](docs/04-ssh-keys.md) | Configure SSH keys for passwordless pushing—an essential GitHub skill and a security best practice |
| 8 | [Git Configuration](docs/05-git-config.md) | Set up your username, email, editor, and other basic settings to make your Git environment personal and efficient |
| 9 | [How Git Works](docs/06-how-git-works.md) | Deeply understand the concepts of the working directory, staging area, and local repository—mastering these will make everything that follows much easier |
| 10 | [Git Basics Guide](docs/00-git-basics-guide.md) | A comprehensive overview of basic Git operations to help you build a complete knowledge framework |
| 11 | [Creating and Cloning Repositories](docs/07-init-clone.md) | Learn both ways: `git init` to initialize a new repository and `git clone` to clone an existing one |
| 12 | [Staging and Committing](docs/08-add-commit.md) | Master `git add` and `git commit`, understand the role of the staging area and commit best practices |
| 13 | [Viewing History and Diffs](docs/09-log-diff.md) | Use `git log`, `git diff`, and other commands to track code changes and become a code detective |
| 14 | [Branching](docs/10-branching.md) | Learn to create, switch, and delete branches, and understand why branching is one of Git's most powerful features |
| 15 | [Merge and Rebase](docs/11-merge-rebase.md) | Master the differences and use cases of `git merge` and `git rebase`, and choose the right integration approach |
| 16 | [Resolving Conflicts](docs/12-resolve-conflicts.md) | Learn to identify and resolve merge conflicts—unavoidable in team collaboration, yet something you can handle gracefully |
| 17 | [Undoing Operations](docs/13-undo.md) | Master `git reset`, `git revert`, `git checkout`, and other undo operations, and know when to use which |

### ✅ Completion Criteria

- [ ] Can independently create a Git repository and make multiple commits
- [ ] Can use `git log` and `git diff` to view history and differences
- [ ] Can create, switch, and merge branches
- [ ] Can resolve simple merge conflicts
- [ ] Understand the difference between `git reset` and `git revert`

### 💡 Study Tips

> Git's learning curve is steep at first, so don't rush. We recommend practicing each command as you learn it, using a test repository to practice repeatedly. Remember: **making mistakes is part of learning**, and almost every Git operation can be undone.

---

## Level 3: Getting Started with GitHub

**🎯 Goal**: Become proficient with GitHub's core features and independently manage remote repositories

**⏱️ Estimated Time**: 1 week

**📋 Prerequisites**: Complete Level 2; be familiar with local Git operations

### What You'll Learn

- Create and manage remote repositories on GitHub
- Write high-quality READMEs and project documentation
- Use Issues to track problems and manage tasks
- Master GitHub's core collaboration features

### 📖 Tutorial List

| No. | Tutorial | Description |
|------|------|------|
| 18 | [GitHub Features Guide](docs/00-github-features-guide.md) | Get a comprehensive view of GitHub's core feature modules and build an overall understanding of the platform |
| 19 | [Creating Repositories](docs/14-create-repo.md) | Create a remote repository on GitHub and set options like visibility, license, and .gitignore |
| 20 | [README and Documentation](docs/15-readme-docs.md) | Learn to write a professional README.md that makes your project clear at a glance and boosts its professionalism and appeal |
| 21 | [Issue Tracking](docs/16-issues.md) | Use Issues to manage tasks, report bugs, and discuss feature requests—the fundamental tool for project management |
| 22 | [GitHub Projects](docs/21-github-projects.md) | Use boards to manage project progress and organize Issues into a visual project management workflow |

### ✅ Completion Criteria

- [ ] Can create a repository on GitHub and push local code to it
- [ ] Can write a clearly structured, complete README
- [ ] Can create and manage Issues and categorize them with labels
- [ ] Can use GitHub Projects boards to manage task progress

### 🔧 Hands-On Project

After completing this level, we suggest a small exercise:

1. Create a personal project repository on GitHub
2. Write a professional README (including project introduction, installation instructions, and usage examples)
3. Create 3-5 Issues as the project's to-do items
4. Manage these Issues with a Projects board

---

## Level 4: Team Collaboration and Open Source Contribution

**🎯 Goal**: Master the core workflows of modern team collaboration and be able to contribute to open source projects

**⏱️ Estimated Time**: 1-2 weeks

**📋 Prerequisites**: Complete Level 3; be familiar with basic GitHub operations

### What You'll Learn

- The complete Pull Request workflow
- Code Review methodology and best practices
- The Fork workflow and the standard process for open source contributions
- Git workflow strategies for team collaboration
- Tag management and version releases

### 📖 Tutorial List

| No. | Tutorial | Description |
|------|------|------|
| 23 | [Pull Requests](docs/17-pull-requests.md) | Master the full PR process of creation, review, and merge—the core mechanism of GitHub collaboration |
| 24 | [Code Review](docs/18-code-review.md) | Learn to conduct effective code reviews and improve code quality—an essential skill for senior developers |
| 25 | [Fork and Open Source Contribution](docs/22-fork-contribute.md) | Master the Fork workflow and learn the standard process and etiquette for contributing to open source projects |
| 26 | [Team Collaboration](docs/00-team-collaboration-guide.md) | A comprehensive guide to team collaboration, including permission management and communication standards |
| 27 | [Team Collaboration in Practice](docs/23-team-collaboration.md) | A deeper dive into team collaboration practices, including code ownership and review strategies |
| 28 | [Git Workflows](docs/24-git-workflow.md) | Learn mainstream workflows such as Git Flow, GitHub Flow, and Trunk Based, and choose the right one for your team |
| 29 | [Tags and Releases](docs/25-tags-releases.md) | Use Git tags and GitHub Releases to manage version releases and establish a standardized version management system |
| 30 | [Advanced Features Guide](docs/00-advanced-features-guide.md) | Explore GitHub's advanced collaboration features to further boost team efficiency |

### ✅ Completion Criteria

- [ ] Can create a PR and hold an effective code discussion with reviewers
- [ ] Can provide constructive Code Reviews on colleagues' code
- [ ] Can fork an open source project and successfully submit a PR
- [ ] Understand the differences and use cases of at least two Git workflows
- [ ] Can use tags and Releases to manage project versions

### 🌍 Open Source Contribution Guide

Contributing to open source projects is one of the best ways to improve your skills. We suggest you:

1. First find a project you're interested in on GitHub and read its `CONTRIBUTING.md`
2. Start with simple tasks (fixing documentation errors, adding test cases, etc.)
3. Follow the project's code and commit conventions
4. Patiently wait for the maintainer's review and actively respond to feedback

---

## Level 5: Automation and CI/CD

**🎯 Goal**: Use GitHub Actions to automate builds, tests, and deployments

**⏱️ Estimated Time**: 1-2 weeks

**📋 Prerequisites**: Complete Level 4; be familiar with PRs and team collaboration workflows

### What You'll Learn

- The core concepts and working principles of GitHub Actions
- Writing automated workflows (build, test, deploy)
- Deploying static websites with GitHub Pages
- Using the GitHub CLI to improve command-line efficiency
- Large file management and Git LFS

### 📖 Tutorial List

| No. | Tutorial | Description |
|------|------|------|
| 31 | [GitHub Actions](docs/19-github-actions.md) | Learn CI/CD automation from scratch and write your first GitHub Actions workflow |
| 32 | [GitHub Pages](docs/20-github-pages.md) | Deploy static websites for free with GitHub Pages and build a personal blog or project homepage |
| 33 | [GitHub CLI](docs/26-github-cli.md) | Install and use the GitHub command-line tool to perform almost any GitHub operation right from your terminal |
| 34 | [Git LFS](docs/27-git-lfs.md) | Use Git Large File Storage to manage large files (images, videos, datasets, etc.) |
| 35 | [Security and DevOps Guide](docs/00-security-devops-guide.md) | Understand the importance of security automation in DevOps practices and lay the foundation for advanced topics ahead |

### ✅ Completion Criteria

- [ ] Can write a complete GitHub Actions workflow
- [ ] Can deploy a static website with GitHub Pages
- [ ] Can use the GitHub CLI to operate repositories and PRs from the command line
- [ ] Understand Git LFS use cases and basic operations

### 🚀 CI/CD Practice Tips

> Automation is at the heart of modern software development. We suggest starting with a simple project:
> 1. Configure an Actions workflow that runs tests automatically
> 2. Add a process that automatically deploys to GitHub Pages
> 3. Try adding code quality checks (linting, formatting, etc.)
> 4. Improve it step by step until you have a complete CI/CD pipeline

---

## Level 6: AI, DevOps, and Advanced Topics

**🎯 Goal**: Master cutting-edge tools and advanced practices to become a well-rounded developer

**⏱️ Estimated Time**: Ongoing

**📋 Prerequisites**: Complete Level 5; have a solid foundation in Git and GitHub

### What You'll Learn

- Use GitHub Copilot for AI-assisted programming
- Master DevOps tools such as Kubernetes and Terraform
- Understand Git's internals and performance optimization
- Learn specialized workflows across domains (frontend, backend, mobile, machine learning, etc.)

### 📖 AI-Assisted Programming

| No. | Tutorial | Description |
|------|------|------|
| 36 | [Copilot Complete Guide](docs/X1-github-copilot-complete-guide.md) | Comprehensively master GitHub Copilot and make AI your programming partner |
| 37 | [Copilot AI Agent](docs/X14-github-copilot-workspace-agents.md) | Learn about Copilot Workspace and AI Agents and experience the next generation of development |

### 📖 DevOps and Infrastructure

| No. | Tutorial | Description |
|------|------|------|
| 38 | [Kubernetes in Practice](docs/X5-kubernetes-github-actions.md) | Deploy and manage Kubernetes clusters with GitHub Actions and automate the operations of containerized applications |
| 39 | [Terraform IaC](docs/X6-terraform-iac-github.md) | Use Terraform for Infrastructure as Code (IaC) management and automate the creation and configuration of cloud resources |
| 40 | [Security and Permissions](docs/28-security-permissions.md) | Deeply understand GitHub's security mechanisms, including permission management, security scanning, and dependency vulnerability detection |
| 41 | [API and Webhooks](docs/29-api-webhooks.md) | Build custom integrations and automation tools with the GitHub API and Webhooks |

### 📖 Advanced Git

| No. | Tutorial | Description |
|------|------|------|
| 42 | [Git Internals](docs/X11-git-internals-deep-dive.md) | Deeply understand Git's object model, reference mechanisms, and internal data structures to become a Git expert |
| 43 | [Git Performance Optimization](docs/X12-git-performance-optimization.md) | Optimize Git performance for large repositories, including advanced techniques like shallow clones and sparse checkouts |

### 📖 Specialized Workflows by Domain

| No. | Tutorial | Description |
|------|------|------|
| 44 | [Machine Learning Workflows](docs/X2-ml-workflow-github.md) | Manage machine learning projects with GitHub, including data version control and model management |
| 45 | [Frontend Development Workflows](docs/X3-frontend-github-workflow.md) | GitHub best practices for frontend projects, including component library management and preview deployments |
| 46 | [Backend CI/CD Guide](docs/X4-backend-cicd-github.md) | A complete continuous integration and continuous deployment solution for backend projects |
| 47 | [Mobile Development Guide](docs/X9-mobile-app-github.md) | GitHub workflows and automation practices for iOS and Android projects |
| 48 | [Microservices Management](docs/X10-microservices-github.md) | Manage microservice architectures with GitHub, including service discovery and configuration management |
| 49 | [Technical Writing Guide](docs/X8-technical-writing-github.md) | Write and manage technical documentation with GitHub and build a professional documentation system |
| 50 | [Open Source License Guide](docs/X7-open-source-licenses-guide.md) | Understand the differences between open source licenses and how to choose one to avoid legal risks |
| 51 | [Project Case Studies](docs/X13-real-world-project-case-studies.md) | Analyze the GitHub practices of real-world projects and learn from success stories |

### ✅ Completion Criteria

- [ ] Can use Copilot to assist with coding and understand how it works
- [ ] Understand the basic use cases of Kubernetes and Terraform
- [ ] Understand Git's internal working mechanisms
- [ ] Deeply study the workflow of at least one specialized domain

### 📚 Continuous Learning

> Technology changes rapidly and learning never ends. We suggest you:
> - Follow the official GitHub blog and Changelog to learn about the latest features
> - Regularly review and update your own workflows
> - Participate in technical community discussions and share your experience
> - Apply what you've learned to real projects

---

## 🧪 Hands-On Exercises

Theory matters, but **practice is the key to mastering skills**. Below are 30 carefully designed exercises, from basic to advanced. We recommend completing them in order.

### 🟢 Beginner Exercises (Level 1-2)

| No. | Exercise | Related Knowledge | Difficulty |
|------|------|-----------|------|
| 1 | [Create a Repository](exercises/exercise-1-create-repo.md) | Creating repositories, initializing Git, first commit | ⭐ |
| 2 | [Branching and Merging](exercises/exercise-2-branch-merge.md) | Branch operations, merge strategies | ⭐⭐ |
| 3 | [Pull Request](exercises/exercise-3-pull-request.md) | Creating PRs, writing descriptions, linking Issues | ⭐⭐ |
| 4 | [Resolving Conflicts](exercises/exercise-4-fix-conflict.md) | Identifying conflicts, resolving manually, verifying results | ⭐⭐ |
| 9 | [Stash](exercises/exercise-9-stash.md) | Use cases and tips for git stash | ⭐⭐ |
| 10 | [Interactive Rebase](exercises/exercise-10-interactive-rebase.md) | Organizing commit history with git rebase -i | ⭐⭐⭐ |

### 🟡 Intermediate Exercises (Level 3-4)

| No. | Exercise | Related Knowledge | Difficulty |
|------|------|-----------|------|
| 5 | [GitHub Pages](exercises/exercise-5-github-pages.md) | Deploying static websites, custom domains | ⭐⭐ |
| 6 | [Open Source Contribution](exercises/exercise-6-open-source.md) | Fork workflow, contribution guidelines | ⭐⭐⭐ |
| 8 | [Discussions](exercises/exercise-8-discussions.md) | GitHub Discussions community features | ⭐⭐ |
| 20 | [Project Board](exercises/exercise-20-project-board.md) | GitHub Projects board management | ⭐⭐ |
| 24 | [Issue Forms](exercises/exercise-24-issue-forms.md) | Issue templates and forms | ⭐⭐ |
| 25 | [Submodules](exercises/exercise-25-submodules.md) | Managing Git Submodules | ⭐⭐⭐ |
| 29 | [Git LFS Workflow](exercises/exercise-29-git-lfs-workflow.md) | Large file storage management | ⭐⭐⭐ |

### 🔴 Advanced Exercises (Level 5-6)

| No. | Exercise | Related Knowledge | Difficulty |
|------|------|-----------|------|
| 7 | [GitHub Actions](exercises/exercise-7-github-actions.md) | Writing CI/CD workflows | ⭐⭐⭐ |
| 11 | [GitHub CLI](exercises/exercise-11-github-cli.md) | Operating GitHub from the command line | ⭐⭐⭐ |
| 12 | [CI/CD Pipeline](exercises/exercise-12-cicd-pipeline.md) | Complete CI/CD configuration | ⭐⭐⭐⭐ |
| 13 | [Docker Deployment](exercises/exercise-13-docker-deploy.md) | Containerized deployment automation | ⭐⭐⭐⭐ |
| 14 | [Security Scanning](exercises/exercise-14-security-scan.md) | Code security scanning configuration | ⭐⭐⭐ |
| 15 | [Release Management](exercises/exercise-15-release-management.md) | Releases and versioning strategies | ⭐⭐⭐ |
| 16 | [Monorepo](exercises/exercise-16-monorepo.md) | Monorepo management strategies | ⭐⭐⭐⭐ |
| 19 | [Reusable Workflows](exercises/exercise-19-reusable-workflows.md) | Reusable Actions components | ⭐⭐⭐⭐ |
| 21 | [Copilot Basics](exercises/exercise-21-copilot-basics.md) | Getting started with AI-assisted programming | ⭐⭐⭐ |
| 22 | [Dependabot](exercises/exercise-22-dependabot-setup.md) | Configuring automatic dependency updates | ⭐⭐⭐ |
| 23 | [Codespaces](exercises/exercise-23-codespaces-dev.md) | Cloud development environments | ⭐⭐⭐ |
| 26 | [Advanced Reusable Workflows](exercises/exercise-26-reusable-workflows.md) | Advanced Actions patterns | ⭐⭐⭐⭐ |
| 27 | [GitHub Models](exercises/exercise-27-github-models.md) | AI model integration | ⭐⭐⭐⭐ |
| 28 | [Advanced Security Scanning](exercises/exercise-28-security-scanning.md) | Advanced security strategies | ⭐⭐⭐⭐ |
| 30 | [Terraform + GitHub](exercises/exercise-30-terraform-github.md) | Infrastructure as Code | ⭐⭐⭐⭐⭐ |

### 🎯 Specialized Exercises

| No. | Exercise | Description |
|------|------|------|
| 17 | [China Environment Setup](exercises/exercise-17-china-setup.md) | Configure mirror sources in China to optimize GitHub access speed |
| 18 | [Enterprise Setup](exercises/exercise-18-enterprise-setup.md) | Enterprise-level GitHub use cases and configuration plans |

### 📝 Exercise Tips

> 1. **Look before you leap**: Each exercise has detailed step-by-step instructions; read through them before you start
> 2. **Don't skip levels**: Basic exercises pave the way for advanced ones, and a solid foundation will make later learning easier
> 3. **Take notes**: Write down issues when you encounter them, and record your insights after solving them—these will become valuable assets
> 4. **Practice repeatedly**: It's normal not to get it right the first time; practice a few more times and you'll be comfortable

---

## 📖 Quick Reference

When you run into problems, these resources will help:

### 🔍 Everyday Reference

| Document | Description | When to Use |
|------|------|---------|
| [Common Commands Cheat Sheet](docs/A-common-commands.md) | A quick reference for common Git and GitHub commands | Quickly look up command usage during daily development |
| [Glossary](docs/E-glossary.md) | Chinese-English reference for Git and GitHub terminology | Look up technical terms when reading English documentation |
| [FAQ](docs/C-faq.md) | The most common problems beginners encounter and their solutions | Come here first when you run into an issue |
| [Troubleshooting](docs/M-troubleshooting.md) | Common error messages and solutions | Quickly locate and fix errors when they occur |

### 🇨🇳 Reference for Users in China

| Document | Description | When to Use |
|------|------|---------|
| [China Acceleration Guide](docs/Q-china-acceleration.md) | Configure mirrors and proxies to speed up GitHub access | Optimization when network access is slow |
| [China Direct Access Guide](docs/Q2-china-direct-access.md) | Multiple direct-connection solutions to network problems | Reference when you need stable GitHub access |

---

## ⏭️ What's Next?

Congratulations on completing the entire learning path! 🎉 But the journey has only just begun:

### 🌟 Take Action Now

1. **⭐ Star this repository** — If this learning path has helped you, please give it a Star for support
2. **🍴 Fork this repository** — Add your own study notes and insights
3. **📢 Share it with friends** — Help more developers learn GitHub

### 🚀 Directions for Growth

- **Contribute to open source projects** — Find a project you're interested in on GitHub and submit your first PR
- **Build your personal brand** — Use GitHub Pages to build a personal blog and share technical articles
- **Keep learning** — Follow the official GitHub blog to learn about the latest features and best practices
- **Help others** — Answer beginners' questions on GitHub Discussions or in the community

### 💬 Community Involvement

> The core of the open source spirit is **sharing and collaboration**. Once you've mastered these skills, don't forget to give back to the community:
> - Submit bug reports or feature suggestions for the open source projects you use
> - Participate in documentation translation and improvement
> - Share your experience and best practices
> - Help other beginners solve problems

---

## 📌 Learning Path at a Glance

| Level | Topic | Estimated Time | Core Skills |
|------|------|---------|---------|
| Level 1 | Absolute Beginner | 1-2 days | Version control concepts, Git installation, GitHub registration |
| Level 2 | Basic Git Operations | 3-5 days | add/commit/branch/merge/rebase |
| Level 3 | GitHub Basics | 1 week | Remote repositories, README, Issues, Projects |
| Level 4 | Team Collaboration | 1-2 weeks | PR, Code Review, Fork, workflows |
| Level 5 | CI/CD Automation | 1-2 weeks | GitHub Actions, Pages, CLI |
| Level 6 | Advanced Topics | Ongoing | Copilot, K8s, Terraform, Git internals |

---

> 📖 **Remember**: Learning isn't a race, it's a journey. Go at your own pace and enjoy the process. Every expert was once a beginner. You've got this! 💪

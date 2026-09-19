# Git LFS Large File Storage Complete Guide

## Chapter 1: Why Git LFS is Needed

### 1.1 Core Pain Points of Git Handling Large Files

As a distributed version control system, Git was originally designed to efficiently manage text-based source code files. Git internally implements version control by storing file differences (delta), which is very efficient for text files because text file modifications usually involve only a few line changes. However, when a repository contains large binary files, Git's mechanism encounters serious problems.

**Problem 1: Repository Size Explosive Growth**

Every time a binary file is modified, Git stores a complete file copy instead of differences. This means a 500MB design file modified 10 times will cause the repository to grow to several GB. This growth is linear, and over time the repository becomes increasingly larger, potentially reaching tens of GB or more.

**Problem 2: Extremely Slow Clone Speed**

When new team members join, they need to clone the repository. If the repository contains many historical large files, the clone process may take hours or even days. This not only affects new members' onboarding experience but also wastes significant network bandwidth and storage space.

**Problem 3: Severe Local Disk Space Waste**

Every developer's local repository contains all historical versions of large files, even if they only need the latest version. A repository with many design files may occupy tens of GB of local disk space, which is especially painful for laptop users.

**Problem 4: Daily Operations Become Slow**

Daily `git push` and `git pull` operations become abnormally slow because they need to transfer large amounts of binary data. Even small code changes may require long waits due to accompanying large file changes.

**Problem 5: Branch Switching and Merging Difficulties**

When large files have multiple versions, switching branches requires downloading different versions of large files, and merging may produce conflicts that cannot be automatically resolved. These operations significantly reduce development efficiency.

### 1.2 Typical Large File Scenarios

In actual development, various scenarios involve large files:

**Design Files**: Including Photoshop PSD files, Illustrator AI files, Sketch design files, Figma export files, etc. These files typically contain multiple layers, effects, and resources, ranging from tens of MB to hundreds of MB. Design teams need version control for these files to track design changes and rollback to previous versions.

**Video and Audio Materials**: Including MP4, MOV, AVI video files, and WAV, FLAC audio files. These media files are usually very large, a few minutes of HD video may be hundreds of MB or even several GB.

**3D Model Files**: Including FBX, OBJ, Blender BLEND files, etc. Game development and animation production projects often need to manage these large 3D resources.

**Dataset Files**: Including CSV, Parquet, HDF5 format datasets. Machine learning and data science projects typically need to manage large datasets, ranging from hundreds of MB to tens of GB.

**Build Artifacts**: Including EXE, DLL, SO, JAR binary executables and library files. Some projects need to include compiled binary files in version control.

**Game Resources**: Including Unity Asset files, Unreal Engine Pak files, etc. Game development projects typically contain a large number of game resources, which are often very large.

**Machine Learning Models**: Including PyTorch PT files, ONNX model files, HDF5 model files, etc. Trained machine learning models are usually large and need to be shared within teams.

### 1.3 Git LFS Birth Background and Development History

Git LFS (Large File Storage) is an open source project developed by Atlassian, officially released in 2015. GitHub announced support for Git LFS in August 2015, making it the standard solution for handling large files.

Git LFS's design goals are:
- Maintain simplicity of Git workflow
- Minimize impact on existing Git tools
- Provide efficient binary file storage
- Support version control for large files
- Seamlessly integrate with existing Git hosting platforms

After years of development, Git LFS has become the industry standard for handling large files, widely used in game development, design collaboration, data science, and other fields. Currently Git LFS's latest version is 3.x series, supporting multiple operating systems and Git hosting platforms.

## Chapter 2: Git LFS Working Principle

### 2.1 Core Architecture Design

Git LFS adopts "pointer replacement" architecture design, which is its most core innovation. When a file is tracked by Git LFS, what's stored in the Git repository is no longer the actual file content, but a small pointer file. This pointer file contains reference information pointing to the actual file content.

In local repositories, Git LFS uses Git's clean filter and smudge filter mechanisms to implement transparent file replacement. When executing `git add` command, clean filter replaces actual file content with pointer file; when executing `git checkout` command, smudge filter replaces pointer file with actual file content.

For remote storage, Git LFS stores actual file content on independent LFS storage servers. Mainstream Git hosting platforms like GitHub, GitLab, Bitbucket all provide built-in LFS storage services. Users can also use self-built LFS servers or third-party storage services.

### 2.2 Pointer File Format Details

Git LFS pointer file uses plain text format, containing three key pieces of information:

```
version https://git-lfs.github.com/spec/v1
oid sha256:4d7a214614ab2935c943f9e0ff69d22eadbb8f32b1258daaa5e2ca24d17e2393
size 123456789
```

**version field**: Specifies LFS specification version number, current version is v1.

**oid field**: Object Identifier, uses SHA-256 hash algorithm to calculate file content hash for unique identification. This hash value is calculated based on file content, same file content produces same hash value, different file content produces different hash values. This enables Git LFS to effectively perform deduplication storage.

**size field**: Original file's byte size, used to estimate required space and time before downloading.

### 2.3 Complete Workflow

**Write Flow (from local to remote)**:

Step 1: Developer creates or modifies large file locally, executes `git add` command to add file to staging area.

Step 2: Git LFS's clean filter detects file matches tracking rules in `.gitattributes`, replaces actual file content with pointer file.

Step 3: Pointer file is stored in Git repository's object database, while actual file content is stored in local LFS cache directory (`.git/lfs/objects`).

Step 4: When executing `git push` command, Git pushes pointer file to remote repository, while Git LFS uploads locally cached actual file content to LFS storage server.

**Read Flow (from remote to local)**:

Step 1: Developer executes `git clone` or `git pull` command to get repository code.

Step 2: Git gets all repository commits, including pointer files.

Step 3: Git LFS's smudge filter detects pointer files, downloads actual file content from LFS storage server.

Step 4: Replaces downloaded actual file content into working directory, while caching to local LFS cache directory.

### 2.4 Role of .gitattributes File

`.gitattributes` file is the core file for configuring Git LFS tracking rules. This file is located in repository root directory, defining which files should be managed by Git LFS.

Each rule line's format is:

```
pattern filter=lfs diff=lfs merge=lfs -text
```

Where each attribute's meaning:
- `filter=lfs`: Use LFS clean filter to process file during `git add`
- `diff=lfs`: Use LFS diff driver to show differences during `git diff`
- `merge=lfs`: Use LFS merge driver to handle merge conflicts
- `-text`: Mark as binary file, don't perform line ending conversion

Common configuration examples:

```
# Track all PSD files
*.psd filter=lfs diff=lfs merge=lfs -text

# Track all ZIP files
*.zip filter=lfs diff=lfs merge=lfs -text

# Track all files in specific directory
assets/videos/** filter=lfs diff=lfs merge=lfs -text

# Track specific file
big-dataset.csv filter=lfs diff=lfs merge=lfs -text
```

## Chapter 3: Installation and Configuration

### 3.1 System Requirements

Before installing Git LFS, ensure the following system requirements are met:
- Git version 1.8.2 or higher
- Supported operating systems: Windows 7 and above, macOS 10.9 and above, mainstream Linux distributions

### 3.2 Windows System Installation

Windows users can install Git LFS through various methods:

**Using winget package manager (recommended)**:

```bash
winget install Git.GitLFS
```

**Using Chocolatey package manager**:

```bash
choco install git-lfs
```

**Using Scoop package manager**:

```bash
scoop install git-lfs
```

**Manual installation**: Visit Git LFS official website (https://git-lfs.github.com/), download Windows installer, run installer and follow prompts to complete installation.

After installation, need to execute initialization command in Git Bash or Command Prompt:

```bash
git lfs install
```

### 3.3 macOS System Installation

macOS users can install Git LFS through the following methods:

**Using Homebrew (recommended)**:

```bash
brew install git-lfs
```

**Using MacPorts**:

```bash
sudo port install git-lfs
```

**Manual installation**: Visit Git LFS official website, download macOS installer (.pkg file), double-click to run installer.

Execute initialization after installation:

```bash
git lfs install
```

### 3.4 Linux System Installation

Linux users can choose appropriate installation methods based on different distributions:

**Ubuntu/Debian Systems**:

```bash
sudo apt update
sudo apt install git-lfs
```

**CentOS/RHEL/Fedora Systems**:

```bash
# CentOS/RHEL
sudo yum install git-lfs

# Fedora
sudo dnf install git-lfs
```

**Arch Linux Systems**:

```bash
sudo pacman -S git-lfs
```

**Compile from source**:

```bash
git clone https://github.com/git-lfs/git-lfs.git
cd git-lfs
make
sudo make install
```

### 3.5 Domestic Mirror Configuration

Due to network reasons, domestic users may encounter slow download speeds or connection failures when using Git LFS. This is because GitHub's servers are overseas, and domestic access may be affected by network restrictions. Here are some solutions to help domestic users use Git LFS more smoothly.

**Using proxy**: Proxy is the most common solution. By configuring HTTP or SOCKS5 proxy, can bypass network restrictions and improve access speed. There are many proxy software choices, such as Clash, V2Ray, etc. After configuring proxy, all Git and LFS operations will go through proxy server.

```bash
# Configure HTTP proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# Configure SOCKS5 proxy
git config --global http.proxy socks5://127.0.0.1:7891
git config --global https.proxy socks5://127.0.0.1:7891
```

**Using domestic Git hosting platforms**:

Domestic platforms like Gitee, Coding also provide Git LFS services, can serve as alternatives to GitHub. These platforms' servers are located domestically, with faster access speed, more suitable for domestic development teams. Gitee provides features similar to GitHub, including code hosting, Issue management, CI/CD, etc. If project mainly targets domestic users, using domestic platform is a good choice.

**Configure custom LFS endpoint**:

If team has self-built LFS server, can configure custom LFS endpoint. Self-built LFS server can provide better performance and larger storage space, suitable for teams with special needs. Common self-built LFS server solutions include using Amazon S3 or MinIO as backend storage. After configuring custom endpoint, all LFS operations will point to self-built server.

```bash
# Configure custom LFS server address
git config lfs.url https://your-lfs-server.com/your-repo.git/info/lfs
```

### 3.6 Initialize Git LFS

After installation, need to initialize Git LFS at system level. Initialization only needs to be executed once, it configures Git's global filter settings to enable Git LFS to work with Git. If initialization not executed, Git LFS tracking rules will not take effect.

```bash
# System level initialization (only needs to be executed once)
git lfs install

# Verify installation
git lfs version
# Output example: git-lfs/3.4.0 (GitHub; linux amd64; go 1.21.1)

# View LFS environment info
git lfs env
```

Initialization command configures Git's global filter settings to enable Git LFS to work with Git.

## Chapter 4: Basic Usage Methods

This chapter will introduce Git LFS's basic usage methods, including tracking files, viewing tracking status, untracking, etc. Mastering these basic operations is the foundation for using Git LFS. Through this chapter's learning, developers can quickly get started using Git LFS to manage large files.

### 4.1 Track Files

Tracking files is the first step in using Git LFS. By specifying file patterns, tells Git LFS which files need to be managed. Tracking rules use wildcard patterns to match filenames, supporting common wildcard syntax. Tracking command creates or modifies `.gitattributes` file in repository root directory, this file needs to be committed to repository so team members can share same tracking rules.

```bash
# Track files with specific extensions
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "*.mp4"
git lfs track "*.wav"

# Track all files in specific directory
git lfs track "assets/**"
git lfs track "data/large-files/**"

# Track specific filename
git lfs track "big-dataset.csv"

# Track multiple file types simultaneously
git lfs track "*.psd" "*.ai" "*.sketch"
```

After executing tracking command, creates or modifies `.gitattributes` file in project root directory. Recommend committing `.gitattributes` file to repository so team members can share same tracking rules.

### 4.2 View Tracking Status

Viewing tracking status helps developers understand which files are managed by Git LFS and current configuration. Git LFS provides multiple commands to view different dimension information. Developers should be familiar with these commands to quickly obtain relevant information when needed.

```bash
# View current tracking rules
git lfs track

# View .gitattributes file content
cat .gitattributes

# View LFS tracked file list (committed)
git lfs ls-files

# View LFS file details (including size)
git lfs ls-files --long

# View LFS status
git lfs status
```

### 4.3 Untrack Files

Untracking files means removing files from Git LFS management, restoring them to ordinary Git objects. Untracking only affects newly added files, already tracked files won't automatically convert back to ordinary Git objects. If need to convert tracked files back to ordinary Git objects, need to use `git lfs migrate` command for migration.

```bash
# Untrack specific file types
git lfs untrack "*.psd"
git lfs untrack "*.zip"

# Untrack all files
git lfs untrack "*"
```

Note that untracking only affects newly added files, already tracked files won't automatically convert back to ordinary Git objects. If need to convert tracked files back to ordinary Git objects, need to use `git lfs migrate` command.

### 4.4 Complete Workflow Example

The following is a complete Git LFS workflow example, showing the complete process from initialization to push. This example is suitable for new project's Git LFS configuration. Developers can follow this workflow to configure Git LFS for new projects, ensuring large files are correctly managed.

```bash
# Step 1: Initialize Git LFS
git lfs install

# Step 2: Configure tracking rules
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "assets/**"

# Step 3: View tracking rules
cat .gitattributes
# Output:
# *.psd filter=lfs diff=lfs merge=lfs -text
# *.mp4 filter=lfs diff=lfs merge=lfs -text
# assets/** filter=lfs diff=lfs merge=lfs -text

# Step 4: Add .gitattributes file
git add .gitattributes

# Step 5: Add large files
git add design.psd
git add video.mp4
git add assets/background.png

# Step 6: View status
git status

# Step 7: Commit
git commit -m "Add design files and video materials"

# Step 8: Push (LFS files auto-upload)
git push origin main
```

### 4.5 Pull and Checkout Operations

Pull and checkout operations are the most commonly used operations in team collaboration. When team members need to get latest code and large files, need to use pull operation. Git LFS provides flexible pull options, allowing developers to pull specific files on demand, avoiding downloading unnecessary large files. This is particularly useful for developers with limited bandwidth.

```bash
# Pull latest code (including LFS files)
git pull

# Only pull LFS files (don't pull Git commits)
git lfs pull

# Pull by file pattern
git lfs pull --include="*.psd"
git lfs pull --exclude="*.mp4"
git lfs pull --include="assets/videos/"

# Restore LFS files from local cache
git lfs checkout

# Checkout specific files
git lfs checkout "*.psd"
```

## Chapter 5: Migrate Existing Repositories to LFS

For existing repositories that already contain a large number of large files, can use migration feature to convert them to use Git LFS. Migration process rewrites Git history, replacing large files with LFS pointers. This is an important operation that needs careful execution. This chapter will introduce timing, methods and precautions for migration.

### 5.1 When Migration is Needed

Migrating existing repositories to Git LFS is a decision that needs careful consideration. Following situations need consideration for migrating to Git LFS: Repository already contains a large number of large file history, causing repository size to be too large; Repository clone speed is too slow, affecting team efficiency; Repository size exceeds GitHub recommended limit (5GB); Daily Git operations (push, pull, clone) slow. Before deciding to migrate, should evaluate migration's benefits and risks, and notify team members in advance.

### 5.2 Using git lfs migrate Command

Git LFS provides `migrate` command to migrate existing repositories. This command can convert large files already committed to Git repository into LFS pointers, while preserving complete commit history. Migration operation rewrites Git history, so needs careful execution. Recommend using `info` subcommand to preview migration impact before migration.

```bash
# Preview migration (don't actually execute)
git lfs migrate info --include="*.psd,*.zip,*.mp4"

# Output example:
# migrate: Fetching remote refs: ..., done.
# migrate: Sorting commits: ..., done.
# migrate: Rewriting commits: 100% (50/50), done.
# 
# *.psd   500 MB  5/5 files
# *.zip   200 MB  3/3 files
# *.mp4   1 GB    2/2 files

# Execute migration (rewrite history)
git lfs migrate import --include="*.psd,*.zip,*.mp4" --everything

# Only migrate specific branch
git lfs migrate import --include="*.psd" --include-ref=refs/heads/main

# Migrate all branches and tags
git lfs migrate import --include="*.psd" --everything
```

### 5.3 Migration Options Details

`git lfs migrate` command provides multiple options, allowing developers to precisely control migration scope and behavior. Understanding these options is crucial for successful migration. Developers should choose appropriate option combinations based on project needs.

```bash
# --include: Specify file patterns to migrate
git lfs migrate import --include="*.psd,*.zip"

# --exclude: Exclude specific file patterns
git lfs migrate import --include="*" --exclude="*.txt"

# --everything: Process all references (branches, tags, etc.)
git lfs migrate import --include="*.psd" --everything

# --above: Only migrate files larger than specified size
git lfs migrate import --above=10MB

# --yes: Skip confirmation prompt
git lfs migrate import --include="*.psd" --yes
```

### 5.4 Migration Precautions

Migrating existing repositories is a task that needs careful operation, the following are key points to note:

**Backup repository**: Migration rewrites Git history, must backup repository before operation. Can use `git clone --mirror` to create complete backup.

**Team coordination**: After migration, all team members need to re-clone repository, or execute specific sync commands. Need to notify team members in advance, and coordinate migration time.

**Force push**: After migration, need to use `--force-with-lease` to push updated branches and tags. This overwrites remote repository's history, ensure all members have synced before execution.

**CI/CD update**: Ensure CI/CD environment has Git LFS installed, and configured with correct authentication information.

**Time cost**: Large repository migration may take several hours, depending on repository size and network speed.

## Chapter 6: LFS File Locking

File locking is an important feature provided by Git LFS, used to solve binary file concurrent modification problems. This chapter will introduce file locking's principle, usage methods and best practices.

### 6.1 Why File Locking is Needed

For binary files, Git cannot automatically merge conflicts like handling text files. When two developers simultaneously modify the same binary file (such as PSD design file), merging will produce unresolvable conflicts. In this case, must manually choose which version of file to use. File locking mechanism allows developers to "lock" file before modification, preventing others from simultaneously modifying, thus avoiding conflicts. This is particularly important for design files, video materials and other large binary files.

### 6.2 Lock and Unlock Operations

Git LFS provides simple commands to lock and unlock files. After locking file, other developers can still view file, but cannot modify. After unlocking file, other developers can lock and modify file. Developers should develop good habits, lock binary files before modification, unlock promptly after modification.

```bash
# Lock single file
git lfs lock design.psd

# Lock multiple files
git lfs lock assets/video.mp4 assets/audio.wav

# View currently locked files
git lfs locks

# Unlock file
git lfs unlock design.psd

# Force unlock (unlock files locked by others)
git lfs unlock design.psd --force

# Unlock using lock ID
git lfs unlock --id=123
```

### 6.3 Locking Workflow

Typical file locking workflow includes four steps: lock file, modify file, commit and push, unlock file. Team members should follow this workflow to ensure file locking mechanism works correctly. If developer forgets to unlock file, other developers can use force unlock feature to unlock file.

Typical file locking workflow:

```bash
# Developer A locks file
git lfs lock assets/design.psd

# Developer A modifies file and commits
git add assets/design.psd
git commit -m "Update design draft"
git push origin main

# Developer A unlocks file
git lfs unlock assets/design.psd

# Developer B can now lock and modify file
git lfs lock assets/design.psd
```

### 6.4 Locking Rule Configuration

Can configure automatic locking rules in `.gitattributes` file. After marking files as `lockable`, Git LFS will treat them as lockable files. Developers should mark all binary files that need locking as `lockable`, so team members can correctly use file locking feature.

Can configure automatic locking rules in `.gitattributes`:

```
# Mark as lockable
*.psd lockable
*.ai lockable
*.sketch lockable
assets/videos/** lockable
```

## Chapter 7: LFS and CI/CD Integration

In modern software development, CI/CD (Continuous Integration/Continuous Deployment) is indispensable. When project uses Git LFS to manage large files, CI/CD pipeline also needs correct configuration to support LFS files. This chapter will introduce how to configure Git LFS in various CI/CD platforms.

### 7.1 GitHub Actions Configuration

GitHub Actions is GitHub's CI/CD service, with good integration with Git LFS. Using LFS files in GitHub Actions is very simple, just enable LFS option in checkout step. After enabling, Actions will automatically download LFS files, ensuring build process can access all needed resources.

```yaml
name: Build with LFS files

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code with LFS
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Verify LFS files
        run: |
          git lfs ls-files
          echo "LFS files downloaded successfully"

      - name: Build project
        run: make build
```

### 7.2 Partial Checkout Optimization

If CI only needs a portion of LFS files, can optimize build time. By specifying which file patterns to download, can avoid downloading unnecessary large files, thus speeding up build speed. This is particularly useful for large projects, because these projects may contain a large number of LFS files, but each build only needs a portion of them.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Pull specific LFS files
        run: |
          git lfs pull --include="assets/models/"
          git lfs pull --include="*.onnx"
```

### 7.3 LFS Cache Configuration

Using cache can accelerate CI builds. By caching LFS files, can avoid re-downloading all LFS files during each build. Cache configuration uses GitHub Actions' cache action, judges whether cache needs update based on LFS file hash values. This caching strategy can significantly reduce build time, especially for projects containing a large number of LFS files.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Cache LFS files
        uses: actions/cache@v3
        with:
          path: .git/lfs
          key: ${{ runner.os }}-lfs-${{ hashFiles('.lfs-files') }}
          restore-keys: |
            ${{ runner.os }}-lfs-

      - name: Checkout with LFS
        uses: actions/checkout@v4
        with:
          lfs: true
```

### 7.4 Other CI Platform Configuration

Besides GitHub Actions, other CI platforms also support Git LFS. The following are GitLab CI and Jenkins configuration examples. These platforms' configuration methods are similar, all need to install Git LFS and pull LFS files before build. Developers should choose appropriate configuration method based on the CI platform being used.

**GitLab CI Configuration**:

```yaml
variables:
  GIT_LFS_SKIP_SMUDGE: "1"

build:
  stage: build
  before_script:
    - git lfs install
    - git lfs pull
  script:
    - make build
```

**Jenkins Configuration**:

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    extensions: [[$class: 'GitLFSPull']],
                    userRemoteConfigs: [[url: 'https://github.com/user/repo.git']]
                ])
            }
        }
    }
}
```

## Chapter 8: LFS Storage Limits and Billing

Using Git LFS requires understanding storage limits and billing rules. GitHub provides different LFS quotas for different plans, exceeding quota requires purchasing additional storage space. This chapter will introduce GitHub LFS quota, usage viewing and optimization methods.

### 8.1 GitHub LFS Quota

GitHub provides different LFS storage quotas for different subscription plans. Free users' quota is smaller, suitable for personal projects and small teams. Paid users' quota is larger, suitable for commercial projects and large teams. Developers should choose appropriate plan based on project needs, and regularly monitor storage usage.

| Plan | Storage Space | Monthly Bandwidth | Price |
|------|---------------|-------------------|-------|
| Free | 1 GB | 1 GB | Free |
| Pro | 2 GB | 2 GB | $4/month |
| Team | 10 GB | 10 GB | $4/user/month |
| Enterprise | 50 GB | 50 GB | $21/user/month |

### 8.2 View Usage

Developers should regularly view LFS storage usage, ensure not exceeding quota. GitHub provides web interface and API two methods to view usage. By monitoring usage, can timely discover storage space shortage problems, and take corresponding measures.

```bash
# View via web
# Visit https://github.com/settings/billing

# View via API
gh api user/settings/billing/lfs-storage
```

### 8.3 Handling Quota Exceedance

When LFS storage exceeds quota, developers will not be able to push new LFS files. Existing LFS files can still be downloaded normally, won't affect team members' work. Solutions for quota exceedance include purchasing additional storage, cleaning unnecessary LFS files, using third-party LFS storage services, etc.
- Cannot push new LFS files
- Existing LFS files can still be downloaded normally
- Can purchase additional storage packages

### 8.4 Optimize Storage Usage

Optimizing storage usage can help teams complete more work within limited quota. The following are some optimization suggestions, including regularly cleaning cache, deleting unnecessary file history, using third-party storage services, etc. Developers should choose appropriate optimization strategy based on project actual situation.

```bash
# Clean unreferenced LFS objects
git lfs prune

# View LFS object occupation
git lfs ls-files --size

# Use third-party LFS storage service
# Such as Gitee, Coding, Alibaba Cloud OSS, etc.
```

## Chapter 9: LFS Alternatives

Although Git LFS is the most popular large file management solution, it's not the only choice. Based on project's specific needs, other solutions may be more appropriate. This chapter will introduce several common Git LFS alternatives, and conduct comparative analysis to help developers make wise choices.

### 9.1 DVC (Data Version Control)

DVC is a data version control tool specially designed for machine learning projects. It supports various storage backends, deep integration with machine learning frameworks. DVC's design concept is to separate data and models from code management, but maintain version synchronization. This enables data scientists to manage data and models like managing code.

**DVC's main advantages**:
- Supports various storage backends (S3, GCS, Azure, SSH, etc.)
- Deep integration with machine learning frameworks
- Supports data pipelines and experiment management
- No need to modify Git history

**DVC's main disadvantages**:
- Steep learning curve
- Team needs additional DVC installation
- Not as closely integrated with GitHub as Git LFS

### 9.2 Git Annex

Git Annex is another large file management solution, developed by Joey Hess. It supports distributed storage and encrypted storage, suitable for projects needing flexible storage strategies. Git Annex's design concept is to separate file content from filename management, file content can be stored in multiple locations, including local disk, remote servers, cloud storage, etc.

**Git Annex's main advantages**:
- Supports distributed storage
- Very flexible storage strategies
- Supports encrypted storage

**Git Annex's main disadvantages**:
- Complex configuration
- Limited integration with GitHub
- High learning cost

### 9.3 Solution Selection Suggestions

Choosing appropriate large file management solution needs to consider multiple factors, including project type, team size, tech stack, storage needs, etc. The following are selection suggestions for different scenarios, helping developers make wise decisions. No one solution fits all scenarios, developers should choose most appropriate solution based on project's specific needs.

- **GitHub projects, general large files** → Git LFS
- **Machine learning/data science projects** → DVC
- **Ultra-large scale data, needs distributed storage** → Git Annex
- **Already has a large number of historical large files** → Git LFS migrate

## Chapter 10: Common Problem Troubleshooting

During using Git LFS, developers may encounter various problems. This chapter will detail common problems' causes and solutions, helping developers quickly locate and solve problems.

### 10.1 LFS Files Display as Pointer Files

**Problem Description**: After cloning repository, LFS files display as text pointers instead of actual content. This is one of the most common problems in Git LFS usage. When developers see file content is text like `version https://git-lfs.github.com/spec/v1`, indicating LFS files not correctly downloaded.

**Problem Cause**: This problem usually has several causes. First, could be developer locally has not installed Git LFS. Git LFS needs to be installed separately, won't be installed with Git. Second, could be Git LFS not correctly initialized. Finally, could be network problem causing LFS file download failure.

**Solution**:

```bash
# Pull LFS files
git lfs pull

# Checkout LFS files
git lfs checkout

# Check if LFS is installed
git lfs version

# If not installed, install and initialize first
git lfs install
git lfs pull
```

### 10.2 LFS Push Failure

**Problem Description**: Error when pushing LFS files. Push failure may have various manifestations, such as network timeout, authentication failure, insufficient storage space, etc. Developers need to judge problem cause based on specific error message.

**Problem Cause**: Common causes of push failure include network connection problems, expired or invalid authentication information, insufficient LFS storage space, remote server configuration errors, etc. In some cases, firewall or proxy settings may also cause push failure.

**Solution**:

```bash
# Check LFS configuration
git lfs env

# Verify remote URL
git remote -v

# Check authentication
git lfs ls-remote

# View detailed error info
GIT_TRACE=1 git push
```

### 10.3 Clone Speed Still Slow

**Problem Description**: Clone still slow after enabling LFS. Even after configuring Git LFS, cloning large repositories still takes a long time, this will affect team's work efficiency.

**Problem Cause**: Slow clone speed may be because LFS files are too many or single file size is too large. Additionally, insufficient network bandwidth, server distance is far, concurrent connection count limits and other factors also affect download speed.

**Solution**:

```bash
# Shallow clone
git clone --depth 1 https://github.com/user/repo.git

# Delay LFS download
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/user/repo.git
cd repo
git lfs pull --include="needed-file.psd"

# Configure proxy
git config --global http.proxy http://127.0.0.1:7890
```

### 10.4 LFS Merge Conflicts

**Problem Description**: LFS file conflict when merging branches. Unlike text files, binary file conflicts cannot be automatically resolved through text merge tools. When two branches modify the same LFS file, merge operation will fail.

**Problem Cause**: Root cause of LFS file conflict is two branches made different modifications to same file. Since binary files have no concept of lines, Git cannot automatically merge these modifications. Developers need to manually choose which version of file to use.

**Solution**:

```bash
# Choose to use current branch's version
git checkout --ours design.psd

# Choose to use target branch's version
git checkout --theirs design.psd

# Mark as resolved after manual resolution
git add design.psd
git commit -m "Resolve LFS file conflict"
```

### 10.5 .gitattributes Not Working

**Problem Description**: Configured tracking rules but files not managed by LFS. Developer configured LFS tracking rules in `.gitattributes` file, but newly added files still stored as ordinary Git objects.

**Problem Cause**: This problem usually has several causes. First, `.gitattributes` file may not have been committed to repository. Second, files may have already been added to Git repository, need to remove cache first then re-add. Finally, tracking rule pattern may not match target files.

**Solution**:

```bash
# Confirm .gitattributes file committed
git add .gitattributes
git commit -m "Add LFS tracking rules"

# Re-add files
git rm --cached design.psd
git add design.psd

# Check tracking rules
git lfs track

# Check if files match pattern
git check-attr filter design.psd
```

### 10.6 Debug LFS Problems

When encountering unresolvable LFS problems, can enable detailed log output to help diagnose problems. Git LFS provides multiple environment variables to control log level and output content. By analyzing log information, developers can understand LFS operation's detailed process, find problem's root cause.

```bash
# Enable detailed log
export GIT_TRACE=1
export GIT_TRANSFER_TRACE=1
export CURL_VERBOSE=1

# Execute LFS operation
git lfs pull

# View LFS environment info
git lfs env

# View LFS configuration
git config --list | grep lfs
```

## Best Practices Summary

During using Git LFS, following best practices can help teams avoid common problems, improve collaboration efficiency. The following are practice-verified suggestions, covering usage scenario selection, team collaboration and performance optimization.

### When to Use LFS

**Scenarios suitable for LFS**:
- Binary files larger than 1MB
- Files frequently change
- Multiple team members collaborate modifying same file
- Large resource files needing version control

**Scenarios not suitable for LFS**:
- Pure text code files
- Small files less than 100KB
- Files not needing version control
- Regenerable build artifacts

### Team Collaboration Suggestions

1. **Unified Configuration**: Explain LFS configuration requirements in project documentation
2. **New Member Onboarding**: Ensure new members install and initialize Git LFS
3. **Code Review**: Check LFS file changes in PRs
4. **Regular Maintenance**: Regularly execute `git lfs prune` to clean cache
5. **Monitor Usage**: Regularly check storage and bandwidth usage

### Performance Optimization Tips

```bash
# Configure concurrent transfer count
git config lfs.concurrenttransfers 8

# Enable transfer retry
git config lfs.transfer.maxretries 3

# Shallow clone + on-demand pull
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 <repo>
git lfs pull --include="*.psd"
```

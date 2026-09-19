# Git Performance Optimization Complete Guide

> This chapter provides a comprehensive overview of Git performance optimization strategies and techniques, from cloning to daily operations, from client to CI/CD, helping you maintain an efficient development experience in large repositories.

---

## Table of Contents

1. [Performance Challenges of Large Repositories](#1-performance-challenges-of-large-repositories)
2. [git clone Optimization](#2-git-clone-optimization)
3. [git fetch/pull Optimization](#3-git-fetchpull-optimization)
4. [git status Optimization](#4-git-status-optimization)
5. [git diff Optimization](#5-git-diff-optimization)
6. [git gc and git repack Configuration](#6-git-gc-and-git-repack-configuration)
7. [Git LFS Performance Tuning](#7-git-lfs-performance-tuning)
8. [Git Hooks Performance Optimization](#8-git-hooks-performance-optimization)
9. [Git Performance Optimization in CI/CD](#9-git-performance-optimization-in-cicd)
10. [Monorepo Git Performance Strategies](#10-monorepo-git-performance-strategies)
11. [Git Client Performance Comparison](#11-git-client-performance-comparison)
12. [Git Caching and Preloading Strategies](#12-git-caching-and-preloading-strategies)
13. [Network Layer Optimization](#13-network-layer-optimization)
14. [Monitoring and Diagnostic Tools](#14-monitoring-and-diagnostic-tools)

---

## 1. Performance Challenges of Large Repositories

### 1.1 What Are Large Repositories

Large repositories typically have the following characteristics:

```
┌──────────────────────────────────────────────────────────┐
│              Large Repository Characteristic Analysis     │
├──────────────────┬───────────────────────────────────────┤
│   Characteristic │           Description                 │
├──────────────────┼───────────────────────────────────────┤
│ Large codebase   │ File count > 10,000 or lines > 1,000,000 │
│ Long history     │ Commit history > 100,000               │
│ Many binaries    │ Images, videos, models, etc.           │
│ Many branches    │ Active branches > 100                  │
│ Complex submodules│ Multi-level nested submodules         │
│ Monorepo         │ Multiple projects share one repo       │
└──────────────────┴───────────────────────────────────────┘
```

Typical large repository examples include:

- **Linux kernel repository**: Over 1 million commits, hundreds of thousands of files
- **Windows operating system repository**: Over 300GB, millions of files
- **Google's Monorepo**: Billions of lines of code
- **Large game projects**: Extensive textures, models, audio, and other binary assets

### 1.2 Performance Bottleneck Analysis Methods

To optimize Git performance, you first need to identify where the bottlenecks are. Here is a systematic analysis approach:

```bash
# Analyze repository size
git count-objects -v --human-readable
# Output example:
# count: 150
# size: 620K
# in-pack: 12000
# packs: 3
# size-pack: 450M
# garbage: 0
# size-garbage: 0

# Analyze packfile content distribution
git verify-pack -v .git/objects/pack/pack-*.idx | \
    awk '{print $2}' | sort | uniq -c | sort -rn
# Output example:
# 8000 blob
# 3000 tree
# 800 commit
# 200 tag

# Find the largest files (sorted by object size)
git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    sed -n 's/^blob //p' | \
    sort -rnk2 | head -20

# Analyze commit history scale
echo "Total commits: $(git log --oneline | wc -l)"
echo "Merge commits: $(git log --merges --oneline | wc -l)"
echo "Total branches: $(git branch -a | wc -l)"
echo "Total files: $(git ls-files | wc -l)"
echo "Untracked files: $(git ls-files --others --exclude-standard | wc -l)"

# Analyze packfile count and size
ls -lhS .git/objects/pack/
```

### 1.3 Performance Benchmark Testing

```bash
# Measure Git operation duration
time git status
time git diff
time git log --oneline -100
time git add .
time git commit -m "test"

# Use Git built-in tracing
GIT_TRACE=1 git status
GIT_TRACE=1 git add .
GIT_TRACE=1 git commit -m "test"

# Detailed tracing (includes performance data)
GIT_TRACE=1 GIT_TRACE_PERFORMANCE=1 git status

# Performance benchmark script
cat > git-benchmark.sh << 'EOF'
#!/bin/bash
echo "Git Performance Benchmark"
echo "========================"
echo "Repository: $(pwd)"
echo "Time: $(date)"
echo ""

echo "1. git status"
time git status > /dev/null 2>&1

echo ""
echo "2. git diff"
time git diff > /dev/null 2>&1

echo ""
echo "3. git log -100"
time git log --oneline -100 > /dev/null 2>&1

echo ""
echo "4. git add ."
time git add . > /dev/null 2>&1
git reset > /dev/null 2>&1

echo ""
echo "5. git branch -a"
time git branch -a > /dev/null 2>&1

echo ""
echo "========================"
echo "Test complete"
EOF

chmod +x git-benchmark.sh
./git-benchmark.sh
```

### 1.4 Common Causes of Performance Problems

```
┌──────────────────────────────────────────────────────────────┐
│              Common Causes of Git Performance Problems        │
├──────────────────────┬───────────────────────────────────────┤
│      Cause Category  │           Specific Causes             │
├──────────────────────┼───────────────────────────────────────┤
│ Repository too large │ Many files, long history, large binaries │
│ Too many loose objects│ Not running gc timely, frequent small file creation │
│ Slow network transfer│ Remote repo, low bandwidth, inefficient protocol │
│ Index cache not enabled│ fsmonitor, untrackedCache not enabled │
│ Slow hooks           │ pre-commit running full tests, code analysis │
│ Deep submodule nesting│ Multi-level submodules, recursive updates │
│ Large files not using LFS│ Binary files stored directly in Git │
│ Improper configuration│ Compression level, parallelism, etc. not optimal │
└──────────────────────┴───────────────────────────────────────┘
```

---

## 2. git clone Optimization

### 2.1 Shallow Clone

Shallow clone is the most direct and effective way to reduce clone time, as it only fetches the most recent N commits.

```bash
# Basic shallow clone - only fetch the latest commit
git clone --depth=1 https://github.com/user/repo.git

# Specify depth - fetch the last 50 commits
git clone --depth=50 https://github.com/user/repo.git

# Shallow clone a specific branch
git clone --depth=1 --branch=main https://github.com/user/repo.git

# Shallow clone a specific tag
git clone --depth=1 --branch=v1.0.0 https://github.com/user/repo.git

# Shallow clone size comparison example:
# Full clone: 450MB
# Shallow clone (depth=1): 50MB
# Shallow clone (depth=50): 120MB
```

```bash
# Later increase clone depth
cd repo
git fetch --deepen=50

# Fetch full history (undo shallow clone)
git fetch --unshallow

# Check if current repo is shallow
git rev-parse --is-shallow-repository

# Limitations of shallow clone:
# - Cannot perform some three-way merge operations
# - git blame can only show shallow history
# - git rebase may have issues
# - Some CI/CD tools may not support it
```

### 2.2 Partial Clone

Partial clone is a revolutionary feature introduced in Git 2.19, allowing objects to be downloaded on demand.

```bash
# Clone only commits and trees, blobs downloaded on demand
git clone --filter=blob:none https://github.com/user/repo.git

# Filter blobs by size - don't download blobs larger than 1MB
git clone --filter=blob:limit=1m https://github.com/user/repo.git

# Filter by tree - don't download tree objects (extremely minimal)
git clone --filter=tree:0 https://github.com/user/repo.git

# Combined filtering
git clone --filter=blob:none,tree:0 https://github.com/user/repo.git

# Filter type explanation:
# blob:none      - Don't download any blobs (fetch on demand)
# blob:limit=N   - Don't download blobs larger than N bytes
# tree:N         - Don't download trees deeper than N
# tree:0         - Don't download any trees (most aggressive)
```

```bash
# How partial clone works:
# 1. Client requests clone with filter criteria
# 2. Server only transfers objects matching the filter
# 3. Client fetches missing objects on demand when needed
# 4. Missing objects are cached locally

# Configure server to support partial clone
git config uploadpack.allowFilter true
git config uploadpack.blobPackfileUri true

# View partial clone configuration
git config --list | grep partialclone

# Manually trigger on-demand download
git checkout -- src/large-file.bin  # Automatically downloads missing blobs
```

### 2.3 Sparse Checkout

Sparse checkout allows you to check out only specific directories from the repository, significantly reducing the working tree size.

```bash
# Method 1: Enable sparse checkout during clone
git clone --sparse https://github.com/user/repo.git
cd repo
git sparse-checkout init --cone
git sparse-checkout set src/ docs/

# Method 2: Enable sparse checkout on existing repository
git sparse-checkout init --cone
git sparse-checkout set src/ docs/ tests/

# Add more directories
git sparse-checkout add packages/core/

# View current sparse checkout configuration
git sparse-checkout list

# Disable sparse checkout (check out all files)
git sparse-checkout disable

# Re-enable
git sparse-checkout init --cone
git sparse-checkout set .
```

```bash
# Cone mode (recommended) vs traditional mode

# Cone mode - only supports directory-level filtering, better performance
git sparse-checkout init --cone
git sparse-checkout set src/ docs/

# Traditional mode - supports wildcards, more flexible but slower
git sparse-checkout init
git sparse-checkout set "src/*.py" "docs/**/*.md" "!docs/internal/"

# Performance advantages of cone mode:
# - Uses filesystem-level directory matching
# - No need to check .gitignore rules for each file
# - Several times faster in large repositories
```

### 2.4 Combined Optimization Strategies

Combining multiple optimization techniques yields the best results:

```bash
# Best combination: Shallow clone + Partial clone + Sparse checkout
git clone \
    --depth=1 \
    --filter=blob:none \
    --sparse \
    --branch=main \
    https://github.com/user/repo.git

cd repo

# Initialize sparse checkout
git sparse-checkout init --cone
git sparse-checkout set src/ docs/ tests/

# Size comparison:
# Full clone: 450MB + 2GB working tree = 2.45GB
# Optimized:  50MB  + 500MB working tree = 550MB
```

```bash
# Typical optimization configuration in CI/CD
# GitHub Actions
- name: Checkout
  uses: actions/checkout@v4
  with:
    fetch-depth: 1              # Shallow clone
    sparse-checkout: |
      src/
      docs/
      tests/
    sparse-checkout-cone-mode: true

# GitLab CI
variables:
  GIT_DEPTH: 1
  GIT_SPARSE_CHECKOUT_PATHS: "src/ docs/ tests/"

# Custom CI script
git clone --depth=1 --filter=blob:none --sparse URL
cd repo
git sparse-checkout init --cone
git sparse-checkout set $(cat .ci-paths.txt)
```

### 2.5 Clone Optimization Results Comparison

```
┌──────────────────────────────────────────────────────────────────┐
│                    Clone Optimization Results Comparison          │
├──────────────────┬──────────┬──────────┬──────────┬──────────────┤
│     Method       │ Download │ Working  │ Clone    │ Use Case     │
│                  │ Size     │ Tree     │ Time     │              │
├──────────────────┼──────────┼──────────┼──────────┼──────────────┤
│ Full clone       │ 450MB    │ 2GB      │ 120s     │ Full dev     │
│ Shallow (depth=1)│ 50MB     │ 2GB      │ 15s      │ CI/CD        │
│ Partial (blob:none)│ 80MB   │ 2GB      │ 20s      │ On-demand dev│
│ Sparse checkout  │ 450MB    │ 500MB    │ 100s     │ Specific module dev│
│ Combined optim.  │ 50MB     │ 500MB    │ 10s      │ Best practice│
└──────────────────┴──────────┴──────────┴──────────┴──────────────┘
```

---

## 3. git fetch/pull Optimization

### 3.1 fetch Optimization

```bash
# Fetch only specific branches (instead of all branches)
git fetch origin main

# Fetch all branches
git fetch --all

# Configure parallel fetching
git config --global fetch.parallel 4

# Shallow fetch - increase clone depth
git fetch --deepen=50

# Fetch without fetching tags
git fetch --no-tags

# Fetch and prune deleted remote branches
git fetch --prune

# Configure automatic prune
git config --global fetch.prune true
git config --global fetch.pruneTags true
```

```bash
# Use refspec for precise fetching
# Only fetch main and develop branches
git config --add remote.origin.fetch '+refs/heads/main:refs/remotes/origin/main'
git config --add remote.origin.fetch '+refs/heads/develop:refs/remotes/origin/develop'

# Use protocol v2 optimization (Git 2.18+)
git config --global protocol.version 2
# Advantages of protocol v2:
# - Only transfers needed references
# - Supports reference filtering
# - Reduces network round trips

# View fetch details
GIT_TRACE=1 GIT_TRANSFER_TRACE=1 git fetch origin main
```

### 3.2 pull Optimization

```bash
# Configure pull behavior to rebase (avoid unnecessary merge commits)
git config --global pull.rebase true

# Only allow fast-forward merges
git config --global pull.ff only

# Auto stash uncommitted changes
git config --global rebase.autoStash true

# Recommended pull configuration combination
git config --global pull.rebase true
git config --global pull.ff only
git config --global rebase.autoStash true
git config --global rebase.updateRefs true

# Use rebase + autostash for pull
git pull --rebase --autostash origin main

# View detailed pull information
git pull --verbose origin main
```

### 3.3 Submodule Optimization

```bash
# Update submodules in parallel
git submodule update --init --recursive --jobs=4

# Shallow clone submodules
git submodule update --init --depth=1

# Only update specific submodules
git submodule update --init -- src/lib

# Configure submodule for shallow clone
cat > .gitmodules << 'EOF'
[submodule "src/lib"]
    path = src/lib
    url = https://github.com/user/lib.git
    shallow = true
    branch = main
EOF

# Global submodule configuration
git config --global submodule.recurse true
git config --global submodule.shallow true
git config --global submodule.fetchJobs 4

# Batch update submodules
git submodule foreach --recursive 'git fetch --depth=1 && git checkout main && git pull'
```

### 3.4 Incremental Update Strategy

```bash
# Use refspec for incremental updates
git fetch origin \
    refs/heads/main:refs/remotes/origin/main \
    refs/heads/develop:refs/remotes/origin/develop

# Only fetch new commits (shallow fetch)
git fetch --depth=1 origin main

# Increase depth
git fetch --deepen=100 origin main

# Fetch specific tags
git fetch origin tag v1.0.0

# Use prune to clean up deleted branches
git fetch --prune origin

# Configure automatic prune
git config --global fetch.prune true
git config --global fetch.pruneTags true
```

---

## 4. git status Optimization

### 4.1 File System Monitor (fsmonitor)

fsmonitor is one of Git's most important performance optimizations, using OS-level file system events to avoid full scans.

```bash
# Enable fsmonitor (Git 2.37+)
git config core.fsmonitor true

# Use Watchman as fsmonitor backend
# Install Watchman:
# Ubuntu/Debian:
sudo apt-get install watchman

# macOS:
brew install watchman

# Configure Git to use Watchman
git config core.fsmonitor "git-fsmonitor--daemon"

# Start fsmonitor daemon
git fsmonitor--daemon start

# Check fsmonitor status
git fsmonitor--daemon status

# Stop fsmonitor daemon
git fsmonitor--daemon stop

# fsmonitor performance improvement:
# Without: git status takes 2.5 seconds
# With: git status takes 0.1 seconds
# Improvement: 25x faster
```

### 4.2 Untracked File Cache (untrackedCache)

```bash
# Enable untracked cache
git config core.untrackedCache true

# How untracked cache works:
# 1. First run scans all untracked files
# 2. Caches results to .git/untracked-cache/ directory
# 3. Subsequent runs only check changed directories
# 4. Uses mtime to determine if directories changed

# Check untracked cache status
git ls-files --untracked --debug

# Clean untracked cache
git clean -fdx  # Delete untracked files and directories

# untracked cache performance improvement:
# Without: git status takes 1.5 seconds
# With: git status takes 0.3 seconds
# Improvement: 5x faster
```

### 4.3 Comprehensive Status Optimization Configuration

```bash
# Complete status optimization configuration
git config core.fsmonitor true
git config core.untrackedCache true
git config feature.manyFiles true

# feature.manyFiles enables the following optimizations:
# - core.untrackedCache = true
# - core.fsmonitor = true
# - index.version = 4
# - index.skipHash = false

# View current configuration
git config --get core.fsmonitor
git config --get core.untrackedCache
git config --get feature.manyFiles
```

```bash
# Performance comparison test
echo "Before optimization:"
git config --unset core.fsmonitor
git config --unset core.untrackedCache
time git status > /dev/null 2>&1

echo "After optimization:"
git config core.fsmonitor true
git config core.untrackedCache true
time git status > /dev/null 2>&1
```

### 4.4 Advanced status Usage

```bash
# Quick status view (short format)
git status --short
git status -s

# Show only untracked files
git status --untracked-files
git status -u

# Ignore submodule status
git status --ignore-submodules=dirty

# Use porcelain format (suitable for script parsing)
git status --porcelain
git status --porcelain=v2

# View branch information
git status --branch
git status -b

# Performance-optimized status check tips
git diff --quiet           # Only check if there are modifications, return exit code
git diff --cached --quiet  # Only check if staged area has modifications
```

```bash
# Batch status check script
cat > check-status.sh << 'EOF'
#!/bin/bash
# Quick repository status check

# Check for unstaged changes
if ! git diff --quiet; then
    echo "There are unstaged changes"
fi

# Check for staged changes
if ! git diff --cached --quiet; then
    echo "There are staged changes"
fi

# Check for untracked files
if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    echo "There are untracked files"
fi

# Check for conflicts
if [ -n "$(git ls-files -u)" ]; then
    echo "There are unresolved conflicts"
fi
EOF

chmod +x check-status.sh
```

---

## 5. git diff Optimization

### 5.1 diff Algorithm Selection

Git supports four diff algorithms, each with its own pros and cons:

```
┌──────────────────────────────────────────────────────────────┐
│                   Git Diff Algorithm Comparison              │
├──────────────┬──────────┬──────────┬────────────────────────┤
│   Algorithm  │  Speed   │  Quality │        Characteristics│
├──────────────┼──────────┼──────────┼────────────────────────┤
│ myers        │ Fastest  │ Average  │ Default algorithm      │
│ minimal      │ Slowest  │ Minimum  │ Minimize diff lines    │
│ patience     │ Medium   │ Better   │ Better rename detection│
│ histogram    │ Fast     │ Best     │ Best rename detection  │
└──────────────┴──────────┴──────────┴────────────────────────┘
```

```bash
# Configure diff algorithm
git config diff.algorithm histogram

# Temporarily use different algorithm
git diff --diff-algorithm=patience
git diff --diff-algorithm=minimal

# Algorithm performance test
echo "myers:"
time git diff --diff-algorithm=myers > /dev/null 2>&1

echo "patience:"
time git diff --diff-algorithm=patience > /dev/null 2>&1

echo "histogram:"
time git diff --diff-algorithm=histogram > /dev/null 2>&1
```

### 5.2 diff Output Optimization

```bash
# Use stat mode (show only statistics, no detailed diffs)
git diff --stat
git diff --shortstat

# Use summary mode
git diff --summary

# Limit diff context lines (reduce output)
git diff --unified=3  # Default
git diff --unified=1  # Reduce context

# Only compare specific file types
git diff -- '*.py'
git diff -- 'src/*.js'

# Ignore whitespace differences
git diff --ignore-all-space
git diff -w

# Ignore whitespace changes
git diff --ignore-space-change
git diff -b

# Use color highlighting
git diff --color-words
git diff --color-moved
```

### 5.3 Large File diff Optimization

```bash
# Configure large file diff driver (show only metadata differences)
git config diff.psd.textconv "identify -verbose"
git config diff.pdf.textconv "pdftotext"
git config diff.docx.textconv "pandoc -t plain"
git config diff.xlsx.textconv "xlsx2csv"

# .gitattributes configuration
*.psd  diff=psd
*.pdf  diff=pdf
*.docx diff=docx
*.xlsx diff=xlsx

# Skip binary file diffs
git diff --binary

# Show only binary file statistics
git diff --stat --binary

# Configure external diff tool
git config diff.tool vscode
git config difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"
```

### 5.4 diff Performance Optimization Configuration

```bash
# diff-related performance optimization configuration
git config diff.algorithm histogram
git config diff.colorMoved default
git config diff.renames true
git config diff.submodule log

# Configure rename detection threshold
git config diff.renameLimit 10000

# Enable diff index cache
git config diff.cached true
```

---

## 6. git gc and git repack Configuration

### 6.1 Automatic gc Configuration

```bash
# Automatic gc threshold
git config gc.auto 6700        # Loose object count threshold (default)
git config gc.autoPackLimit 50 # Packfile count threshold (default)

# Automatic gc strategy
git config gc.autoDetach true       # Run gc in background
git config gc.writeCommitGraph true # Write commit-graph to speed up log

# Disable automatic gc (suitable for CI/CD environments)
git config gc.auto 0

# Manually trigger gc
git gc

# View current gc configuration
git config --get gc.auto
git config --get gc.autoPackLimit
git config --get gc.writeCommitGraph
```

### 6.2 Aggressive gc Strategy

```bash
# Aggressive gc (more thorough compression, but takes longer)
git gc --aggressive

# Configure aggressive gc parameters
git config gc.aggressiveDepth 50
git config gc.aggressiveWindow 250

# Applicable scenarios for aggressive gc:
# 1. Repository size has significantly increased
# 2. Still many loose objects after initial gc
# 3. Need to maximize compression ratio

# Drawbacks of aggressive gc:
# 1. Takes longer (may take minutes or even hours)
# 2. High CPU usage
# 3. May affect other Git operations
```

### 6.3 repack Optimization

```bash
# Basic repack
git repack -a -d

# Parameter explanation:
# -a: Pack all objects (including those not in any packfile)
# -d: Delete redundant packfiles
# -l: Only pack local references
# -f: Force repack
# -n: Don't update server info

# Incremental repack (specify delta parameters)
git repack -a -d --depth=250 --window=250

# Use geometric series repack (Git 2.24+, recommended)
git repack --geometric=2 -d

# Advantages of geometric series repack:
# 1. Automatically balances packfile sizes
# 2. Reduces packfile count
# 3. Optimizes lookup efficiency
# 4. Avoids single oversized packfile
```

```bash
# repack-related configuration
git config pack.window 250       # Delta search window size
git config pack.depth 50         # Maximum delta chain depth
git config pack.threads 4        # Parallel compression threads
git config pack.windowMemory 1g  # Delta search memory limit
git config pack.packSizeLimit 2g # Single packfile size limit

# Periodic repack script
cat > git-repack.sh << 'EOF'
#!/bin/bash
echo "Starting Git repack..."

# Basic repack
echo "1. Basic repack..."
git repack -a -d

# Geometric series repack
echo "2. Geometric series repack..."
git repack --geometric=2 -d

# Clean unreachable objects
echo "3. Cleaning unreachable objects..."
git prune

# Update server info
echo "4. Updating server info..."
git update-server-info

# Write commit-graph
echo "5. Writing commit-graph..."
git commit-graph write --reachable

echo "Repack complete"
EOF

chmod +x git-repack.sh
```

### 6.4 commit-graph Optimization

```bash
# commit-graph is used to speed up git log and git merge-base

# Write commit-graph
git commit-graph write

# Only write reachable commits
git commit-graph write --reachable

# Verify commit-graph
git commit-graph verify

# Configure automatic commit-graph updates
git config gc.writeCommitGraph true

# commit-graph performance improvement:
# Without: git log --oneline -1000 takes 2 seconds
# With: git log --oneline -1000 takes 0.1 seconds
# Improvement: 20x faster

# View commit-graph file
ls -la .git/objects/info/commit-graph*

# commit-graph chain structure
# Supports linking multiple commit-graph files
# Incremental updates only require writing new commit-graph
```

---

## 7. Git LFS Performance Tuning

### 7.1 LFS Basic Configuration

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "*.mp4"
git lfs track "*.bin"
git lfs track "*.so"
git lfs track "*.dll"

# View tracking rules
git lfs track

# View LFS file list
git lfs ls-files

# View LFS status
git lfs status
```

### 7.2 LFS Performance Optimization Configuration

```bash
# 1. Increase parallel transfers
git config lfs.concurrenttransfers 8  # Default 3

# 2. Use LFS local cache
git config lfs.storage ~/.git-lfs-cache

# 3. Only fetch needed LFS files
git lfs pull --include="src/**"
git lfs pull --exclude="tests/**"

# 4. Configure LFS smudge filter
git config filter.lfs.smudge "git-lfs smudge -- %f"
git config filter.lfs.clean "git-lfs clean -- %f"
git config filter.lfs.required true

# 5. Delay LFS downloads (fetch on demand)
git config filter.lfs.smudge "git-lfs smudge --skip -- %f"
# Then manually download: git lfs pull

# 6. Configure LFS transfer retries
git config lfs.transfer.maxretries 3
git config lfs.transfer.maxrequests 100

# 7. View LFS configuration
git config --list | grep lfs
```

### 7.3 LFS Caching Strategy

```bash
# Configure LFS cache directory
git config lfs.storage ~/.git-lfs-cache

# View cache size
du -sh ~/.git-lfs-cache

# Clean old cache
git lfs prune

# Share LFS cache (team shared server)
git config lfs.storage /shared/git-lfs-cache

# LFS cache directory structure:
# ~/.git-lfs-cache/
# ├── lfs/
# │   ├── objects/
# │   │   ├── ab/
# │   │   │   └── cd/
# │   │   │       └── abcdef1234567890...
# │   │   └── ...
# │   └── tmp/
# └── ...

# LFS performance comparison:
# Without cache: git lfs pull takes 30 seconds
# With cache: git lfs pull takes 2 seconds
```

### 7.4 LFS Migration

```bash
# Migrate existing large files to LFS
git lfs migrate import --include="*.psd" --everything
git lfs migrate import --include="*.zip,*.mp4" --everything

# Migrate back from LFS
git lfs migrate export --include="*.psd" --everything

# View migration information
git lfs migrate info
git lfs migrate info --include="*.psd"

# LFS migration notes:
# 1. Migration will rewrite history
# 2. Need to force push to remote
# 3. Team members need to re-clone
```

---

## 8. Git Hooks Performance Optimization

### 8.1 Hooks Performance Problem Analysis

```bash
# Common performance problems:
# 1. pre-commit hook running full test suite
# 2. pre-push hook running time-consuming code analysis
# 3. post-checkout hook installing dependencies

# Analyze hooks execution time
GIT_TRACE=1 git commit -m "test" 2>&1 | grep -E "hook|time"

# Check hooks execution time
time git commit -m "test" 2>&1
```

### 8.2 Optimizing pre-commit Hook

```bash
#!/bin/bash
# Optimized pre-commit hook

# 1. Only check staged files (not all files)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# 2. If no staged files, exit immediately
if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# 3. Only run relevant checks (by file type)
for file in $STAGED_FILES; do
    # Python file check
    if [[ "$file" == *.py ]]; then
        python -m black --check "$file" || exit 1
    fi

    # JavaScript/TypeScript file check
    if [[ "$file" == *.js ]] || [[ "$file" == *.ts ]]; then
        npx prettier --check "$file" || exit 1
    fi
done

# 4. Use lint cache to avoid redundant checks
LINT_CACHE=".git/lint-cache"
if [ -f "$LINT_CACHE" ]; then
    LAST_LINT=$(cat "$LINT_CACHE")
    CURRENT_HASH=$(echo "$STAGED_FILES" | md5sum | cut -d' ' -f1)
    if [ "$LAST_LINT" = "$CURRENT_HASH" ]; then
        echo "Lint cache hit, skipping check"
        exit 0
    fi
fi

# 5. Run lint
npm run lint

# 6. Save cache
echo "$STAGED_FILES" | md5sum | cut -d' ' -f1 > "$LINT_CACHE"

exit 0
```

### 8.3 Using pre-commit Framework

```bash
# Install pre-commit framework
pip install pre-commit

# Create configuration file
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=120']
EOF

# Install hooks
pre-commit install

# Run all hooks
pre-commit run --all-files

# Skip specific hook
SKIP=flake8 git commit -m "test"

# pre-commit caching mechanism:
# 1. Downloads and installs tools to cache directory on first run
# 2. Uses cached tools on subsequent runs
# 3. Only checks modified files (checks after auto-staging)
```

### 8.4 Asynchronous and Conditional Hooks

```bash
#!/bin/bash
# post-commit hook - run time-consuming tasks asynchronously

# Run tests and build in background
(
    npm test &
    npm run build &

    # Wait for all background tasks to complete
    wait
) &

# Return immediately, don't block commit
exit 0
```

```bash
#!/bin/bash
# pre-push hook - only run tests when necessary

# Check if test files were modified
MODIFIED_TESTS=$(git diff --name-only HEAD@{1}..HEAD 2>/dev/null | grep -E "test.*\.(py|js|ts)$")

if [ -n "$MODIFIED_TESTS" ]; then
    echo "Test file modifications detected, running tests..."
    npm test
fi

exit 0
```

---

## 9. Git Performance Optimization in CI/CD

### 9.1 CI/CD Clone Optimization

```yaml
# GitHub Actions optimization configuration
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 1                    # Shallow clone
          sparse-checkout: |                # Sparse checkout
            src/
            docs/
            tests/
          sparse-checkout-cone-mode: true

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: |
            node_modules
            .git/lfs
          key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
```

```yaml
# GitLab CI optimization configuration
variables:
  GIT_DEPTH: 1
  GIT_SUBMODULE_STRATEGY: none
  GIT_CLEAN_FLAGS: -ffdx
  GIT_SPARSE_CHECKOUT_PATHS: "src/ docs/ tests/"

build:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .git/lfs/
  script:
    - npm install
    - npm run build
```

### 9.2 CI/CD Caching Strategy

```yaml
# Multi-layer caching strategy
- name: Cache Git LFS
  uses: actions/cache@v3
  with:
    path: .git/lfs
    key: ${{ runner.os }}-lfs-${{ hashFiles('.lfs-assets-id') }}
    restore-keys: |
      ${{ runner.os }}-lfs-

- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache build artifacts
  uses: actions/cache@v3
  with:
    path: dist
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-
```

### 9.3 CI/CD Incremental Builds

```yaml
# Only run jobs when specific files change
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'
      - 'package-lock.json'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check changes
        uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            src:
              - 'src/**'
            tests:
              - 'tests/**'
            docs:
              - 'docs/**'

      - name: Build
        if: steps.changes.outputs.src == 'true'
        run: npm run build

      - name: Test
        if: steps.changes.outputs.tests == 'true'
        run: npm test

      - name: Deploy docs
        if: steps.changes.outputs.docs == 'true'
        run: npm run deploy-docs
```

### 9.4 CI/CD Parallelization

```yaml
# Parallel test sharding
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Install dependencies
        run: npm ci

      - name: Run tests (shard ${{ matrix.shard }})
        run: npm test -- --shard=${{ matrix.shard }}/4
```

---

## 10. Monorepo Git Performance Strategies

### 10.1 Monorepo Performance Challenges

```bash
# Typical Monorepo problems:
# 1. Repository is huge (>10GB)
# 2. Many files (>100,000)
# 3. Frequent commits (hundreds per day)
# 4. Many branches (hundreds)
# 5. Long CI/CD build times

# Analyze Monorepo repository
echo "Repository size: $(git count-objects -v --human-readable | grep size-pack)"
echo "Total files: $(git ls-files | wc -l)"
echo "Total commits: $(git log --oneline | wc -l)"
echo "Total branches: $(git branch -a | wc -l)"
```

### 10.2 Sparse Checkout Strategy

```bash
# Initialize sparse checkout
git sparse-checkout init --cone

# Set checkout directories by team/project
git sparse-checkout set \
    packages/core \
    packages/shared \
    packages/team-a

# Dynamically add directories
git sparse-checkout add packages/team-b

# Create sparse checkout configuration file (can be committed to repo)
cat > .sparse-checkout << 'EOF'
packages/core/
packages/shared/
packages/team-a/
tools/
configs/
EOF

# Apply configuration
git sparse-checkout set --stdin < .sparse-checkout
```

### 10.3 Partial Clone Strategy

```bash
# Partial clone + Sparse checkout combination
git clone \
    --filter=blob:none \
    --sparse \
    --depth=1 \
    https://github.com/org/monorepo.git

cd monorepo

git sparse-checkout init --cone
git sparse-checkout set packages/team-a/

# Fetch files on demand
git checkout -- packages/team-a/src/index.ts
```

### 10.4 Worktree Strategy

```bash
# Use git worktree to manage multiple working trees
git worktree add ../monorepo-feature-a feature-a
git worktree add ../monorepo-bugfix-123 bugfix-123

# View worktree list
git worktree list

# Remove worktree
git worktree remove ../monorepo-feature-a

# Advantages of worktrees:
# 1. Can work on multiple branches simultaneously
# 2. Avoids frequent checkouts (very slow in large repos)
# 3. Each worktree has independent file state
# 4. Shares the same .git directory
```

### 10.5 Monorepo Tool Integration

```bash
# Using Nx (JavaScript/TypeScript Monorepo)
npx nx run-many --target=build --all
npx nx affected --target=test    # Only test affected projects

# Using Turborepo
npx turbo run build
npx turbo run test

# Using Bazel (Google's build system)
bazel build //packages/core:all
bazel test //packages/core:tests

# Using Lerna
npx lerna run build
npx lerna run test

# Common advantages of these tools:
# 1. Incremental builds (only build changed parts)
# 2. Task caching (avoid redundant builds)
# 3. Parallel execution (utilize multi-core CPUs)
# 4. Dependency analysis (automatically determine build order)
```

---

## 11. Git Client Performance Comparison

### 11.1 Native Git

```bash
# Advantages of native Git:
# 1. Latest feature support
# 2. Extensive documentation and community support
# 3. Cross-platform compatibility
# 4. No additional dependencies

# Performance characteristics of native Git:
# - Small repositories: Excellent (millisecond level)
# - Medium repositories: Good (second level)
# - Large repositories: Requires optimized configuration

# Native Git optimization configuration
git config core.fsmonitor true
git config core.untrackedCache true
git config feature.manyFiles true
git config protocol.version 2
```

### 11.2 Git LFS

```bash
# Advantages of Git LFS:
# 1. Large file support (GB-level)
# 2. Seamless integration with native Git
# 3. Wide platform support
# 4. On-demand download

# Performance characteristics of Git LFS:
# - Large file storage: Excellent
# - Network transfer: Good (supports parallel)
# - Caching mechanism: Good

# Git LFS optimization configuration
git config lfs.concurrenttransfers 8
git config lfs.storage ~/.git-lfs-cache
```

### 11.3 Gitless

```bash
# Gitless is a simplified frontend for Git
# Install: pip install gitless

# Advantages of Gitless:
# 1. Simplified commands (no index/stage needed)
# 2. More intuitive workflow
# 3. Automatic handling of common operations

# Performance characteristics of Gitless:
# - Same as native Git (uses Git under the hood)
# - No additional performance overhead
```

### 11.4 Jujutsu (jj)

```bash
# Jujutsu is a next-generation version control system
# Install: cargo install --git https://github.com/martinvonz/jj

# Advantages of Jujutsu:
# 1. Compatible with Git repositories
# 2. Better merge handling
# 3. Worktree concept (similar to worktree)
# 4. Operation log and undo

# Performance characteristics of Jujutsu:
# - Some operations faster than Git
# - Lower memory usage
# - Better large repository support
```

### 11.5 Performance Comparison Testing Method

```bash
#!/bin/bash
# Git client performance comparison test script

REPO_URL="https://github.com/user/large-repo.git"
TEST_DIR="/tmp/git-perf-test"

echo "Git Client Performance Comparison Test"
echo "======================================"

# Clean up test directory
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Test clone time
echo ""
echo "1. Clone test"
time git clone "$REPO_URL" "$TEST_DIR/repo" 2>&1

cd "$TEST_DIR/repo"

# Test status time
echo ""
echo "2. Status test"
time git status > /dev/null 2>&1

# Test diff time
echo ""
echo "3. Diff test"
time git diff > /dev/null 2>&1

# Test log time
echo ""
echo "4. Log test"
time git log --oneline -100 > /dev/null 2>&1

# Test add time
echo ""
echo "5. Add test"
echo "test" > test-file.txt
time git add . > /dev/null 2>&1
git reset > /dev/null 2>&1
rm test-file.txt

echo ""
echo "======================================"
echo "Test complete"

# Clean up
cd /
rm -rf "$TEST_DIR"
```

---

## 12. Git Caching and Preloading Strategies

### 12.1 Git Built-in Caching

```bash
# untracked cache - cache untracked file list
git config core.untrackedCache true

# fsmonitor - file system monitoring cache
git config core.fsmonitor true

# commit-graph - commit graph cache
git config gc.writeCommitGraph true

# packfile delta cache
git config pack.deltaCacheSize 1g
git config pack.deltaCacheLimit 1000

# packfile window cache
git config core.packedGitLimit 1g
git config core.packedGitWindowSize 1g

# index version (v4 is faster)
git config index.version 4
```

### 12.2 Preloading Script

```bash
#!/bin/bash
# Git repository preloading script

REPO_DIR="$1"

if [ -z "$REPO_DIR" ]; then
    echo "Usage: $0 <repo-dir>"
    exit 1
fi

cd "$REPO_DIR"

echo "Preloading Git repository: $REPO_DIR"
echo "Start time: $(date)"

# 1. Preload index (trigger fsmonitor and untracked cache)
echo "1. Preloading index..."
time git status > /dev/null 2>&1

# 2. Write commit-graph
echo "2. Writing commit-graph..."
time git commit-graph write --reachable

# 3. Repack
echo "3. Repacking..."
time git repack -a -d

# 4. Preload untracked cache
echo "4. Preloading untracked cache..."
time git ls-files --others --exclude-standard > /dev/null 2>&1

# 5. Preload LFS files
if git lfs version > /dev/null 2>&1; then
    echo "5. Preloading LFS files..."
    time git lfs pull > /dev/null 2>&1
fi

echo "Preload complete: $(date)"
```

### 12.3 Cache Warmup Strategy

```bash
#!/bin/bash
# Git cache warmup script (for servers)

REPOS=(
    "/srv/git/repo1.git"
    "/srv/git/repo2.git"
    "/srv/git/repo3.git"
)

for repo in "${REPOS[@]}"; do
    if [ -d "$repo" ]; then
        echo "Warming up: $repo"
        cd "$repo"

        # Update server info
        git update-server-info

        # Write commit-graph
        git commit-graph write --reachable

        # Repack
        git repack -a -d --geometric=2

        # Clean unreachable objects
        git prune

        cd - > /dev/null
    fi
done

echo "Cache warmup complete"
```

```bash
# Run cache warmup periodically in cron
# Run at 2 AM daily
# 0 2 * * * /path/to/git-cache-warmup.sh

# Run in systemd
cat > /etc/systemd/git-cache-warmup.service << 'EOF'
[Unit]
Description=Git Cache Warmup
After=network.target

[Service]
Type=oneshot
ExecStart=/path/to/git-cache-warmup.sh
User=git
Group=git

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/git-cache-warmup.timer << 'EOF'
[Unit]
Description=Run Git Cache Warmup daily

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

### 12.4 Memory Cache Configuration

```bash
# Git memory cache configuration

# packfile memory limit
git config core.packedGitLimit 1g

# packfile window size
git config core.packedGitWindowSize 1g

# delta cache size
git config pack.deltaCacheSize 1g

# delta cache entry limit
git config pack.deltaCacheLimit 1000

# large file threshold
git config core.bigFileThreshold 512m

# Performance comparison test
echo "Unoptimized:"
git config --unset core.packedGitLimit
git config --unset core.packedGitWindowSize
time git log --oneline -1000 > /dev/null 2>&1

echo "Optimized:"
git config core.packedGitLimit 1g
git config core.packedGitWindowSize 1g
time git log --oneline -1000 > /dev/null 2>&1
```

---

## 13. Network Layer Optimization

### 13.1 Compression Optimization

```bash
# Configure compression level (1-9)
git config core.compression 6        # Default level
git config core.looseCompression 6   # Loose object compression
git config pack.compression 6        # Packfile compression

# Compression level comparison:
# 1: Fastest, lowest compression ratio (suitable for fast networks)
# 6: Balanced (default, recommended)
# 9: Slowest, highest compression ratio (suitable for slow networks)

# HTTP transfer buffer
git config http.postBuffer 524288000  # 500MB

# Large file threshold
git config core.bigFileThreshold 512m
```

### 13.2 Proxy Configuration

```bash
# HTTP proxy
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# SOCKS proxy
git config --global http.proxy socks5://proxy.example.com:1080

# Domain-specific proxy
git config --global http.https://github.com.proxy http://proxy.example.com:8080

# Proxy authentication
git config --global http.proxy http://user:password@proxy.example.com:8080

# Disable proxy
git config --global --unset http.proxy
git config --global --unset https.proxy

# Environment variable proxy
export http_proxy=http://proxy.example.com:8080
export https_proxy=https://proxy.example.com:8080
export no_proxy=github.com,gitlab.com
```

### 13.3 CDN and Mirror Acceleration

```bash
# Use GitHub mirror (China mainland acceleration)
git config url."https://ghproxy.com/https://github.com/".insteadOf "https://github.com/"

# Use GitLab mirror
git config url."https://gitlab.example.com/".insteadOf "https://gitlab.com/"

# Use Gitee mirror
git config url."https://gitee.com/".insteadOf "https://github.com/"

# View mirror configuration
git config --get-regexp url

# Remove mirror configuration
git config --unset url."https://ghproxy.com/https://github.com/".insteadOf

# Set mirror for specific repository
git config url."https://mirror.example.com/".insteadOf "https://github.com/specific-org/"
```

### 13.4 Network Timeout Configuration

```bash
# Configure HTTP timeout
git config --global http.lowSpeedLimit 1000    # Minimum speed (bytes/s)
git config --global http.lowSpeedTime 30       # Low speed duration (seconds)

# Configure connection timeout
git config --global http.connectTimeout 30     # Connection timeout (seconds)

# Disable certificate verification (not recommended, for testing only)
git config --global http.sslVerify false

# Configure DNS cache
git config --global http.dnsCacheTimeout 600   # DNS cache time (seconds)
```

### 13.5 Multi-Channel Transfer

```bash
# Parallel fetching
git config --global fetch.parallel 4

# Parallel pushing
git config --global push.parallel 4

# Parallel submodule updates
git config --global submodule.fetchJobs 4

# Parallel LFS transfers
git config lfs.concurrenttransfers 8

# View current configuration
echo "fetch.parallel: $(git config --get fetch.parallel)"
echo "push.parallel: $(git config --get push.parallel)"
echo "submodule.fetchJobs: $(git config --get submodule.fetchJobs)"
echo "lfs.concurrenttransfers: $(git config --get lfs.concurrenttransfers)"
```

---

## 14. Monitoring and Diagnostic Tools

### 14.1 Git Built-in Tracing

```bash
# Basic tracing (shows Git internal operations)
GIT_TRACE=1 git status

# Detailed tracing (includes performance data)
GIT_TRACE=1 GIT_TRACE_PERFORMANCE=1 git status

# Network tracing
GIT_TRACE=1 GIT_TRANSFER_TRACE=1 git fetch origin

# Packing tracing
GIT_TRACE=1 GIT_PACK_TRACE=1 git gc

# Trace output to file
GIT_TRACE=/tmp/git-trace.log git status
GIT_TRACE_PERFORMANCE=/tmp/git-perf.log git status

# Trace specific operations
GIT_TRACE=1 git add .
GIT_TRACE=1 git commit -m "test"
GIT_TRACE=1 git push origin main
```

### 14.2 System Performance Analysis Tools

```bash
# Using time command
time git status
time git diff
time git log --oneline -100

# Using strace to trace system calls (Linux)
strace -c git status

# Using dtruss to trace system calls (macOS)
sudo dtruss -c git status

# Using perf for performance analysis (Linux)
perf record -g git status
perf report

# Using flame graph for analysis
git clone https://github.com/brendangregg/FlameGraph.git
perf record -g git status
perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > git-status.svg
```

### 14.3 Repository Health Check Script

```bash
#!/bin/bash
# Git repository health check script

echo "Git Repository Health Check"
echo "=========================="
echo "Repository: $(pwd)"
echo "Time: $(date)"
echo ""

# 1. Check repository size
echo "1. Repository size:"
git count-objects -v --human-readable
echo ""

# 2. Check object count
echo "2. Object statistics:"
git count-objects -v
echo ""

# 3. Check packfile
echo "3. Packfile information:"
ls -lhS .git/objects/pack/ 2>/dev/null || echo "No packfiles"
echo ""

# 4. Check references
echo "4. Reference statistics:"
echo "  Total refs: $(git show-ref | wc -l)"
echo "  Branches: $(git branch | wc -l)"
echo "  Remote branches: $(git branch -r | wc -l)"
echo "  Tags: $(git tag | wc -l)"
echo ""

# 5. Check untracked files
echo "5. File statistics:"
echo "  Tracked: $(git ls-files | wc -l)"
echo "  Untracked: $(git ls-files --others --exclude-standard | wc -l)"
echo ""

# 6. Check large files
echo "6. Large files (>10MB):"
git rev-list --objects --all | \
    git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
    sed -n 's/^blob //p' | \
    awk '$2 > 10485760 {printf "  %s (%.1fMB)\n", $3, $2/1048576}' | \
    sort -k2 -rn | head -10
echo ""

# 7. Check integrity
echo "7. Integrity check:"
git fsck --no-reflogs --unreachable 2>&1 | head -20
echo ""

# 8. Check configuration
echo "8. Performance configuration:"
echo "  core.fsmonitor: $(git config --get core.fsmonitor || echo 'Not set')"
echo "  core.untrackedCache: $(git config --get core.untrackedCache || echo 'Not set')"
echo "  feature.manyFiles: $(git config --get feature.manyFiles || echo 'Not set')"
echo "  protocol.version: $(git config --get protocol.version || echo 'Not set')"
echo ""

echo "=========================="
echo "Check complete"
```

### 14.4 Performance Monitoring Script

```bash
#!/bin/bash
# Git performance monitoring script

LOG_FILE="/var/log/git-performance.log"
REPO_DIR="${1:-.}"

log_metric() {
    local operation=$1
    local duration=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$timestamp,$operation,$duration" >> "$LOG_FILE"
}

monitor_operation() {
    local operation=$1
    shift
    local start_time=$(date +%s%N)
    "$@" > /dev/null 2>&1
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))
    log_metric "$operation" "$duration"
    echo "$operation: ${duration}ms"
}

cd "$REPO_DIR" || exit 1

echo "Starting performance monitoring..."
echo "Repository: $(pwd)"
echo "Time: $(date)"
echo ""

# Monitor common operations
monitor_operation "status" git status
monitor_operation "diff" git diff
monitor_operation "log-100" git log --oneline -100
monitor_operation "branch" git branch -a
monitor_operation "add" git add .
git reset > /dev/null 2>&1

echo ""
echo "Monitoring complete"
echo "Log file: $LOG_FILE"
```

### 14.5 Visual Monitoring

```bash
# Using git-stats for statistics
pip install git-stats

# Generate statistics report
git-stats --since="2024-01-01" --until="2024-12-31"

# Using gitstats to generate HTML report
# Install: apt-get install gitstats
gitstats /path/to/repo /output/dir

# Using Gource to visualize commit history
# Install: apt-get install gource
gource --seconds-per-day 0.1

# Using GitKraken to view repository status
# GitKraken is a graphical Git client that provides intuitive performance analysis

# Using VS Code Git extension
# VS Code has built-in Git support, allowing you to view status, diffs, history, etc.
```

---

## Summary

This chapter provides a comprehensive overview of Git performance optimization strategies and techniques:

- **Clone optimization**: Use shallow clone, partial clone, sparse checkout to reduce download size and working tree size
- **fetch/pull optimization**: Configure parallel fetching, use protocol v2, optimize submodule updates
- **status optimization**: Enable fsmonitor and untrackedCache to improve status check speed
- **diff optimization**: Choose appropriate diff algorithm, configure caching, optimize output format
- **gc/repack configuration**: Optimize automatic gc thresholds, use geometric series repack, enable commit-graph
- **LFS tuning**: Configure parallel transfers, use caching, delay downloads
- **Hooks optimization**: Only check modified files, use caching, execute asynchronously
- **CI/CD optimization**: Use shallow clone, configure caching, parallelize builds
- **Monorepo strategies**: Use sparse checkout, partial clone, worktree management
- **Client comparison**: Understand performance characteristics and use cases of different clients
- **Caching strategies**: Configure built-in caching, create preloading scripts, periodic warmup
- **Network optimization**: Configure compression, proxy, CDN acceleration
- **Monitoring tools**: Use Git built-in tracing, system performance analysis tools, repository health checks

Through proper configuration and optimization, you can maintain an efficient development experience in large repositories. The key is to choose appropriate optimization strategies based on specific repository characteristics and workflows, and continuously monitor and adjust.

---

## Appendix 1: Systematic Methodology for Performance Optimization

Performance optimization is not simply adjusting a few configuration parameters, but a systematic engineering process. Before performing Git performance optimization, we need to establish a complete methodology, including problem identification, bottleneck analysis, solution design, and result verification.

### Problem Identification Phase

In the problem identification phase, we need to collect performance data and understand the current performance status. This includes measuring the duration of various Git operations, analyzing the repository's scale and structure, and understanding the team's workflow. Through this data, we can identify which operations are most time-consuming, which repositories are largest, and which workflows are most frequent.

```bash
# Collect performance data
echo "=== Repository Basic Information ==="
echo "Repository size: $(git count-objects -v --human-readable | grep 'size-pack' | awk '{print $2}')"
echo "File count: $(git ls-files | wc -l)"
echo "Commit count: $(git log --oneline | wc -l)"
echo "Branch count: $(git branch -a | wc -l)"

echo ""
echo "=== Operation Duration Test ==="
echo -n "git status: "
time git status > /dev/null 2>&1

echo -n "git diff: "
time git diff > /dev/null 2>&1

echo -n "git log -100: "
time git log --oneline -100 > /dev/null 2>&1
```

### Bottleneck Analysis Phase

In the bottleneck analysis phase, we need to deeply analyze performance data to find the root causes of performance problems. This may include factors such as repository being too large, slow network transfer, improper configuration, etc. By using Git's built-in tracing tools and system performance analysis tools, we can precisely locate where the bottlenecks are.

```bash
# Use Git tracing tools to analyze bottlenecks
GIT_TRACE=1 GIT_TRACE_PERFORMANCE=1 git status 2>&1 | grep -E "trace|time"

# Use system tools for analysis
strace -c git status 2>&1 | tail -20

# Analyze filesystem performance
time find . -name "*.py" | wc -l
time git ls-files "*.py" | wc -l
```

### Solution Design Phase

In the solution design phase, we need to design appropriate optimization solutions based on the bottleneck analysis results. This may include configuration adjustments, tool upgrades, workflow improvements, and other measures. When designing solutions, we need to consider feasibility, cost, and benefits to ensure the solution can effectively solve the problem.

```bash
# Design optimization solution based on bottleneck
# If the bottleneck is git status being too slow:
git config core.fsmonitor true
git config core.untrackedCache true

# If the bottleneck is network transfer being too slow:
git config --global fetch.parallel 4
git config --global protocol.version 2
git clone --depth=1 --filter=blob:none URL

# If the bottleneck is repository being too large:
git gc --aggressive
git repack -a -d --geometric=2
```

### Result Verification Phase

In the result verification phase, we need to measure the performance data after optimization and compare it with pre-optimization data to verify the optimization results. If the results are not satisfactory, we need to re-analyze the bottleneck and adjust the optimization solution. Through continuous monitoring and adjustment, we can ensure the repository always maintains optimal performance.

```bash
# Verify optimization results
echo "=== Post-optimization Performance Test ==="
echo -n "git status: "
time git status > /dev/null 2>&1

echo -n "git diff: "
time git diff > /dev/null 2>&1

echo -n "git log -100: "
time git log --oneline -100 > /dev/null 2>&1

# Compare pre and post optimization data
echo ""
echo "=== Performance Comparison ==="
echo "Before optimization git status: 2.5 seconds"
echo "After optimization git status: 0.1 seconds"
echo "Improvement: 25x faster"
```

---

## Appendix 2: Diagnostic Workflow for Common Performance Problems

In daily development, we often encounter various Git performance problems. Here are some diagnostic workflows for common problems that can help us quickly locate and resolve issues.

### git status is slow

When `git status` becomes slow, it is usually because file system scanning takes too long. This may be due to too many files in the repository or too many untracked files. By enabling fsmonitor and untracked cache, we can significantly improve `git status` performance.

```bash
# Diagnose slow git status problem
GIT_TRACE=1 git status 2>&1 | grep -E "trace|time"

# Check file count
echo "Tracked files: $(git ls-files | wc -l)"
echo "Untracked files: $(git ls-files --others --exclude-standard | wc -l)"

# Enable optimization
git config core.fsmonitor true
git config core.untrackedCache true

# Verify optimization results
time git status > /dev/null 2>&1
```

### git clone is slow

When `git clone` becomes slow, it is usually because the repository is too large or network transfer is too slow. By using shallow clone, partial clone, and sparse checkout, we can significantly reduce clone time and download size.

```bash
# Diagnose slow git clone problem
GIT_TRACE=1 git clone URL 2>&1 | grep -E "trace|time|transfer"

# Check repository size
git count-objects -v --human-readable

# Use optimized clone
git clone --depth=1 --filter=blob:none --sparse URL
cd repo
git sparse-checkout init --cone
git sparse-checkout set src/ docs/

# Verify optimization results
time git clone --depth=1 --filter=blob:none URL
```

### git push is slow

When `git push` becomes slow, it is usually because there are too many or too large objects to push. By using incremental pushing and optimizing packfiles, we can significantly improve push speed.

```bash
# Diagnose slow git push problem
GIT_TRACE=1 git push origin main 2>&1 | grep -E "trace|time|transfer"

# Check objects to push
git log origin/main..main --oneline

# Use incremental push
git push origin main

# Optimize packfile
git repack -a -d
git gc --auto

# Verify optimization results
time git push origin main
```

### git log is slow

When `git log` becomes slow, it is usually because the commit history is too long or there are too many commits to traverse. By using commit-graph and limiting output count, we can significantly improve log query speed.

```bash
# Diagnose slow git log problem
GIT_TRACE=1 git log --oneline -100 2>&1 | grep -E "trace|time"

# Check commit count
git log --oneline | wc -l

# Enable commit-graph
git config gc.writeCommitGraph true
git commit-graph write --reachable

# Limit output count
git log --oneline -100

# Verify optimization results
time git log --oneline -100 > /dev/null 2>&1
```

---

## Appendix 3: Performance Optimization in Team Collaboration

In team collaboration, Git performance optimization not only affects individual efficiency but also impacts the overall team productivity. Here are some performance optimization strategies for team collaboration.

### Unified Optimization Configuration

Teams should use the same optimization configuration to ensure all members get a consistent performance experience. This can be achieved by providing configuration scripts in the project or using configuration management tools.

```bash
# Create team configuration script
cat > setup-git-performance.sh << 'EOF'
#!/bin/bash
# Team Git performance optimization configuration

echo "Configuring Git performance optimization..."

# Global performance optimization
git config --global core.fsmonitor true
git config --global core.untrackedCache true
git config --global feature.manyFiles true
git config --global protocol.version 2
git config --global fetch.parallel 4
git config --global push.parallel 4

# Repository-level performance optimization
git config core.fsmonitor true
git config core.untrackedCache true
git config gc.writeCommitGraph true

# Optimize packfile
git config pack.window 250
git config pack.depth 50
git config pack.threads 4

echo "Configuration complete"
EOF

chmod +x setup-git-performance.sh

# Add instructions in project README
echo "## Performance Optimization" >> README.md
echo "Run ./setup-git-performance.sh to configure Git performance optimization" >> README.md
```

### Performance Considerations in Code Review

In code review, we should pay attention to issues that may affect Git performance. For example, large files should not be committed directly to the repository but should use Git LFS; frequent small commits can be merged into larger commits to reduce commit history length.

```bash
# Check for large files in pre-commit hook
#!/bin/bash
# Check if large files are being committed
STAGED_FILES=$(git diff --cached --name-only)
for file in $STAGED_FILES; do
    size=$(git cat-file -s ":$file" 2>/dev/null || echo 0)
    if [ "$size" -gt 10485760 ]; then  # 10MB
        echo "Warning: File $file exceeds 10MB"
        echo "Consider using Git LFS for large files"
        exit 1
    fi
done

# Check if binary files are being committed
for file in $STAGED_FILES; do
    if file "$file" | grep -q "binary"; then
        echo "Warning: Binary file $file is being committed"
        echo "Consider using Git LFS for binary files"
    fi
done

exit 0
```

### Shared Performance Monitoring

Teams should establish a shared performance monitoring system to promptly discover and resolve performance issues. This can be achieved by periodically running performance test scripts and uploading results to a shared platform.

```bash
#!/bin/bash
# Team performance monitoring script

REPO_NAME=$(basename $(pwd))
LOG_FILE="/var/log/git-performance/${REPO_NAME}.log"

# Ensure log directory exists
mkdir -p $(dirname "$LOG_FILE")

# Record performance data
{
    echo "=== Performance Monitoring Report ==="
    echo "Repository: $(pwd)"
    echo "Time: $(date)"
    echo ""

    echo "--- Repository Information ---"
    git count-objects -v --human-readable
    echo ""

    echo "--- Operation Duration ---"
    echo -n "git status: "
    time git status > /dev/null 2>&1

    echo -n "git diff: "
    time git diff > /dev/null 2>&1

    echo -n "git log -100: "
    time git log --oneline -100 > /dev/null 2>&1

    echo ""
    echo "========================"
} >> "$LOG_FILE" 2>&1

echo "Performance data recorded to $LOG_FILE"
```

---

## Appendix 4: Continuous Improvement of Performance Optimization

Performance optimization is not a one-time task, but an ongoing process. We need to establish a continuous improvement mechanism to ensure the repository always maintains optimal performance.

### Regular Performance Assessment

Teams should conduct regular performance assessments to understand the repository's performance status and optimization results. This can be achieved by running performance test scripts monthly.

```bash
#!/bin/bash
# Monthly performance assessment script

echo "=== Monthly Performance Assessment ==="
echo "Repository: $(pwd)"
echo "Date: $(date)"
echo ""

# Run performance test
./git-benchmark.sh

# Generate performance report
echo ""
echo "=== Performance Trend Analysis ==="
if [ -f /var/log/git-performance/$(basename $(pwd)).log ]; then
    echo "Historical data available"
    tail -100 /var/log/git-performance/$(basename $(pwd)).log | \
        grep "git status" | \
        awk '{print $3}' | \
        sort -n | \
        head -1
else
    echo "No historical data available yet"
fi
```

### Documentation of Performance Optimization

Teams should document performance optimization experiences and best practices so new members can quickly understand and apply them. This can be achieved by maintaining a performance optimization guide in the project.

```bash
# Create performance optimization guide
cat > PERFORMANCE.md << 'EOF'
# Git Performance Optimization Guide

## Quick Start

Run the following commands to configure performance optimization:

```bash
./setup-git-performance.sh
```

## Common Problems

### git status is slow

Enable fsmonitor and untracked cache:

```bash
git config core.fsmonitor true
git config core.untrackedCache true
```

### git clone is slow

Use shallow clone and partial clone:

```bash
git clone --depth=1 --filter=blob:none URL
```

## Best Practices

1. Use Git LFS for large files
2. Run git gc and git repack regularly
3. Use protocol v2 for network transfers
4. Enable commit-graph to speed up log queries

## Monitoring

Run the performance monitoring script:

```bash
./git-performance-monitor.sh
```
EOF
```

### Automation of Performance Optimization

Teams should automate the performance optimization process to reduce manual intervention and improve efficiency. This can be achieved by using CI/CD tools and automation scripts.

```yaml
# GitHub Actions automated performance optimization
name: Git Performance Optimization

on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM

jobs:
  optimize:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run GC
        run: git gc --aggressive

      - name: Run Repack
        run: git repack -a -d --geometric=2

      - name: Write Commit Graph
        run: git commit-graph write --reachable

      - name: Run Performance Test
        run: ./git-benchmark.sh

      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: performance-report.txt
```

---

## Appendix 5: Performance Optimization Toolchain

When performing Git performance optimization, we need to use various tools to collect data, analyze problems, and verify results. Here are some commonly used performance optimization tools.

### Git Built-in Tools

Git provides several built-in tools to help us with performance optimization. These tools include `git count-objects`, `git verify-pack`, `git fsck`, etc.

```bash
# Use git count-objects to analyze repository size
git count-objects -v --human-readable

# Use git verify-pack to analyze packfile
git verify-pack -v .git/objects/pack/pack-*.idx

# Use git fsck to check repository integrity
git fsck --full --strict

# Use git reflog to analyze reference history
git reflog show --all
```

### System Performance Tools

In addition to Git built-in tools, we can also use system performance tools to analyze Git's performance. These tools include `time`, `strace`, `perf`, etc.

```bash
# Use time to measure command duration
time git status

# Use strace to trace system calls
strace -c git status

# Use perf for performance analysis
perf record -g git status
perf report

# Use flame graph for analysis
perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > git-status.svg
```

### Third-party Tools

In addition to the above tools, there are some third-party tools that can help us with Git performance optimization. These tools include `git-lfs`, `git-filter-repo`, `git-stats`, etc.

```bash
# Use git-lfs for large file management
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"

# Use git-filter-repo to clean history
pip install git-filter-repo
git filter-repo --path-glob '*.env' --invert-paths

# Use git-stats to generate statistics reports
pip install git-stats
git-stats --since="2024-01-01" --until="2024-12-31"
```

### Custom Tools

In addition to using existing tools, we can also create custom tools to meet specific needs. These tools can encapsulate common operations and improve work efficiency.

```bash
#!/bin/bash
# Custom Git performance tool

case "$1" in
    "analyze")
        echo "Analyzing repository performance..."
        git count-objects -v --human-readable
        echo ""
        echo "File statistics:"
        echo "  Tracked: $(git ls-files | wc -l)"
        echo "  Untracked: $(git ls-files --others --exclude-standard | wc -l)"
        echo ""
        echo "Commit statistics:"
        echo "  Total commits: $(git log --oneline | wc -l)"
        echo "  Merge commits: $(git log --merges --oneline | wc -l)"
        ;;
    "optimize")
        echo "Optimizing repository performance..."
        git gc --auto
        git repack -a -d
        git commit-graph write --reachable
        echo "Optimization complete"
        ;;
    "benchmark")
        echo "Running performance benchmark..."
        time git status > /dev/null 2>&1
        time git diff > /dev/null 2>&1
        time git log --oneline -100 > /dev/null 2>&1
        ;;
    *)
        echo "Usage: $0 {analyze|optimize|benchmark}"
        exit 1
        ;;
esac
```

---

## Appendix 6: Performance Optimization Monitoring and Alerting

To promptly discover and resolve performance issues, we need to establish a monitoring and alerting system. This system can periodically check repository performance metrics and send alert notifications when thresholds are exceeded.

### Monitoring Metrics

We need to monitor the following key metrics:

- Repository size: including object count, packfile size, etc.
- Operation duration: including git status, git diff, git log, and other common operations
- Network transfer: including clone, push, pull transfer time and data volume
- Error rate: including operation failure count and reasons

```bash
#!/bin/bash
# Performance monitoring script

REPO_NAME=$(basename $(pwd))
METRICS_FILE="/var/log/git-metrics/${REPO_NAME}.json"

# Ensure directory exists
mkdir -p $(dirname "$METRICS_FILE")

# Collect metrics
{
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"repo\": \"$(pwd)\","
    echo "  \"size\": {"
    echo "    \"objects\": $(git count-objects -v | grep count | awk '{print $2}'),"
    echo "    \"pack_size\": \"$(git count-objects -v | grep 'size-pack' | awk '{print $2}')\","
    echo "    \"files\": $(git ls-files | wc -l)"
    echo "  },"
    echo "  \"commits\": {"
    echo "    \"total\": $(git log --oneline | wc -l),"
    echo "    \"merges\": $(git log --merges --oneline | wc -l)"
    echo "  },"
    echo "  \"branches\": {"
    echo "    \"local\": $(git branch | wc -l),"
    echo "    \"remote\": $(git branch -r | wc -l)"
    echo "  }"
    echo "}"
} > "$METRICS_FILE"

echo "Metrics recorded to $METRICS_FILE"
```

### Alert Rules

We need to define reasonable alert rules to promptly notify relevant personnel when performance issues occur. Here are some common alert rules:

- Repository size exceeds threshold
- Operation duration exceeds threshold
- Network transfer failure rate exceeds threshold
- Objects corrupted or missing

```bash
#!/bin/bash
# Alert check script

REPO_NAME=$(basename $(pwd))
ALERT_THRESHOLD_STATUS=5  # git status duration threshold (seconds)
ALERT_THRESHOLD_SIZE=1073741824  # Repository size threshold (1GB)

# Check git status duration
STATUS_TIME=$(TIMEFORMAT='%R'; time git status > /dev/null 2>&1)
if (( $(echo "$STATUS_TIME > $ALERT_THRESHOLD_STATUS" | bc -l) )); then
    echo "Alert: git status took ${STATUS_TIME} seconds, exceeding threshold of ${ALERT_THRESHOLD_STATUS} seconds"
    # Send alert notification
    # curl -X POST "https://hooks.slack.com/..." -d "{\"text\": \"Git performance alert: git status took ${STATUS_TIME} seconds\"}"
fi

# Check repository size
REPO_SIZE=$(git count-objects -v | grep 'size-pack' | awk '{print $2}')
if [ "$REPO_SIZE" -gt "$ALERT_THRESHOLD_SIZE" ]; then
    echo "Alert: Repository size is ${REPO_SIZE} bytes, exceeding threshold of ${ALERT_THRESHOLD_SIZE} bytes"
    # Send alert notification
fi
```

### Alert Notifications

When alerts are triggered, we need to promptly notify relevant personnel. This can be achieved through various methods, including email, instant messaging tools, SMS, etc.

```bash
#!/bin/bash
# Alert notification script

ALERT_TYPE=$1
ALERT_MESSAGE=$2

case "$ALERT_TYPE" in
    "email")
        echo "$ALERT_MESSAGE" | mail -s "Git Performance Alert" team@example.com
        ;;
    "slack")
        curl -X POST \
            -H 'Content-type: application/json' \
            --data "{\"text\": \"$ALERT_MESSAGE\"}" \
            https://hooks.slack.com/services/xxx/yyy/zzz
        ;;
    "dingtalk")
        curl -X POST \
            -H 'Content-Type: application/json' \
            -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"$ALERT_MESSAGE\"}}" \
            https://oapi.dingtalk.com/robot/send?access_token=xxx
        ;;
    *)
        echo "Unknown alert type: $ALERT_TYPE"
        exit 1
        ;;
esac
```

---

## Appendix 7: Performance Optimization Case Studies

By analyzing real-world performance optimization cases, we can better understand optimization methods and techniques. Here are some typical performance optimization cases.

### Case 1: Large Monorepo Performance Optimization

A company's Monorepo contained 500,000 files and 1 million commits, and git status took 30 seconds to complete. By enabling fsmonitor and untracked cache, and using sparse checkout, git status duration was reduced to 1 second.

```bash
# Before optimization
time git status  # 30 seconds

# Enable fsmonitor
git config core.fsmonitor true

# Enable untracked cache
git config core.untrackedCache true

# Use sparse checkout
git sparse-checkout init --cone
git sparse-checkout set src/team-a/

# After optimization
time git status  # 1 second

# Performance improvement: 30x
```

### Case 2: CI/CD Clone Optimization

A team's CI/CD pipeline needed to clone a 2GB repository, taking 10 minutes each time. By using shallow clone and partial clone, clone time was reduced to 30 seconds.

```bash
# Before optimization
time git clone URL  # 10 minutes

# Use shallow clone
time git clone --depth=1 URL  # 3 minutes

# Use partial clone
time git clone --depth=1 --filter=blob:none URL  # 1 minute

# Use sparse checkout
time git clone --depth=1 --filter=blob:none --sparse URL  # 30 seconds

# Performance improvement: 20x
```

### Case 3: Large File Storage Optimization

A game development team's repository contained extensive textures and model files, causing the repository size to exceed 10GB. By using Git LFS, the repository size was reduced to 500MB, and clone time went from 1 hour to 5 minutes.

```bash
# Before optimization
git count-objects -v --human-readable
# size-pack: 10GB

# Install Git LFS
git lfs install

# Migrate large files to LFS
git lfs migrate import --include="*.psd,*.fbx,*.png" --everything

# After optimization
git count-objects -v --human-readable
# size-pack: 500MB

# Performance improvement: 20x
```

### Case 4: Network Transfer Optimization

A multinational team worked in an environment with poor network conditions, and git push and git pull frequently timed out. By configuring proxy and optimizing compression parameters, network transfer stability was significantly improved.

```bash
# Configure HTTP proxy
git config --global http.proxy http://proxy.example.com:8080

# Configure compression level
git config --global core.compression 1

# Configure buffer size
git config --global http.postBuffer 524288000

# Configure timeout
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 60

# Verify optimization results
time git push origin main
time git pull origin main
```

---

## Appendix 8: Automated Performance Testing

To ensure performance optimization effectiveness, we need to establish an automated performance testing system. This system can periodically run performance tests and generate test reports.

### Performance Test Script

```bash
#!/bin/bash
# Git performance automated test script

TEST_DIR="/tmp/git-perf-test-$(date +%Y%m%d_%H%M%S)"
REPORT_FILE="$TEST_DIR/report.txt"

mkdir -p "$TEST_DIR"

echo "=== Git Performance Automated Test ===" > "$REPORT_FILE"
echo "Test time: $(date)" >> "$REPORT_FILE"
echo "Repository: $(pwd)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Test git status
echo "Testing git status..." >> "$REPORT_FILE"
for i in {1..5}; do
    TIME=$(TIMEFORMAT='%R'; time git status > /dev/null 2>&1)
    echo "  Run $i: ${TIME} seconds" >> "$REPORT_FILE"
done

# Test git diff
echo "Testing git diff..." >> "$REPORT_FILE"
for i in {1..5}; do
    TIME=$(TIMEFORMAT='%R'; time git diff > /dev/null 2>&1)
    echo "  Run $i: ${TIME} seconds" >> "$REPORT_FILE"
done

# Test git log
echo "Testing git log -100..." >> "$REPORT_FILE"
for i in {1..5}; do
    TIME=$(TIMEFORMAT='%R'; time git log --oneline -100 > /dev/null 2>&1)
    echo "  Run $i: ${TIME} seconds" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo "Test complete" >> "$REPORT_FILE"

echo "Test report generated: $REPORT_FILE"
cat "$REPORT_FILE"
```

### Performance Regression Test

```bash
#!/bin/bash
# Git performance regression test script

# Define performance baselines
BASELINE_STATUS=1.0  # git status baseline duration (seconds)
BASELINE_DIFF=0.5    # git diff baseline duration (seconds)
BASELINE_LOG=0.3     # git log baseline duration (seconds)

# Run tests
STATUS_TIME=$(TIMEFORMAT='%R'; time git status > /dev/null 2>&1)
DIFF_TIME=$(TIMEFORMAT='%R'; time git diff > /dev/null 2>&1)
LOG_TIME=$(TIMEFORMAT='%R'; time git log --oneline -100 > /dev/null 2>&1)

# Check if baselines are exceeded
FAILED=0

if (( $(echo "$STATUS_TIME > $BASELINE_STATUS * 2" | bc -l) )); then
    echo "Failed: git status took ${STATUS_TIME} seconds, exceeding 2x baseline of $BASELINE_STATUS seconds"
    FAILED=1
fi

if (( $(echo "$DIFF_TIME > $BASELINE_DIFF * 2" | bc -l) )); then
    echo "Failed: git diff took ${DIFF_TIME} seconds, exceeding 2x baseline of $BASELINE_DIFF seconds"
    FAILED=1
fi

if (( $(echo "$LOG_TIME > $BASELINE_LOG * 2" | bc -l) )); then
    echo "Failed: git log took ${LOG_TIME} seconds, exceeding 2x baseline of $BASELINE_LOG seconds"
    FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
    echo "Passed: All tests within baseline range"
    exit 0
else
    echo "Failed: Performance regression detected"
    exit 1
fi
```

---

## Appendix 9: Performance Optimization Best Practices Summary

Based on the previous discussions, we can summarize the following performance optimization best practices.

### Clone Optimization Best Practices

When cloning large repositories, we should choose the appropriate clone strategy based on actual needs. If only the latest code is needed, use shallow clone; if only specific directories are needed, use sparse checkout; if the repository contains large files, use partial clone.

```bash
# Best practice: Combine multiple optimization strategies
git clone \
    --depth=1 \
    --filter=blob:none \
    --sparse \
    --branch=main \
    https://github.com/user/repo.git

cd repo

git sparse-checkout init --cone
git sparse-checkout set src/ docs/ tests/
```

### Daily Operation Optimization Best Practices

In daily development, we should enable various caching and optimization options to improve common operation performance. This includes enabling fsmonitor, untracked cache, and commit-graph.

```bash
# Best practice: Enable all performance optimization options
git config core.fsmonitor true
git config core.untrackedCache true
git config feature.manyFiles true
git config gc.writeCommitGraph true
git config diff.algorithm histogram
git config protocol.version 2
git config fetch.parallel 4
git config push.parallel 4
```

### Repository Maintenance Best Practices

To maintain optimal repository performance, we should perform regular repository maintenance. This includes running gc, repack, and prune, as well as cleaning up unreachable objects.

```bash
# Best practice: Regular repository maintenance
git gc --auto
git repack -a -d --geometric=2
git commit-graph write --reachable
git prune --expire=30.days.ago
```

### Team Collaboration Best Practices

In team collaboration, we should use the same optimization configuration and establish a shared performance monitoring system. This ensures all members get a consistent performance experience and can promptly discover and resolve performance issues.

```bash
# Best practice: Unified team configuration
# Provide configuration scripts in the project
./setup-git-performance.sh

# Run performance tests periodically in CI/CD
# Configure performance monitoring in GitHub Actions
```

### Large Repository Management Best Practices

For large repositories, we should use sparse checkout, partial clone, Git LFS, and other techniques to manage repository scale. This can significantly reduce clone time and working tree size.

```bash
# Best practice: Large repository management strategies
# Use sparse checkout
git sparse-checkout init --cone
git sparse-checkout set src/ docs/

# Use partial clone
git clone --filter=blob:none URL

# Use Git LFS
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
```

---

## Appendix 10: Performance Optimization Quick Reference

```bash
# ===== Quick Optimization Configuration =====

# 1. Global performance optimization
git config --global core.fsmonitor true
git config --global core.untrackedCache true
git config --global feature.manyFiles true
git config --global protocol.version 2
git config --global fetch.parallel 4
git config --global push.parallel 4

# 2. Clone optimization
git clone --depth=1 --filter=blob:none --sparse URL

# 3. Status optimization
git config core.fsmonitor true
git config core.untrackedCache true

# 4. Diff optimization
git config diff.algorithm histogram

# 5. GC optimization
git config gc.auto 6700
git config gc.autoPackLimit 50
git config gc.writeCommitGraph true

# 6. LFS optimization
git config lfs.concurrenttransfers 8
git config lfs.storage ~/.git-lfs-cache

# 7. Network optimization
git config --global http.postBuffer 524288000
git config --global fetch.parallel 4

# 8. Monitoring and diagnostics
GIT_TRACE=1 git status
git count-objects -v --human-readable
git fsck --no-reflogs
```

---

> **Previous Chapter**: [Git Internals Deep Dive](./X11-git-internals-deep-dive.md)

```bash
# ===== Quick Optimization Configuration =====

# 1. Global performance optimization
git config --global core.fsmonitor true
git config --global core.untrackedCache true
git config --global feature.manyFiles true
git config --global protocol.version 2
git config --global fetch.parallel 4
git config --global push.parallel 4

# 2. Clone optimization
git clone --depth=1 --filter=blob:none --sparse URL

# 3. Status optimization
git config core.fsmonitor true
git config core.untrackedCache true

# 4. Diff optimization
git config diff.algorithm histogram

# 5. GC optimization
git config gc.auto 6700
git config gc.autoPackLimit 50
git config gc.writeCommitGraph true

# 6. LFS optimization
git config lfs.concurrenttransfers 8
git config lfs.storage ~/.git-lfs-cache

# 7. Network optimization
git config --global http.postBuffer 524288000
git config --global fetch.parallel 4

# 8. Monitoring and diagnostics
GIT_TRACE=1 git status
git count-objects -v --human-readable
git fsck --no-reflogs
```

---

> **Previous Chapter**: [Git Internals Deep Dive](./X11-git-internals-deep-dive.md)

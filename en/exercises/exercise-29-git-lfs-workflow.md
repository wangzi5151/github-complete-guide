# Exercise 29: Git LFS Large File Management in Practice

## Learning Objectives

After completing this exercise, you will be able to:

- Understand how Git LFS (Large File Storage) works
- Configure Git LFS to track large files
- Migrate an existing repository to Git LFS
- Properly use Git LFS in CI/CD workflows
- Manage LFS storage quotas and optimize storage usage

## Prerequisites

- Git 2.15+ installed
- Git LFS client installed
- A GitHub repository
- Basic understanding of Git operations

## Background Knowledge

### What is Git LFS

Git LFS (Large File Storage) is an extension for Git that manages large files. It works in the following way:

1. **Pointer files**: Stores small pointer files in the Git repository
2. **External storage**: The actual large files are stored on the LFS server
3. **On-demand download**: Large files are only downloaded when needed

### Why Use Git LFS

- **Repository size**: Prevents the repository from becoming too large
- **Clone speed**: Speeds up cloning and pulling
- **Version control**: Enables version control for large files
- **Collaboration efficiency**: Reduces network transfer volume

### Git LFS Limits

- GitHub free account: 1GB storage + 1GB bandwidth per month
- GitHub Pro: 2GB storage + 2GB bandwidth per month
- GitHub Team: 4GB storage + 4GB bandwidth per month
- File size limit: Maximum 2GB per file

---

## Exercise Steps

### Part 1: Installing and Configuring Git LFS

#### Step 1: Install Git LFS

**macOS:**

```bash
# Using Homebrew
brew install git-lfs

# Or using MacPorts
port install git-lfs
```

**Linux (Ubuntu/Debian):**

```bash
# Using package manager
sudo apt-get install git-lfs

# Or download from GitHub
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
```

**Windows:**

```bash
# Using Chocolatey
choco install git-lfs

# Or using Scoop
scoop install git-lfs

# Or download installer from the official website
# https://git-lfs.github.com/
```

**Verify installation:**

```bash
git lfs version
# Example output: git-lfs/3.4.0 (GitHub; linux amd64; go 1.21.5)
```

#### Step 2: Initialize Git LFS

```bash
# Initialize LFS in the repository
git lfs install

# Verify initialization
git lfs env
```

Expected output:

```
git-lfs/3.4.0 (GitHub; linux amd64; go 1.21.5)
git version 2.43.0

LocalWorkingDir=/home/user/my-repo
LocalGitDir=/home/user/my-repo/.git
LocalGitStorageDir=/home/user/my-repo/.git
LocalMediaDir=/home/user/my-repo/.git/lfs/objects
LocalReferenceDirs=
TempDir=/home/user/my-repo/.git/lfs/tmp
ConcurrentTransfers=8
TusTransfers=false
BasicTransfers=true
SkipFetchError=false
FetchRecentAlways=false
FetchRecentRefsDays=7
FetchRecentCommitsDays=0
FetchRecentIncludeRemotes=1
PruneOffsetDays=3
PruneVerifyRemotesAlways=false
PruneRemoteName=origin
LfsStorageDir=/home/user/my-repo/.git/lfs
AccessDownload=none
AccessUpload=none
DownloadTransfers=basic
UploadTransfers=basic
GIT_EXEC_PATH=/usr/lib/git-core
GIT_LFS_PATH=/usr/bin/git-lfs
```

#### Step 3: Configure LFS Tracking Rules

```bash
# Track specific file types
git lfs track "*.psd"
git lfs track "*.zip"
git lfs track "*.tar.gz"
git lfs track "*.mp4"
git lfs track "*.mov"
git lfs track "*.avi"
git lfs track "*.png"
git lfs track "*.jpg"
git lfs track "*.jpeg"
git lfs track "*.gif"
git lfs track "*.bmp"
git lfs track "*.tiff"
git lfs track "*.webp"
git lfs track "*.mp3"
git lfs track "*.wav"
git lfs track "*.flac"
git lfs track "*.ogg"
git lfs track "*.unitypackage"
git lfs track "*.fbx"
git lfs track "*.obj"
git lfs track "*.blend"
git lfs track "*.max"
git lfs track "*.ma"
git lfs track "*.mb"

# Track files in specific directories
git lfs track "assets/**"
git lfs track "media/**"
git lfs track "resources/**"

# Track files of a specific size (requires pre-commit hook configuration)
git lfs track "*.bin"
```

#### Step 4: View and Manage Tracking Rules

```bash
# View current tracking rules
git lfs track

# Example output:
# Listing tracked patterns
#     *.psd (.gitattributes)
#     *.zip (.gitattributes)
#     *.mp4 (.gitattributes)
#     *.png (.gitattributes)
#     *.jpg (.gitattributes)

# View LFS tracked files
git lfs ls-files

# Example output:
# 2a83d6f5e4 * assets/images/logo.png
# 8b7c6d5e4a * assets/videos/intro.mp4
# 5c4b3a2d1e * assets/models/character.fbx

# View LFS status
git lfs status

# View LFS file sizes
git lfs ls-files --size
```

### Part 2: Using Git LFS to Manage Large Files

#### Step 5: Create a Test Repository

```bash
# Create a new repository
mkdir lfs-demo && cd lfs-demo
git init

# Initialize LFS
git lfs install

# Configure tracking rules
git lfs track "*.bin"
git lfs track "*.dat"
git lfs track "*.large"

# Create .gitattributes file
cat > .gitattributes << 'EOF'
# Git LFS tracking rules
*.bin filter=lfs diff=lfs merge=lfs -text
*.dat filter=lfs diff=lfs merge=lfs -text
*.large filter=lfs diff=lfs merge=lfs -text
*.psd filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
EOF

# Commit .gitattributes
git add .gitattributes
git commit -m "Initialize Git LFS configuration"
```

#### Step 6: Add Large Files

```bash
# Create test large files
dd if=/dev/urandom of=test-file-1.bin bs=1M count=10
dd if=/dev/urandom of=test-file-2.bin bs=1M count=20
dd if=/dev/urandom of=test-data.dat bs=1M count=15

# Create a normal text file
echo "This is a normal text file" > readme.txt

# Check file status
git status

# Add files
git add .

# Check LFS status
git lfs status

# Expected output:
# On branch main
#
# Git LFS objects to be pushed to origin/main:
#
#     test-file-1.bin (10 MB)
#     test-file-2.bin (20 MB)
#     test-data.dat (15 MB)

# Commit
git commit -m "Add large files for testing"
```

#### Step 7: View LFS Pointer Files

```bash
# View LFS pointer file content
cat test-file-1.bin

# Expected output:
# version https://git-lfs.github.com/spec/v1
# oid sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
# size 10485760

# View Git object type
git cat-file -t HEAD:test-file-1.bin
# Output: blob

# View Git object size
git cat-file -s HEAD:test-file-1.bin
# Output: 133 (size of the pointer file)

# Compare with normal files
git cat-file -s HEAD:readme.txt
# Output: actual file size
```

#### Step 8: Push to Remote Repository

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/lfs-demo.git

# Push (LFS files will be uploaded automatically)
git push -u origin main

# Expected output:
# Uploading LFS objects: 100% (3/3), 45 MB | 0 B/s
# Enumerating objects: 6
# Counting objects: 100% (6/6)
# Delta compression using up to 8 threads
# Compressing objects: 100% (4/4)
# Writing objects: 100% (5/5)
# Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
# To https://github.com/yourusername/lfs-demo.git
#  * [new branch]      main -> main
```

### Part 3: Migrating an Existing Repository to Git LFS

#### Step 9: Install the git-lfs-migrate Tool

```bash
# Install using Homebrew (macOS)
brew install git-lfs-migrate

# Or download from GitHub
# https://github.com/git-lfs/git-lfs/releases

# Verify installation
git lfs migrate --version
```

#### Step 10: Migrate the Existing Repository

```bash
# Enter the existing repository
cd existing-repo

# Initialize LFS
git lfs install

# View which files are suitable for LFS migration
git lfs migrate info --include="*.psd,*.zip,*.mp4,*.png,*.jpg"

# Expected output:
# migrate: Fetching remote refs: ..., done
# migrate: Sorting commits: ..., done
#
# *.psd   2 MB   2/2 files(s)   100%
# *.zip   50 MB  5/5 files(s)   100%
# *.mp4   200 MB 3/3 files(s)   100%
# *.png   10 MB  50/50 files(s) 100%
# *.jpg   5 MB   30/30 files(s) 100%

# Execute migration (without rewriting history, only migrate future commits)
git lfs migrate import --include="*.psd,*.zip,*.mp4,*.png,*.jpg"

# If you need to rewrite history (use with caution!)
# git lfs migrate import --include="*.psd,*.zip,*.mp4,*.png,*.jpg" --everything

# Commit the migration results
git add .gitattributes
git commit -m "Migrate to Git LFS"

# Force push (if history was rewritten)
# git push --force origin main
```

#### Step 11: Post-Migration Verification

```bash
# Verify LFS files
git lfs ls-files

# Check repository size
git count-objects -vH

# Expected output (should be much smaller than before migration):
# count: 50
# size: 2.50 MiB
# in-pack: 100
# packs: 1
# size-pack: 3.00 MiB
# prunepackable: 0
# garbage: 0
# size-garbage: 0 bytes

# Verify file integrity
git lfs fsck
```

### Part 4: Using Git LFS in CI/CD

#### Step 12: GitHub Actions Configuration

Create the file `.github/workflows/lfs-build.yml`:

```yaml
name: Build with LFS

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code (with LFS)
        uses: actions/checkout@v4
        with:
          lfs: true
      
      - name: Verify LFS files
        run: |
          echo "Checking LFS files..."
          git lfs ls-files
          
          echo "Verifying LFS file integrity..."
          git lfs fsck
      
      - name: Build project
        run: |
          echo "Building with LFS files..."
          # Add actual build commands here
          ls -la assets/
      
      - name: Run tests
        run: |
          echo "Running tests..."
          # Run tests using LFS files
```

#### Step 13: Advanced CI/CD Configuration

Create the file `.github/workflows/lfs-pipeline.yml`:

```yaml
name: LFS Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  GIT_LFS_SKIP_SMUDGE: 0  # Ensure LFS files are downloaded

jobs:
  # Test job
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          lfs: true
      
      - name: Cache LFS files
        uses: actions/cache@v4
        with:
          path: .git/lfs
          key: ${{ runner.os }}-lfs-${{ hashFiles('.lfs-assets-id') }}
          restore-keys: |
            ${{ runner.os }}-lfs-
      
      - name: Pull LFS files
        run: git lfs pull
      
      - name: Verify LFS files
        run: |
          git lfs ls-files --size
          git lfs fsck
      
      - name: Run tests
        run: |
          # Run tests using LFS files
          echo "Running tests..."
  
  # Build job
  build:
    needs: test
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          lfs: true
      
      - name: Build project
        run: |
          echo "Building on ${{ matrix.os }}..."
          # Build logic
  
  # Deploy job
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          lfs: true
      
      - name: Deploy to server
        run: |
          echo "Deploying project with LFS files..."
          # Deploy logic
```

#### Step 14: Create an LFS Cache Script

Create the file `.github/scripts/cache-lfs.sh`:

```bash
#!/bin/bash

# Git LFS cache management script

set -e

CACHE_DIR="${HOME}/.git-lfs-cache"
REPO_URL=$(git remote get-url origin)
REPO_HASH=$(echo -n "$REPO_URL" | sha256sum | cut -d' ' -f1)
CACHE_PATH="${CACHE_DIR}/${REPO_HASH}"

# Create cache directory
mkdir -p "$CACHE_PATH"

# Set LFS cache path
export GIT_LFS_CACHE_PATH="$CACHE_PATH"

# Check if cache exists
if [ -d "$CACHE_PATH" ] && [ "$(ls -A $CACHE_PATH)" ]; then
    echo "Using existing LFS cache: $CACHE_PATH"
    
    # Copy LFS files from cache
    if [ -d ".git/lfs" ]; then
        cp -r "$CACHE_PATH/objects" ".git/lfs/" 2>/dev/null || true
    fi
else
    echo "Creating new LFS cache"
fi

# Pull LFS files
git lfs pull

# Update cache
if [ -d ".git/lfs/objects" ]; then
    echo "Updating LFS cache..."
    rsync -a ".git/lfs/objects/" "$CACHE_PATH/objects/"
fi

echo "LFS cache path: $CACHE_PATH"
echo "Cache size: $(du -sh $CACHE_PATH | cut -f1)"
```

### Part 5: LFS Storage Optimization

#### Step 15: Clean Up LFS Cache

```bash
# View LFS storage usage
git lfs ls-files --size | awk '{sum += $2} END {print "Total size:", sum/1024/1024, "MB"}'

# Clean up local LFS cache
git lfs prune

# Expected output:
# prune: 5 local objects removed, 3 retained

# View status after cleanup
git lfs status

# Force cleanup (including recently used files)
# git lfs prune --force

# Clean up files older than a specific time
git lfs prune --dry-run  # Preview what will be deleted
git lfs prune --recent 7d  # Keep files from the last 7 days
```

#### Step 16: Configure LFS Storage Strategy

Create the file `.lfsconfig`:

```ini
[lfs]
    # Storage path
    storage = /path/to/lfs/storage
    
    # Number of concurrent transfers
    concurrenttransfers = 8
    
    # Whether to skip smudge (for CI/CD)
    # skip_smudge = true
    
    # Batch processing size
    batchsize = 100

[lfs "fetch"]
    # Fetch recent references
    recentrefs = 7d
    
    # Fetch recent commits
    recentcommits = 0
    
    # Include remote references
    includeremotes = origin

[lfs "prune"]
    # Retention offset days
    offsetdays = 3
    
    # Verify remotes
    verifyremotesalways = false
    
    # Remote name
    remotename = origin
```

#### Step 17: Create an LFS Management Script

Create the file `scripts/lfs-manager.sh`:

```bash
#!/bin/bash

# Git LFS management script

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function: Show help
show_help() {
    echo "Git LFS Management Tool"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  status    - Show LFS status"
    echo "  info      - Show LFS file information"
    echo "  cleanup   - Clean LFS cache"
    echo "  migrate   - Migrate files to LFS"
    echo "  verify    - Verify LFS file integrity"
    echo "  help      - Show this help message"
}

# Function: Show status
show_status() {
    echo -e "${GREEN}=== Git LFS Status ===${NC}"
    echo ""
    
    echo "LFS version:"
    git lfs version
    echo ""
    
    echo "Tracked file types:"
    git lfs track
    echo ""
    
    echo "LFS file list:"
    git lfs ls-files --size
    echo ""
    
    echo "Storage usage:"
    if [ -d ".git/lfs" ]; then
        du -sh .git/lfs
    else
        echo "LFS storage not found"
    fi
}

# Function: Show file information
show_info() {
    echo -e "${GREEN}=== LFS File Information ===${NC}"
    echo ""
    
    echo "File type statistics:"
    git lfs ls-files | awk -F'.' '{print $NF}' | sort | uniq -c | sort -rn
    echo ""
    
    echo "Sorted by size (top 10):"
    git lfs ls-files --size | sort -k2 -rn | head -10
    echo ""
    
    echo "Total files: $(git lfs ls-files | wc -l)"
    echo "Total size: $(git lfs ls-files --size | awk '{sum += $2} END {printf "%.2f MB", sum/1024/1024}')"
}

# Function: Clean up cache
cleanup() {
    echo -e "${YELLOW}=== Cleaning LFS Cache ===${NC}"
    echo ""
    
    echo "Before cleanup:"
    du -sh .git/lfs 2>/dev/null || echo "LFS storage not found"
    echo ""
    
    echo "Running cleanup..."
    git lfs prune
    echo ""
    
    echo "After cleanup:"
    du -sh .git/lfs 2>/dev/null || echo "LFS storage not found"
}

# Function: Migrate files
migrate_files() {
    echo -e "${YELLOW}=== Migrating Files to LFS ===${NC}"
    echo ""
    
    read -p "Enter file extensions to migrate (comma-separated, e.g., *.psd,*.zip): " extensions
    
    if [ -z "$extensions" ]; then
        echo -e "${RED}No extensions specified${NC}"
        return 1
    fi
    
    echo "Will migrate the following file types: $extensions"
    echo ""
    
    read -p "Confirm migration? (y/N) " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        git lfs migrate import --include="$extensions"
        echo -e "${GREEN}Migration complete${NC}"
    else
        echo "Migration cancelled"
    fi
}

# Function: Verify files
verify_files() {
    echo -e "${GREEN}=== Verifying LFS File Integrity ===${NC}"
    echo ""
    
    git lfs fsck
    echo ""
    
    echo -e "${GREEN}Verification complete${NC}"
}

# Main logic
case "${1:-help}" in
    status)
        show_status
        ;;
    info)
        show_info
        ;;
    cleanup)
        cleanup
        ;;
    migrate)
        migrate_files
        ;;
    verify)
        verify_files
        ;;
    help|*)
        show_help
        ;;
esac
```

```bash
# Make the script executable
chmod +x scripts/lfs-manager.sh

# Use the script
./scripts/lfs-manager.sh status
./scripts/lfs-manager.sh info
./scripts/lfs-manager.sh cleanup
./scripts/lfs-manager.sh verify
```

---

## Verify Exercise Results

### Checklist

After completing the exercise, please verify the following:

- [ ] Git LFS is correctly installed and initialized
- [ ] Tracking rules are configured in `.gitattributes`
- [ ] Large files are correctly added to LFS
- [ ] Push to remote repository is successful
- [ ] CI/CD workflow can correctly handle LFS files
- [ ] LFS cache cleanup works properly

### Verification Commands

```bash
# Check LFS installation
git lfs version

# View tracking rules
git lfs track

# View LFS files
git lfs ls-files

# Verify file integrity
git lfs fsck

# Check repository size
git count-objects -vH

# Test cloning (in a new directory)
cd /tmp
git clone https://github.com/yourusername/lfs-demo.git lfs-test
cd lfs-test
git lfs ls-files
```

---

## Advanced Challenges

### Challenge 1: Create an LFS Storage Monitoring Script

Create a script to monitor LFS storage usage:

```bash
#!/bin/bash

# Monitor LFS storage usage

THRESHOLD_MB=100  # Warning threshold

# Get LFS storage size
get_lfs_size() {
    if [ -d ".git/lfs" ]; then
        du -sm .git/lfs | cut -f1
    else
        echo 0
    fi
}

# Check size
LFS_SIZE=$(get_lfs_size)

if [ "$LFS_SIZE" -gt "$THRESHOLD_MB" ]; then
    echo "Warning: LFS storage is using ${LFS_SIZE}MB, exceeding threshold of ${THRESHOLD_MB}MB"
    
    # Send notification
    # Can integrate with Slack, email, etc.
fi
```

### Challenge 2: Implement LFS File Deduplication

Create a tool to detect and remove duplicate LFS files:

```python
#!/usr/bin/env python3

import hashlib
import os
from collections import defaultdict

def find_duplicate_lfs_files():
    """Find duplicate LFS files"""
    
    lfs_dir = ".git/lfs/objects"
    if not os.path.exists(lfs_dir):
        return {}
    
    # Group files by size
    size_groups = defaultdict(list)
    
    for root, dirs, files in os.walk(lfs_dir):
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            size_groups[size].append(filepath)
    
    # Find potentially duplicate files
    duplicates = {}
    for size, files in size_groups.items():
        if len(files) > 1:
            # Calculate file hashes
            hash_groups = defaultdict(list)
            for filepath in files:
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                hash_groups[file_hash].append(filepath)
            
            # Save duplicate files
            for file_hash, hash_files in hash_groups.items():
                if len(hash_files) > 1:
                    duplicates[file_hash] = {
                        'size': size,
                        'files': hash_files
                    }
    
    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicate_lfs_files()
    
    if duplicates:
        print("Duplicate LFS files found:")
        for file_hash, info in duplicates.items():
            print(f"\nHash: {file_hash}")
            print(f"Size: {info['size']} bytes")
            print("Files:")
            for filepath in info['files']:
                print(f"  - {filepath}")
    else:
        print("No duplicate LFS files found")
```

### Challenge 3: Create an LFS Backup Tool

Create a tool to automatically back up LFS files:

```bash
#!/bin/bash

# LFS backup script

BACKUP_DIR="/path/to/backup"
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="${BACKUP_DIR}/${REPO_NAME}_${TIMESTAMP}"

# Create backup directory
mkdir -p "$BACKUP_PATH"

# Back up LFS files
echo "Backing up LFS files..."
if [ -d ".git/lfs/objects" ]; then
    cp -r ".git/lfs/objects" "$BACKUP_PATH/"
fi

# Back up configuration
cp .gitattributes "$BACKUP_PATH/" 2>/dev/null || true
cp .lfsconfig "$BACKUP_PATH/" 2>/dev/null || true

# Compress backup
echo "Compressing backup..."
tar -czf "${BACKUP_PATH}.tar.gz" -C "$BACKUP_DIR" "$(basename $BACKUP_PATH)"

# Clean up temporary directory
rm -rf "$BACKUP_PATH"

echo "Backup complete: ${BACKUP_PATH}.tar.gz"
echo "Backup size: $(du -sh ${BACKUP_PATH}.tar.gz | cut -f1)"
```

### Challenge 4: Implement LFS File Version Management

Create a tool to manage LFS file versions:

```python
#!/usr/bin/env python3

import subprocess
import json
from datetime import datetime

def get_lfs_file_versions(filepath):
    """Get all versions of an LFS file"""
    
    # Get commit history for the file
    result = subprocess.run(
        ['git', 'log', '--pretty=format:%H|%ai|%s', '--follow', '--', filepath],
        capture_output=True,
        text=True
    )
    
    versions = []
    for line in result.stdout.strip().split('\n'):
        if line:
            commit_hash, date, message = line.split('|', 2)
            versions.append({
                'commit': commit_hash,
                'date': date,
                'message': message
            })
    
    return versions

def get_file_size_at_commit(filepath, commit):
    """Get file size at a specific commit"""
    
    result = subprocess.run(
        ['git', 'cat-file', '-s', f'{commit}:{filepath}'],
        capture_output=True,
        text=True
    )
    
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0

if __name__ == "__main__":
    filepath = input("Enter file path: ")
    versions = get_lfs_file_versions(filepath)
    
    print(f"\nVersion history for {filepath}:")
    print("-" * 60)
    
    for version in versions:
        size = get_file_size_at_commit(filepath, version['commit'])
        print(f"Commit: {version['commit'][:8]}")
        print(f"Date: {version['date']}")
        print(f"Message: {version['message']}")
        print(f"Size: {size / 1024 / 1024:.2f} MB")
        print("-" * 60)
```

---

## Frequently Asked Questions

### Q1: What is the difference between Git LFS and Git submodules?

| Feature | Git LFS | Git Submodules |
|---------|---------|----------------|
| Purpose | Manage large files | Reference other repositories |
| Storage | External storage | Independent repository |
| Clone | Download on demand | Requires additional cloning |
| Version | Synchronized with main repository | Independent versions |

### Q2: How do I check my LFS storage quota?

```bash
# View GitHub LFS usage
gh api user/settings/billing/summary --jq '.plans[].name'

# Or visit the GitHub web interface:
# Settings → Billing and plans → Usage
```

### Q3: What should I do if LFS files are accidentally deleted?

```bash
# Restore from LFS cache
git lfs checkout

# Re-download from remote
git lfs pull

# Check LFS file status
git lfs status
```

### Q4: How do I optimize LFS clone speed?

```bash
# Shallow clone + LFS
git clone --depth 1 --filter=blob:none https://github.com/user/repo.git

# Clone only a specific branch
git clone -b main --single-branch https://github.com/user/repo.git

# Skip LFS files (download on demand later)
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/user/repo.git
git lfs pull --include="specific-file"
```

---

## In-Depth Understanding and Best Practices of Git LFS

### How LFS Works Internally

Understanding Git LFS's internal mechanism helps with better usage and troubleshooting. When you execute the `git add` command to add a file tracked by LFS, Git LFS's filter automatically intervenes. First, LFS calculates the file's SHA-256 hash, which serves as the file's unique identifier. Then, LFS stores the actual file content in the local `.git/lfs/objects` directory, organized by the first two characters of the hash as subdirectories. Finally, a pointer file is stored in the Git repository, which is very small, typically only about a hundred bytes, containing version information, hash, and file size.

When you execute the `git push` command, Git LFS uploads the locally stored large files to the LFS server. After uploading, the LFS server returns a confirmation. When you execute `git clone` or `git pull`, Git first fetches the pointer files, then automatically downloads the corresponding large files through the smudge filter. If the `GIT_LFS_SKIP_SMUDGE` environment variable is set, LFS files will not be downloaded automatically, and you need to manually execute `git lfs pull` to fetch them.

### When to Use Git LFS

Not all large files need to be managed with Git LFS. You can consider the following dimensions to determine whether LFS is needed. File size is an important factor; binary files over 1MB are generally recommended for LFS management. File change frequency is also critical; frequently changing large files will cause the repository to grow rapidly, and using LFS can avoid this issue. File type determines compression efficiency; already compressed formats like ZIP, JPEG, MP4, etc., have poor incremental compression in Git, making LFS more suitable. Team collaboration scale also affects the decision; in large teams where each person's clone cost is higher, using LFS can significantly reduce clone times.

File types suitable for LFS management include image assets such as PSD source files, AI design files, and TIFF high-resolution images. Video and audio files such as MP4 video, WAV audio, and project audio engineering files. 3D model files such as FBX, OBJ, Blend, and Maya format model files. Game resource files such as Unity's AssetBundle and Unreal's Pak files. Build artifacts such as large binary installers and compiled dynamic link libraries. Dataset files such as machine learning training data and large CSV data files.

Files less suitable for LFS include text source code files, as Git has high efficiency in versioning text files. Small configuration files, which are small and compress well. History files already efficiently managed by Git, unless the repository is already too large and needs to be trimmed.

### LFS Workflow in Team Collaboration

Using LFS in team collaboration requires establishing unified workflow standards. First, all team members need to install the Git LFS client; installation instructions can be provided in the project documentation. Second, LFS tracking rules should be committed to the repository's `.gitattributes` file to ensure everyone uses the same configuration. Third, during code reviews, pay attention to checking whether new large files are added but not tracked by LFS. Fourth, establish naming and organization standards for large files to avoid files being scattered throughout the repository.

For non-developers such as designers and content creators, simplified operational guides should be provided. You can create graphical operation manuals explaining how to install LFS, how to commit large files, and how to get the latest version. Consider using Git GUI tools such as GitKraken, SourceTree, or GitHub Desktop, which have good support for LFS. Establish a regular synchronization mechanism to ensure designers' work can be integrated into the project in a timely manner.

### LFS Storage Cost Management

GitHub has quota limits on LFS storage and bandwidth, so managing storage costs properly is very important. Regularly review files in LFS and delete history versions that are no longer needed. Use the `git lfs prune` command to clean up local LFS file caches that are no longer needed. For large projects, consider using a self-hosted LFS server or third-party storage services. Configure the LFS server to use object storage services such as AWS S3, Azure Blob Storage, or Alibaba Cloud OSS to leverage their cost advantages.

Monitor LFS usage and set alert thresholds for storage and bandwidth usage. In CI/CD workflows, optimize LFS file downloads to only download files needed for the current build. Use caching mechanisms to avoid downloading the same LFS files repeatedly. For large binary files, consider whether they can be generated at build time instead of being stored in the repository.

### Migrating Back from LFS to Git

In some cases, you may need to migrate LFS-managed files back to regular Git management. This typically happens when file sizes are small, changes are infrequent, or LFS is no longer needed. The migration process requires using the `git lfs migrate export` command, which replaces LFS pointer files with actual file contents. After migration, you need to force push to the remote repository, as this rewrites Git history.

Note that migrating back to Git will increase repository size and affect clone and pull speeds. Before migration, you should assess the repository size change to ensure it is within an acceptable range. It is recommended to create a backup branch before migration so you can roll back if issues occur. After migration, all team members need to be notified to re-clone the repository to avoid history conflicts.

### LFS and Git Submodules Integration

In projects using Git submodules, special attention is needed for LFS configuration. Submodules need to initialize LFS separately, and each submodule has its own independent LFS configuration. When cloning a repository with submodules, use `git submodule update --init --recursive` and ensure LFS is initialized. If LFS is used in a submodule, you need to run `git lfs install` and `git lfs pull` in the submodule directory.

It is recommended to document the LFS configuration requirements for submodules in the main repository's documentation. You can create initialization scripts to automate the cloning and LFS initialization process for submodules. In CI/CD workflows, ensure the workflow includes submodule and LFS initialization steps.

### Binary Differences in LFS Files

Git LFS does not support incremental diffs for binary files; every modification stores a complete file copy. This means frequently modified large files will quickly consume storage quota. To optimize storage usage, consider the following strategies. For large files that can be split, split them into multiple smaller files and only update the changed parts. For image files, keep the source files while generating optimized versions. For video files, use version numbering instead of committing every modification. For data files, consider using incremental update mechanisms to store only the changed data. Regularly clean up old versions of LFS files, keeping only the most recent versions.

---

## Further Reading

- [Git LFS Official Documentation](https://git-lfs.github.com/)
- [GitHub LFS Documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files)
- [Git LFS Best Practices](https://github.com/git-lfs/git-lfs/wiki/Tutorial)

---

## Exercise Summary

Through this exercise, you have learned:

1. ✅ Installing and configuring Git LFS
2. ✅ Setting up file tracking rules
3. ✅ Using LFS to manage large files
4. ✅ Migrating existing repositories to LFS
5. ✅ Integrating LFS in CI/CD
6. ✅ Optimizing LFS storage usage

Git LFS is an important tool for managing large binary files. It is recommended to configure LFS early in the project to avoid the hassle of later migration.

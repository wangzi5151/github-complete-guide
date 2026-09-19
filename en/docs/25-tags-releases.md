# Git Tags and GitHub Releases Complete Guide

## Overview

In software development, version management is crucial. Git Tags and GitHub Releases are core tools for marking project milestones and managing release versions. This chapter will deeply explain various Git tag usages, complete GitHub Releases operation workflow, and how to build automated release systems.

---

## 1. Git Tag Concepts

### 1.1 What are Tags

Tags are references in Git used to mark specific commits, typically used to identify version release points. Unlike branches, the commit pointed to by a tag is fixed and does not move with new commits.

The essence of a tag is an immutable pointer to a specific commit, giving that commit a human-readable name for easy future reference and citation.

### 1.2 Lightweight Tags

Lightweight tags are the simplest form of tags, just a pointer to a specific commit without any additional information.

```bash
# Create lightweight tag
git tag v1.0.0
```

Characteristics of lightweight tags:
- Do not store tag creator information
- Do not store creation time
- Do not store tag messages
- Do not support GPG signatures
- Essentially an immutable branch reference

### 1.3 Annotated Tags

Annotated tags are the recommended tag type in Git, stored as complete objects in the Git database.

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Official release version 1.0.0"
```

Characteristics of annotated tags:
- Store tag creator name and email
- Store creation date and time
- Store tag messages (description text)
- Support GPG signature verification
- Can be checksummed and verified for integrity

### 1.4 Comparison of Two Tag Types

| Feature | Lightweight Tag | Annotated Tag |
|---------|-----------------|---------------|
| Creation method | `git tag <name>` | `git tag -a <name> -m "msg"` |
| Stored as Git object | No | Yes |
| Contains author info | No | Yes |
| Contains timestamp | No | Yes |
| Contains message | No | Yes |
| Supports GPG signature | No | Yes |
| Recommended for release | No | Yes |
| Space usage | Very small | Small |

**Best Practice**: In formal projects, always use annotated tags to mark version releases. Lightweight tags are only for temporary marking or personal use.

---

## 2. Create, List, Delete Tags

### 2.1 Create Tags

```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Create tag for historical commit
git tag -a v0.9.0 abc1234 -m "Beta version 0.9.0"

# Create tag using full commit hash
git tag -a v0.8.0 9fceb02d0ae7906dd5e9f9ef49e8c01e51a1b33b

# Create tag on specific commit
git log --oneline
# Output:
# a1b2c3d Complete login feature
# e4f5g6h Add user module
# i7j8k9l Initial commit

git tag -a v0.1.0 i7j8k9l -m "Project initialization"
```

### 2.2 List Tags

```bash
# List all tags
git tag
# Output:
# v0.1.0
# v0.9.0
# v1.0.0

# Filter tags by pattern
git tag -l "v1.*"
# Output:
# v1.0.0
# v1.0.1
# v1.1.0

git tag -l "v*.*.*"
# Output all semantic version tags

# View tag details (annotated tag)
git show v1.0.0
# Output:
# tag v1.0.0
# Tagger: John Doe <johndoe@example.com>
# Date:   Mon Jan 1 12:00:00 2024 +0800
#
# Release version 1.0.0
#
# commit a1b2c3d...
# Author: John Doe <johndoe@example.com>
# ...

# View lightweight tag info
git show v1.0.0-lightweight
# Only shows commit info, no tag metadata

# List tags sorted by version
git tag -l --sort=-version:refname
# Output:
# v2.0.0
# v1.2.0
# v1.1.0
# v1.0.0

# View commit pointed to by tag
git rev-parse v1.0.0
# Output full commit hash
```

### 2.3 Delete Tags

```bash
# Delete local tag
git tag -d v1.0.0
# Output: Deleted tag 'v1.0.0'

# Delete remote tag (old method)
git push origin :refs/tags/v1.0.0

# Delete remote tag (recommended method)
git push origin --delete v1.0.0

# Batch delete local tags
git tag -l "v0.*" | xargs git tag -d

# Batch delete remote tags
git tag -l "v0.*" | xargs -I {} git push origin --delete {}
```

### 2.4 Rename Tags

Git has no direct tag rename command, need to delete and recreate:

```bash
# Steps to rename tag
# 1. Get commit pointed to by old tag
COMMIT=$(git rev-list -n 1 old-tag-name)

# 2. Delete old tag
git tag -d old-tag-name
git push origin --delete old-tag-name

# 3. Create new tag on same commit
git tag -a new-tag-name $COMMIT -m "Renamed from old-tag-name"

# 4. Push new tag
git push origin new-tag-name
```

### 2.5 Checkout Tags

```bash
# Checkout code corresponding to tag (enter detached HEAD state)
git checkout v1.0.0

# Create new branch based on tag (recommended for fixing old versions)
git checkout -b hotfix-v1.0.0 v1.0.0

# Switch back to main branch
git checkout main
```

---

## 3. Tag Signing (GPG Signing)

### 3.1 Why Signing is Needed

GPG signatures can verify the authenticity and integrity of tags, ensuring tags are indeed created by project maintainers and content has not been tampered with. This is crucial for open source project security.

### 3.2 Configure GPG Keys

```bash
# Check if GPG key already exists
gpg --list-keys

# Generate new GPG key
gpg --full-generate-key

# Select according to prompts:
# 1. Key type: RSA and RSA
# 2. Key length: 4096
# 3. Expiration: 0 (never expires) or specified time
# 4. Name, email (must match Git configuration)
# 5. Set password

# View GPG key ID
gpg --list-secret-keys --keyid-format=long
# Output:
# sec   rsa4096/ABCDEF1234567890 2024-01-01 [SC]
#       1234567890ABCDEF1234567890ABCDEF12345678
# uid                 [ultimate] John Doe <johndoe@example.com>
# ssb   rsa4096/1234567890ABCDEF 2024-01-01 [E]

# Export public key (for uploading to GitHub)
gpg --armor --export ABCDEF1234567890
```

### 3.3 Configure Git to Use GPG

```bash
# Set Git to use specified GPG key
git config --global user.signingkey ABCDEF1234567890

# Set to auto-sign all tags
git config --global tag.forceSignAnnotated true

# Set GPG program path (if using GPG2)
git config --global gpg.program /usr/bin/gpg2
```

### 3.4 Create Signed Tags

```bash
# Create signed tag (interactive password input)
git tag -s v1.0.0 -m "Signed release v1.0.0"

# Create signed tag and specify key
git tag -u ABCDEF1234567890 v1.0.0 -m "Signed release v1.0.0"

# Verify signed tag
git tag -v v1.0.0
# Output contains:
# gpg: Good signature from "John Doe <johndoe@example.com>"
```

### 3.5 Add GPG Public Key to GitHub

```bash
# Steps:
# 1. Export public key
gpg --armor --export ABCDEF1234567890

# 2. Copy output content (including BEGIN and END lines)

# 3. Add on GitHub:
#    Settings -> SSH and GPG keys -> New GPG key
#    Paste public key content and save

# 4. Verify tag displays as "Verified" on GitHub
```

---

## 4. GitHub Releases Details

### 4.1 What is GitHub Release

GitHub Release is a release management feature built on Git tags, providing:

- A formal version release page
- Release Notes
- Binary file attachments (Assets)
- Pre-release version marking
- Draft release functionality
- Community participation (discussion, feedback)

### 4.2 Relationship between Release and Tag

- Each Release must be based on a Tag
- One Tag can only correspond to one Release
- Release contains additional information beyond Tag (description, attachments, etc.)
- Tags can be used without Release, but not vice versa

### 4.3 Release Lifecycle

```
Create Draft → Edit Content → Publish (Official/Pre-release) → Edit/Delete
    ↓
  Draft   →  Edit  →    Publish      →  Update/Delete
```

---

## 5. Create Release and Release Notes

### 5.1 Create Release via Web Interface

**Detailed Steps:**

1. Enter GitHub repository page
2. Click "Releases" link in right sidebar
3. Click "Draft a new release" or "Create a new release"
4. Fill in following information:
   - **Choose a tag**: Select existing tag or create new tag
   - **Target**: Select target branch (when creating new tag)
   - **Release title**: Release title (usually tag name)
   - **Describe this release**: Detailed release notes
   - **Attach binaries**: Upload binary files
   - **This is a pre-release**: Mark as pre-release
   - **Create a discussion**: Create discussion for release
5. Click "Publish release" or "Save draft"

### 5.2 Write Release Notes via Web Interface

**Writing Template:**

```markdown
## 🚀 What's New

- Add user login feature
- Support OAuth 2.0 third-party login
- Add dark mode theme

## 🐛 Bug Fixes

- Fix slow homepage loading issue (#123)
- Fix mobile display misalignment (#124)

## ⚡ Performance

- Optimize image loading speed, reduce 50% load time
- Database query optimization

## 📦 Dependencies

- Upgrade React to 18.2.0
- Upgrade Node.js to 20.x

## 💔 Breaking Changes

- API endpoint /api/v1/users changed to /api/v2/users
- Remove deprecated legacy module

## 🙏 Contributors

Thanks to the following contributors for their participation:
@contributor1, @contributor2, @contributor3

**Full Changelog**: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

### 5.3 Create Release via GitHub CLI

```bash
# Create simple Release
gh release create v1.0.0 --title "v1.0.0" --notes "First official release"

# Create Release with detailed notes
gh release create v1.0.0 \
  --title "v1.0.0 - Official Version" \
  --notes-file CHANGELOG.md

# Create Release with attachments
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "Official release" \
  ./dist/app-linux.tar.gz \
  ./dist/app-macos.zip \
  ./dist/app-windows.exe

# Create Draft Release
gh release create v1.0.0 \
  --title "v1.0.0" \
  --notes "To be released" \
  --draft

# Create Pre-release
gh release create v1.0.0-beta.1 \
  --title "v1.0.0 Beta 1" \
  --notes "Test version" \
  --prerelease
```

### 5.4 Create Release via GitHub API

```bash
# Use curl to call API
curl -X POST \
  -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/releases \
  -d '{
    "tag_name": "v1.0.0",
    "target_commitish": "main",
    "name": "v1.0.0",
    "body": "## New Features\n\n- Feature 1\n- Feature 2",
    "draft": false,
    "prerelease": false,
    "generate_release_notes": true
  }'
```

---

## 6. Auto-generate Release Notes

### 6.1 GitHub Built-in Auto-generation

GitHub provides automatic Release Notes generation based on PRs and commits:

```bash
# Enable auto-generation using CLI
gh release create v1.0.0 --generate-notes

# Enable auto-generation using API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/releases \
  -d '{
    "tag_name": "v1.0.0",
    "generate_release_notes": true
  }'
```

### 6.2 Configure Auto Release Notes Template

Create `.github/release.yml` file in repository root:

```yaml
# .github/release.yml
changelog:
  exclude:
    labels:
      - ignore-for-release
    authors:
      - dependabot
      - github-actions
  categories:
    - title: 🚀 New Features
      labels:
        - enhancement
        - feature
    - title: 🐛 Bug Fixes
      labels:
        - bug
        - fix
        - bugfix
    - title: ⚡ Performance
      labels:
        - performance
        - optimization
    - title: 📚 Documentation
      labels:
        - documentation
        - docs
    - title: 🔧 Maintenance
      labels:
        - chore
        - maintenance
        - dependencies
    - title: 💔 Breaking Changes
      labels:
        - breaking-change
        - major
    - title: 🆕 Other Changes
      labels:
        - "*"
```

### 6.3 Use Release Drafter

Release Drafter is a GitHub Action that automatically updates draft Release every time a PR is merged.

**Configuration file `.github/release-drafter.yml`:**

```yaml
# .github/release-drafter.yml
name-template: 'v$RESOLVED_VERSION 🌈'
tag-template: 'v$RESOLVED_VERSION'

categories:
  - title: '🚀 New Features'
    labels:
      - 'feature'
      - 'enhancement'
  - title: '🐛 Bug Fixes'
    labels:
      - 'fix'
      - 'bugfix'
      - 'bug'
  - title: '🧰 Maintenance'
    labels:
      - 'chore'
      - 'dependencies'
  - title: '📖 Documentation'
    labels:
      - 'documentation'
      - 'docs'

change-template: '- $TITLE @$AUTHOR (#$NUMBER)'
change-title-escapes: '\<*_&'
no-changes-template: 'No changes.'

version-resolver:
  major:
    labels:
      - 'major'
      - 'breaking-change'
  minor:
    labels:
      - 'minor'
      - 'feature'
      - 'enhancement'
  patch:
    labels:
      - 'patch'
      - 'fix'
      - 'bugfix'
      - 'bug'
  default: patch

template: |
  ## Changes

  $CHANGES

  ## Installation

  ```bash
  npm install my-package@$RESOLVED_VERSION
  ```

  **Full Changelog**: https://github.com/$OWNER/$REPOSITORY/compare/$PREVIOUS_TAG...v$RESOLVED_VERSION

autolabeler:
  - label: 'feature'
    title:
      - '/^feat/i'
  - label: 'bug'
    title:
      - '/^fix/i'
  - label: 'documentation'
    title:
      - '/^docs/i'
  - label: 'dependencies'
    title:
      - '/^deps/i'
```

**GitHub Action configuration `.github/workflows/release-drafter.yml`:**

```yaml
# .github/workflows/release-drafter.yml
name: Release Drafter

on:
  push:
    branches:
      - main
  pull_request:
    types:
      - opened
      - reopened
      - synchronize

permissions:
  contents: read
  pull-requests: write

jobs:
  update_release_draft:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: release-drafter/release-drafter@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 6.4 Use Conventional Changelog

```bash
# Install conventional-changelog-cli
npm install -g conventional-changelog-cli

# Generate complete changelog
conventional-changelog -p angular -i CHANGELOG.md -s

# Generate from last tag
conventional-changelog -p angular -i CHANGELOG.md -s -r 1

# Use conventional-github-releaser to directly create Release
npm install -g conventional-github-releaser
conventional-github-releaser -p angular -t $GITHUB_TOKEN
```

**Configuration file `.conventional-changelog.json`:**

```json
{
  "types": [
    { "type": "feat", "section": "🚀 New Features" },
    { "type": "fix", "section": "🐛 Bug Fixes" },
    { "type": "perf", "section": "⚡ Performance" },
    { "type": "docs", "section": "📖 Documentation" },
    { "type": "chore", "hidden": true },
    { "type": "style", "hidden": true },
    { "type": "refactor", "section": "♻️ Code Refactoring" },
    { "type": "test", "hidden": true },
    { "type": "ci", "hidden": true }
  ]
}
```

---

## 7. Release Assets (Attachment Management)

### 7.1 What are Release Assets

Release Assets are binary files attached to Releases, common uses include:

- Compiled programs (executables, installers)
- Compressed source code packages
- Documentation (PDF, HTML)
- Configuration file templates
- Docker image tar packages

### 7.2 Upload Assets via Web

1. Edit or create Release
2. Drag files or click to select in "Attach binaries" area
3. Wait for upload to complete
4. Save Release

### 7.3 Manage Assets via CLI

```bash
# Create Release and upload files
gh release create v1.0.0 \
  ./dist/app-linux-amd64 \
  ./dist/app-linux-arm64 \
  ./dist/app-darwin-amd64 \
  ./dist/app-windows-amd64.exe \
  --title "v1.0.0" \
  --notes "Cross-platform release"

# Add files to existing Release
gh release upload v1.0.0 ./new-asset.zip

# Replace existing file with same name
gh release upload v1.0.0 ./app-linux --clobber

# Delete Asset
gh release delete-asset v1.0.0 old-file.zip --yes

# Download Asset
gh release download v1.0.0 --pattern "*.zip"

# Download to specified directory
gh release download v1.0.0 --dir ./downloads --pattern "app-*"

# Download specific file only
gh release download v1.0.0 --pattern "app-linux-*"
```

### 7.4 Manage Assets via API

```bash
# Upload Asset
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  "https://uploads.github.com/repos/OWNER/REPO/releases/RELEASE_ID/assets?name=myfile.zip" \
  --data-binary @myfile.zip

# List Assets
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/releases/RELEASE_ID/assets

# Delete Asset
curl -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/releases/assets/ASSET_ID
```

### 7.5 Asset Naming Best Practices

```
Recommended naming format:
<project-name>-<version>-<platform>-<architecture>[.<extension>]

Examples:
myapp-1.0.0-linux-amd64.tar.gz
myapp-1.0.0-linux-arm64.tar.gz
myapp-1.0.0-darwin-amd64.tar.gz
myapp-1.0.0-darwin-arm64.tar.gz (Apple Silicon)
myapp-1.0.0-windows-amd64.zip
myapp-1.0.0-windows-arm64.zip

Include checksum file:
myapp-1.0.0-checksums.txt
myapp-1.0.0-checksums.sha256
```

---

## 8. Pre-release Versions

### 8.1 Pre-release Version Concepts

Pre-release versions are used to let users test new features before official release. Common pre-release identifiers:

| Identifier | Meaning | Example |
|------------|---------|---------|
| alpha | Internal test version | v1.0.0-alpha.1 |
| beta | Public test version | v1.0.0-beta.1 |
| rc | Release candidate | v1.0.0-rc.1 |
| dev | Development version | v1.0.0-dev.1 |
| canary | Canary version | v1.0.0-canary.1 |

### 8.2 Create Pre-release Versions

```bash
# Create via CLI
gh release create v2.0.0-beta.1 \
  --title "v2.0.0 Beta 1" \
  --notes "## ⚠️ This is a test version\n\nDo not use in production environment." \
  --prerelease

# Create via web
# 1. Create Release
# 2. Check "This is a pre-release" option
# 3. Publish

# Create via API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/releases \
  -d '{
    "tag_name": "v2.0.0-beta.1",
    "name": "v2.0.0 Beta 1",
    "prerelease": true
  }'
```

### 8.3 Pre-release Version Display

- On Releases page, pre-release versions will have obvious markers
- By default not shown in latest Release
- npm and other package managers can install via `@beta` tag

```bash
# Install pre-release version via npm
npm install my-package@beta
npm install my-package@2.0.0-beta.1

# View all pre-release versions
npm versions --json
```

---

## 9. Draft Release

### 9.1 Uses of Draft

- Prepare Release content in advance, publish when the time is ripe
- Coordinate with CI/CD to auto-fill Release Notes
- Team collaboration to review Release content
- Batch prepare Releases for multiple versions

### 9.2 Manage Draft Release

```bash
# Create Draft Release
gh release create v1.1.0 \
  --title "v1.1.0" \
  --notes "In development..." \
  --draft

# List all Releases (including Draft)
gh release list --limit 20

# View Draft Release details
gh release view v1.1.0

# Edit Draft Release
gh release edit v1.1.0 \
  --title "v1.1.0 - New Version" \
  --notes-file RELEASE_NOTES.md

# Publish Draft Release (cancel draft status)
gh release edit v1.1.0 --draft=false

# Delete Draft Release
gh release delete v1.1.0 --yes
```

### 9.3 Automated Draft Release Workflow

```yaml
# .github/workflows/auto-release-draft.yml
name: Auto Release Draft

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Changelog
        id: changelog
        run: |
          # Get previous tag
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREV_TAG" ]; then
            CHANGES=$(git log --oneline --no-merges)
          else
            CHANGES=$(git log --oneline --no-merges ${PREV_TAG}..HEAD)
          fi
          echo "changes<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create Draft Release
        uses: softprops/action-gh-release@v1
        with:
          draft: true
          generate_release_notes: true
          body: |
            ## Changes

            ${{ steps.changelog.outputs.changes }}

            ## Installation Instructions

            Please download the installation package for your platform from Assets below.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 10. Semantic Versioning Details

### 10.1 Semantic Versioning Specification

Semantic Versioning (SemVer) is a version number naming specification, format:

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

Examples:
1.0.0
2.1.3
1.0.0-alpha.1
1.0.0-beta.2+build.123
```

| Component | Description | When to Increment |
|-----------|-------------|-------------------|
| MAJOR | Major version number | Incompatible API changes |
| MINOR | Minor version number | Backward compatible new features |
| PATCH | Patch number | Backward compatible bug fixes |
| PRERELEASE | Pre-release identifier | Test versions |
| BUILD | Build metadata | Build info (doesn't affect priority) |

### 10.2 Version Number Increment Rules

```bash
# Initial development phase: 0.y.z
# Any changes can happen in 0.y.z
0.1.0 → 0.2.0 (may have breaking changes)

# Official release: 1.0.0
# After this, strictly follow SemVer rules

# PATCH revision: 1.0.0 → 1.0.1
# - Bug fixes
# - Performance optimization
# - Documentation corrections

# MINOR version: 1.0.0 → 1.1.0
# - New features
# - Deprecated features (not removed)
# - Internal refactoring (doesn't affect public API)

# MAJOR version: 1.0.0 → 2.0.0
# - Remove features
# - Change existing feature behavior
# - Change public API signature
```

### 10.3 Version Comparison Rules

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta
< 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11
< 1.0.0-rc.1 < 1.0.0
```

### 10.4 Use Tools to Manage Version Numbers

```bash
# Use npm version to auto-increment version number
npm version patch   # 1.0.0 → 1.0.1
npm version minor   # 1.0.0 → 1.1.0
npm version major   # 1.0.0 → 2.0.0

# Create pre-release version
npm version prepatch --preid=beta   # 1.0.0 → 1.0.1-beta.0
npm version preminor --preid=alpha  # 1.0.0 → 1.1.0-alpha.0
npm version premajor --preid=rc     # 1.0.0 → 2.0.0-rc.0

# Use standard-version
npm install -g standard-version
standard-version  # Auto-analyze commits and increment version

# Use semantic-release
npx semantic-release  # Fully automated version management
```

---

## 11. Automated Release Process (GitHub Actions)

### 11.1 Basic Automated Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - os: linux
            arch: amd64
          - os: linux
            arch: arm64
          - os: darwin
            arch: amd64
          - os: darwin
            arch: arm64
          - os: windows
            arch: amd64

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Build
        env:
          GOOS: ${{ matrix.os }}
          GOARCH: ${{ matrix.arch }}
        run: |
          EXTENSION=""
          if [ "$GOOS" = "windows" ]; then
            EXTENSION=".exe"
          fi
          go build -ldflags="-s -w" -o myapp-${{ matrix.os }}-${{ matrix.arch }}${EXTENSION} .

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: myapp-${{ matrix.os }}-${{ matrix.arch }}
          path: myapp-*

  release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts

      - name: Generate Checksums
        run: |
          cd artifacts
          find . -type f -name "myapp-*" -exec sha256sum {} \; > ../checksums.txt

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
          files: |
            artifacts/myapp-*/myapp-*
            checksums.txt
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 11.2 Auto-release Based on Conventional Commits

```yaml
# .github/workflows/semantic-release.yml
name: Semantic Release

on:
  push:
    branches:
      - main

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'

      - name: Install Dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run Tests
        run: npm test

      - name: Release
        run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

**`.releaserc.json` configuration file:**

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    "@semantic-release/git"
  ]
}
```

### 11.3 Multi-platform Docker Image Release

```yaml
# .github/workflows/docker-release.yml
name: Docker Release

on:
  push:
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            myuser/myapp
            ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 12. Auto-generate Changelog

### 12.1 Changelog Based on PR Labels

```yaml
# .github/workflows/changelog.yml
name: Generate Changelog

on:
  release:
    types: [published]

jobs:
  changelog:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate Changelog
        run: |
          # Get current and previous version
          CURRENT_TAG=${{ github.event.release.tag_name }}
          PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

          if [ -z "$PREV_TAG" ]; then
            echo "First release, generating complete changelog"
            RANGE="HEAD"
          else
            RANGE="${PREV_TAG}..${CURRENT_TAG}"
          fi

          # Generate changelog
          {
            echo "# Changelog"
            echo ""
            echo "## ${CURRENT_TAG} ($(date +%Y-%m-%d))"
            echo ""
            echo "### 🚀 New Features"
            git log $RANGE --oneline --grep="^feat" | sed 's/^[a-z0-9]* /- /'
            echo ""
            echo "### 🐛 Bug Fixes"
            git log $RANGE --oneline --grep="^fix" | sed 's/^[a-z0-9]* /- /'
            echo ""
            echo "### ⚡ Performance"
            git log $RANGE --oneline --grep="^perf" | sed 's/^[a-z0-9]* /- /'
            echo ""
            echo "### 📖 Documentation"
            git log $RANGE --oneline --grep="^docs" | sed 's/^[a-z0-9]* /- /'
          } > NEW_CHANGELOG.md

          # Merge with existing changelog
          if [ -f CHANGELOG.md ]; then
            tail -n +2 CHANGELOG.md >> NEW_CHANGELOG.md
          fi
          mv NEW_CHANGELOG.md CHANGELOG.md

      - name: Commit Changelog
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add CHANGELOG.md
          git commit -m "docs: update changelog for ${CURRENT_TAG}" || true
          git push
```

### 12.2 Use git-cliff to Generate Changelog

```yaml
# .github/workflows/git-cliff.yml
name: Git Cliff Changelog

on:
  release:
    types: [published]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Generate a changelog
        uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --latest --strip header
        env:
          OUTPUT: CHANGES.md
          GITHUB_REPO: ${{ github.repository }}

      - name: Upload changelog to release
        uses: softprops/action-gh-release@v1
        with:
          body_path: CHANGES.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**`cliff.toml` configuration:**

```toml
# cliff.toml
[changelog]
header = """
# Changelog\n
"""
body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {% if commit.scope %}**{{ commit.scope }}:** {% endif %}\
            {{ commit.message | upper_first }}\
            {% if commit.links %} ({{ commit.links | join(sep=", ") }}){% endif %}\
    {% endfor %}
{% endfor %}\n
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = true
split_commits = false

commit_parsers = [
  { message = "^feat", group = "🚀 New Features" },
  { message = "^fix", group = "🐛 Bug Fixes" },
  { message = "^doc", group = "📖 Documentation" },
  { message = "^perf", group = "⚡ Performance" },
  { message = "^refactor", group = "♻️ Code Refactoring" },
  { message = "^style", group = "💄 Styles" },
  { message = "^test", group = "✅ Tests" },
  { message = "^chore", group = "🔧 Maintenance" },
]
```

---

## 13. Multi-platform Release Strategy

### 13.1 Cross-platform Build Matrix

```yaml
# .github/workflows/cross-platform.yml
name: Cross Platform Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-latest
            target: linux-amd64
          - os: ubuntu-latest
            target: linux-arm64
          - os: macos-latest
            target: darwin-amd64
          - os: macos-14
            target: darwin-arm64
          - os: windows-latest
            target: windows-amd64

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: |
          echo "Building for ${{ matrix.target }}"
          # Execute different build commands based on target
```

### 13.2 Multi-package Manager Release

```yaml
# .github/workflows/multi-registry.yml
name: Publish to Multiple Registries

on:
  release:
    types: [published]

jobs:
  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  publish-gpr:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 'lts/*'
          registry-url: 'https://npm.pkg.github.com'
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 14. Practice: Set Up Automated Version Release

### 14.1 Complete Release Process Design

```
Developer pushes code
       ↓
PR triggers CI testing
       ↓
Merge to main branch
       ↓
Auto-analyze conventional commits
       ↓
Auto-generate Release Notes draft
       ↓
Manual review and publish (or auto-publish)
       ↓
Trigger build pipeline
       ↓
Build multi-platform binaries
       ↓
Upload to Release Assets
       ↓
Publish to package manager (npm/pypi/crates.io)
       ↓
Update Docker images
       ↓
Notify community (email, Discord, Slack)
```

### 14.2 Complete Automation Configuration

**Step 1: Configure `package.json`**

```json
{
  "name": "my-awesome-project",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc && webpack --mode production",
    "test": "jest --coverage",
    "lint": "eslint src/ --ext .ts,.tsx",
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major",
    "release:patch": "standard-version --release-as patch"
  },
  "devDependencies": {
    "standard-version": "^9.5.0",
    "@commitlint/cli": "^18.0.0",
    "@commitlint/config-conventional": "^18.0.0",
    "husky": "^9.0.0"
  }
}
```

**Step 2: Configure Commitlint**

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Fix
        'docs',     // Documentation
        'style',    // Format
        'refactor', // Refactor
        'perf',     // Performance
        'test',     // Test
        'build',    // Build
        'ci',       // CI
        'chore',    // Maintenance
        'revert',   // Revert
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 100],
  },
};
```

**Step 3: Configure Husky Git Hooks**

```bash
# Initialize husky
npx husky init

# Add commit-msg hook
echo 'npx --no -- commitlint --edit $1' > .husky/commit-msg

# Add pre-push hook
echo 'npm run lint && npm test' > .husky/pre-push
```

**Step 4: Configure `.versionrc` (standard-version)**

```json
{
  "types": [
    { "type": "feat", "section": "🚀 New Features" },
    { "type": "fix", "section": "🐛 Bug Fixes" },
    { "type": "perf", "section": "⚡ Performance" },
    { "type": "refactor", "section": "♻️ Code Refactoring" },
    { "type": "docs", "section": "📖 Documentation Update" },
    { "type": "test", "section": "✅ Tests", "hidden": true },
    { "type": "chore", "section": "🔧 Maintenance", "hidden": true },
    { "type": "style", "section": "💄 Styles", "hidden": true },
    { "type": "ci", "section": "🔄 CI", "hidden": true }
  ],
  "commitUrlFormat": "https://github.com/owner/repo/commit/{{hash}}",
  "compareUrlFormat": "https://github.com/owner/repo/compare/{{previousTag}}...{{currentTag}}",
  "issueUrlFormat": "https://github.com/owner/repo/issues/{{id}}"
}
```

**Step 5: Complete CI/CD Workflow**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  # Continuous Integration
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Build
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/

  # Auto-release (only on main branch)
  release:
    needs: ci
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write
      packages: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build
          path: dist/

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Release
        run: npx standard-version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Push changes
        run: git push --follow-tags origin main

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
          files: dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Publish to npm
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 14.3 Release Checklist

```markdown
## Pre-release Checklist

### Code Quality
- [ ] All tests passed
- [ ] Code coverage meets standard (≥80%)
- [ ] No lint errors
- [ ] TypeScript type check passed

### Documentation
- [ ] README updated
- [ ] API documentation updated
- [ ] CHANGELOG generated
- [ ] Migration guide written (if breaking changes)

### Version
- [ ] Version number conforms to SemVer
- [ ] Tag name format correct (v1.2.3)
- [ ] Pre-release version tested

### Release
- [ ] Release Notes reviewed
- [ ] Binary files built and tested
- [ ] Package manager published successful
- [ ] Docker image pushed

### Post-release
- [ ] Release page accessible
- [ ] Download links working
- [ ] Community notified
- [ ] Documentation website updated
```

### 14.4 Rollback Release

```bash
# If release has issues, need emergency rollback

# 1. Delete problematic Release
gh release delete v1.2.0 --yes

# 2. Delete tag
git tag -d v1.2.0
git push origin --delete v1.2.0

# 3. Unpublish from npm (can operate within 72 hours)
npm unpublish my-package@1.2.0

# 4. Create fix version
git revert HEAD
git tag -a v1.2.1 -m "Rollback v1.2.0 changes"
git push origin main --tags

# 5. Publish fix version
gh release create v1.2.1 \
  --title "v1.2.1 - Emergency Fix" \
  --notes "Rollback issues introduced in v1.2.0"
```

---

## Summary

This chapter details Git Tags and GitHub Releases complete knowledge system:

1. **Git Tags**: Differences and usage scenarios of lightweight and annotated tags
2. **Tag Management**: Complete operations for creating, listing, deleting, renaming tags
3. **GPG Signing**: Signing mechanism to ensure release security
4. **GitHub Releases**: Complete flow from creation to management
5. **Auto Release Notes**: Multiple auto-generation solutions
6. **Release Assets**: Binary file attachment management
7. **Pre-release Versions**: alpha, beta, rc version management
8. **Draft Release**: Usage scenarios of draft releases
9. **Semantic Versioning**: SemVer specification detailed explanation
10. **Automated Release**: Complete CI/CD release process
11. **Changelog Auto-generation**: Multiple tools and solutions
12. **Multi-platform Release**: Cross-platform build and multi-registry release
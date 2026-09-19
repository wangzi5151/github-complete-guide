# Chapter 2: Install and Configure Git

## 2.1 Windows Installation

### Method 1: Official Download (Recommended for Beginners)

#### Step 1: Open Download Page

1. Open browser and visit **https://git-scm.com/download/win**
2. The page will automatically detect your system and start downloading
3. If it doesn't download automatically, click **Click here to download manually**

```
┌─────────────────────────────────────────────────────┐
│  Download Git for Windows                            │
│                                                     │
│  Click here to download manually                     │
│                                                     │
│  ✓ 64-bit Git for Windows Setup                     │
│  ✓ 32-bit Git for Windows Setup                     │
│  ✓ Portable Git for Windows                          │
└─────────────────────────────────────────────────────┘
```

#### Step 2: Run Installer

1. Find the downloaded file (usually in "Downloads" folder)
2. Double-click to run `Git-xxx-xxx-bit.exe`
3. If a security prompt appears, click **Run**

#### Step 3: Installation Wizard

Click through the following steps:

**Welcome Page:**
```
┌─────────────────────────────────────────────┐
│  Git Setup                                   │
│                                             │
│  Welcome to Git Setup                       │
│                                             │
│  This will install Git version x.x.x on     │
│  your computer.                             │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

**License Agreement:**
```
┌─────────────────────────────────────────────┐
│  GNU General Public License                 │
│                                             │
│  GNU GENERAL PUBLIC LICENSE                 │
│  Version 2, June 1991                       │
│                                             │
│  [Read full agreement]                      │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

**Select Components:**
```
┌─────────────────────────────────────────────┐
│  Select Components                           │
│                                             │
│  ☑ Git Bash                                 │
│  ☑ Git GUI                                  │
│  ☑ Git LFS                                  │
│  ☑ Associate .git* files with Git           │
│  ☑ Add Git Bash Profile to Windows Terminal│
│  ☑ Add a Git Bash Profile to Windows       │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

**Important Setting - PATH Environment:**
```
┌─────────────────────────────────────────────┐
│  Adjusting your PATH environment            │
│                                             │
│  ● Use Git from the Windows Command Prompt  │
│    ← Recommended                            │
│  ○ Use Git and optional Unix tools from the │
│    Windows Command Prompt                   │
│  ○ Use Git from the Windows Command Prompt  │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

**Important Setting - SSH Executable:**
```
┌─────────────────────────────────────────────┐
│  Choosing the SSH executable                 │
│                                             │
│  ● Use bundled OpenSSH                      │
│    ← Recommended                            │
│  ○ Use external OpenSSH                     │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

**Important Setting - Line Ending Conversion:**
```
┌─────────────────────────────────────────────┐
│  Configuring line ending conversions         │
│                                             │
│  ● Checkout Windows-style, commit           │
│    Unix-style line endings                  │
│    ← Recommended for Windows users          │
│                                             │
│  ○ Checkout as-is, commit Unix-style        │
│  ○ Checkout as-is, commit as-is             │
│                                             │
│               [Next >]                       │
└─────────────────────────────────────────────┘
```

#### Step 4: Complete Installation

1. Click **Install** to start installation
2. Wait for installation to complete
3. Click **Finish**

### Method 2: Using Winget

```powershell
# Open Command Prompt or PowerShell
winget install Git.Git
```

### Method 3: Using Chocolatey

```powershell
choco install git
```

## 2.2 macOS Installation

### Method 1: Homebrew (Recommended)

#### Step 1: Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Git

```bash
brew install git
```

### Method 2: Xcode Command Line Tools

```bash
xcode-select --install
```

Click **Install** when the dialog appears.

### Method 3: Official Download

1. Visit **https://git-scm.com/download/mac**
2. Download the installer
3. Double-click to install

## 2.3 Linux Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install git
```

### CentOS/RHEL

```bash
sudo yum install git
```

### Fedora

```bash
sudo dnf install git
```

### Arch Linux

```bash
sudo pacman -S git
```

### Compile from Source

```bash
# Install dependencies
sudo apt install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext

# Download source
git clone https://github.com/git/git.git
cd git

# Compile and install
make prefix=/usr/local all
sudo make prefix=/usr/local install
```

## 2.4 Verify Installation

### Open Terminal

**Windows:**
- Press `Win + R`
- Type `cmd`
- Press Enter

**macOS:**
- Press `Command + Space`
- Type `Terminal`
- Press Enter

**Linux:**
- Press `Ctrl + Alt + T`

### Enter Command

```bash
git --version
```

### Expected Output

```
git version 2.43.0.windows.1
```

Seeing the version number means installation was successful!

## 2.5 Initial Configuration

### Why Configure?

Git needs to know who you are so it can record your information with each commit.

### Set Username

```bash
git config --global user.name "Your Name"
```

**Example:**
```bash
git config --global user.name "John Doe"
```

### Set Email

```bash
git config --global user.email "your@email.com"
```

**Example:**
```bash
git config --global user.email "johndoe@example.com"
```

⚠️ **Important: The email must match your GitHub account email!**

### Set Default Branch Name

```bash
git config --global init.defaultBranch main
```

### Set Default Editor

```bash
# If using VS Code
git config --global core.editor "code --wait"

# If using Vim
git config --global core.editor "vim"

# If using Nano
git config --global core.editor "nano"

# If using Notepad++
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"
```

### Enable Color Output

```bash
git config --global color.ui auto
```

### Configure Line Ending Handling

```bash
# Windows users
git config --global core.autocrlf true

# macOS/Linux users
git config --global core.autocrlf input
```

### Configure Chinese Filenames

```bash
# Prevent Chinese filenames from displaying as garbled text
git config --global core.quotepath false
```

### Configure Default Merge Tool

```bash
# Use VS Code as merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

## 2.6 View Configuration

### View All Configuration

```bash
git config --list
```

### View Specific Configuration

```bash
# View username
git config user.name

# View email
git config user.email

# View editor
git config core.editor
```

### Configuration File Locations

| Level | File Location | Description |
|-------|--------------|-------------|
| `--system` | `/etc/gitconfig` | System-level configuration |
| `--global` | `~/.gitconfig` | User-level configuration (recommended) |
| `--local` | `.git/config` | Repository-level configuration |

**Priority:** `local` > `global` > `system`

### Configuration File Content

```ini
# ~/.gitconfig file content example
[user]
    name = John Doe
    email = johndoe@example.com
[core]
    editor = code --wait
    autocrlf = true
    quotepath = false
[init]
    defaultBranch = main
[color]
    ui = auto
```

## 2.7 Advanced Configuration

### Set Git Aliases

```bash
# Common aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "reset HEAD --"
```

### Configure Proxy

```bash
# HTTP proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# SOCKS5 proxy
git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890

# Remove proxy
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### Configure SSH

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your@email.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519
```

### Configure Large File Handling

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
```

## 2.8 Common Issues

### Q: Can't find git command after Windows installation?

**Solution:**
1. Reopen Command Prompt
2. Check PATH environment variable
3. Reinstall Git, make sure to check "Add Git to PATH"

### Q: macOS shows "command not found: git"?

**Solution:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Or install using Homebrew
brew install git
```

### Q: Configured email but commit shows different email?

**Solution:**
```bash
# Check current configuration
git config --list

# Reset email
git config --global user.email "correct@email.com"

# Check system-level configuration
git config --system user.email
```

### Q: How to delete configuration?

```bash
# Delete global configuration
git config --global --unset user.name
git config --global --unset user.email

# Edit configuration file
git config --global --edit
```

## 2.9 Best Practices

1. **Use Real Information**: Username and email should match GitHub account
2. **Use Global Configuration**: Unless special needs, use `--global` configuration
3. **Configure Editor**: Choose an editor you're familiar with
4. **Configure Proxy**: If having issues accessing GitHub, configure proxy
5. **Configure Aliases**: Set aliases for commonly used commands to improve efficiency

## 2.10 Chapter Summary

This chapter provides a detailed introduction to Git installation and configuration methods, including:

- Windows, macOS, Linux installation methods
- Initial configuration steps
- Advanced configuration options
- Common issue solutions

**Key Takeaways:**
- Git must be configured after installation
- Email must match GitHub account
- Can configure proxy, aliases, etc. as needed

**Next Step:**
[Register GitHub Account →](03-signup-github.md)

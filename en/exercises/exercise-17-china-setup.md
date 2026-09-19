# Exercise 17: Domestic Environment Configuration Practice

## Learning Objectives

- Configure domestic acceleration solutions
- Set up domestic package manager mirrors
- Optimize Git connections

## Steps

### Step 1: Configure GitHub520

```bash
# Install GitHub520
pip install github520

# Verify hosts file
cat /etc/hosts | grep github
```

### Step 2: Configure npm Mirror

```bash
# Permanently set Taobao mirror
npm config set registry https://registry.npmmirror.com

# Verify
npm config get registry
# Output: https://registry.npmmirror.com

# Test speed
npm install -g typescript
```

### Step 3: Configure pip Mirror

```bash
# Permanently set Alibaba Cloud mirror
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set global.trusted-host mirrors.aliyun.com

# Verify
pip config list

# Test speed
pip install requests
```

### Step 4: Configure Git SSH

```bash
# Convert to SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"

# Verify
git config --global --get-regexp url
```

### Step 5: Configure Go Mirror

```bash
# Set proxy
go env -w GOPROXY=https://goproxy.cn,direct

# Verify
go env GOPROXY
```

### Step 6: Configure Docker Mirror

```bash
# Create configuration directory
sudo mkdir -p /etc/docker

# Write configuration
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
EOF

# Restart Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# Verify
docker info | grep -A 5 "Registry Mirrors"
```

## Practical Tasks

1. Install and configure GitHub520
2. Configure domestic mirrors for npm/pip/Docker
3. Test download speeds for each tool
4. Compare speed differences before and after configuration

## Verification Checklist

- [ ] GitHub520 installed and running
- [ ] npm mirror configured
- [ ] pip mirror configured
- [ ] Git SSH configured
- [ ] Go mirror configured
- [ ] Docker mirror configured
- [ ] Can access GitHub normally

## Next Steps

Congratulations on completing all exercises! You can now efficiently use GitHub in a domestic environment.
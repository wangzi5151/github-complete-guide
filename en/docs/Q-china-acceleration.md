# GitHub Domestic Acceleration Guide

> This chapter will explain in detail various acceleration methods for domestic developers to access GitHub, including modifying Hosts file, using acceleration proxy, configuring Git proxy, using domestic mirrors, SSH connection optimization, etc.

---

## Table of Contents

1. [Why Acceleration is Needed?](#why-acceleration-is-needed)
2. [Method 1: Modify Hosts File](#method-1-modify-hosts-file)
3. [Method 2: Use GitHub Acceleration Proxy](#method-2-use-github-acceleration-proxy)
4. [Method 3: Configure Git Proxy](#method-3-configure-git-proxy)
5. [Method 4: Use Domestic Mirrors](#method-4-use-domestic-mirrors)
6. [Method 5: Use SSH Connection](#method-5-use-ssh-connection)
7. [Method 6: Optimize Git Configuration](#method-6-optimize-git-configuration)
8. [Method 7: Use CDN Acceleration](#method-7-use-cdn-acceleration)
9. [Method 8: Use GitHub Actions Proxy](#method-8-use-github-actions-proxy)
10. [Enterprise Solutions](#enterprise-solutions)
11. [FAQ](#faq)
12. [Recommended Tools](#recommended-tools)
13. [Related Resources](#related-resources)

---

## Why Acceleration is Needed?

Due to network reasons, domestic access to GitHub is sometimes slow, main reasons include:

### Network Problem Analysis

**DNS Pollution**:
- Domestic DNS servers may return wrong IP addresses
- Causes connection to wrong server when accessing GitHub
- Solution: Use foreign DNS servers or modify Hosts file

**Network Latency**:
- Physical distance from domestic to GitHub servers is far
- Network routing may not be optimal path
- Solution: Use CDN acceleration or proxy services

**Bandwidth Limitations**:
- International bandwidth is limited, peak hours may be congested
- Large file download speed is slow
- Solution: Use mirror sites or chunked downloads

**Unstable Connection**:
- Network fluctuations cause connection interruptions
- Long operations tend to fail
- Solution: Use SSH connection or configure retry mechanism

### Acceleration Effect Comparison

| Acceleration Method | Speed Improvement | Stability | Ease of Use | Applicable Scenario |
|---------------------|-------------------|-----------|-------------|---------------------|
| Modify Hosts | Medium | Medium | Simple | Temporary use |
| Acceleration Proxy | High | High | Simple | Daily use |
| Git Proxy | High | High | Medium | Have proxy server |
| Domestic Mirror | High | High | Simple | Read-only operations |
| SSH Connection | Medium | High | Medium | Push code |
| CDN Acceleration | High | High | Complex | Enterprise use |

## Method 1: Modify Hosts File

### Principle
By modifying hosts file, directly specify GitHub's IP address, avoid DNS pollution.

### Steps

1. **Get GitHub IP Address**

Visit following websites to get latest IP:
- https://github.com/ipaddresses
- https://www.ipaddress.com/
- https://ip.tool.lu/

Domains to get:
- `github.com`
- `github.global.ssl.fastly.net`
- `assets-cdn.github.com`
- `github.io`
- `api.github.com`
- `raw.githubusercontent.com`
- `gist.github.com`

2. **Modify hosts File**

**Windows**:
```cmd
# Open Notepad as administrator
notepad C:\Windows\System32\drivers\etc\hosts

# Add following content
# GitHub
140.82.114.4 github.com
199.232.69.194 github.global.ssl.fastly.net
185.199.108.153 assets-cdn.github.com
140.82.114.20 github.io
140.82.113.22 api.github.com
140.82.114.6 nodeload.github.com
185.199.108.133 raw.githubusercontent.com
140.82.114.10 gist.github.com
```

**macOS/Linux**:
```bash
# Edit hosts file
sudo nano /etc/hosts

# Add following content
# GitHub
140.82.114.4 github.com
199.232.69.194 github.global.ssl.fastly.net
185.199.108.153 assets-cdn.github.com
140.82.114.20 github.io
140.82.113.22 api.github.com
140.82.114.6 nodeload.github.com
185.199.108.133 raw.githubusercontent.com
140.82.114.10 gist.github.com
```

3. **Flush DNS Cache**

**Windows**:
```cmd
ipconfig /flushdns
```

**macOS**:
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

**Linux**:
```bash
sudo systemd-resolve --flush-caches
# Or
sudo /etc/init.d/networking restart
```

### Auto Update Script

**Python Script**:
```python
#!/usr/bin/env python3
import requests
import re
import platform
import subprocess

def get_github_ips():
    """Get GitHub IP addresses"""
    domains = [
        'github.com',
        'github.global.ssl.fastly.net',
        'assets-cdn.github.com',
        'github.io',
        'api.github.com',
        'raw.githubusercontent.com'
    ]
    
    ips = {}
    for domain in domains:
        try:
            response = requests.get(f'https://ip.tool.lu/{domain}')
            ip = response.text.strip()
            ips[domain] = ip
        except:
            print(f"Cannot get IP address for {domain}")
    
    return ips

def update_hosts(ips):
    """Update hosts file"""
    system = platform.system()
    
    if system == 'Windows':
        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    else:
        hosts_path = '/etc/hosts'
    
    # Read existing content
    with open(hosts_path, 'r') as f:
        content = f.read()
    
    # Remove old GitHub entries
    content = re.sub(r'# GitHub\n.*?\n\n', '', content, flags=re.DOTALL)
    
    # Add new entries
    new_entries = '# GitHub\n'
    for domain, ip in ips.items():
        new_entries += f'{ip} {domain}\n'
    new_entries += '\n'
    
    # Write file
    with open(hosts_path, 'w') as f:
        f.write(content + new_entries)
    
    print("hosts file updated")

def flush_dns():
    """Flush DNS cache"""
    system = platform.system()
    
    if system == 'Windows':
        subprocess.run(['ipconfig', '/flushdns'], check=True)
    elif system == 'Darwin':
        subprocess.run(['sudo', 'dscacheutil', '-flushcache'], check=True)
        subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True)
    else:
        subprocess.run(['sudo', 'systemd-resolve', '--flush-caches'], check=True)
    
    print("DNS cache flushed")

if __name__ == '__main__':
    print("Getting GitHub IP addresses...")
    ips = get_github_ips()
    
    if ips:
        print("Updating hosts file...")
        update_hosts(ips)
        
        print("Flushing DNS cache...")
        flush_dns()
        
        print("Done!")
    else:
        print("Cannot get IP addresses, please update manually")
```

**Shell Script**:
```bash
#!/bin/bash

# GitHub IP Update Script

# Get GitHub IP
get_ip() {
    local domain=$1
    curl -s "https://ip.tool.lu/$domain" | head -1
}

# Update hosts file
update_hosts() {
    local hosts_file="/etc/hosts"
    
    # Backup original file
    sudo cp "$hosts_file" "$hosts_file.bak"
    
    # Remove old GitHub entries
    sudo sed -i '/# GitHub/,/^$/d' "$hosts_file"
    
    # Add new entries
    echo "# GitHub" | sudo tee -a "$hosts_file"
    echo "$(get_ip github.com) github.com" | sudo tee -a "$hosts_file"
    echo "$(get_ip github.global.ssl.fastly.net) github.global.ssl.fastly.net" | sudo tee -a "$hosts_file"
    echo "$(get_ip assets-cdn.github.com) assets-cdn.github.com" | sudo tee -a "$hosts_file"
    echo "$(get_ip github.io) github.io" | sudo tee -a "$hosts_file"
    echo "$(get_ip api.github.com) api.github.com" | sudo tee -a "$hosts_file"
    echo "$(get_ip raw.githubusercontent.com) raw.githubusercontent.com" | sudo tee -a "$hosts_file"
    echo "" | sudo tee -a "$hosts_file"
}

# Flush DNS cache
flush_dns() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sudo dscacheutil -flushcache
        sudo killall -HUP mDNSResponder
    else
        sudo systemd-resolve --flush-caches
    fi
}

echo "Updating GitHub IP addresses..."
update_hosts
echo "Flushing DNS cache..."
flush_dns
echo "Done!"
```

## Method 2: Use GitHub Acceleration Proxy

### Public Proxy Services

| Service | URL | Description |
|---------|-----|-------------|
| GHProxy | https://ghproxy.com | Free, supports multiple operations |
| GitHub Mirror | https://mirror.ghproxy.com | Stable and reliable |
| Dev-sidecar | https://github.com/docmirror/dev-sidecar | Open source client |

### Use GHProxy to Accelerate Downloads

```bash
# Accelerate clone
git clone https://ghproxy.com/https://github.com/user/repo.git

# Accelerate file download
wget https://ghproxy.com/https://github.com/user/repo/raw/main/file.zip
```

### Use Dev-sidecar

1. Download and install Dev-sidecar
2. Start service
3. Automatically accelerate GitHub access

## Method 3: Configure Git Proxy

If you have a proxy server:

```bash
# Configure HTTP proxy
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# Configure SOCKS5 proxy
git config --global http.proxy socks5://127.0.0.1:7890
git config --global https.proxy socks5://127.0.0.1:7890

# Remove proxy
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## Method 4: Use Domestic Mirrors

### GitHub Mirror Sites

| Mirror | URL | Description |
|--------|-----|-------------|
| Gitee | https://gitee.com | Largest domestic code hosting platform |
| GitCode | https://gitcode.com | Under CSDN |
| CODING | https://coding.net | Tencent Cloud DevOps |

### Clone from Mirror

```bash
# Clone from Gitee mirror
git clone https://gitee.com/mirrors/user-repo.git
```

## Method 5: Use SSH Connection

SSH connection is usually more stable than HTTPS:

```bash
# Clone using SSH
git clone git@github.com:user/repo.git
```

## Method 6: Configure Git to Use SSH

```bash
# Convert HTTPS to SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

## FAQ

### Q: Clone speed is very slow?
**A:** Try the following methods:
1. Use SSH instead of HTTPS
2. Use shallow clone: `git clone --depth 1`
3. Use acceleration proxy

### Q: Push fails?
**A:** Check:
1. Whether SSH key is correctly configured
2. Whether network connection is normal
3. Try using proxy

### Q: GitHub Pages cannot be accessed?
**A:** May be blocked, try:
1. Use proxy to access
2. Configure custom domain
3. Use CDN acceleration

## Recommended Tools

| Tool | Description |
|------|-------------|
| Dev-sidecar | Open source GitHub acceleration tool |
| Watt Toolkit | Former Steam++, supports GitHub acceleration |
| Proxifier | Proxy client |

## Related Resources

- [GitHub Official Documentation](https://docs.github.com)
---
type: Reference
title: Download for Linux
date_created: 2026-07-01
source_url: https://antigravity.google/download/linux
description: Download CLI for Linux environments.
tags: [concept, llms-txt, js-rendered]
platform: cli
---

## deb-based Linux distributions (eg. Debian, Ubuntu)

### 1. Add the repository to sources.list.d

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://us-central1-apt.pkg.dev/doc/repo-signing-key.gpg | \
  sudo gpg --dearmor --yes -o /etc/apt/keyrings/antigravity-repo-key.gpg
echo "deb [signed-by=/etc/apt/keyrings/antigravity-repo-key.gpg] https://us-central1-apt.pkg.dev/projects/antigravity-auto-updater-dev/ antigravity-debian main" | \
  sudo tee /etc/apt/sources.list.d/antigravity.list > /dev/null
```

### 2. Update the package cache

```
sudo apt update
```

### 3. Install the package

```
sudo apt install antigravity
```

## rpm-based Linux distributions (eg. Red Hat, Fedora, SUSE)

### 1. Add the repository to /etc/yum.repos.d

```
sudo tee /etc/yum.repos.d/antigravity.repo << EOL
[antigravity-rpm]
name=Antigravity RPM Repository
baseurl=https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm
enabled=1
gpgcheck=0
EOL
```

### 2. Update the package cache

```
sudo dnf makecache
```

### 3. Install the package

```
sudo dnf install antigravity
```

Using another distribution? You can download the source tarball [here](https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/1.23.2-4781536860569600/linux-x64/Antigravity.tar.gz).

Using MacOS or Windows? [View all download options](/download)
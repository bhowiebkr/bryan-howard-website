# Phase 1: Repository Setup - Implementation Guide

**Duration**: Week 1  
**Prerequisites**: GitHub account, Git installed locally  
**Goal**: Complete repository and development environment setup for Pelican + GitHub Pages

## Overview

This phase establishes the foundation for your personal website by configuring the GitHub repository, setting up GitHub Pages, and preparing your local development environment.

## 📋 Checklist Overview

- [ ] 1.1 Configure GitHub Repository
- [ ] 1.2 Set up GitHub Pages 
- [ ] 1.3 Configure Custom Domain (`bryan-howard.ca`)
- [ ] 1.4 Set up Local Development Environment
- [ ] 1.5 Test Basic Pelican Installation
- [ ] 1.6 Verify GitHub Pages Deployment

---

## 🔧 Task 1.1: Configure GitHub Repository

### ✅ Current Repository Analysis
**Repository**: `https://github.com/bhowiebkr/bryan-howard-website`

### 📝 Steps:

#### 1.1.1 Verify Repository Settings
```bash
# Clone repository (if not already local)
git clone https://github.com/bhowiebkr/bryan-howard-website.git
cd bryan-howard-website
```

#### 1.1.2 Ensure Repository is Public
1. Navigate to: `https://github.com/bhowiebkr/bryan-howard-website/settings`
2. Scroll to **"Danger Zone"** section
3. Verify repository visibility is **"Public"**
4. If private, click **"Change visibility"** → **"Make public"**

#### 1.1.3 Configure Repository Description and Topics
1. Go to main repository page
2. Click **"⚙️"** next to "About"
3. **Description**: `Personal website of Bryan Howard - Developer, Content Creator, Problem Solver`
4. **Website**: `https://bryan-howard.ca`
5. **Topics**: `pelican`, `github-pages`, `personal-website`, `python`, `static-site`

#### 1.1.4 Create Initial File Structure
```bash
# Create basic directory structure
mkdir -p docs content theme plugins scripts tests .github/workflows

# Create .gitignore
cat > .gitignore << 'EOF'
# Pelican
output/
cache/
__pycache__/
*.pyc

# Python
.venv/
pelican-env/
*.egg-info/
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Logs
*.log
EOF
```

---

## 🌐 Task 1.2: Set up GitHub Pages

### 📝 Steps:

#### 1.2.1 Enable GitHub Pages
1. Navigate to: `https://github.com/bhowiebkr/bryan-howard-website/settings/pages`
2. **Source**: Select **"Deploy from a branch"**
3. **Branch**: Select **"gh-pages"** (will be created later by GitHub Actions)
4. **Folder**: Select **"/ (root)"**
5. Click **"Save"**

#### 1.2.2 Verify GitHub Actions Permissions
1. Go to: `https://github.com/bhowiebkr/bryan-howard-website/settings/actions`
2. **Actions permissions**: Select **"Allow all actions and reusable workflows"**
3. **Workflow permissions**: Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **"Save"**

---

## 🔗 Task 1.3: Configure Custom Domain

### 📝 Steps:

#### 1.3.1 Add Domain to GitHub Pages
1. In GitHub Pages settings (from Task 1.2)
2. **Custom domain**: Enter `bryan-howard.ca`
3. Click **"Save"**
4. Wait for DNS check (may take a few minutes)

#### 1.3.2 Configure DNS Records
**At your domain registrar** (where you registered `bryan-howard.ca`):

```dns
# A Records (Apex domain)
Type: A
Name: @
Value: 185.199.108.153

Type: A  
Name: @
Value: 185.199.109.153

Type: A
Name: @  
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153

# CNAME Record (www subdomain)
Type: CNAME
Name: www
Value: bhowiebkr.github.io
```

#### 1.3.3 Verify DNS Propagation
```bash
# Check DNS propagation (may take 24-48 hours)
nslookup bryan-howard.ca
dig bryan-howard.ca

# Check when ready
curl -I https://bryan-howard.ca
```

---

## 💻 Task 1.4: Set up Local Development Environment

### 📝 Steps:

#### 1.4.1 Verify Python Installation
```bash
# Check Python version (3.8+ required)
python --version
# or
python3 --version

# If Python not installed, download from: https://python.org
```

#### 1.4.2 Create Virtual Environment
```bash
# Navigate to project directory
cd bryan-howard-website

# Create virtual environment
python -m venv pelican-env

# Activate virtual environment
# Windows:
pelican-env\Scripts\activate
# Mac/Linux:
source pelican-env/bin/activate

# Verify activation (should show (pelican-env) in prompt)
which python
```

#### 1.4.3 Create Requirements File
```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
pelican[markdown]==4.9.1
beautifulsoup4==4.12.2
typogrify==2.0.7
pelican-sitemap==1.0.2
requests==2.31.0
markdown==3.5.1
pygments==2.16.1
ghp-import==2.1.0
EOF
```

#### 1.4.4 Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pelican --version
```

---

## 🧪 Task 1.5: Test Basic Pelican Installation

### 📝 Steps:

#### 1.5.1 Initialize Pelican Project
```bash
# Run Pelican quickstart
pelican-quickstart

# Answer prompts:
# Where do you want to create your new web site? [.] 
# What will be the title of this web site? Bryan Howard
# Who will be the author of this web site? Bryan Howard
# What will be the default language of this web site? [en]
# Do you want to specify a URL prefix? (Y/n) Y
# What is your URL prefix? https://bryan-howard.ca
# Do you want to enable article pagination? (Y/n) Y
# How many articles per page? [10]
# What is your time zone? [Europe/Rome] America/Toronto
# Do you want to generate a tasks.py/Makefile? (Y/n) Y
# Do you want to upload using FTP? (y/N) N
# Do you want to upload using SSH? (y/N) N
# Do you want to upload using Dropbox? (y/N) N
# Do you want to upload using S3? (y/N) N
# Do you want to upload using Rackspace Cloud Files? (y/N) N
# Do you want to upload using GitHub Pages? (y/N) Y
# Is this your personal page (username.github.io)? (y/N) N
```

#### 1.5.2 Create Test Content
```bash
# Create test blog post
mkdir -p content/blog/2025
cat > content/blog/2025/welcome.md << 'EOF'
Title: Welcome to My New Website
Date: 2025-01-15 10:00
Category: General
Tags: website, pelican, python
Slug: welcome
Author: Bryan Howard
Summary: Welcome to my new personal website built with Pelican!

# Welcome!

This is my new personal website built with Pelican, a Python-powered static site generator.

## Features

- Fast static site generation
- Markdown support
- Python-based
- GitHub Pages hosting
- Custom domain support

Stay tuned for more content!
EOF

# Create about page
mkdir -p content/pages
cat > content/pages/about.md << 'EOF'
Title: About
Slug: about

# About Bryan Howard

I'm a passionate developer with expertise in Python, web development, and content creation.

## Skills
- Python Development
- Web Development
- Content Creation
- YouTube Production

## Links
- [GitHub](https://github.com/bhowiebkr)
- [YouTube](https://www.youtube.com/@BryanHoward)
EOF
```

#### 1.5.3 Test Local Build
```bash
# Build site
pelican content

# Start development server
pelican --listen --autoreload

# Open browser to: http://localhost:8000
# Verify site loads and displays content
```

---

## 🚀 Task 1.6: Verify GitHub Pages Deployment

### 📝 Steps:

#### 1.6.1 Commit Initial Setup
```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial Pelican setup with test content

- Add basic Pelican configuration
- Create test blog post and about page
- Add requirements.txt with dependencies
- Configure .gitignore for Python/Pelican

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git push origin main
```

#### 1.6.2 Verify Repository Update
1. Navigate to: `https://github.com/bhowiebkr/bryan-howard-website`
2. Verify files are uploaded
3. Check that GitHub recognizes the repository structure

#### 1.6.3 Check GitHub Pages Status
1. Go to: `https://github.com/bhowiebkr/bryan-howard-website/settings/pages`
2. Look for green checkmark and message: **"Your site is published at..."**
3. Note: Full setup will complete in Phase 2 with GitHub Actions

---

## ✅ Phase 1 Completion Checklist

### Repository Configuration ✓
- [ ] Repository is public
- [ ] Description and topics added
- [ ] Basic directory structure created
- [ ] .gitignore configured

### GitHub Pages Setup ✓
- [ ] GitHub Pages enabled
- [ ] Custom domain (`bryan-howard.ca`) configured
- [ ] DNS records updated
- [ ] Actions permissions configured

### Development Environment ✓
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Pelican installation verified

### Initial Content ✓
- [ ] Pelican project initialized
- [ ] Test blog post created
- [ ] About page created
- [ ] Local build successful
- [ ] Development server working

### Version Control ✓
- [ ] Changes committed to Git
- [ ] Code pushed to GitHub
- [ ] Repository structure verified

---

## 🔗 Next Steps

**Phase 2: Basic Site Structure** will cover:
- GitHub Actions workflow implementation
- Production Pelican configuration
- Automated deployment setup
- Content structure optimization

## 📞 Troubleshooting

### Common Issues:

**Python/Pelican Installation Issues:**
```bash
# If pip install fails
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel

# If virtual environment issues
deactivate
rm -rf pelican-env
python -m venv pelican-env
```

**DNS Configuration Issues:**
- DNS changes can take 24-48 hours to propagate
- Use online DNS checker tools
- Verify records with domain registrar

**GitHub Pages Issues:**
- Ensure repository is public
- Check Actions permissions
- Verify custom domain spelling

## 📚 Resources

- [Pelican Documentation](https://docs.getpelican.com/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [DNS Configuration Guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

**Phase 1 Complete!** 🎉  
**Estimated Time**: 2-4 hours  
**Next**: Phase 2 - Basic Site Structure
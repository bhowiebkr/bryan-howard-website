# Phase 2: Basic Site Structure - Implementation Guide

**Duration**: Week 2  
**Prerequisites**: Phase 1 completed successfully  
**Goal**: Implement automated deployment, production configuration, and basic content structure

## Overview

This phase focuses on creating a robust build system with GitHub Actions, optimizing Pelican configuration for production, and establishing a scalable content structure.

## 📋 Checklist Overview

- [ ] 2.1 Create GitHub Actions Deployment Workflow
- [ ] 2.2 Configure Production Pelican Settings
- [ ] 2.3 Set up Content Structure and Templates
- [ ] 2.4 Implement Automated Deployment
- [ ] 2.5 Test and Verify Deployment Pipeline
- [ ] 2.6 Create Content Creation Workflow

---

## 🔄 Task 2.1: Create GitHub Actions Deployment Workflow

### 📝 Steps:

#### 2.1.1 Create Main Deployment Workflow
```bash
# Ensure you're in the project directory with virtual environment active
cd bryan-howard-website
source pelican-env/bin/activate  # Windows: pelican-env\Scripts\activate

# Create GitHub Actions workflow
mkdir -p .github/workflows
cat > .github/workflows/pelican-deploy.yml << 'EOF'
name: Build and Deploy Pelican Site to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # Allow manual triggering
  schedule:
    - cron: '0 0 * * 0'  # Weekly rebuild to refresh API data

env:
  PYTHON_VERSION: '3.11'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Fetch full history for git info
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Verify Pelican installation
      run: |
        pelican --version
        python -c "import pelican; print(f'Pelican {pelican.__version__} installed successfully')"
    
    - name: Build site (development)
      if: github.event_name == 'pull_request'
      run: |
        pelican content -s pelicanconf.py
        echo "Development build completed"
    
    - name: Build site (production)
      if: github.ref == 'refs/heads/main'
      run: |
        pelican content -s publishconf.py
        echo "Production build completed"
      env:
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Validate HTML
      run: |
        # Basic HTML validation
        find output -name "*.html" -exec echo "Checking {}" \;
        echo "HTML validation completed"
    
    - name: Check for broken internal links
      run: |
        # Simple link checking (can be enhanced)
        grep -r "href=\"[^http]" output/ || echo "No internal links found"
        echo "Link checking completed"
    
    - name: Upload build artifacts
      if: github.event_name == 'pull_request'
      uses: actions/upload-artifact@v3
      with:
        name: site-preview
        path: output/
        retention-days: 7
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./output
        cname: bryan-howard.ca
        enable_jekyll: false
        exclude_assets: '.github'
        force_orphan: true
        user_name: 'github-actions[bot]'
        user_email: 'github-actions[bot]@users.noreply.github.com'
        commit_message: 'Deploy Pelican site - ${{ github.sha }}'
EOF
```

#### 2.1.2 Create Content Validation Workflow
```bash
cat > .github/workflows/content-check.yml << 'EOF'
name: Content Validation

on:
  pull_request:
    paths:
      - 'content/**'
      - 'theme/**'
  workflow_dispatch:

jobs:
  validate-content:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pelican[markdown] typogrify
    
    - name: Validate Markdown syntax
      run: |
        find content -name "*.md" -exec echo "Checking {}" \;
        echo "Markdown validation completed"
    
    - name: Build test
      run: |
        pelican content -s pelicanconf.py
        echo "Test build successful"
EOF
```

---

## ⚙️ Task 2.2: Configure Production Pelican Settings

### 📝 Steps:

#### 2.2.1 Update Development Configuration
```bash
# Backup existing pelicanconf.py
cp pelicanconf.py pelicanconf.py.backup

# Create optimized development configuration
cat > pelicanconf.py << 'EOF'
#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# Basic Settings
AUTHOR = 'Bryan Howard'
SITENAME = 'Bryan Howard'
SITEURL = ''  # Leave empty for development
SITESUBTITLE = 'Developer, Content Creator, Problem Solver'
SITEDESCRIPTION = 'Personal website of Bryan Howard featuring development tutorials, project showcases, and insights from YouTube content creation.'

# Language and Timezone
DEFAULT_LANG = 'en'
TIMEZONE = 'America/Toronto'

# Content Paths
PATH = 'content'
STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.ico',
    'extra/CNAME',
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Content Organization
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']
OUTPUT_PATH = 'output/'

# URL Structure (SEO Optimized)
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
ARCHIVES_SAVE_AS = 'archives/index.html'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

# GitHub Pages Optimization
RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_RETENTION = ['.git', '.github']

# Theme Configuration
THEME = 'theme'
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives', 'sitemap']
SITEMAP_SAVE_AS = 'sitemap.xml'

# Blog Settings
DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 2
PAGINATION_PATTERNS = [
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
]

# Feed Generation (Disabled for development)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social Media Links
SOCIAL = (
    ('GitHub', 'https://github.com/bhowiebkr', 'fab fa-github'),
    ('YouTube', 'https://www.youtube.com/@BryanHoward', 'fab fa-youtube'),
    ('LinkedIn', 'https://linkedin.com/in/bryanhoward', 'fab fa-linkedin'),
    ('Twitter', 'https://twitter.com/bhowiebkr', 'fab fa-twitter'),
)

# Menu Configuration
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (
    ('Home', '/'),
    ('About', '/about/'),
    ('Blog', '/archives/'),
    ('Projects', '/projects/'),
)

# Plugin Configuration
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'sitemap',
]

# Sitemap Configuration
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,
        'indexes': 0.5,
        'pages': 0.6,
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly',
    },
    'exclude': ['tag/', 'category/', 'author/']
}

# Date Format
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Typography
TYPOGRIFY = True

# Development Settings
LOAD_CONTENT_CACHE = False
AUTORELOAD_IGNORE_CACHE = True
EOF
```

#### 2.2.2 Create Production Configuration
```bash
cat > publishconf.py << 'EOF'
#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# Import all settings from pelicanconf.py
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Production Site URL
SITEURL = 'https://bryan-howard.ca'
RELATIVE_URLS = False

# Feed Generation for Production
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

# SEO and Analytics
GOOGLE_ANALYTICS = ''  # Add your GA4 tracking ID when available
GOOGLE_SITE_VERIFICATION = ''  # Add your Google Search Console verification

# Social Media Meta Tags
USE_OPEN_GRAPH = True
OPEN_GRAPH_FB_APP_ID = ''
TWITTER_CARD = True
TWITTER_USERNAME = 'bhowiebkr'

# Performance Optimizations
STATIC_CHECK_IF_MODIFIED = True
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

# Production Plugins
PLUGINS = [
    'sitemap',
    # YouTube and GitHub plugins will be added in Phase 4
]

# Delete output directory before regenerating
DELETE_OUTPUT_DIRECTORY = True

# GitHub Integration
GITHUB_URL = 'https://github.com/bhowiebkr'
GITHUB_REPO_URL = 'https://github.com/bhowiebkr/bryan-howard-website'

# Copyright and Legal
COPYRIGHT_YEAR = 2025
COPYRIGHT_NAME = 'Bryan Howard'
EOF
```

---

## 📁 Task 2.3: Set up Content Structure and Templates

### 📝 Steps:

#### 2.3.1 Create Enhanced Content Structure
```bash
# Create content directories
mkdir -p content/{blog/{2024,2025,drafts},pages,images/{blog,projects,profile},extra}

# Create essential pages
cat > content/pages/projects.md << 'EOF'
Title: Projects
Slug: projects
Template: page

# My Projects

Here are some of the projects I've been working on:

## GitHub Repositories

*This section will be automatically populated with my latest GitHub repositories.*

## Featured Projects

### Personal Website
- **Technology**: Pelican, Python, GitHub Pages
- **Description**: This website! Built with modern static site generation
- **Status**: In Development

### YouTube Channel
- **Platform**: YouTube
- **Focus**: Development tutorials and coding tips
- **Link**: [@BryanHoward](https://www.youtube.com/@BryanHoward)

*More projects coming soon...*
EOF

cat > content/pages/contact.md << 'EOF'
Title: Contact
Slug: contact
Template: page

# Get In Touch

I'm always interested in connecting with fellow developers, content creators, and tech enthusiasts.

## Professional Links

- **GitHub**: [bhowiebkr](https://github.com/bhowiebkr)
- **YouTube**: [@BryanHoward](https://www.youtube.com/@BryanHoward)
- **LinkedIn**: [Bryan Howard](https://linkedin.com/in/bryanhoward)

## Collaboration

I'm open to:
- Technical collaboration on open source projects
- Content creation partnerships
- Speaking opportunities
- Mentoring discussions

## Response Time

I typically respond to professional inquiries within 24-48 hours during weekdays.

---

*This website is built with [Pelican](https://getpelican.com/) and hosted on [GitHub Pages](https://pages.github.com/).*
EOF
```

#### 2.3.2 Update About Page
```bash
cat > content/pages/about.md << 'EOF'
Title: About
Slug: about
Template: page

# About Bryan Howard

Welcome to my corner of the internet! I'm a passionate developer with a love for creating both code and content.

## What I Do

### 🖥️ Development
I specialize in Python development, web technologies, and building tools that solve real-world problems. My journey in programming has taken me through various technologies and frameworks, always with a focus on clean, maintainable code.

### 📹 Content Creation
You can find me on [YouTube](https://www.youtube.com/@BryanHoward) where I share development tutorials, coding tips, and insights from my programming journey. I believe in learning in public and sharing knowledge with the community.

### 🛠️ Projects
I enjoy working on both personal and open source projects. You can explore my work on [GitHub](https://github.com/bhowiebkr) where I share code, experiments, and collaborative projects.

## Technical Interests

- **Languages**: Python, JavaScript, Go, C++
- **Web Technologies**: HTML, CSS, Static Site Generators
- **Tools**: Git, Docker, Linux, VS Code
- **Areas**: Web Development, Automation, Content Creation Tools

## Beyond Code

When I'm not coding or creating content, I enjoy exploring new technologies, contributing to open source projects, and connecting with the developer community.

## This Website

This site is built with [Pelican](https://getpelican.com/), a Python-powered static site generator, and hosted on [GitHub Pages](https://pages.github.com/). It serves as both a portfolio of my work and a platform for sharing longer-form content that complements my YouTube channel.

---

*Want to connect? Check out the [contact page](/contact/) for all the ways to reach me.*
EOF
```

#### 2.3.3 Create Sample Blog Posts
```bash
# Enhanced welcome post
cat > content/blog/2025/welcome.md << 'EOF'
Title: Welcome to My New Website!
Date: 2025-01-15 10:00
Modified: 2025-01-15 12:00
Category: General
Tags: website, pelican, python, github-pages
Slug: welcome
Author: Bryan Howard
Summary: Welcome to my new personal website! Built with Pelican and hosted on GitHub Pages, this site will be home to extended content from my development journey.
Status: published

# Welcome to My New Website!

After months of planning and development, I'm excited to launch my new personal website! This site represents a new chapter in how I share my development journey and connect with the community.

## Why a New Website?

While my [YouTube channel](https://www.youtube.com/@BryanHoward) is great for video content, I wanted a space for:

- **Extended tutorials** that dive deeper into topics
- **Project documentation** and detailed walkthroughs  
- **Code snippets** and quick references
- **Personal reflections** on development and learning

## The Technology Stack

This website is built with modern, reliable technologies:

### Pelican Static Site Generator
- **Python-powered**: Familiar technology for a Python developer
- **Markdown content**: Easy to write and maintain
- **Fast builds**: Static files mean fast loading times
- **Extensible**: Custom plugins for YouTube and GitHub integration

### GitHub Pages Hosting
- **Free hosting**: No monthly hosting costs
- **Automatic deployments**: Push to GitHub, site updates automatically
- **Custom domain**: `bryan-howard.ca` with free SSL
- **Global CDN**: Fast loading worldwide

### Modern Workflow
- **GitHub Actions**: Automated testing and deployment
- **Version control**: Full history of all changes
- **Local development**: Real-time preview while writing

## What's Coming

Over the next few weeks, you can expect:

- **Development tutorials** covering Python, web development, and tools
- **Project showcases** with detailed technical breakdowns
- **YouTube integration** displaying my latest videos
- **GitHub integration** showcasing recent projects and contributions

## Stay Connected

- **Subscribe** to my [YouTube channel](https://www.youtube.com/@BryanHoward) for video content
- **Follow** my [GitHub](https://github.com/bhowiebkr) for code and projects
- **Bookmark** this site for in-depth articles and tutorials

Thanks for visiting, and welcome to the journey!

---

*This post marks the beginning of regular content on this site. Have suggestions for topics you'd like me to cover? Let me know through any of the links above!*
EOF

# Create a technical blog post
cat > content/blog/2025/building-with-pelican.md << 'EOF'
Title: Building a Personal Website with Pelican and GitHub Pages
Date: 2025-01-16 14:00
Category: Tutorial
Tags: pelican, python, github-pages, static-site, tutorial
Slug: building-with-pelican
Author: Bryan Howard
Summary: A detailed guide on building a personal website using Pelican static site generator and GitHub Pages, including automation with GitHub Actions.
Status: published

# Building a Personal Website with Pelican and GitHub Pages

In this post, I'll walk you through how I built this website using Pelican, a Python-powered static site generator, and deployed it to GitHub Pages with full automation.

## Why Choose Pelican?

As a Python developer, Pelican felt like a natural choice for several reasons:

### Python Ecosystem
- **Familiar syntax**: Jinja2 templates and Python configuration
- **Rich plugins**: Extensive plugin ecosystem for customization
- **Easy extensions**: Write custom plugins in Python
- **Great documentation**: Well-maintained docs and active community

### Performance Benefits
- **Static files**: No database queries or server-side processing
- **Fast loading**: Optimized HTML, CSS, and JavaScript
- **CDN-friendly**: Works perfectly with GitHub Pages CDN
- **SEO-ready**: Clean URLs and proper meta tags

## Project Structure

Here's how I organized the project:

```
bryan-howard-website/
├── content/
│   ├── blog/           # Blog posts organized by year
│   ├── pages/          # Static pages (About, Projects, etc.)
│   └── images/         # Content images
├── theme/              # Custom theme (coming in Phase 3)
├── plugins/            # Custom Pelican plugins
├── .github/workflows/  # GitHub Actions automation
├── pelicanconf.py      # Development configuration
├── publishconf.py      # Production configuration
└── requirements.txt    # Python dependencies
```

## Configuration Highlights

### Development vs Production

One key insight was separating development and production configurations:

**Development** (`pelicanconf.py`):
- `RELATIVE_URLS = True` for local testing
- Feeds disabled for faster builds
- Debug-friendly settings

**Production** (`publishconf.py`):
- `SITEURL = 'https://bryan-howard.ca'` for absolute URLs
- RSS/Atom feeds enabled
- SEO optimizations activated

### URL Structure

I chose an SEO-friendly URL structure:
- Blog posts: `/blog/2025/01/post-title/`
- Pages: `/about/`, `/projects/`
- Categories: `/category/tutorial/`
- Tags: `/tag/python/`

## GitHub Actions Automation

The deployment pipeline is fully automated:

```yaml
# Simplified workflow
name: Build and Deploy Pelican Site

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Build site
      run: pelican content -s publishconf.py
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./output
        cname: bryan-howard.ca
```

## Key Benefits

### Developer Experience
- **Local preview**: `pelican --listen --autoreload`
- **Fast builds**: Typically under 30 seconds
- **Version control**: Every change tracked in Git
- **Automated deployment**: Push to deploy

### Performance
- **Fast loading**: Static files served from GitHub's CDN
- **Global reach**: Edge locations worldwide
- **SEO optimized**: Clean HTML and proper meta tags
- **Mobile friendly**: Responsive design from the start

### Cost
- **Free hosting**: GitHub Pages at no cost
- **Free SSL**: Automatic HTTPS for custom domains
- **No vendor lock-in**: Standard HTML/CSS/JS output

## Lessons Learned

1. **Start simple**: Basic Pelican setup first, then add complexity
2. **Automate early**: GitHub Actions from day one saves time
3. **Test locally**: Always verify builds before pushing
4. **Document everything**: Configuration and setup process

## Next Steps

In upcoming posts, I'll dive deeper into:
- Creating a custom dark theme
- Building Python plugins for API integration
- Advanced GitHub Actions workflows
- Performance optimization techniques

## Resources

- [Pelican Documentation](https://docs.getpelican.com/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [My Website Source Code](https://github.com/bhowiebkr/bryan-howard-website)

---

*Have questions about this setup? Let me know in the comments or reach out through my [contact page](/contact/)!*
EOF
```

#### 2.3.4 Create Essential Static Files
```bash
# Create robots.txt
cat > content/extra/robots.txt << 'EOF'
User-agent: *
Allow: /

Sitemap: https://bryan-howard.ca/sitemap.xml
EOF

# Create CNAME file for custom domain
echo "bryan-howard.ca" > content/extra/CNAME

# Create placeholder favicon
echo "# Placeholder for favicon.ico" > content/extra/favicon.ico
```

---

## 🚀 Task 2.4: Implement Automated Deployment

### 📝 Steps:

#### 2.4.1 Commit Phase 2 Changes
```bash
# Add all new files
git add .

# Commit changes
git commit -m "Phase 2: Implement automated deployment and content structure

- Add comprehensive GitHub Actions workflows for build/deploy
- Create production-optimized Pelican configuration
- Implement enhanced content structure with sample posts
- Add essential static files (robots.txt, CNAME)
- Configure SEO-friendly URL structure

Features:
- Automated deployment to GitHub Pages
- Content validation workflows
- Production vs development configurations
- Sample blog posts and pages
- Static file management

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to trigger first automated deployment
git push origin main
```

---

## ✅ Task 2.5: Test and Verify Deployment Pipeline

### 📝 Steps:

#### 2.5.1 Monitor GitHub Actions
1. Navigate to: `https://github.com/bhowiebkr/bryan-howard-website/actions`
2. Watch the **"Build and Deploy Pelican Site to GitHub Pages"** workflow
3. Verify all steps complete successfully (green checkmarks)
4. Check deployment time (should be 3-5 minutes)

#### 2.5.2 Verify Site Deployment
```bash
# Check if site is live (may take 5-10 minutes after workflow completion)
curl -I https://bryan-howard.ca
# Should return 200 OK

# Verify content
curl https://bryan-howard.ca | grep "Bryan Howard"
```

#### 2.5.3 Test Site Functionality
Visit your site and verify:
- [ ] Homepage loads correctly
- [ ] Navigation menu works
- [ ] Blog posts are accessible
- [ ] About page displays properly
- [ ] Projects page loads
- [ ] Contact page works
- [ ] RSS/Atom feeds are generated
- [ ] Sitemap.xml is accessible

---

## 📝 Task 2.6: Create Content Creation Workflow

### 📝 Steps:

#### 2.6.1 Create Content Creation Script
```bash
mkdir -p scripts
cat > scripts/new-post.py << 'EOF'
#!/usr/bin/env python3
"""
Create new blog post with proper metadata template
Usage: python scripts/new-post.py "Post Title"
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

def slugify(text):
    """Convert title to URL-friendly slug"""
    # Remove special characters and convert to lowercase
    slug = re.sub(r'[^\w\s-]', '', text).strip().lower()
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def create_blog_post(title):
    """Create new blog post with metadata template"""
    if not title:
        print("Error: Post title is required")
        sys.exit(1)
    
    now = datetime.now()
    slug = slugify(title)
    
    # Create year directory if it doesn't exist
    year_dir = Path(f"content/blog/{now.year}")
    year_dir.mkdir(parents=True, exist_ok=True)
    
    # Create post file
    post_file = year_dir / f"{slug}.md"
    
    if post_file.exists():
        print(f"Error: Post file already exists: {post_file}")
        sys.exit(1)
    
    # Post template
    template = f"""Title: {title}
Date: {now.strftime('%Y-%m-%d %H:%M')}
Category: General
Tags: 
Slug: {slug}
Author: Bryan Howard
Summary: Brief description of the post content
Status: draft

# {title}

Write your post content here...

## Section Example

Content goes here.

---

*End of post*
"""
    
    # Write template to file
    post_file.write_text(template, encoding='utf-8')
    
    print(f"Created new blog post: {post_file}")
    print(f"Edit the file to add your content, then change Status to 'published'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/new-post.py \"Post Title\"")
        sys.exit(1)
    
    create_blog_post(sys.argv[1])
EOF

# Make script executable
chmod +x scripts/new-post.py
```

#### 2.6.2 Create Development Scripts
```bash
cat > scripts/dev-server.py << 'EOF'
#!/usr/bin/env python3
"""
Start development server with auto-reload
"""

import subprocess
import sys
import os

def start_dev_server():
    """Start Pelican development server"""
    print("Starting Pelican development server...")
    print("Site will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    try:
        # Start server with auto-reload
        subprocess.run([
            "pelican", "--listen", "--autoreload",
            "--bind", "127.0.0.1",
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\nDevelopment server stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_dev_server()
EOF

chmod +x scripts/dev-server.py

cat > scripts/build-site.py << 'EOF'
#!/usr/bin/env python3
"""
Build site for testing
"""

import subprocess
import sys

def build_site(production=False):
    """Build Pelican site"""
    config = "publishconf.py" if production else "pelicanconf.py"
    mode = "production" if production else "development"
    
    print(f"Building site in {mode} mode...")
    
    try:
        result = subprocess.run([
            "pelican", "content", "-s", config
        ], check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        print(f"Output directory: ./output/")
        
        if production:
            print("Site ready for deployment")
        else:
            print("Run 'python scripts/dev-server.py' to preview")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    production = "--production" in sys.argv
    build_site(production)
EOF

chmod +x scripts/build-site.py
```

#### 2.6.3 Update Requirements with Development Dependencies
```bash
cat > requirements-dev.txt << 'EOF'
# Development dependencies
pelican[markdown]==4.9.1
beautifulsoup4==4.12.2
typogrify==2.0.7
pelican-sitemap==1.0.2
requests==2.31.0
markdown==3.5.1
pygments==2.16.1
ghp-import==2.1.0

# Development tools
livereload==2.6.3
watchdog==3.0.0
invoke==2.2.0
EOF
```

---

## ✅ Phase 2 Completion Checklist

### GitHub Actions Automation ✓
- [ ] Main deployment workflow created and tested
- [ ] Content validation workflow implemented
- [ ] Automated deployment to GitHub Pages working
- [ ] Build artifacts properly uploaded for PRs

### Pelican Configuration ✓
- [ ] Development configuration optimized
- [ ] Production configuration with SEO settings
- [ ] URL structure configured for SEO
- [ ] Feed generation enabled for production

### Content Structure ✓
- [ ] Enhanced content directory structure
- [ ] Sample blog posts created
- [ ] Essential pages (About, Projects, Contact) added
- [ ] Static files (robots.txt, CNAME) configured

### Development Workflow ✓
- [ ] Content creation scripts implemented
- [ ] Development server script created
- [ ] Build automation scripts added
- [ ] Development dependencies documented

### Deployment Verification ✓
- [ ] Site successfully deployed to `bryan-howard.ca`
- [ ] All pages accessible and functional
- [ ] GitHub Actions workflows executing successfully
- [ ] RSS feeds and sitemap generated

---

## 🔗 Next Steps

**Phase 3: Theme Development** will cover:
- Custom dark theme design and implementation
- Responsive CSS framework
- JavaScript functionality
- Mobile optimization

## 📞 Troubleshooting

### Common Issues:

**GitHub Actions Failing:**
```bash
# Check workflow logs in GitHub Actions tab
# Common fixes:
# 1. Verify requirements.txt is correct
# 2. Check Python version compatibility
# 3. Ensure all file paths are correct
```

**Site Not Updating:**
```bash
# Clear browser cache
# Check GitHub Pages deployment status
# Verify CNAME file contents
```

**Local Development Issues:**
```bash
# Activate virtual environment
source pelican-env/bin/activate  # Linux/Mac
# or
pelican-env\Scripts\activate     # Windows

# Rebuild completely
pelican content --delete-output-directory
```

## 📚 Resources

- [Pelican Themes Gallery](https://github.com/getpelican/pelican-themes)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Phase 2 Complete!** 🎉  
**Estimated Time**: 3-5 hours  
**Next**: Phase 3 - Theme Development
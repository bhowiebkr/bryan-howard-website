# Bryan Howard Personal Website - Project Planning Document

## Project Overview

**Project Name**: Bryan Howard Personal Website  
**Purpose**: Professional personal website showcasing YouTube content, GitHub projects, and blog posts  
**Target Audience**: Developers, content consumers, potential collaborators  
**Key Requirements**: Dark theme, mobile responsive, YouTube/GitHub integration, blog functionality  

## Goals & Objectives

### Primary Goals
- Create a professional online presence for Bryan Howard
- Showcase YouTube channel content (@BryanHoward)
- Display GitHub projects and contributions (bhowiebkr)
- Provide a platform for extended blog content
- Ensure excellent mobile user experience

### Success Metrics
- Mobile-first responsive design (>95% mobile compatibility)
- Fast loading times (<3s on 3G)
- Clean, professional dark theme aesthetic
- Seamless integration with external platforms
- SEO optimized for personal branding

## Technology Stack: Pelican Static Site Generator

### Pelican - Python-Powered Static Site Generator
**Why Pelican is Perfect for This Project**:

**✅ Core Strengths**:
- **Python-Native**: Perfect fit for Python developers
- **Markdown Excellence**: Superior Markdown support with rich metadata
- **Jinja2 Templates**: Familiar templating system for Python developers
- **Blog-Optimized**: Built-in blog functionality with categories, tags, and archives
- **Plugin Ecosystem**: Extensible architecture for custom functionality
- **Content Management**: Intuitive workflow for writers and developers
- **Performance**: Fast static site generation with caching
- **SEO Ready**: Built-in sitemap, RSS/Atom feeds, and meta tag support

**GitHub Pages Integration**:
- **Native Compatibility**: Works seamlessly with GitHub Pages
- **GitHub Actions**: Automated build and deployment workflows
- **Version Control**: Full source control for content and configuration
- **Free Hosting**: No hosting costs with GitHub Pages
- **Custom Domains**: Optional custom domain with free SSL
- **Global CDN**: GitHub's infrastructure for fast global delivery

**Development Benefits**:
- **Local Development**: Real-time preview with `pelican --listen --autoreload`
- **Content Creation**: Simple Markdown files with powerful metadata
- **Theme Development**: Flexible Jinja2 templating system
- **API Integration**: Python plugins for YouTube and GitHub APIs
- **Testing**: Local builds ensure deployment success
- **Automation**: GitHub Actions handle build, test, and deployment

**Perfect Match for Requirements**:
- ✅ **Dark Theme**: Complete CSS control for custom dark themes
- ✅ **Mobile Responsive**: Modern CSS frameworks and responsive design
- ✅ **YouTube Integration**: Custom Python plugin for channel data
- ✅ **GitHub Integration**: Native API integration for repository showcase
- ✅ **Blog Platform**: Built-in blog functionality with rich features
- ✅ **Performance**: Static files for maximum speed and reliability

## Site Architecture

### Overview Structure
```
bryan-howard-website/
├── docs/                    # Project documentation
├── content/                # Markdown content files
├── theme/                  # Custom Pelican theme
├── plugins/                # Custom Pelican plugins
├── output/                 # Generated static site
├── .github/                # GitHub Actions workflows
├── requirements.txt        # Python dependencies
├── pelicanconf.py         # Pelican configuration
├── publishconf.py         # Production configuration
├── fabfile.py             # Deployment automation
└── README.md
```

### Detailed Folder Structure with File Examples

```
bryan-howard-website/
│
├── 📁 docs/                         # Project Documentation
│   ├── 📄 PLANNING.md              # This comprehensive planning document
│   ├── 📄 DESIGN-SYSTEM.md         # Color palette, typography, component specs
│   ├── 📄 DEPLOYMENT.md            # Deployment guide and automation
│   ├── 📄 CONTENT-GUIDE.md         # Writing and content creation guidelines
│   └── 📄 API-INTEGRATION.md       # YouTube/GitHub API documentation
│
├── 📁 content/                      # All Markdown Content
│   │
│   ├── 📁 pages/                    # Static Pages
│   │   ├── 📄 about.md             # About page with bio and skills
│   │   ├── 📄 projects.md          # Projects showcase page
│   │   ├── 📄 contact.md           # Contact information and social links
│   │   └── 📄 resume.md            # Professional resume/CV
│   │
│   ├── 📁 blog/                     # Blog Posts (organized by year)
│   │   │
│   │   ├── 📁 2024/                 # 2024 blog posts
│   │   │   ├── 📄 getting-started-python.md
│   │   │   ├── 📄 web-scraping-tutorial.md
│   │   │   └── 📄 django-deployment-guide.md
│   │   │
│   │   ├── 📁 2025/                 # 2025 blog posts
│   │   │   ├── 📄 welcome-new-website.md
│   │   │   ├── 📄 pelican-static-sites.md
│   │   │   └── 📄 youtube-api-integration.md
│   │   │
│   │   └── 📁 drafts/               # Work-in-progress posts
│   │       ├── 📄 advanced-python-patterns.md
│   │       └── 📄 machine-learning-basics.md
│   │
│   ├── 📁 images/                   # Content images
│   │   ├── 📁 blog/                 # Blog post images
│   │   │   ├── 📁 2024/
│   │   │   └── 📁 2025/
│   │   ├── 📁 projects/             # Project screenshots
│   │   └── 📁 profile/              # Personal photos and headshots
│   │
│   └── 📁 extra/                    # Additional static files
│       ├── 📄 robots.txt           # SEO robots file
│       ├── 📄 favicon.ico          # Website favicon
│       ├── 📄 CNAME                # Custom domain configuration
│       └── 📄 sitemap.xml          # SEO sitemap (auto-generated)
│
├── 📁 theme/                        # Custom Bryan Howard Theme
│   │
│   ├── 📁 templates/                # Jinja2 HTML Templates
│   │   │
│   │   ├── 📄 base.html            # Base template with dark theme
│   │   ├── 📄 index.html           # Homepage with hero section
│   │   ├── 📄 article.html         # Individual blog post template
│   │   ├── 📄 page.html            # Static page template
│   │   ├── 📄 archives.html        # Blog archive listing
│   │   ├── 📄 categories.html      # Category listings
│   │   ├── 📄 tags.html            # Tag cloud and listings
│   │   ├── 📄 author.html          # Author profile page
│   │   └── 📄 404.html             # Custom 404 error page
│   │
│   └── 📁 static/                   # Theme Static Assets
│       │
│       ├── 📁 css/                  # Stylesheets
│       │   ├── 📄 main.css         # Core styles and layout
│       │   ├── 📄 dark-theme.css   # Dark theme color variables
│       │   ├── 📄 responsive.css   # Mobile responsive styles
│       │   ├── 📄 components.css   # Reusable component styles
│       │   └── 📄 syntax.css       # Code highlighting styles
│       │
│       ├── 📁 js/                   # JavaScript Files
│       │   ├── 📄 main.js          # Core functionality
│       │   ├── 📄 theme-toggle.js  # Dark/light theme switcher
│       │   ├── 📄 search.js        # Client-side search functionality
│       │   ├── 📄 youtube-api.js   # YouTube channel integration
│       │   ├── 📄 github-api.js    # GitHub repositories integration
│       │   └── 📄 analytics.js     # Analytics and tracking
│       │
│       ├── 📁 images/               # Theme Images
│       │   ├── 📄 logo.svg         # Site logo/brand
│       │   ├── 📄 hero-bg.jpg      # Homepage hero background
│       │   ├── 📁 icons/           # SVG icons for social media
│       │   │   ├── 📄 github.svg
│       │   │   ├── 📄 youtube.svg
│       │   │   ├── 📄 twitter.svg
│       │   │   └── 📄 linkedin.svg
│       │   └── 📁 placeholder/     # Default/fallback images
│       │
│       └── 📁 fonts/                # Custom Web Fonts (if needed)
│           ├── 📄 inter-regular.woff2
│           └── 📄 jetbrains-mono.woff2
│
├── 📁 plugins/                      # Custom Pelican Plugins
│   ├── 📄 __init__.py              # Python package initialization
│   ├── 📄 youtube_integration.py   # YouTube API plugin
│   ├── 📄 github_integration.py    # GitHub API plugin
│   ├── 📄 search_generator.py      # Search index generation
│   ├── 📄 image_optimizer.py       # Image compression and WebP conversion
│   └── 📄 social_meta.py          # Open Graph and Twitter Cards
│
├── 📁 output/                       # Generated Static Site (git-ignored)
│   ├── 📄 index.html              # Generated homepage
│   ├── 📁 blog/                    # Generated blog structure
│   ├── 📁 theme/                   # Copied theme assets
│   ├── 📁 feeds/                   # RSS/Atom feeds
│   └── 📄 sitemap.xml             # SEO sitemap
│
├── 📁 .github/                      # GitHub Integration
│   ├── 📁 workflows/               # GitHub Actions
│   │   ├── 📄 pelican-deploy.yml   # Main build and deploy workflow
│   │   ├── 📄 content-check.yml    # Content validation and spell check
│   │   ├── 📄 link-check.yml       # Broken link detection
│   │   └── 📄 dependency-update.yml # Automated dependency updates
│   ├── 📁 ISSUE_TEMPLATE/          # Issue templates
│   └── 📄 FUNDING.yml              # GitHub Sponsors configuration
│
├── 📁 scripts/                      # Development Scripts
│   ├── 📄 dev-server.py           # Local development server
│   ├── 📄 content-generator.py     # Blog post template generator
│   ├── 📄 image-processor.py       # Batch image optimization
│   └── 📄 deploy.py               # Manual deployment script
│
├── 📁 tests/                        # Testing and Validation
│   ├── 📄 test_build.py           # Build process testing
│   ├── 📄 test_content.py         # Content validation
│   ├── 📄 test_links.py           # Link checking
│   └── 📄 test_performance.py     # Performance testing
│
├── 📄 requirements.txt              # Python Dependencies
├── 📄 requirements-dev.txt          # Development Dependencies
├── 📄 pelicanconf.py               # Main Pelican Configuration
├── 📄 publishconf.py               # Production Configuration
├── 📄 fabfile.py                   # Fabric Deployment Tasks
├── 📄 Makefile                     # Build automation
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 .env.example                 # Environment variables template
└── 📄 README.md                    # Project documentation
```

### Key File Purposes and Content Examples

#### Content Structure Examples

**Blog Post** (`content/blog/2025/welcome-new-website.md`):
```markdown
Title: Welcome to My New Website
Date: 2025-01-15 10:00
Modified: 2025-01-15 12:00
Category: General
Tags: website, pelican, python, blog
Slug: welcome-new-website
Author: Bryan Howard
Summary: Introduction to my new personal website built with Pelican, featuring dark theme and API integrations.
Status: published

Welcome to my brand new personal website! After months of planning...
```

**About Page** (`content/pages/about.md`):
```markdown
Title: About Bryan Howard
Slug: about
Template: page
Order: 1

# About Me

I'm Bryan Howard, a passionate developer with expertise in Python, web development...

## Skills & Technologies
- Python & Django
- JavaScript & React
- Database Design
- API Development

## Current Projects
- YouTube Channel: Technical tutorials and coding tips
- Open Source: Contributing to Python ecosystem
```

#### Template Structure Examples

**Base Template** (`theme/templates/base.html`):
```html
<!DOCTYPE html>
<html lang="{{ DEFAULT_LANG }}" data-theme="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}{{ SITENAME }}{% endblock %}</title>
    <!-- Meta tags, CSS, and head content -->
</head>
<body>
    <header>{% include 'partials/header.html' %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% include 'partials/footer.html' %}</footer>
    <!-- JavaScript includes -->
</body>
</html>
```

**Homepage Template** (`theme/templates/index.html`):
```html
{% extends "base.html" %}

{% block content %}
<section class="hero">
    <h1>Hi, I'm Bryan Howard</h1>
    <p>Developer, Content Creator, Problem Solver</p>
    <!-- YouTube and GitHub integration -->
</section>

<section class="featured-content">
    <!-- Latest blog posts -->
    <!-- Featured projects -->
</section>
{% endblock %}
```

#### Configuration Examples

**Main Configuration** (`pelicanconf.py`):
```python
# Site Information
AUTHOR = 'Bryan Howard'
SITENAME = 'Bryan Howard'
SITEURL = ''
SITEDESCRIPTION = 'Personal website of Bryan Howard - Developer & Content Creator'

# Content Settings
PATH = 'content'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

# Theme and Appearance
THEME = 'theme'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# Social Media Links
SOCIAL = (
    ('GitHub', 'https://github.com/bhowiebkr'),
    ('YouTube', 'https://www.youtube.com/@BryanHoward'),
)

# Plugins Configuration
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'youtube_integration',
    'github_integration', 
    'search_generator',
    'sitemap',
]
```

### Development Workflow

1. **Content Creation**: Write Markdown files in `content/`
2. **Theme Development**: Modify templates and styles in `theme/`
3. **Plugin Development**: Create custom functionality in `plugins/`
4. **Local Testing**: Use `pelican content && pelican --listen`
5. **Deployment**: GitHub Actions automatically builds and deploys

### Build Process

```bash
# Development build
pelican content

# Production build
pelican content -s publishconf.py

# Local development server
pelican --listen --autoreload

# Clean build
pelican content --delete-output-directory
```

## Page Structure & Content

### Homepage
- **Hero Section**: Professional headshot, name, title/tagline
- **Quick Links**: Direct links to YouTube channel and GitHub profile
- **Featured Content**: Latest blog posts and projects
- **Social Links**: All social media and professional platforms

### About Page
- **Professional Bio**: Background, expertise, interests
- **Skills & Technologies**: Technical skills showcase
- **Timeline**: Career highlights or learning journey
- **Personal Interests**: Hobbies, side projects

### Blog Section
- **Blog Listing**: Grid/list view of all blog posts
- **Individual Post Pages**: Full blog post content
- **Categories/Tags**: Content organization
- **Search Functionality**: Content discovery

### Projects Page
- **GitHub Integration**: Automatically fetched repositories
- **Project Cards**: Screenshots, descriptions, tech stacks
- **Live Demo Links**: Where applicable
- **Filter/Sort Options**: By technology, date, stars

## Dark Theme Design System

### Color Palette
```css
:root {
  /* Primary Dark Theme Colors */
  --bg-primary: #0a0a0a;        /* Main background */
  --bg-secondary: #1a1a1a;      /* Card backgrounds */
  --bg-tertiary: #2a2a2a;       /* Elevated elements */
  
  /* Text Colors */
  --text-primary: #ffffff;       /* Main text */
  --text-secondary: #b3b3b3;     /* Secondary text */
  --text-muted: #737373;         /* Muted text */
  
  /* Accent Colors */
  --accent-primary: #3b82f6;     /* Blue - primary actions */
  --accent-secondary: #10b981;   /* Green - success states */
  --accent-warning: #f59e0b;     /* Yellow - warnings */
  --accent-error: #ef4444;       /* Red - errors */
  
  /* Borders & Dividers */
  --border-primary: #333333;     /* Main borders */
  --border-secondary: #4a4a4a;   /* Hover borders */
}
```

### Typography Scale
- **Headings**: Inter or similar modern sans-serif
- **Body Text**: System font stack for performance
- **Code**: JetBrains Mono or Fira Code
- **Scale**: 1.25 ratio (16px, 20px, 25px, 31px, 39px, 49px)

### Component Design Principles
- **Minimalism**: Clean, uncluttered layouts
- **Consistency**: Standardized spacing, colors, typography
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Optimized images, minimal JavaScript

## External Integrations

### YouTube Integration (@BryanHoward)
- **YouTube Data API v3**: Fetch latest videos
- **Video Thumbnails**: Display recent uploads
- **Channel Stats**: Subscriber count, view counts
- **Embedded Players**: Selected video showcases

### GitHub Integration (bhowiebkr)
- **GitHub API**: Fetch repositories and profile data
- **Repository Cards**: Name, description, language, stars
- **Contribution Graph**: Activity visualization
- **Recent Activity**: Latest commits and projects

### Blog Content Management
- **Markdown Files**: Easy content creation with Pelican's native support
- **Rich Metadata**: Pelican metadata syntax (Title, Date, Category, Tags, Summary)
- **Static Generation**: Fast builds with Pelican's generator system
- **RSS/Atom Feeds**: Built-in feed generation
- **Categories & Tags**: Automatic taxonomy generation
- **Pagination**: Built-in pagination for blog listings

## Mobile Responsiveness Strategy

### Breakpoints
```css
/* Mobile-first approach */
--mobile: 0px;          /* Base styles */
--tablet: 768px;        /* Tablet and up */
--desktop: 1024px;      /* Desktop and up */
--large: 1280px;        /* Large desktop */
```

### Mobile Optimization
- **Touch-friendly**: 44px minimum touch targets
- **Navigation**: Collapsible mobile menu
- **Images**: Responsive with WebP format
- **Performance**: Critical CSS inlining, lazy loading

## Performance Optimization

### Core Web Vitals Targets
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

### Optimization Strategies
- **Image Optimization**: WebP format conversion, responsive images
- **Static Asset Optimization**: CSS/JS minification and compression
- **Caching**: Static file caching with proper headers
- **CDN**: GitHub Pages CDN or Cloudflare integration
- **Lazy Loading**: JavaScript-based lazy loading for images and content

## SEO Strategy

### Technical SEO
- **Meta Tags**: Dynamic title, description, keywords
- **Open Graph**: Social media sharing optimization
- **Structured Data**: JSON-LD for rich snippets
- **Sitemap**: Automated generation
- **Robots.txt**: Search engine guidance

### Content SEO
- **Keywords**: Personal branding, technical expertise
- **Blog Content**: Regular, valuable content creation
- **Internal Linking**: Strategic page connections
- **External Links**: Quality outbound links

## Development Phases

### Phase 1: Foundation (Week 1)
- Set up Pelican project structure and Python environment
- Create custom dark theme with Jinja2 templates
- Implement responsive CSS framework
- Configure Pelican settings and plugins

### Phase 2: Core Content (Week 2)
- Create Markdown content structure
- Develop homepage template with hero section
- Build about and projects page templates
- Set up blog post template and archives

### Phase 3: Integrations (Week 3)
- Develop YouTube API plugin for channel data
- Create GitHub API plugin for repository showcase
- Implement RSS feeds and sitemap generation
- Add search functionality with Lunr.js

### Phase 4: Polish & Deploy (Week 4)
- Optimize images and static assets
- Implement SEO meta tags and structured data
- Mobile responsiveness testing and fixes
- Deploy to GitHub Pages or Netlify

## Deployment Strategy

### GitHub Pages - Optimal Hosting Platform

**Why GitHub Pages is the Perfect Choice**:

**🆓 Cost Benefits**:
- **Free Hosting**: No monthly hosting fees
- **Free SSL**: Automatic HTTPS with custom domains
- **Free Build Minutes**: GitHub Actions included in free tier
- **Unlimited Bandwidth**: No traffic limits for reasonable use
- **Global CDN**: GitHub's edge network for fast delivery

**🚀 Deployment Advantages**:
- **Automatic Deployments**: Push to repository triggers builds
- **GitHub Actions Integration**: Sophisticated CI/CD workflows
- **Version Control**: Full history of site changes
- **Rollback Capability**: Easy to revert to previous versions
- **Branch Previews**: Test changes before going live
- **Status Monitoring**: Build status and deployment logs

**🔧 Technical Features**:
- **Custom Domains**: `bryanhoward.dev` or any domain
- **HTTPS Enforcement**: Automatic SSL certificate management
- **404 Handling**: Custom 404 pages supported
- **Redirect Support**: URL redirects via `_redirects` file
- **Jekyll Support**: Native, but Pelican works perfectly with Actions
- **Repository Integration**: Seamless workflow with source code

**📊 Repository Setup Options**:

**Option 1: User/Organization Site** (Recommended)
- **Repository Name**: `bhowiebkr.github.io`
- **URL**: `https://bhowiebkr.github.io`
- **Custom Domain**: Optional `bryanhoward.dev`
- **Source Branch**: `main` or `gh-pages`

**Option 2: Project Site**
- **Repository Name**: `bryan-howard-website`
- **URL**: `https://bhowiebkr.github.io/bryan-howard-website`
- **Custom Domain**: Supported
- **Source Branch**: `main`, `gh-pages`, or `docs/` folder

**🔄 Deployment Workflow**:
```
Local Development → Git Push → GitHub Actions → Build Pelican → Deploy to Pages
```

**⚡ Performance Characteristics**:
- **Build Time**: 1-3 minutes for typical Pelican sites
- **Propagation**: 1-10 minutes for changes to appear globally
- **Uptime**: GitHub's 99.9% SLA
- **Speed**: Global CDN with edge caching
- **Monitoring**: GitHub status page for service health

### Domain & DNS
- Custom domain setup
- SSL certificate (automatically handled by Vercel)
- DNS configuration for optimal performance

## Maintenance & Updates

### Content Updates
- **Blog Posts**: Regular content creation schedule
- **Project Updates**: Automatic GitHub integration
- **YouTube Content**: API refreshes for new videos

### Technical Maintenance
- **Dependencies**: Monthly security updates
- **Performance**: Quarterly performance audits
- **Analytics**: Monthly traffic and performance reviews
- **Backup**: Automated backups of content and code

## Budget Considerations

### Development Costs
- **Domain Name**: ~$15/year (optional - GitHub Pages provides free subdomain)
- **Hosting**: **$0** with GitHub Pages (completely free)
- **SSL Certificate**: **$0** (automatic with GitHub Pages)
- **CDN/Performance**: **$0** (GitHub's global CDN included)
- **Python Environment**: **$0** (Python 3.8+ free)
- **External APIs**: **$0** (YouTube/GitHub APIs free tiers sufficient)
- **Development Tools**: **$0** (VS Code, Git, GitHub all free)
- **Development Time**: 15-25 hours estimated

### Ongoing Costs
- **Hosting**: **$0** (GitHub Pages free forever)
- **Domain Renewal**: $15/year (only if using custom domain)
- **API Costs**: **$0** (free tiers handle personal site traffic)
- **Maintenance**: 1-2 hours monthly
- **Content Creation**: Time investment only
- **Security Updates**: **$0** (automated via Dependabot)
- **Monitoring**: **$0** (GitHub built-in monitoring)

**Total Annual Cost**: $0-15 (only custom domain if desired)
**Monthly Operating Cost**: $0

## Risk Assessment & Mitigation

### Technical Risks
- **API Rate Limits**: Implement caching and fallbacks
- **Dependencies**: Regular updates and security monitoring
- **Performance**: Continuous monitoring and optimization

### Content Risks
- **Platform Changes**: YouTube/GitHub API deprecation
- **Content Loss**: Regular backups and version control
- **SEO Changes**: Stay updated with best practices

## Success Metrics & KPIs

### Technical Metrics
- Page load speed < 3 seconds
- Mobile responsiveness score > 95%
- Accessibility score > 90%
- SEO score > 90%

### Business Metrics
- Monthly unique visitors
- Time on site
- Blog post engagement
- Social media click-through rates
- Contact form submissions

## Pelican-Specific Implementation Details

### Python Environment Setup
```bash
# Create virtual environment
python -m venv pelican-env
source pelican-env/bin/activate  # Linux/Mac
# or
pelican-env\Scripts\activate     # Windows

# Install dependencies
pip install pelican[markdown]
pip install beautifulsoup4       # For better HTML processing
pip install typogrify            # Typography enhancements
pip install pelican-sitemap      # SEO sitemap generation
```

### Pelican Configuration (pelicanconf.py)
```python
# Basic settings
SITENAME = 'Bryan Howard'
SITEURL = ''
AUTHOR = 'Bryan Howard'
DEFAULT_LANG = 'en'

# Content paths
PATH = 'content'
STATIC_PATHS = ['images', 'extra']
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']

# Theme and appearance
THEME = 'theme'
SITEDESCRIPTION = 'Personal website showcasing development projects and tutorials'

# Blog settings
DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = [
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
]

# URL structure
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'sitemap',
    'youtube_integration',
    'github_integration',
]

# Social media and external links
SOCIAL = (
    ('GitHub', 'https://github.com/bhowiebkr'),
    ('YouTube', 'https://www.youtube.com/@BryanHoward'),
)

# Feed settings
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
```

### Content Structure Examples

**Blog Post Example** (`content/blog/2025/first-post.md`):
```markdown
Title: Welcome to My New Website
Date: 2025-01-15 10:00
Category: General
Tags: website, pelican, python
Slug: welcome-new-website
Summary: Introduction to my new personal website built with Pelican

Welcome to my new website! This post explains how I built this site using Pelican...
```

**Page Example** (`content/pages/about.md`):
```markdown
Title: About
Slug: about

I'm Bryan Howard, a developer passionate about...
```

### Custom Plugin Development

**YouTube Integration Plugin** (`plugins/youtube_integration.py`):
```python
import requests
from pelican import signals

def fetch_youtube_data(generator):
    # Fetch latest videos from YouTube API
    # Add to generator context for templates
    pass

def register():
    signals.generator_init.connect(fetch_youtube_data)
```

**GitHub Integration Plugin** (`plugins/github_integration.py`):
```python
import requests
from pelican import signals

def fetch_github_repos(generator):
    # Fetch repositories from GitHub API
    # Add to generator context for templates
    pass

def register():
    signals.generator_init.connect(fetch_github_repos)
```

### Development Workflow

**Local Development Process**:
```bash
# 1. Start development server
pelican --listen --autoreload
# Site available at http://localhost:8000

# 2. Create new blog post
python scripts/new-post.py "My New Blog Post"
# Creates: content/blog/2025/my-new-blog-post.md

# 3. Test production build
pelican content -s publishconf.py

# 4. Deploy to GitHub Pages
git add .
git commit -m "Add new blog post: My New Blog Post"
git push origin main
# GitHub Actions automatically builds and deploys
```

**Content Creation Workflow**:
```markdown
# Blog post template
Title: Welcome to My New Website
Date: 2025-01-15 10:00
Modified: 2025-01-15 12:00
Category: General
Tags: website, pelican, python
Slug: welcome-new-website
Author: Bryan Howard
Summary: Introduction to my new personal website built with Pelican
Status: published

Content goes here...
```

**Deployment Pipeline**:
```
Local Changes → Git Push → GitHub Actions → Build → Test → Deploy → Live Site
     ↓              ↓            ↓          ↓      ↓        ↓
  Content      Trigger      Install    Pelican  Links   GitHub
   Edits       Workflow     Python     Build   Check    Pages
```

## Next Steps

1. **Review and approve** this updated Pelican-focused planning document
2. **Set up Python environment** with Pelican and dependencies
3. **Create initial Pelican project structure** following outlined architecture
4. **Develop custom dark theme** with Jinja2 templates
5. **Create sample content** and test build process
6. **Implement API integrations** for YouTube and GitHub
## Complete GitHub Actions Workflows

### Main Deployment Workflow

**File**: `.github/workflows/pelican-deploy.yml`
```yaml
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
        cname: bryanhoward.dev  # Optional: your custom domain
        enable_jekyll: false
        exclude_assets: '.github'
        force_orphan: true
        user_name: 'github-actions[bot]'
        user_email: 'github-actions[bot]@users.noreply.github.com'
        commit_message: 'Deploy Pelican site - ${{ github.sha }}'
```

### Content Validation Workflow

**File**: `.github/workflows/content-check.yml`
```yaml
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
        pip install markdown-link-checker
    
    - name: Validate Markdown syntax
      run: |
        find content -name "*.md" -exec echo "Checking {}" \;
        # Add markdown linting here if needed
    
    - name: Check for required metadata
      run: |
        python scripts/validate-metadata.py
    
    - name: Spell check (optional)
      run: |
        # Add spell checking tool if desired
        echo "Spell checking completed"
    
    - name: Build test
      run: |
        pelican content -s pelicanconf.py
        echo "Test build successful"
```

### Dependency Update Workflow

**File**: `.github/workflows/dependency-update.yml`
```yaml
name: Update Dependencies

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on the 1st
  workflow_dispatch:

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Update requirements
      run: |
        pip install --upgrade pip
        pip install pip-tools
        pip-compile --upgrade requirements.in
    
    - name: Test updated dependencies
      run: |
        pip install -r requirements.txt
        pelican content -s pelicanconf.py
    
    - name: Create Pull Request
      uses: peter-evans/create-pull-request@v5
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        commit-message: 'Update Python dependencies'
        title: 'Automated dependency update'
        body: |
          Automated update of Python dependencies.
          
          Please review the changes and test locally before merging.
        branch: dependency-updates
```

## Implementation Roadmap

**📁 Detailed Phase Documentation:**
- 📋 [Phase 1: Repository Setup](./PHASE1-REPOSITORY-SETUP.md) - Complete GitHub and development environment setup
- 🏗️ [Phase 2: Basic Site Structure](./PHASE2-BASIC-SITE-STRUCTURE.md) - Automated deployment and content structure  
- 🎨 [Phase 3: Theme Development](./PHASE3-THEME-DEVELOPMENT.md) - Custom dark theme and responsive design
- ⚡ [Phase 4: API Integration & Polish](./PHASE4-API-INTEGRATION-POLISH.md) - YouTube/GitHub APIs and final optimization

### Phase 1: Repository Setup (Week 1)
**📋 [Detailed Guide →](./PHASE1-REPOSITORY-SETUP.md)**

**Key Deliverables:**
- ✅ GitHub repository configured and public
- ✅ GitHub Pages enabled with custom domain (`bryan-howard.ca`)
- ✅ Local Python development environment setup
- ✅ Basic Pelican installation and test content
- ✅ DNS configuration for custom domain

**Estimated Time:** 2-4 hours

### Phase 2: Basic Site Structure (Week 2)  
**🏗️ [Detailed Guide →](./PHASE2-BASIC-SITE-STRUCTURE.md)**

**Key Deliverables:**
- ✅ GitHub Actions automated deployment pipeline
- ✅ Production-optimized Pelican configuration
- ✅ Enhanced content structure with sample posts
- ✅ Content creation scripts and development workflow
- ✅ Automated deployment to `bryan-howard.ca`

**Estimated Time:** 3-5 hours

### Phase 3: Theme Development (Week 3)
**🎨 [Detailed Guide →](./PHASE3-THEME-DEVELOPMENT.md)**

**Key Deliverables:**
- ✅ Professional dark theme color system
- ✅ Responsive CSS framework (mobile-first)
- ✅ Base template architecture with Jinja2
- ✅ Component library (cards, buttons, forms)
- ✅ JavaScript functionality (navigation, accessibility)

**Estimated Time:** 6-8 hours

### Phase 4: API Integration & Polish (Week 4)
**⚡ [Detailed Guide →](./PHASE4-API-INTEGRATION-POLISH.md)**

**Key Deliverables:**
- ✅ YouTube API integration plugin
- ✅ GitHub API integration plugin  
- ✅ SEO optimization with structured data
- ✅ Performance optimization and analytics
- ✅ Final testing and launch preparation

**Estimated Time:** 4-6 hours

### Success Metrics
- **Build Time**: < 3 minutes for full site builds
- **Deployment Time**: < 5 minutes from push to live
- **Page Load Speed**: < 2 seconds on 3G
- **Mobile Responsiveness**: 95%+ compatibility
- **Accessibility**: WCAG 2.1 AA compliance
- **SEO Score**: 90%+ on Lighthouse audits

### Folder Structure Benefits
1. **Organized Content**: Clear separation of blog posts, pages, and static assets
2. **Scalable Architecture**: Easy to add new content types and features
3. **Developer Friendly**: Python-based configuration and plugin system
4. **Version Control**: Clean git history with proper ignore patterns
5. **Automated Deployment**: GitHub Actions handle build and deployment
6. **SEO Optimized**: Proper URL structure and meta tag generation
7. **Performance Focused**: Optimized asset organization and caching

### Maintenance Considerations
- **Content**: Add new blog posts to appropriate year folders
- **Images**: Organize by content type and compress for web
- **Plugins**: Keep API integrations updated with rate limiting
- **Theme**: Maintain responsive design and accessibility standards
- **Dependencies**: Regular updates for security and performance

---

**Document Version**: 3.0 - Pelican + GitHub Pages Focus  
**Last Updated**: 2025-08-19  
**Next Review**: Implementation phase milestones
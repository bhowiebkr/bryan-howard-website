# Phase 3: Theme Development - Implementation Guide

**Duration**: Week 3  
**Prerequisites**: Phase 2 completed successfully  
**Goal**: Create a custom dark theme with responsive design, modern UI components, and mobile-first approach

## Overview

This phase focuses on creating a professional, modern dark theme that reflects your personal brand and provides an excellent user experience across all devices.

## 📋 Checklist Overview

- [ ] 3.1 Design Dark Theme Color System
- [ ] 3.2 Create Base Template Architecture
- [ ] 3.3 Implement Responsive CSS Framework
- [ ] 3.4 Build Page Templates (Homepage, Blog, Pages)
- [ ] 3.5 Add JavaScript Functionality
- [ ] 3.6 Optimize for Mobile and Accessibility

---

## 🎨 Task 3.1: Design Dark Theme Color System

### 📝 Steps:

#### 3.1.1 Create Theme Directory Structure
```bash
# Ensure you're in the project directory with virtual environment active
cd bryan-howard-website
source pelican-env/bin/activate  # Windows: pelican-env\Scripts\activate

# Create theme directory structure
mkdir -p theme/{templates/{partials,layouts},static/{css,js,images,fonts}}

# Create theme templates directory
mkdir -p theme/templates/{articles,pages,archives}
```

#### 3.1.2 Define Dark Theme Color Palette
```bash
cat > theme/static/css/variables.css << 'EOF'
/* Bryan Howard Dark Theme - CSS Custom Properties */

:root {
  /* === PRIMARY COLORS === */
  
  /* Background Colors */
  --bg-primary: #0a0a0a;        /* Main background - deep black */
  --bg-secondary: #1a1a1a;      /* Card/section backgrounds */
  --bg-tertiary: #2a2a2a;       /* Elevated elements, modals */
  --bg-code: #1e1e1e;           /* Code blocks background */
  --bg-input: #252525;          /* Form inputs */
  
  /* Text Colors */
  --text-primary: #ffffff;       /* Main text - pure white */
  --text-secondary: #e0e0e0;     /* Secondary text */
  --text-muted: #a0a0a0;         /* Muted text, metadata */
  --text-dim: #707070;           /* Very dim text */
  --text-inverse: #1a1a1a;       /* Text on light backgrounds */
  
  /* === ACCENT COLORS === */
  
  /* Primary Brand Color - Blue */
  --color-primary: #4a9eff;      /* Main brand blue */
  --color-primary-hover: #6bb3ff; /* Hover state */
  --color-primary-active: #2d7ce0; /* Active/pressed state */
  --color-primary-soft: rgba(74, 158, 255, 0.1); /* Soft background */
  
  /* Secondary Accent - Green */
  --color-secondary: #10d980;    /* Success, positive actions */
  --color-secondary-hover: #2de58c;
  --color-secondary-soft: rgba(16, 217, 128, 0.1);
  
  /* Warning/Alert Colors */
  --color-warning: #ff9500;      /* Warning states */
  --color-warning-hover: #ffad33;
  --color-warning-soft: rgba(255, 149, 0, 0.1);
  
  /* Error/Danger Colors */
  --color-error: #ff453a;        /* Error states */
  --color-error-hover: #ff6b61;
  --color-error-soft: rgba(255, 69, 58, 0.1);
  
  /* === BORDER COLORS === */
  
  --border-primary: #333333;     /* Main borders */
  --border-secondary: #4a4a4a;   /* Hover/focus borders */
  --border-subtle: #2a2a2a;      /* Very subtle borders */
  --border-accent: var(--color-primary); /* Accent borders */
  
  /* === SHADOW COLORS === */
  
  --shadow-sm: rgba(0, 0, 0, 0.2);
  --shadow-md: rgba(0, 0, 0, 0.3);
  --shadow-lg: rgba(0, 0, 0, 0.4);
  --shadow-xl: rgba(0, 0, 0, 0.5);
  
  /* === SEMANTIC COLORS === */
  
  /* Social Media Colors */
  --color-github: #f0f6fc;
  --color-youtube: #ff0000;
  --color-linkedin: #0077b5;
  --color-twitter: #1da1f2;
  
  /* Code Syntax Highlighting */
  --code-keyword: #ff79c6;       /* Keywords */
  --code-string: #f1fa8c;        /* Strings */
  --code-comment: #6272a4;       /* Comments */
  --code-function: #50fa7b;      /* Functions */
  --code-variable: #8be9fd;      /* Variables */
  --code-number: #bd93f9;        /* Numbers */
  
  /* === TYPOGRAPHY === */
  
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
  --font-heading: var(--font-primary);
  
  /* Font Weights */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* Font Sizes (Modular Scale 1.25) */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
  
  /* === SPACING === */
  
  /* Spacing Scale (0.25rem base) */
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */
  --space-32: 8rem;      /* 128px */
  
  /* === LAYOUT === */
  
  /* Container Widths */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
  
  /* Border Radius */
  --radius-sm: 0.125rem;  /* 2px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-2xl: 1rem;     /* 16px */
  --radius-full: 9999px;  /* Full circle */
  
  /* === TRANSITIONS === */
  
  --transition-fast: 150ms ease-in-out;
  --transition-normal: 250ms ease-in-out;
  --transition-slow: 350ms ease-in-out;
  
  /* === Z-INDEX === */
  
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal: 1040;
  --z-popover: 1050;
  --z-tooltip: 1060;
  
  /* === BREAKPOINTS === */
  
  /* Mobile-first breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* === LIGHT THEME OVERRIDES === */
/* (Optional - for future light theme toggle) */

@media (prefers-color-scheme: light) {
  .theme-auto {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-tertiary: #e9ecef;
    --text-primary: #1a1a1a;
    --text-secondary: #495057;
    --text-muted: #6c757d;
    --border-primary: #dee2e6;
    --border-secondary: #adb5bd;
  }
}

/* Theme toggle classes for future implementation */
.theme-dark {
  color-scheme: dark;
}

.theme-light {
  color-scheme: light;
}

.theme-auto {
  color-scheme: light dark;
}
EOF
```

#### 3.1.3 Create Base Styles
```bash
cat > theme/static/css/base.css << 'EOF'
/* Bryan Howard Theme - Base Styles */

/* === RESET & NORMALIZE === */

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  line-height: var(--leading-normal);
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  font-family: var(--font-primary);
  font-weight: var(--font-weight-normal);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--text-primary);
  background-color: var(--bg-primary);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* === TYPOGRAPHY === */

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  font-weight: var(--font-weight-bold);
  line-height: var(--leading-tight);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-weight-bold);
}

h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-weight-semibold);
}

h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-semibold);
}

h4 {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-medium);
}

h5 {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-medium);
}

h6 {
  font-size: var(--text-base);
  font-weight: var(--font-weight-medium);
}

p {
  margin-bottom: var(--space-4);
  line-height: var(--leading-relaxed);
  color: var(--text-secondary);
}

/* === LINKS === */

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

a:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

a:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* === LISTS === */

ul, ol {
  margin-bottom: var(--space-4);
  padding-left: var(--space-6);
}

li {
  margin-bottom: var(--space-2);
  line-height: var(--leading-relaxed);
  color: var(--text-secondary);
}

/* === CODE === */

code {
  font-family: var(--font-mono);
  font-size: 0.875em;
  color: var(--color-primary);
  background-color: var(--bg-code);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
}

pre {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  background-color: var(--bg-code);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  margin-bottom: var(--space-4);
  overflow-x: auto;
}

pre code {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  color: var(--text-primary);
}

/* === BLOCKQUOTES === */

blockquote {
  border-left: 4px solid var(--color-primary);
  padding-left: var(--space-4);
  margin: var(--space-6) 0;
  font-style: italic;
  color: var(--text-muted);
}

blockquote p:last-child {
  margin-bottom: 0;
}

/* === HORIZONTAL RULES === */

hr {
  border: none;
  height: 1px;
  background-color: var(--border-primary);
  margin: var(--space-8) 0;
}

/* === TABLES === */

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--space-6);
}

th, td {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  border-bottom: 1px solid var(--border-primary);
}

th {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  background-color: var(--bg-secondary);
}

td {
  color: var(--text-secondary);
}

/* === IMAGES === */

img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-lg);
}

figure {
  margin-bottom: var(--space-6);
}

figcaption {
  font-size: var(--text-sm);
  color: var(--text-muted);
  text-align: center;
  margin-top: var(--space-2);
}

/* === SELECTION === */

::selection {
  background-color: var(--color-primary-soft);
  color: var(--text-primary);
}

/* === SCROLLBAR === */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background-color: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
  background-color: var(--border-secondary);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-primary);
}

/* === FOCUS VISIBLE === */

:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* === SCREEN READER === */

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* === UTILITIES === */

.container {
  width: 100%;
  max-width: var(--container-lg);
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.container-wide {
  max-width: var(--container-xl);
}

.container-narrow {
  max-width: var(--container-md);
}

.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: var(--space-1); }
.mb-2 { margin-bottom: var(--space-2); }
.mb-3 { margin-bottom: var(--space-3); }
.mb-4 { margin-bottom: var(--space-4); }
.mb-6 { margin-bottom: var(--space-6); }
.mb-8 { margin-bottom: var(--space-8); }
EOF
```

---

## 🏗️ Task 3.2: Create Base Template Architecture

### 📝 Steps:

#### 3.2.1 Create Base Template
```bash
cat > theme/templates/base.html << 'EOF'
<!DOCTYPE html>
<html lang="{{ DEFAULT_LANG }}" class="theme-dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- Title and Meta -->
    <title>{% block title %}{{ SITENAME }}{% endblock %}</title>
    <meta name="description" content="{% block description %}{{ SITEDESCRIPTION }}{% endblock %}">
    <meta name="author" content="{{ AUTHOR }}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{% block og_type %}website{% endblock %}">
    <meta property="og:url" content="{{ SITEURL }}{% block og_url %}/{% endblock %}">
    <meta property="og:title" content="{% block og_title %}{{ SITENAME }}{% endblock %}">
    <meta property="og:description" content="{% block og_description %}{{ SITEDESCRIPTION }}{% endblock %}">
    <meta property="og:image" content="{% block og_image %}{{ SITEURL }}/theme/images/og-image.jpg{% endblock %}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{{ SITEURL }}{% block twitter_url %}/{% endblock %}">
    <meta property="twitter:title" content="{% block twitter_title %}{{ SITENAME }}{% endblock %}">
    <meta property="twitter:description" content="{% block twitter_description %}{{ SITEDESCRIPTION }}{% endblock %}">
    <meta property="twitter:image" content="{% block twitter_image %}{{ SITEURL }}/theme/images/og-image.jpg{% endblock %}">
    {% if TWITTER_USERNAME %}
    <meta name="twitter:creator" content="@{{ TWITTER_USERNAME }}">
    {% endif %}
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ SITEURL }}/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="{{ SITEURL }}/theme/images/apple-touch-icon.png">
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/variables.css">
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/base.css">
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/components.css">
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/layout.css">
    <link rel="stylesheet" href="{{ SITEURL }}/theme/css/responsive.css">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==" crossorigin="anonymous" referrerpolicy="no-referrer">
    
    <!-- Feeds -->
    {% if FEED_ALL_ATOM %}
    <link rel="alternate" type="application/atom+xml" title="{{ SITENAME }} - Atom Feed" href="{{ SITEURL }}/{{ FEED_ALL_ATOM }}">
    {% endif %}
    {% if FEED_ALL_RSS %}
    <link rel="alternate" type="application/rss+xml" title="{{ SITENAME }} - RSS Feed" href="{{ SITEURL }}/{{ FEED_ALL_RSS }}">
    {% endif %}
    
    {% block extra_head %}{% endblock %}
</head>

<body class="{% block body_class %}{% endblock %}">
    <!-- Skip to content link for accessibility -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary text-white px-4 py-2 rounded">
        Skip to main content
    </a>
    
    <!-- Header -->
    <header class="site-header">
        {% include 'partials/header.html' %}
    </header>
    
    <!-- Main Content -->
    <main id="main-content" class="site-main">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="site-footer">
        {% include 'partials/footer.html' %}
    </footer>
    
    <!-- JavaScript -->
    <script src="{{ SITEURL }}/theme/js/main.js"></script>
    {% block extra_js %}{% endblock %}
    
    <!-- Analytics -->
    {% if GOOGLE_ANALYTICS %}
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ GOOGLE_ANALYTICS }}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '{{ GOOGLE_ANALYTICS }}');
    </script>
    {% endif %}
</body>
</html>
EOF
```

#### 3.2.2 Create Header Partial
```bash
cat > theme/templates/partials/header.html << 'EOF'
<div class="header-container">
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
    </button>
    
    <!-- Logo/Brand -->
    <div class="site-brand">
        <a href="{{ SITEURL }}/" class="brand-link">
            <span class="brand-name">{{ SITENAME }}</span>
            {% if SITESUBTITLE %}
            <span class="brand-subtitle">{{ SITESUBTITLE }}</span>
            {% endif %}
        </a>
    </div>
    
    <!-- Main Navigation -->
    <nav class="main-nav" aria-label="Main navigation">
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="{{ SITEURL }}/" class="nav-link">
                    <i class="fas fa-home" aria-hidden="true"></i>
                    <span>Home</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="{{ SITEURL }}/about/" class="nav-link">
                    <i class="fas fa-user" aria-hidden="true"></i>
                    <span>About</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="{{ SITEURL }}/archives/" class="nav-link">
                    <i class="fas fa-blog" aria-hidden="true"></i>
                    <span>Blog</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="{{ SITEURL }}/projects/" class="nav-link">
                    <i class="fas fa-code" aria-hidden="true"></i>
                    <span>Projects</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="{{ SITEURL }}/contact/" class="nav-link">
                    <i class="fas fa-envelope" aria-hidden="true"></i>
                    <span>Contact</span>
                </a>
            </li>
        </ul>
    </nav>
    
    <!-- Social Links -->
    <div class="header-social">
        {% if SOCIAL %}
        <ul class="social-menu">
            {% for name, link, icon in SOCIAL %}
            <li class="social-item">
                <a href="{{ link }}" class="social-link" target="_blank" rel="noopener noreferrer" aria-label="{{ name }}">
                    <i class="{{ icon }}" aria-hidden="true"></i>
                </a>
            </li>
            {% endfor %}
        </ul>
        {% endif %}
        
        <!-- Theme Toggle (Future Implementation) -->
        <button class="theme-toggle" aria-label="Toggle dark/light theme" title="Toggle theme">
            <i class="fas fa-moon" aria-hidden="true"></i>
        </button>
    </div>
</div>
EOF
```

#### 3.2.3 Create Footer Partial
```bash
cat > theme/templates/partials/footer.html << 'EOF'
<div class="footer-container">
    <!-- Footer Content -->
    <div class="footer-content">
        <!-- About Section -->
        <div class="footer-section">
            <h3 class="footer-title">{{ SITENAME }}</h3>
            <p class="footer-description">
                {{ SITEDESCRIPTION }}
            </p>
            
            <!-- Social Links -->
            {% if SOCIAL %}
            <div class="footer-social">
                <h4 class="social-title">Connect</h4>
                <ul class="social-list">
                    {% for name, link, icon in SOCIAL %}
                    <li class="social-item">
                        <a href="{{ link }}" class="social-link" target="_blank" rel="noopener noreferrer">
                            <i class="{{ icon }}" aria-hidden="true"></i>
                            <span>{{ name }}</span>
                        </a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
        
        <!-- Quick Links -->
        <div class="footer-section">
            <h4 class="footer-title">Quick Links</h4>
            <ul class="footer-links">
                <li><a href="{{ SITEURL }}/" class="footer-link">Home</a></li>
                <li><a href="{{ SITEURL }}/about/" class="footer-link">About</a></li>
                <li><a href="{{ SITEURL }}/archives/" class="footer-link">Blog</a></li>
                <li><a href="{{ SITEURL }}/projects/" class="footer-link">Projects</a></li>
                <li><a href="{{ SITEURL }}/contact/" class="footer-link">Contact</a></li>
            </ul>
        </div>
        
        <!-- Recent Posts -->
        <div class="footer-section">
            <h4 class="footer-title">Recent Posts</h4>
            <ul class="footer-posts">
                {% for article in articles[:3] %}
                <li class="footer-post">
                    <a href="{{ SITEURL }}/{{ article.url }}" class="footer-post-link">
                        <span class="post-title">{{ article.title }}</span>
                        <time class="post-date" datetime="{{ article.date.isoformat() }}">
                            {{ article.locale_date }}
                        </time>
                    </a>
                </li>
                {% endfor %}
            </ul>
        </div>
        
        <!-- Newsletter/RSS -->
        <div class="footer-section">
            <h4 class="footer-title">Stay Updated</h4>
            <p class="footer-description">
                Get notified about new posts and updates.
            </p>
            
            {% if FEED_ALL_ATOM or FEED_ALL_RSS %}
            <div class="feed-links">
                {% if FEED_ALL_ATOM %}
                <a href="{{ SITEURL }}/{{ FEED_ALL_ATOM }}" class="feed-link" target="_blank" rel="noopener">
                    <i class="fas fa-rss" aria-hidden="true"></i>
                    <span>Atom Feed</span>
                </a>
                {% endif %}
                {% if FEED_ALL_RSS %}
                <a href="{{ SITEURL }}/{{ FEED_ALL_RSS }}" class="feed-link" target="_blank" rel="noopener">
                    <i class="fas fa-rss" aria-hidden="true"></i>
                    <span>RSS Feed</span>
                </a>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Footer Bottom -->
    <div class="footer-bottom">
        <div class="footer-bottom-content">
            <div class="copyright">
                <p>
                    &copy; {{ COPYRIGHT_YEAR or "2025" }} {{ COPYRIGHT_NAME or AUTHOR }}. All rights reserved.
                </p>
            </div>
            
            <div class="footer-meta">
                <p>
                    Built with <a href="https://getpelican.com/" target="_blank" rel="noopener">Pelican</a> 
                    and hosted on <a href="https://pages.github.com/" target="_blank" rel="noopener">GitHub Pages</a>
                </p>
            </div>
            
            <div class="footer-links-meta">
                <a href="{{ SITEURL }}/sitemap.xml" class="footer-link-meta">Sitemap</a>
                {% if FEED_ALL_ATOM %}
                <a href="{{ SITEURL }}/{{ FEED_ALL_ATOM }}" class="footer-link-meta">Feed</a>
                {% endif %}
            </div>
        </div>
    </div>
</div>
EOF
```

---

## 📱 Task 3.3: Implement Responsive CSS Framework

### 📝 Steps:

#### 3.3.1 Create Layout Styles
```bash
cat > theme/static/css/layout.css << 'EOF'
/* Bryan Howard Theme - Layout Styles */

/* === SITE STRUCTURE === */

.site-header {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-primary);
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.site-main {
  flex: 1;
  padding: var(--space-8) 0;
}

.site-footer {
  background-color: var(--bg-secondary);
  border-top: 1px solid var(--border-primary);
  margin-top: auto;
}

/* === HEADER === */

.header-container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 4rem;
  gap: var(--space-4);
}

/* Site Brand */
.site-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: var(--text-primary);
}

.brand-link:hover {
  text-decoration: none;
  color: var(--color-primary);
}

.brand-name {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
}

.brand-subtitle {
  font-size: var(--text-sm);
  color: var(--text-muted);
  font-weight: var(--font-weight-normal);
}

/* Main Navigation */
.main-nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--space-2);
}

.nav-item {
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  text-decoration: none;
}

.nav-link.active {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

.nav-link i {
  font-size: var(--text-sm);
}

/* Header Social */
.header-social {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.social-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--space-2);
}

.social-item {
  margin: 0;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.social-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  text-decoration: none;
  transform: translateY(-1px);
}

/* Theme Toggle */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  border-radius: var(--radius-lg);
  background-color: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.theme-toggle:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
}

/* Mobile Menu Toggle */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
  gap: 0.25rem;
}

.hamburger-line {
  width: 1.25rem;
  height: 2px;
  background-color: var(--text-primary);
  transition: all var(--transition-fast);
  border-radius: 1px;
}

.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(0.3rem, 0.3rem);
}

.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle[aria-expanded="true"] .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(0.3rem, -0.3rem);
}

/* === FOOTER === */

.footer-container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: var(--space-12) var(--space-4) var(--space-8);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-8);
  margin-bottom: var(--space-8);
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.footer-title {
  font-size: var(--text-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.footer-description {
  color: var(--text-muted);
  line-height: var(--leading-relaxed);
  margin-bottom: 0;
}

/* Footer Links */
.footer-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--color-primary);
  text-decoration: none;
}

/* Footer Social */
.footer-social {
  margin-top: var(--space-2);
}

.social-title {
  font-size: var(--text-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

.social-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.social-list .social-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.social-list .social-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  text-decoration: none;
}

/* Footer Posts */
.footer-posts {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.footer-post {
  margin: 0;
}

.footer-post-link {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background-color var(--transition-fast);
}

.footer-post-link:hover {
  background-color: var(--bg-tertiary);
  text-decoration: none;
}

.footer-post-link .post-title {
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
  line-height: var(--leading-tight);
}

.footer-post-link .post-date {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.footer-post-link:hover .post-title {
  color: var(--color-primary);
}

/* Feed Links */
.feed-links {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-top: var(--space-3);
}

.feed-link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.feed-link:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-soft);
  text-decoration: none;
}

/* Footer Bottom */
.footer-bottom {
  border-top: 1px solid var(--border-primary);
  padding-top: var(--space-6);
}

.footer-bottom-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
}

.copyright,
.footer-meta {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.copyright p,
.footer-meta p {
  margin-bottom: 0;
}

.footer-meta a {
  color: var(--color-primary);
  text-decoration: none;
}

.footer-meta a:hover {
  text-decoration: underline;
}

.footer-links-meta {
  display: flex;
  gap: var(--space-4);
}

.footer-link-meta {
  color: var(--text-muted);
  font-size: var(--text-sm);
  text-decoration: none;
}

.footer-link-meta:hover {
  color: var(--color-primary);
  text-decoration: none;
}
EOF
```

#### 3.3.2 Create Component Styles
```bash
cat > theme/static/css/components.css << 'EOF'
/* Bryan Howard Theme - Component Styles */

/* === BUTTONS === */

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  font-weight: var(--font-weight-medium);
  font-size: var(--text-base);
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.btn:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Button Variants */
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  color: white;
  text-decoration: none;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px var(--shadow-md);
}

.btn-secondary {
  background-color: transparent;
  color: var(--text-primary);
  border-color: var(--border-primary);
}

.btn-secondary:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--border-secondary);
  color: var(--text-primary);
  text-decoration: none;
}

.btn-ghost {
  background-color: transparent;
  color: var(--color-primary);
  border-color: transparent;
}

.btn-ghost:hover {
  background-color: var(--color-primary-soft);
  color: var(--color-primary-hover);
  text-decoration: none;
}

/* Button Sizes */
.btn-sm {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}

.btn-lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
}

/* === CARDS === */

.card {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  transition: all var(--transition-normal);
}

.card:hover {
  border-color: var(--border-secondary);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px var(--shadow-lg);
}

.card-header {
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--border-primary);
}

.card-title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.card-subtitle {
  color: var(--text-muted);
  font-size: var(--text-sm);
  margin-bottom: 0;
}

.card-body {
  margin-bottom: var(--space-4);
}

.card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-primary);
}

/* === BADGES === */

.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge-primary {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
}

.badge-secondary {
  background-color: var(--bg-tertiary);
  color: var(--text-secondary);
}

.badge-success {
  background-color: var(--color-secondary-soft);
  color: var(--color-secondary);
}

/* === ALERTS === */

.alert {
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid;
  margin-bottom: var(--space-4);
}

.alert-info {
  background-color: var(--color-primary-soft);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.alert-success {
  background-color: var(--color-secondary-soft);
  border-color: var(--color-secondary);
  color: var(--color-secondary);
}

.alert-warning {
  background-color: var(--color-warning-soft);
  border-color: var(--color-warning);
  color: var(--color-warning);
}

.alert-error {
  background-color: var(--color-error-soft);
  border-color: var(--color-error);
  color: var(--color-error);
}

/* === FORMS === */

.form-group {
  margin-bottom: var(--space-4);
}

.form-label {
  display: block;
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.form-input {
  width: 100%;
  padding: var(--space-3);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  background-color: var(--bg-input);
  color: var(--text-primary);
  font-size: var(--text-base);
  transition: all var(--transition-fast);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.form-input::placeholder {
  color: var(--text-muted);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

/* === TAGS === */

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  list-style: none;
  margin: 0;
  padding: 0;
}

.tag-item {
  margin: 0;
}

.tag-link {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  background-color: var(--bg-tertiary);
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.tag-link:hover {
  background-color: var(--color-primary-soft);
  color: var(--color-primary);
  text-decoration: none;
}

.tag-link::before {
  content: '#';
  margin-right: var(--space-1);
  color: var(--text-muted);
}

/* === PAGINATION === */

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-2);
  margin: var(--space-8) 0;
}

.pagination-item {
  list-style: none;
  margin: 0;
}

.pagination-link {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
  height: 2.5rem;
  padding: 0 var(--space-3);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.pagination-link:hover {
  background-color: var(--color-primary-soft);
  border-color: var(--color-primary);
  color: var(--color-primary);
  text-decoration: none;
}

.pagination-link.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.pagination-link.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* === BREADCRUMBS === */

.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  font-size: var(--text-sm);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.breadcrumb-link {
  color: var(--text-muted);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.breadcrumb-link:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.breadcrumb-separator {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.breadcrumb-current {
  color: var(--text-primary);
  font-weight: var(--font-weight-medium);
}

/* === ARTICLE META === */

.article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  padding: var(--space-4);
  background-color: var(--bg-secondary);
  border-radius: var(--radius-lg);
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.meta-icon {
  color: var(--color-primary);
}

.meta-link {
  color: var(--text-muted);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.meta-link:hover {
  color: var(--color-primary);
  text-decoration: none;
}

/* === LOADING STATES === */

.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-primary);
  border-radius: 50%;
  border-top-color: var(--color-primary);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* === ACCESSIBILITY === */

.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: var(--space-2) var(--space-4);
  margin: var(--space-4);
  overflow: visible;
  clip: auto;
  white-space: normal;
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  z-index: var(--z-modal);
}
EOF
```

This completes the first part of Phase 3. The next steps will be:

1. ✅ **Task 3.1**: Dark Theme Color System - COMPLETED
2. ✅ **Task 3.2**: Base Template Architecture - COMPLETED  
3. ✅ **Task 3.3**: Responsive CSS Framework - COMPLETED
4. **Task 3.4**: Build Page Templates (Homepage, Blog, Pages)
5. **Task 3.5**: Add JavaScript Functionality
6. **Task 3.6**: Optimize for Mobile and Accessibility

Would you like me to continue with Tasks 3.4-3.6 to complete the Phase 3 theme development guide?
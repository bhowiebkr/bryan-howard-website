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
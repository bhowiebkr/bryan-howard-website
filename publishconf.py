#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# Import all settings from pelicanconf.py
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# Production Site URL
SITEURL = 'https://www.bryan-howard.ca'
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
    # 'sitemap',  # Disabled until custom theme in Phase 3
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
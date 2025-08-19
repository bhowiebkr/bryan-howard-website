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
# Using default theme for Phase 2, custom theme will be added in Phase 3
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives']
# SITEMAP_SAVE_AS = 'sitemap.xml'  # Disabled until custom theme in Phase 3

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
    ('GitHub', 'https://github.com/bhowiebkr'),
    ('YouTube', 'https://www.youtube.com/@BryanHoward'),
    ('LinkedIn', 'https://linkedin.com/in/bryanhoward'),
    ('Twitter', 'https://twitter.com/bhowiebkr'),
)

# Menu Configuration
DISPLAY_PAGES_ON_MENU = False  # Disable auto-adding pages to avoid duplicates
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (
    ('Home', '/'),
    ('About', '/about/'),
    ('Blog', '/archives/'),
    ('Projects', '/projects/'),
    ('Contact', '/contact/'),
)

# Plugin Configuration
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    # 'sitemap',  # Disabled until custom theme in Phase 3
]

# Sitemap Configuration (disabled until Phase 3)
# SITEMAP = {
#     'format': 'xml',
#     'priorities': {
#         'articles': 0.7,
#         'indexes': 0.5,
#         'pages': 0.6,
#     },
#     'changefreqs': {
#         'articles': 'weekly',
#         'indexes': 'daily',
#         'pages': 'monthly',
#     },
#     'exclude': ['tag/', 'category/', 'author/']
# }

# Date Format
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Typography
TYPOGRIFY = True

# Development Settings
LOAD_CONTENT_CACHE = False
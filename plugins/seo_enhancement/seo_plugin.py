"""
SEO Enhancement Plugin for Pelican
Adds structured data, meta tags, and SEO improvements
"""

import json
import logging
from datetime import datetime
from pelican import signals
from pelican.contents import Article, Page

logger = logging.getLogger(__name__)

def add_structured_data(generator, metadata):
    """Add JSON-LD structured data to articles and pages"""
    
    # Website structured data (added to all pages)
    website_data = {
        "@context": "https://schema.org",
        "@type": "Website",
        "name": generator.settings.get('SITENAME', ''),
        "description": generator.settings.get('SITEDESCRIPTION', ''),
        "url": generator.settings.get('SITEURL', ''),
        "author": {
            "@type": "Person",
            "name": generator.settings.get('AUTHOR', ''),
            "url": generator.settings.get('SITEURL', '')
        },
        "publisher": {
            "@type": "Person",
            "name": generator.settings.get('AUTHOR', '')
        }
    }
    
    if not hasattr(generator, 'context'):
        return
        
    generator.context['structured_data'] = {
        'website': website_data
    }

def add_article_structured_data(article_generator):
    """Add structured data to articles"""
    for article in article_generator.articles:
        if hasattr(article, 'structured_data'):
            continue
            
        # Article structured data
        article_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": article.title,
            "description": getattr(article, 'summary', '') or article.title,
            "image": get_article_image(article),
            "datePublished": article.date.isoformat(),
            "dateModified": getattr(article, 'modified', article.date).isoformat(),
            "author": {
                "@type": "Person",
                "name": article.author.name if hasattr(article.author, 'name') else str(article.author)
            },
            "publisher": {
                "@type": "Person",
                "name": article_generator.settings.get('AUTHOR', '')
            },
            "url": f"{article_generator.settings.get('SITEURL', '')}/{article.url}",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{article_generator.settings.get('SITEURL', '')}/{article.url}"
            }
        }
        
        # Add categories as keywords
        if hasattr(article, 'category') and article.category:
            article_data['keywords'] = [str(article.category)]
            
        # Add tags as additional keywords
        if hasattr(article, 'tags') and article.tags:
            if 'keywords' in article_data:
                article_data['keywords'].extend([str(tag) for tag in article.tags])
            else:
                article_data['keywords'] = [str(tag) for tag in article.tags]
        
        article.structured_data = article_data

def get_article_image(article):
    """Get article featured image or fallback"""
    # Check for featured image in metadata
    if hasattr(article, 'image'):
        return article.image
    
    # Check for image in content (simplified)
    content = getattr(article, 'content', '')
    if 'img src=' in content:
        # This is a simplified approach - in practice, you might want to parse HTML
        pass
    
    # Fallback to site default
    return "/theme/images/og-image.jpg"

def add_breadcrumb_data(generator):
    """Add breadcrumb structured data"""
    if not hasattr(generator, 'context'):
        return
    
    # This will be used in templates to generate breadcrumb JSON-LD
    breadcrumb_template = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    generator.context['breadcrumb_template'] = breadcrumb_template

def enhance_meta_tags(article_generator):
    """Enhance meta tags for articles"""
    for article in article_generator.articles:
        # Add meta description if not present
        if not hasattr(article, 'meta_description'):
            description = getattr(article, 'summary', '')
            if description:
                # Clean and truncate description
                description = description.replace('\n', ' ').strip()
                if len(description) > 155:
                    description = description[:152] + '...'
                article.meta_description = description
        
        # Add Open Graph tags
        if not hasattr(article, 'og_title'):
            article.og_title = article.title
            
        if not hasattr(article, 'og_description'):
            article.og_description = getattr(article, 'meta_description', article.title)
            
        if not hasattr(article, 'og_image'):
            article.og_image = get_article_image(article)
        
        # Add Twitter Card tags
        if not hasattr(article, 'twitter_title'):
            article.twitter_title = article.title
            
        if not hasattr(article, 'twitter_description'):
            article.twitter_description = getattr(article, 'meta_description', article.title)
            
        if not hasattr(article, 'twitter_image'):
            article.twitter_image = get_article_image(article)

def register():
    """Register the plugin"""
    signals.generator_init.connect(add_structured_data)
    signals.article_generator_finalized.connect(add_article_structured_data)
    signals.article_generator_finalized.connect(enhance_meta_tags)
    signals.generator_init.connect(add_breadcrumb_data)
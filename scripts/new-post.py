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
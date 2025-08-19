#!/usr/bin/env python3
"""
Site validation script for Bryan Howard Website
Performs comprehensive testing of generated site
"""

import os
import sys
import json
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

class SiteValidator:
    def __init__(self, base_url="http://localhost:8000", output_dir="output"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        """Log an error"""
        self.errors.append(message)
        print(f"✗ ERROR: {message}")
        
    def log_warning(self, message):
        """Log a warning"""
        self.warnings.append(message)
        print(f"⚠ WARNING: {message}")
        
    def log_success(self, message):
        """Log a success"""
        print(f"✓ {message}")
        
    def validate_file_structure(self):
        """Validate the output file structure"""
        print("\n📁 Validating file structure...")
        
        required_files = [
            "index.html",
            "theme/css/variables.css",
            "theme/css/base.css",
            "theme/css/components.css",
            "theme/css/layout.css",
            "theme/css/responsive.css",
            "theme/js/main.js",
            "feeds/all.atom.xml",
            "sitemap.xml"
        ]
        
        for file_path in required_files:
            full_path = self.output_dir / file_path
            if full_path.exists():
                self.log_success(f"Found {file_path}")
            else:
                self.log_error(f"Missing required file: {file_path}")
        
        # Check theme directories
        theme_dirs = ["css", "js", "images"]
        for dir_name in theme_dirs:
            dir_path = self.output_dir / "theme" / dir_name
            if dir_path.exists():
                self.log_success(f"Found theme/{dir_name}/ directory")
            else:
                self.log_error(f"Missing theme directory: theme/{dir_name}/")
    
    def validate_html_pages(self):
        """Validate HTML pages for basic structure and SEO"""
        print("\n🔍 Validating HTML pages...")
        
        html_files = list(self.output_dir.glob("**/*.html"))
        
        for html_file in html_files[:10]:  # Limit to first 10 for performance
            rel_path = html_file.relative_to(self.output_dir)
            
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                
                # Check basic HTML structure
                if not soup.find('title'):
                    self.log_error(f"{rel_path}: Missing <title> tag")
                
                if not soup.find('meta', attrs={'name': 'description'}):
                    self.log_warning(f"{rel_path}: Missing meta description")
                
                # Check for structured data
                structured_data = soup.find('script', attrs={'type': 'application/ld+json'})
                if structured_data:
                    self.log_success(f"{rel_path}: Has structured data")
                else:
                    self.log_warning(f"{rel_path}: Missing structured data")
                
                # Check for Open Graph tags
                og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
                if og_tags:
                    self.log_success(f"{rel_path}: Has Open Graph tags")
                else:
                    self.log_warning(f"{rel_path}: Missing Open Graph tags")
                
                self.log_success(f"Validated {rel_path}")
                
            except Exception as e:
                self.log_error(f"Error validating {rel_path}: {e}")
    
    def validate_css_js_files(self):
        """Validate CSS and JavaScript files"""
        print("\n🎨 Validating CSS and JavaScript files...")
        
        # Check CSS files
        css_files = list(self.output_dir.glob("theme/css/*.css"))
        for css_file in css_files:
            if css_file.stat().st_size == 0:
                self.log_error(f"Empty CSS file: {css_file.name}")
            else:
                self.log_success(f"CSS file has content: {css_file.name}")
        
        # Check JavaScript files
        js_files = list(self.output_dir.glob("theme/js/*.js"))
        for js_file in js_files:
            if js_file.stat().st_size == 0:
                self.log_error(f"Empty JS file: {js_file.name}")
            else:
                self.log_success(f"JS file has content: {js_file.name}")
    
    def validate_feeds(self):
        """Validate RSS/Atom feeds"""
        print("\n📡 Validating feeds...")
        
        feed_files = [
            "feeds/all.atom.xml",
            "feeds/all.rss.xml"
        ]
        
        for feed_path in feed_files:
            feed_file = self.output_dir / feed_path
            if feed_file.exists():
                try:
                    with open(feed_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if '<feed' in content or '<rss' in content:
                            self.log_success(f"Valid feed: {feed_path}")
                        else:
                            self.log_error(f"Invalid feed format: {feed_path}")
                except Exception as e:
                    self.log_error(f"Error reading feed {feed_path}: {e}")
            else:
                self.log_warning(f"Feed not found: {feed_path}")
    
    def validate_live_site(self):
        """Validate the live site if server is running"""
        print(f"\n🌐 Validating live site at {self.base_url}...")
        
        try:
            # Test main page
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_success("Site is accessible")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for key elements
                if soup.find('header', class_='site-header'):
                    self.log_success("Header is present")
                else:
                    self.log_error("Site header not found")
                
                if soup.find('main', class_='site-main'):
                    self.log_success("Main content area is present")
                else:
                    self.log_error("Main content area not found")
                
                if soup.find('footer', class_='site-footer'):
                    self.log_success("Footer is present")
                else:
                    self.log_error("Site footer not found")
                
                # Check for mobile menu toggle
                if soup.find(class_='mobile-menu-toggle'):
                    self.log_success("Mobile navigation is present")
                else:
                    self.log_warning("Mobile navigation not found")
                
                # Check for theme toggle
                if soup.find(class_='theme-toggle'):
                    self.log_success("Theme toggle is present")
                else:
                    self.log_warning("Theme toggle not found")
                
            else:
                self.log_error(f"Site returned status code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_warning("Could not connect to live site (server may not be running)")
        except Exception as e:
            self.log_error(f"Error validating live site: {e}")
    
    def validate_performance(self):
        """Basic performance validation"""
        print("\n⚡ Validating performance...")
        
        # Check file sizes
        large_files = []
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > 1:  # Files larger than 1MB
                    large_files.append((file_path.relative_to(self.output_dir), size_mb))
        
        if large_files:
            self.log_warning(f"Found {len(large_files)} files larger than 1MB:")
            for file_path, size in large_files:
                print(f"   - {file_path}: {size:.2f}MB")
        else:
            self.log_success("No excessively large files found")
        
        # Check CSS/JS minification (basic check)
        main_css = self.output_dir / "theme/css/base.css"
        if main_css.exists():
            with open(main_css, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content.splitlines()) > 1000:
                    self.log_warning("CSS files might benefit from minification")
                else:
                    self.log_success("CSS file size looks reasonable")
    
    def validate_accessibility(self):
        """Basic accessibility validation"""
        print("\n♿ Validating accessibility...")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for alt attributes on images
                images = soup.find_all('img')
                images_without_alt = [img for img in images if not img.get('alt')]
                
                if images_without_alt:
                    self.log_warning(f"Found {len(images_without_alt)} images without alt attributes")
                else:
                    self.log_success("All images have alt attributes")
                
                # Check for semantic HTML
                if soup.find('main'):
                    self.log_success("Uses semantic <main> element")
                else:
                    self.log_warning("Missing semantic <main> element")
                
                if soup.find('nav'):
                    self.log_success("Uses semantic <nav> element")
                else:
                    self.log_warning("Missing semantic <nav> element")
                
                # Check for skip links
                skip_link = soup.find('a', href='#main-content')
                if skip_link:
                    self.log_success("Has skip to main content link")
                else:
                    self.log_warning("Missing skip to main content link")
                
        except Exception as e:
            self.log_warning(f"Could not validate accessibility: {e}")
    
    def generate_report(self):
        """Generate a summary report"""
        print("\n" + "="*60)
        print("                 VALIDATION REPORT")
        print("="*60)
        
        total_issues = len(self.errors) + len(self.warnings)
        
        if len(self.errors) == 0:
            print("✅ No critical errors found!")
        else:
            print(f"❌ Found {len(self.errors)} critical errors:")
            for error in self.errors:
                print(f"   - {error}")
        
        if len(self.warnings) == 0:
            print("✅ No warnings!")
        else:
            print(f"⚠️  Found {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        print(f"\nTotal issues: {total_issues}")
        
        if len(self.errors) == 0:
            print("\n🚀 Site is ready for deployment!")
            return True
        else:
            print("\n🛑 Please fix critical errors before deployment.")
            return False
    
    def run_all_validations(self):
        """Run all validations"""
        print("🔍 Starting comprehensive site validation...")
        print(f"Output directory: {self.output_dir}")
        print(f"Base URL: {self.base_url}")
        
        self.validate_file_structure()
        self.validate_html_pages()
        self.validate_css_js_files()
        self.validate_feeds()
        self.validate_live_site()
        self.validate_performance()
        self.validate_accessibility()
        
        return self.generate_report()

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    validator = SiteValidator(base_url=base_url)
    success = validator.run_all_validations()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
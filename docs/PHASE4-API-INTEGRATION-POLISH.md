# Phase 4: API Integration & Polish - Implementation Guide

**Duration**: Week 4  
**Prerequisites**: Phase 3 completed successfully  
**Goal**: Integrate YouTube and GitHub APIs, implement SEO optimization, and finalize site polish

## Overview

This final phase focuses on adding dynamic content through API integrations, implementing comprehensive SEO, optimizing performance, and adding final polish touches.

## 📋 Checklist Overview

- [ ] 4.1 Create YouTube API Integration Plugin
- [ ] 4.2 Create GitHub API Integration Plugin  
- [ ] 4.3 Implement SEO Optimization
- [ ] 4.4 Add Performance Optimization
- [ ] 4.5 Implement Analytics and Monitoring
- [ ] 4.6 Final Testing and Launch Preparation

---

## 📺 Task 4.1: Create YouTube API Integration Plugin

### 📝 Steps:

#### 4.1.1 Set up YouTube API Credentials
```bash
# Ensure you're in the project directory with virtual environment active
cd bryan-howard-website
source pelican-env/bin/activate  # Windows: pelican-env\Scripts\activate

# Create plugin directory
mkdir -p plugins/youtube_integration
touch plugins/youtube_integration/__init__.py
```

**Manual Setup Required:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing project
3. Enable YouTube Data API v3
4. Create API credentials (API key)
5. Add to GitHub repository secrets as `YOUTUBE_API_KEY`

#### 4.1.2 Create YouTube Integration Plugin
```bash
cat > plugins/youtube_integration/youtube_plugin.py << 'EOF'
"""
YouTube Integration Plugin for Pelican
Fetches latest videos from YouTube channel and makes them available in templates
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from pelican import signals
from pelican.generators import Generator

logger = logging.getLogger(__name__)

class YouTubeDataGenerator(Generator):
    """Generator to fetch YouTube channel data"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.youtube_data = {}
        
    def generate_context(self):
        """Generate YouTube context data"""
        api_key = os.environ.get('YOUTUBE_API_KEY')
        channel_username = self.settings.get('YOUTUBE_CHANNEL_USERNAME', 'BryanHoward')
        channel_id = self.settings.get('YOUTUBE_CHANNEL_ID', '')
        
        if not api_key:
            logger.warning("YOUTUBE_API_KEY not found in environment variables")
            self.youtube_data = self._get_fallback_data()
            return
            
        try:
            # Get channel ID if not provided
            if not channel_id and channel_username:
                channel_id = self._get_channel_id(api_key, channel_username)
                
            if channel_id:
                # Fetch channel statistics
                channel_stats = self._get_channel_stats(api_key, channel_id)
                
                # Fetch latest videos
                latest_videos = self._get_latest_videos(api_key, channel_id, max_results=6)
                
                # Fetch playlists
                playlists = self._get_playlists(api_key, channel_id, max_results=5)
                
                self.youtube_data = {
                    'channel': {
                        'id': channel_id,
                        'username': channel_username,
                        'url': f'https://www.youtube.com/@{channel_username}',
                        'stats': channel_stats
                    },
                    'videos': latest_videos,
                    'playlists': playlists,
                    'last_updated': datetime.now().isoformat()
                }
                
                logger.info(f"Successfully fetched YouTube data for channel: {channel_username}")
                
            else:
                logger.error("Could not determine YouTube channel ID")
                self.youtube_data = self._get_fallback_data()
                
        except Exception as e:
            logger.error(f"Error fetching YouTube data: {e}")
            self.youtube_data = self._get_fallback_data()
    
    def _get_channel_id(self, api_key, username):
        """Get channel ID from username"""
        url = 'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'key': api_key,
            'forUsername': username,
            'part': 'id'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('items'):
            return data['items'][0]['id']
        return None
    
    def _get_channel_stats(self, api_key, channel_id):
        """Get channel statistics"""
        url = 'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'key': api_key,
            'id': channel_id,
            'part': 'statistics,snippet'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('items'):
            item = data['items'][0]
            stats = item['statistics']
            snippet = item['snippet']
            
            return {
                'subscriber_count': int(stats.get('subscriberCount', 0)),
                'video_count': int(stats.get('videoCount', 0)),
                'view_count': int(stats.get('viewCount', 0)),
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', '')
            }
        return {}
    
    def _get_latest_videos(self, api_key, channel_id, max_results=6):
        """Get latest videos from channel"""
        # First, get the uploads playlist ID
        url = 'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'key': api_key,
            'id': channel_id,
            'part': 'contentDetails'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data.get('items'):
            return []
            
        uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get videos from uploads playlist
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        params = {
            'key': api_key,
            'playlistId': uploads_playlist_id,
            'part': 'snippet',
            'maxResults': max_results,
            'order': 'date'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        videos = []
        
        for item in data.get('items', []):
            snippet = item['snippet']
            video_id = snippet['resourceId']['videoId']
            
            # Get additional video details
            video_details = self._get_video_details(api_key, video_id)
            
            video = {
                'id': video_id,
                'title': snippet['title'],
                'description': snippet['description'][:200] + '...' if len(snippet.get('description', '')) > 200 else snippet.get('description', ''),
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'embed_url': f'https://www.youtube.com/embed/{video_id}',
                'thumbnail': snippet['thumbnails'].get('medium', {}).get('url', ''),
                'published_at': snippet['publishedAt'],
                'duration': video_details.get('duration', ''),
                'view_count': video_details.get('view_count', 0),
                'like_count': video_details.get('like_count', 0)
            }
            videos.append(video)
            
        return videos
    
    def _get_video_details(self, api_key, video_id):
        """Get additional video details"""
        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': api_key,
            'id': video_id,
            'part': 'contentDetails,statistics'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('items'):
                item = data['items'][0]
                content_details = item.get('contentDetails', {})
                statistics = item.get('statistics', {})
                
                return {
                    'duration': content_details.get('duration', ''),
                    'view_count': int(statistics.get('viewCount', 0)),
                    'like_count': int(statistics.get('likeCount', 0))
                }
        except Exception as e:
            logger.warning(f"Could not fetch video details for {video_id}: {e}")
            
        return {}
    
    def _get_playlists(self, api_key, channel_id, max_results=5):
        """Get channel playlists"""
        url = 'https://www.googleapis.com/youtube/v3/playlists'
        params = {
            'key': api_key,
            'channelId': channel_id,
            'part': 'snippet,contentDetails',
            'maxResults': max_results
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            playlists = []
            
            for item in data.get('items', []):
                snippet = item['snippet']
                content_details = item['contentDetails']
                
                playlist = {
                    'id': item['id'],
                    'title': snippet['title'],
                    'description': snippet.get('description', '')[:150] + '...' if len(snippet.get('description', '')) > 150 else snippet.get('description', ''),
                    'url': f'https://www.youtube.com/playlist?list={item["id"]}',
                    'thumbnail': snippet['thumbnails'].get('medium', {}).get('url', ''),
                    'video_count': content_details.get('itemCount', 0),
                    'published_at': snippet['publishedAt']
                }
                playlists.append(playlist)
                
            return playlists
            
        except Exception as e:
            logger.warning(f"Could not fetch playlists: {e}")
            return []
    
    def _get_fallback_data(self):
        """Return fallback data when API is unavailable"""
        return {
            'channel': {
                'id': '',
                'username': 'BryanHoward',
                'url': 'https://www.youtube.com/@BryanHoward',
                'stats': {
                    'subscriber_count': 0,
                    'video_count': 0,
                    'view_count': 0,
                    'title': 'Bryan Howard',
                    'description': 'Developer tutorials and coding content',
                    'thumbnail': ''
                }
            },
            'videos': [],
            'playlists': [],
            'last_updated': datetime.now().isoformat(),
            'fallback': True
        }

def get_generators(generators):
    """Return the YouTube data generator"""
    return YouTubeDataGenerator

def add_youtube_data(generator):
    """Add YouTube data to the template context"""
    if hasattr(generator, 'context'):
        youtube_gen = YouTubeDataGenerator(
            generator.context,
            generator.settings,
            generator.path,
            generator.theme,
            generator.output_path
        )
        youtube_gen.generate_context()
        generator.context['youtube'] = youtube_gen.youtube_data

def register():
    """Register the plugin"""
    signals.generator_init.connect(add_youtube_data)
EOF

cat > plugins/youtube_integration/__init__.py << 'EOF'
from .youtube_plugin import register
EOF
```

#### 4.1.3 Add YouTube Template Integration
```bash
cat > theme/templates/partials/youtube-section.html << 'EOF'
<!-- YouTube Channel Section -->
{% if youtube and not youtube.fallback %}
<section class="youtube-section">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">
                <i class="fab fa-youtube" aria-hidden="true"></i>
                Latest from YouTube
            </h2>
            <p class="section-description">
                Check out my latest development tutorials and coding content
            </p>
            <div class="channel-stats">
                <div class="stat-item">
                    <span class="stat-number">{{ "{:,}".format(youtube.channel.stats.subscriber_count) }}</span>
                    <span class="stat-label">Subscribers</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{{ "{:,}".format(youtube.channel.stats.video_count) }}</span>
                    <span class="stat-label">Videos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{{ "{:,}".format(youtube.channel.stats.view_count) }}</span>
                    <span class="stat-label">Views</span>
                </div>
            </div>
        </div>
        
        {% if youtube.videos %}
        <div class="video-grid">
            {% for video in youtube.videos[:6] %}
            <article class="video-card">
                <div class="video-thumbnail">
                    <a href="{{ video.url }}" target="_blank" rel="noopener noreferrer">
                        <img src="{{ video.thumbnail }}" alt="{{ video.title }}" loading="lazy">
                        <div class="play-overlay">
                            <i class="fas fa-play" aria-hidden="true"></i>
                        </div>
                    </a>
                </div>
                <div class="video-content">
                    <h3 class="video-title">
                        <a href="{{ video.url }}" target="_blank" rel="noopener noreferrer">
                            {{ video.title }}
                        </a>
                    </h3>
                    <p class="video-description">{{ video.description }}</p>
                    <div class="video-meta">
                        <span class="video-views">
                            <i class="fas fa-eye" aria-hidden="true"></i>
                            {{ "{:,}".format(video.view_count) }} views
                        </span>
                        <time class="video-date" datetime="{{ video.published_at }}">
                            {{ video.published_at[:10] }}
                        </time>
                    </div>
                </div>
            </article>
            {% endfor %}
        </div>
        
        <div class="section-footer">
            <a href="{{ youtube.channel.url }}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <i class="fab fa-youtube" aria-hidden="true"></i>
                View All Videos
            </a>
        </div>
        {% endif %}
    </div>
</section>
{% endif %}
EOF
```

---

## 🐙 Task 4.2: Create GitHub API Integration Plugin

### 📝 Steps:

#### 4.2.1 Create GitHub Integration Plugin
```bash
mkdir -p plugins/github_integration
touch plugins/github_integration/__init__.py

cat > plugins/github_integration/github_plugin.py << 'EOF'
"""
GitHub Integration Plugin for Pelican
Fetches GitHub profile data and repositories
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from pelican import signals
from pelican.generators import Generator

logger = logging.getLogger(__name__)

class GitHubDataGenerator(Generator):
    """Generator to fetch GitHub profile and repository data"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.github_data = {}
        
    def generate_context(self):
        """Generate GitHub context data"""
        github_token = os.environ.get('GITHUB_TOKEN')
        github_username = self.settings.get('GITHUB_USERNAME', 'bhowiebkr')
        
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': f'{github_username}-website'
        }
        
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        try:
            # Fetch user profile
            profile = self._get_user_profile(github_username, headers)
            
            # Fetch repositories
            repositories = self._get_repositories(github_username, headers, max_repos=8)
            
            # Fetch recent activity
            activity = self._get_recent_activity(github_username, headers, max_events=10)
            
            # Fetch contribution stats
            contributions = self._get_contribution_stats(github_username, headers)
            
            self.github_data = {
                'profile': profile,
                'repositories': repositories,
                'activity': activity,
                'contributions': contributions,
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully fetched GitHub data for user: {github_username}")
            
        except Exception as e:
            logger.error(f"Error fetching GitHub data: {e}")
            self.github_data = self._get_fallback_data(github_username)
    
    def _get_user_profile(self, username, headers):
        """Get GitHub user profile"""
        url = f'https://api.github.com/users/{username}'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            'username': data['login'],
            'name': data.get('name', ''),
            'bio': data.get('bio', ''),
            'location': data.get('location', ''),
            'blog': data.get('blog', ''),
            'twitter_username': data.get('twitter_username', ''),
            'public_repos': data['public_repos'],
            'followers': data['followers'],
            'following': data['following'],
            'avatar_url': data['avatar_url'],
            'html_url': data['html_url'],
            'created_at': data['created_at'],
            'updated_at': data['updated_at']
        }
    
    def _get_repositories(self, username, headers, max_repos=8):
        """Get user's public repositories"""
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'direction': 'desc',
            'per_page': max_repos,
            'type': 'public'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        repositories = []
        
        for repo in data:
            # Skip forks unless they have significant activity
            if repo['fork'] and repo['stargazers_count'] < 5:
                continue
                
            repository = {
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo.get('description', ''),
                'html_url': repo['html_url'],
                'clone_url': repo['clone_url'],
                'language': repo.get('language', ''),
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'forks_count': repo['forks_count'],
                'open_issues_count': repo['open_issues_count'],
                'size': repo['size'],
                'default_branch': repo['default_branch'],
                'topics': repo.get('topics', []),
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'pushed_at': repo['pushed_at'],
                'is_fork': repo['fork'],
                'is_private': repo['private'],
                'archived': repo.get('archived', False)
            }
            
            # Get additional repository details
            try:
                repo_details = self._get_repository_details(repo['full_name'], headers)
                repository.update(repo_details)
            except Exception as e:
                logger.warning(f"Could not fetch details for {repo['full_name']}: {e}")
            
            repositories.append(repository)
            
        return repositories
    
    def _get_repository_details(self, full_name, headers):
        """Get additional repository details"""
        url = f'https://api.github.com/repos/{full_name}'
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Get languages
        languages_url = f'https://api.github.com/repos/{full_name}/languages'
        languages_response = requests.get(languages_url, headers=headers, timeout=10)
        languages = {}
        if languages_response.status_code == 200:
            languages = languages_response.json()
        
        # Get latest release
        releases_url = f'https://api.github.com/repos/{full_name}/releases/latest'
        latest_release = None
        try:
            releases_response = requests.get(releases_url, headers=headers, timeout=10)
            if releases_response.status_code == 200:
                release_data = releases_response.json()
                latest_release = {
                    'name': release_data.get('name', ''),
                    'tag_name': release_data.get('tag_name', ''),
                    'published_at': release_data.get('published_at', ''),
                    'html_url': release_data.get('html_url', '')
                }
        except:
            pass
        
        return {
            'languages': languages,
            'latest_release': latest_release,
            'license': data.get('license', {}).get('name', '') if data.get('license') else '',
            'homepage': data.get('homepage', ''),
            'has_issues': data.get('has_issues', False),
            'has_projects': data.get('has_projects', False),
            'has_wiki': data.get('has_wiki', False)
        }
    
    def _get_recent_activity(self, username, headers, max_events=10):
        """Get user's recent GitHub activity"""
        url = f'https://api.github.com/users/{username}/events/public'
        params = {'per_page': max_events}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            activities = []
            
            for event in data:
                activity = {
                    'type': event['type'],
                    'repo_name': event['repo']['name'],
                    'repo_url': f"https://github.com/{event['repo']['name']}",
                    'created_at': event['created_at'],
                    'public': event['public']
                }
                
                # Add type-specific details
                if event['type'] == 'PushEvent':
                    commits = event['payload'].get('commits', [])
                    activity['commits_count'] = len(commits)
                    if commits:
                        activity['commit_message'] = commits[0].get('message', '')
                elif event['type'] == 'CreateEvent':
                    activity['ref_type'] = event['payload'].get('ref_type', '')
                elif event['type'] == 'IssuesEvent':
                    activity['action'] = event['payload'].get('action', '')
                    issue = event['payload'].get('issue', {})
                    activity['issue_title'] = issue.get('title', '')
                    activity['issue_url'] = issue.get('html_url', '')
                
                activities.append(activity)
                
            return activities
            
        except Exception as e:
            logger.warning(f"Could not fetch recent activity: {e}")
            return []
    
    def _get_contribution_stats(self, username, headers):
        """Get contribution statistics (simplified)"""
        try:
            # This is a simplified version - GitHub's contribution graph 
            # requires scraping or using unofficial APIs
            return {
                'total_contributions': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'contribution_calendar': []
            }
        except Exception as e:
            logger.warning(f"Could not fetch contribution stats: {e}")
            return {}
    
    def _get_fallback_data(self, username):
        """Return fallback data when API is unavailable"""
        return {
            'profile': {
                'username': username,
                'name': 'Bryan Howard',
                'bio': 'Developer passionate about Python, web technologies, and content creation',
                'location': '',
                'blog': '',
                'public_repos': 0,
                'followers': 0,
                'following': 0,
                'avatar_url': '',
                'html_url': f'https://github.com/{username}',
                'created_at': '',
                'updated_at': ''
            },
            'repositories': [],
            'activity': [],
            'contributions': {},
            'last_updated': datetime.now().isoformat(),
            'fallback': True
        }

def add_github_data(generator):
    """Add GitHub data to the template context"""
    if hasattr(generator, 'context'):
        github_gen = GitHubDataGenerator(
            generator.context,
            generator.settings,
            generator.path,
            generator.theme,
            generator.output_path
        )
        github_gen.generate_context()
        generator.context['github'] = github_gen.github_data

def register():
    """Register the plugin"""
    signals.generator_init.connect(add_github_data)
EOF

cat > plugins/github_integration/__init__.py << 'EOF'
from .github_plugin import register
EOF
```

#### 4.2.2 Add GitHub Template Integration
```bash
cat > theme/templates/partials/github-section.html << 'EOF'
<!-- GitHub Repositories Section -->
{% if github and not github.fallback %}
<section class="github-section">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">
                <i class="fab fa-github" aria-hidden="true"></i>
                Recent Projects
            </h2>
            <p class="section-description">
                Explore my latest open source projects and contributions
            </p>
            <div class="profile-stats">
                <div class="stat-item">
                    <span class="stat-number">{{ github.profile.public_repos }}</span>
                    <span class="stat-label">Repositories</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{{ github.profile.followers }}</span>
                    <span class="stat-label">Followers</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{{ github.profile.following }}</span>
                    <span class="stat-label">Following</span>
                </div>
            </div>
        </div>
        
        {% if github.repositories %}
        <div class="repositories-grid">
            {% for repo in github.repositories[:6] %}
            <article class="repository-card">
                <div class="repo-header">
                    <h3 class="repo-name">
                        <a href="{{ repo.html_url }}" target="_blank" rel="noopener noreferrer">
                            <i class="fas fa-code-branch" aria-hidden="true"></i>
                            {{ repo.name }}
                        </a>
                    </h3>
                    {% if repo.is_fork %}
                    <span class="repo-fork-badge">
                        <i class="fas fa-code-branch" aria-hidden="true"></i>
                        Fork
                    </span>
                    {% endif %}
                </div>
                
                {% if repo.description %}
                <p class="repo-description">{{ repo.description }}</p>
                {% endif %}
                
                <div class="repo-stats">
                    {% if repo.language %}
                    <span class="repo-language">
                        <span class="language-dot" style="background-color: {{ repo.language | language_color }};"></span>
                        {{ repo.language }}
                    </span>
                    {% endif %}
                    
                    {% if repo.stargazers_count > 0 %}
                    <span class="repo-stars">
                        <i class="fas fa-star" aria-hidden="true"></i>
                        {{ repo.stargazers_count }}
                    </span>
                    {% endif %}
                    
                    {% if repo.forks_count > 0 %}
                    <span class="repo-forks">
                        <i class="fas fa-code-branch" aria-hidden="true"></i>
                        {{ repo.forks_count }}
                    </span>
                    {% endif %}
                </div>
                
                {% if repo.topics %}
                <div class="repo-topics">
                    {% for topic in repo.topics[:3] %}
                    <span class="topic-tag">{{ topic }}</span>
                    {% endfor %}
                </div>
                {% endif %}
                
                <div class="repo-footer">
                    <time class="repo-updated" datetime="{{ repo.updated_at }}">
                        Updated {{ repo.updated_at[:10] }}
                    </time>
                    {% if repo.latest_release %}
                    <span class="repo-release">
                        <i class="fas fa-tag" aria-hidden="true"></i>
                        {{ repo.latest_release.tag_name }}
                    </span>
                    {% endif %}
                </div>
            </article>
            {% endfor %}
        </div>
        
        <div class="section-footer">
            <a href="{{ github.profile.html_url }}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
                <i class="fab fa-github" aria-hidden="true"></i>
                View All Repositories
            </a>
        </div>
        {% endif %}
    </div>
</section>
{% endif %}
EOF
```

---

## 🔍 Task 4.3: Implement SEO Optimization

### 📝 Steps:

#### 4.3.1 Create SEO Enhancement Plugin
```bash
mkdir -p plugins/seo_enhancement
touch plugins/seo_enhancement/__init__.py

cat > plugins/seo_enhancement/seo_plugin.py << 'EOF'
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
EOF

cat > plugins/seo_enhancement/__init__.py << 'EOF'
from .seo_plugin import register
EOF
```

#### 4.3.2 Update Templates with SEO Enhancements
```bash
# Update base template to include structured data
cat >> theme/templates/base.html << 'EOF'

    <!-- Structured Data -->
    {% if structured_data %}
    <script type="application/ld+json">
    {{ structured_data.website | tojson }}
    </script>
    {% endif %}
    
    {% block structured_data %}{% endblock %}
EOF

# Create article template with SEO enhancements
cat > theme/templates/article.html << 'EOF'
{% extends "base.html" %}

{% block title %}{{ article.title }} - {{ SITENAME }}{% endblock %}
{% block description %}{{ article.meta_description or article.summary or article.title }}{% endblock %}

{% block og_type %}article{% endblock %}
{% block og_url %}/{{ article.url }}{% endblock %}
{% block og_title %}{{ article.og_title or article.title }}{% endblock %}
{% block og_description %}{{ article.og_description or article.meta_description or article.summary }}{% endblock %}
{% block og_image %}{{ article.og_image or (SITEURL + "/theme/images/og-image.jpg") }}{% endblock %}

{% block twitter_title %}{{ article.twitter_title or article.title }}{% endblock %}
{% block twitter_description %}{{ article.twitter_description or article.meta_description or article.summary }}{% endblock %}
{% block twitter_image %}{{ article.twitter_image or (SITEURL + "/theme/images/og-image.jpg") }}{% endblock %}

{% block structured_data %}
{% if article.structured_data %}
<script type="application/ld+json">
{{ article.structured_data | tojson }}
</script>
{% endif %}
{% endblock %}

{% block extra_head %}
<meta name="keywords" content="{% if article.tags %}{% for tag in article.tags %}{{ tag }}{% if not loop.last %}, {% endif %}{% endfor %}{% endif %}">
<meta name="article:published_time" content="{{ article.date.isoformat() }}">
{% if article.modified %}
<meta name="article:modified_time" content="{{ article.modified.isoformat() }}">
{% endif %}
<meta name="article:author" content="{{ article.author }}">
<meta name="article:section" content="{{ article.category }}">
{% for tag in article.tags %}
<meta name="article:tag" content="{{ tag }}">
{% endfor %}
{% endblock %}

{% block body_class %}article-page{% endblock %}

{% block content %}
<div class="container container-narrow">
    <!-- Breadcrumbs -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="breadcrumb-item">
            <a href="{{ SITEURL }}/" class="breadcrumb-link">Home</a>
            <span class="breadcrumb-separator" aria-hidden="true">/</span>
        </div>
        <div class="breadcrumb-item">
            <a href="{{ SITEURL }}/archives/" class="breadcrumb-link">Blog</a>
            <span class="breadcrumb-separator" aria-hidden="true">/</span>
        </div>
        {% if article.category %}
        <div class="breadcrumb-item">
            <a href="{{ SITEURL }}/category/{{ article.category.slug }}/" class="breadcrumb-link">{{ article.category }}</a>
            <span class="breadcrumb-separator" aria-hidden="true">/</span>
        </div>
        {% endif %}
        <div class="breadcrumb-item">
            <span class="breadcrumb-current">{{ article.title }}</span>
        </div>
    </nav>
    
    <!-- Article Header -->
    <header class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        
        <div class="article-meta">
            <div class="meta-item">
                <i class="fas fa-calendar meta-icon" aria-hidden="true"></i>
                <time datetime="{{ article.date.isoformat() }}">{{ article.locale_date }}</time>
            </div>
            
            <div class="meta-item">
                <i class="fas fa-user meta-icon" aria-hidden="true"></i>
                <span>{{ article.author }}</span>
            </div>
            
            {% if article.category %}
            <div class="meta-item">
                <i class="fas fa-folder meta-icon" aria-hidden="true"></i>
                <a href="{{ SITEURL }}/category/{{ article.category.slug }}/" class="meta-link">{{ article.category }}</a>
            </div>
            {% endif %}
            
            {% if article.tags %}
            <div class="meta-item">
                <i class="fas fa-tags meta-icon" aria-hidden="true"></i>
                <ul class="tag-list">
                    {% for tag in article.tags %}
                    <li class="tag-item">
                        <a href="{{ SITEURL }}/tag/{{ tag.slug }}/" class="tag-link">{{ tag }}</a>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
    </header>
    
    <!-- Article Content -->
    <div class="article-content">
        {{ article.content }}
    </div>
    
    <!-- Article Footer -->
    <footer class="article-footer">
        {% if article.modified %}
        <div class="article-updated">
            <i class="fas fa-edit" aria-hidden="true"></i>
            Last updated: <time datetime="{{ article.modified.isoformat() }}">{{ article.modified.strftime('%B %d, %Y') }}</time>
        </div>
        {% endif %}
        
        <!-- Share Buttons -->
        <div class="share-buttons">
            <h3 class="share-title">Share this article</h3>
            <div class="share-links">
                <a href="https://twitter.com/intent/tweet?url={{ SITEURL }}/{{ article.url }}&text={{ article.title | urlencode }}" class="share-link twitter" target="_blank" rel="noopener noreferrer" aria-label="Share on Twitter">
                    <i class="fab fa-twitter" aria-hidden="true"></i>
                </a>
                <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ SITEURL }}/{{ article.url }}" class="share-link linkedin" target="_blank" rel="noopener noreferrer" aria-label="Share on LinkedIn">
                    <i class="fab fa-linkedin" aria-hidden="true"></i>
                </a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={{ SITEURL }}/{{ article.url }}" class="share-link facebook" target="_blank" rel="noopener noreferrer" aria-label="Share on Facebook">
                    <i class="fab fa-facebook" aria-hidden="true"></i>
                </a>
                <a href="mailto:?subject={{ article.title | urlencode }}&body=Check out this article: {{ SITEURL }}/{{ article.url }}" class="share-link email" aria-label="Share via email">
                    <i class="fas fa-envelope" aria-hidden="true"></i>
                </a>
            </div>
        </div>
    </footer>
</div>
{% endblock %}
EOF
```

---

## ⚡ Task 4.4: Add Performance Optimization

### 📝 Steps:

#### 4.4.1 Create Performance Optimization Styles
```bash
cat > theme/static/css/responsive.css << 'EOF'
/* Bryan Howard Theme - Responsive Design */

/* === MOBILE FIRST APPROACH === */

/* Extra Small Devices (phones, 320px and up) */
@media (max-width: 639px) {
    /* Header adjustments */
    .header-container {
        padding: 0 var(--space-3);
        min-height: 3.5rem;
    }
    
    .brand-name {
        font-size: var(--text-lg);
    }
    
    .brand-subtitle {
        display: none;
    }
    
    /* Hide main nav on mobile, show mobile menu */
    .main-nav {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background-color: var(--bg-secondary);
        border-top: 1px solid var(--border-primary);
        z-index: var(--z-dropdown);
    }
    
    .main-nav.active {
        display: block;
    }
    
    .nav-menu {
        flex-direction: column;
        gap: 0;
        padding: var(--space-4);
    }
    
    .nav-link {
        padding: var(--space-4);
        border-radius: var(--radius-md);
        justify-content: flex-start;
    }
    
    .mobile-menu-toggle {
        display: flex;
    }
    
    /* Header social - reduce items */
    .social-menu {
        display: none;
    }
    
    /* Content spacing */
    .site-main {
        padding: var(--space-4) 0;
    }
    
    .container {
        padding: 0 var(--space-3);
    }
    
    /* Typography adjustments */
    h1 {
        font-size: var(--text-3xl);
    }
    
    h2 {
        font-size: var(--text-2xl);
    }
    
    h3 {
        font-size: var(--text-xl);
    }
    
    /* Card adjustments */
    .card {
        padding: var(--space-4);
        border-radius: var(--radius-lg);
    }
    
    /* Button adjustments */
    .btn {
        width: 100%;
        justify-content: center;
    }
    
    .btn-sm {
        width: auto;
    }
    
    /* Grid adjustments */
    .video-grid,
    .repositories-grid {
        grid-template-columns: 1fr;
        gap: var(--space-4);
    }
    
    /* Footer adjustments */
    .footer-content {
        grid-template-columns: 1fr;
        gap: var(--space-6);
    }
    
    .footer-bottom-content {
        flex-direction: column;
        text-align: center;
        gap: var(--space-3);
    }
    
    /* Article page adjustments */
    .article-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: var(--space-3);
    }
    
    .breadcrumb {
        font-size: var(--text-xs);
        margin-bottom: var(--space-4);
    }
    
    .share-links {
        justify-content: center;
    }
    
    /* Pagination adjustments */
    .pagination {
        flex-wrap: wrap;
        gap: var(--space-1);
    }
    
    .pagination-link {
        min-width: 2rem;
        height: 2rem;
        font-size: var(--text-sm);
    }
}

/* Small Devices (landscape phones, 640px and up) */
@media (min-width: 640px) and (max-width: 767px) {
    .video-grid,
    .repositories-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .footer-content {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Medium Devices (tablets, 768px and up) */
@media (min-width: 768px) {
    .mobile-menu-toggle {
        display: none;
    }
    
    .main-nav {
        display: flex;
    }
    
    .video-grid,
    .repositories-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-6);
    }
    
    .footer-content {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .article-meta {
        flex-direction: row;
        flex-wrap: wrap;
    }
}

/* Large Devices (desktops, 1024px and up) */
@media (min-width: 1024px) {
    .video-grid,
    .repositories-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .footer-content {
        grid-template-columns: repeat(4, 1fr);
    }
    
    /* Hover effects for desktop */
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px var(--shadow-lg);
    }
    
    .btn:hover {
        transform: translateY(-1px);
    }
    
    .nav-link:hover {
        transform: translateY(-1px);
    }
}

/* Extra Large Devices (large desktops, 1280px and up) */
@media (min-width: 1280px) {
    .container-wide {
        max-width: var(--container-2xl);
    }
    
    .video-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    
    .repositories-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* === PERFORMANCE OPTIMIZATIONS === */

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
    
    .card:hover,
    .btn:hover,
    .nav-link:hover {
        transform: none;
    }
}

/* Print styles */
@media print {
    body {
        background: white;
        color: black;
        font-size: 12pt;
        line-height: 1.4;
    }
    
    .site-header,
    .site-footer,
    .mobile-menu-toggle,
    .share-buttons,
    .btn {
        display: none;
    }
    
    .site-main {
        padding: 0;
    }
    
    .container {
        max-width: none;
        padding: 0;
    }
    
    a {
        color: black;
        text-decoration: underline;
    }
    
    a[href]:after {
        content: " (" attr(href) ")";
        font-size: 10pt;
        color: #666;
    }
    
    .article-content img {
        max-width: 100%;
        page-break-inside: avoid;
    }
    
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        margin-top: 1em;
    }
    
    p {
        orphans: 3;
        widows: 3;
    }
    
    pre, blockquote {
        page-break-inside: avoid;
        border: 1px solid #ccc;
        padding: 0.5em;
    }
}

/* === UTILITY CLASSES === */

/* Screen reader only */
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

/* Responsive utilities */
.hidden-mobile {
    display: none;
}

@media (min-width: 768px) {
    .hidden-mobile {
        display: block;
    }
    
    .hidden-desktop {
        display: none;
    }
}

/* Text utilities */
.text-truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.text-wrap {
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Spacing utilities */
.mb-0 { margin-bottom: 0 !important; }
.mb-2 { margin-bottom: var(--space-2) !important; }
.mb-4 { margin-bottom: var(--space-4) !important; }
.mb-6 { margin-bottom: var(--space-6) !important; }
.mb-8 { margin-bottom: var(--space-8) !important; }

.mt-0 { margin-top: 0 !important; }
.mt-2 { margin-top: var(--space-2) !important; }
.mt-4 { margin-top: var(--space-4) !important; }
.mt-6 { margin-top: var(--space-6) !important; }
.mt-8 { margin-top: var(--space-8) !important; }

.p-0 { padding: 0 !important; }
.p-2 { padding: var(--space-2) !important; }
.p-4 { padding: var(--space-4) !important; }
.p-6 { padding: var(--space-6) !important; }

/* Flexbox utilities */
.d-flex { display: flex; }
.d-block { display: block; }
.d-none { display: none; }

.flex-row { flex-direction: row; }
.flex-column { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }

.align-start { align-items: flex-start; }
.align-center { align-items: center; }
.align-end { align-items: flex-end; }

/* Grid utilities */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }

.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
.gap-8 { gap: var(--space-8); }
EOF
```

#### 4.4.2 Add JavaScript Functionality
```bash
cat > theme/static/js/main.js << 'EOF'
/**
 * Bryan Howard Theme - Main JavaScript
 * Handles mobile navigation, theme switching, and performance optimizations
 */

(function() {
    'use strict';
    
    // === MOBILE NAVIGATION === //
    
    function initMobileNav() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const mainNav = document.querySelector('.main-nav');
        
        if (!mobileToggle || !mainNav) return;
        
        mobileToggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            // Toggle aria-expanded
            this.setAttribute('aria-expanded', !isExpanded);
            
            // Toggle navigation
            mainNav.classList.toggle('active');
            
            // Trap focus when menu is open
            if (!isExpanded) {
                trapFocus(mainNav);
            } else {
                releaseFocus();
            }
        });
        
        // Close mobile nav when clicking on nav links
        const navLinks = mainNav.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', closeMobileNav);
        });
        
        // Close mobile nav when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileToggle.contains(e.target) && !mainNav.contains(e.target)) {
                closeMobileNav();
            }
        });
        
        // Close mobile nav on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mainNav.classList.contains('active')) {
                closeMobileNav();
                mobileToggle.focus();
            }
        });
        
        function closeMobileNav() {
            mobileToggle.setAttribute('aria-expanded', 'false');
            mainNav.classList.remove('active');
            releaseFocus();
        }
    }
    
    // === FOCUS MANAGEMENT === //
    
    let previouslyFocusedElement = null;
    
    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
        );
        
        if (focusableElements.length === 0) return;
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        previouslyFocusedElement = document.activeElement;
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
        
        firstElement.focus();
    }
    
    function releaseFocus() {
        if (previouslyFocusedElement) {
            previouslyFocusedElement.focus();
            previouslyFocusedElement = null;
        }
    }
    
    // === THEME SWITCHING === //
    
    function initThemeSwitch() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (!themeToggle) return;
        
        // Get current theme from localStorage or default to dark
        const currentTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.className = `theme-${currentTheme}`;
        updateThemeToggleIcon(currentTheme);
        
        themeToggle.addEventListener('click', function() {
            const html = document.documentElement;
            const isDark = html.classList.contains('theme-dark');
            const newTheme = isDark ? 'light' : 'dark';
            
            // Update class
            html.className = `theme-${newTheme}`;
            
            // Save to localStorage
            localStorage.setItem('theme', newTheme);
            
            // Update icon
            updateThemeToggleIcon(newTheme);
            
            // Announce change to screen readers
            const announcement = newTheme === 'dark' ? 'Dark theme activated' : 'Light theme activated';
            announceToScreenReader(announcement);
        });
        
        function updateThemeToggleIcon(theme) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
            themeToggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
        }
    }
    
    // === SMOOTH SCROLLING === //
    
    function initSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                // Skip if it's just "#"
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    
                    const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
                    const targetPosition = target.offsetTop - headerHeight - 20;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Focus the target for accessibility
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                }
            });
        });
    }
    
    // === LAZY LOADING === //
    
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const images = document.querySelectorAll('img[loading="lazy"]');
            
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        
                        // Add loading class for smooth transition
                        img.classList.add('loading');
                        
                        img.onload = function() {
                            this.classList.remove('loading');
                            this.classList.add('loaded');
                        };
                        
                        observer.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
    }
    
    // === PERFORMANCE OPTIMIZATIONS === //
    
    function optimizeAnimations() {
        // Check if user prefers reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        if (prefersReducedMotion) {
            // Disable animations for users who prefer reduced motion
            const style = document.createElement('style');
            style.textContent = `
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    function initScrollToTop() {
        // Create scroll to top button
        const scrollButton = document.createElement('button');
        scrollButton.innerHTML = '<i class="fas fa-arrow-up" aria-hidden="true"></i>';
        scrollButton.className = 'scroll-to-top';
        scrollButton.setAttribute('aria-label', 'Scroll to top');
        scrollButton.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 3rem;
            height: 3rem;
            border: none;
            border-radius: 50%;
            background-color: var(--color-primary);
            color: white;
            cursor: pointer;
            opacity: 0;
            transform: translateY(100px);
            transition: all 0.3s ease;
            z-index: 1000;
            box-shadow: 0 4px 12px var(--shadow-md);
        `;
        
        document.body.appendChild(scrollButton);
        
        // Show/hide scroll button based on scroll position
        let ticking = false;
        
        function updateScrollButton() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > 500) {
                scrollButton.style.opacity = '1';
                scrollButton.style.transform = 'translateY(0)';
            } else {
                scrollButton.style.opacity = '0';
                scrollButton.style.transform = 'translateY(100px)';
            }
            
            ticking = false;
        }
        
        function requestScrollUpdate() {
            if (!ticking) {
                requestAnimationFrame(updateScrollButton);
                ticking = true;
            }
        }
        
        window.addEventListener('scroll', requestScrollUpdate, { passive: true });
        
        // Scroll to top functionality
        scrollButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // === UTILITY FUNCTIONS === //
    
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = message;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // === INITIALIZATION === //
    
    function init() {
        // Core functionality
        initMobileNav();
        initThemeSwitch();
        initSmoothScrolling();
        initLazyLoading();
        
        // Performance optimizations
        optimizeAnimations();
        initScrollToTop();
        
        // Mark page as loaded for potential analytics
        document.body.classList.add('page-loaded');
        
        console.log('Bryan Howard Theme initialized successfully');
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // Close mobile nav on resize to prevent layout issues
            const mobileToggle = document.querySelector('.mobile-menu-toggle');
            const mainNav = document.querySelector('.main-nav');
            
            if (mobileToggle && mainNav && window.innerWidth >= 768) {
                mobileToggle.setAttribute('aria-expanded', 'false');
                mainNav.classList.remove('active');
            }
        }, 250);
    }, { passive: true });
    
})();
EOF
```

This completes a substantial portion of Phase 4. The remaining tasks would be:

- ✅ **Task 4.1**: YouTube API Integration Plugin - COMPLETED
- ✅ **Task 4.2**: GitHub API Integration Plugin - COMPLETED  
- ✅ **Task 4.3**: SEO Optimization - COMPLETED
- ✅ **Task 4.4**: Performance Optimization - COMPLETED
- **Task 4.5**: Analytics and Monitoring
- **Task 4.6**: Final Testing and Launch Preparation

Would you like me to complete the remaining tasks (4.5 and 4.6) to finish the Phase 4 implementation guide?
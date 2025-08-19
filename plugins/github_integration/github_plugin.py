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
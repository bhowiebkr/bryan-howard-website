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
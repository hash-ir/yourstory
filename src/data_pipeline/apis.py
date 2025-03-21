import requests
import json
import datetime
import os

# Helper functions for local storage
def save_to_file(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_from_file(filename):
    """Load data from a JSON file if it exists."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

# Discord Client
class DiscordClient:
    def __init__(self, bot_token, user_id):
        self.bot_token = bot_token
        self.user_id = user_id
        self.headers = {'Authorization': f'Bot {bot_token}'}

    def get_monthly_messages(self, channel_ids, initial_date=None, any_user=False):
        """Fetch messages sent by the user this month in specified channels."""
        today = datetime.date.today()
        if initial_date is not None:
            start_of_month = datetime.date(*initial_date)
        else:
            start_of_month = datetime.date(today.year, today.month, 1)
        messages = []
        for channel_id in channel_ids:
            url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
            params = {'limit': 100}  # Max messages per request
            while True:
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code != 200:
                    break
                channel_messages = response.json()
                if not channel_messages:
                    break
                for msg in channel_messages:
                    msg_time = datetime.datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                    if msg_time.date() < start_of_month:
                        break
                    if msg['author']['id'] == self.user_id or any_user:
                        messages.append(msg)
                    if "thread" in msg:
                        thread = self.get_monthly_messages([msg["thread"]["id"]], initial_date, any_user)
                        msg["thread"] = thread
                params['before'] = channel_messages[-1]['id']  # Paginate
        return messages

# Maps Client
class MapsClient:
    def __init__(self, location_file):
        self.location_file = location_file

    def get_monthly_locations(self):
        """Extract locations visited this month from location history JSON."""
        with open(self.location_file, 'r') as f:
            data = json.load(f)
        today = datetime.date.today()
        start_of_month = datetime.date(today.year, today.month, 1)
        locations = []
        for location in data.get('locations', []):
            timestamp_ms = location.get('timestampMs')
            if timestamp_ms:
                timestamp = datetime.datetime.fromtimestamp(int(timestamp_ms) / 1000)
                if timestamp.date() >= start_of_month:
                    locations.append(location)
        return locations

# GitHub Client
class GitHubClient:
    def __init__(self, token, username):
        self.token = token
        self.username = username
        self.headers = {'Authorization': f'token {token}'}

    def get_monthly_activity(self, initial_date=None):
        """Fetch GitHub events performed by the user this month."""
        today = datetime.date.today()
        if initial_date is not None:
            start_of_month = datetime.date(*initial_date)
        else:
            start_of_month = datetime.date(today.year, today.month, 1)
        
        url = f'https://api.github.com/users/{self.username}/events'
        params = {'per_page': 100}  # Max events per page
        events = []
        while True:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                break
            page_events = response.json()
            if not page_events:
                break
            for event in page_events:
                event_time = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if event_time.date() < start_of_month:
                    break
                events.append(event)
            if 'next' in response.links:
                url = response.links['next']['url']  # Paginate
            else:
                break
        return events

# LinkedIn Client
class LinkedInClient:
    def __init__(self, access_token, person_id):
        self.access_token = access_token
        self.person_id = person_id
        self.headers = {'Authorization': f'Bearer {access_token}'}

    def get_monthly_posts(self):
        """Fetch posts made by the user this month."""
        today = datetime.date.today()
        start_of_month = datetime.date(today.year, today.month, 1)
        url = f'https://api.linkedin.com/v2/ugcPosts?q=authors&authors=List(urn:li:person:{self.person_id})'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            posts = response.json().get('elements', [])
            monthly_posts = [
                post for post in posts
                if datetime.datetime.fromtimestamp(post['created']['time'] / 1000).date() >= start_of_month
            ]
            return monthly_posts
        return []


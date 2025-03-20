from apis import DiscordClient, MapsClient, GitHubClient, LinkedInClient, load_from_file, save_to_file

if __name__ == "__main__":
    # File names for local storage
    discord_file = 'discord_monthly.json'
    maps_file = 'maps_monthly.json'
    github_file = 'github_monthly.json'
    linkedin_file = 'linkedin_monthly.json'

    # Initialize clients with your credentials
    discord = DiscordClient(
        bot_token='your_discord_bot_token',
        user_id='your_discord_user_id'
    )
    maps = MapsClient(
        location_file='path_to_location_history.json'
    )
    github = GitHubClient(
        token='your_github_token',
        username='your_github_username'
    )
    linkedin = LinkedInClient(
        access_token='your_linkedin_access_token',
        person_id='your_linkedin_person_id'
    )

    # Function to get or fetch data
    def get_or_fetch(client, method, file):
        data = load_from_file(file)
        if data is None:
            data = method()
            save_to_file(data, file)
        return data

    # Fetch or load monthly data
    discord_messages = get_or_fetch(discord, lambda: discord.get_monthly_messages(['channel_id1', 'channel_id2']), discord_file)
    maps_locations = get_or_fetch(maps, maps.get_monthly_locations, maps_file)
    github_events = get_or_fetch(github, github.get_monthly_activity, github_file)
    linkedin_posts = get_or_fetch(linkedin, linkedin.get_monthly_posts, linkedin_file)

    # Print summaries
    print(f"Discord: {len(discord_messages)} messages this month.")
    print(f"Maps: Visited {len(maps_locations)} locations this month.")
    print(f"GitHub: {len(github_events)} events this month.")
    print(f"LinkedIn: {len(linkedin_posts)} posts this month.")
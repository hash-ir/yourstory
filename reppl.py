#%%
from src.data_pipeline.apis import DiscordClient, MapsClient, GitHubClient, LinkedInClient, load_from_file, save_to_file
from dotenv import load_dotenv
import os

load_dotenv()
#%%

discord_file = 'data/raw/discord_monthly.json'
discord = DiscordClient(
    bot_token=os.getenv('DISCORD_BOT_TOKEN'),
    user_id=os.getenv('DISCORD_USER_ID')
)

# %%
data = discord.get_monthly_messages(['1333760748987613216'],initial_date=(2023, 5, 1), any_user = True)
data
save_to_file(data, discord_file)

# %%
github = GitHubClient(
    token=os.getenv('GITHUB_TOKEN'),
    username=os.getenv('GITHUB_USERNAME')
)
# %%
data =github.get_monthly_activity(initial_date=(2025, 3, 15))
github_file = 'data/raw/github_monthly.json'
save_to_file(data, github_file)
# %%
len(data)
# %%

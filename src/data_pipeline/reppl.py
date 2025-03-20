#%%
from apis import DiscordClient, MapsClient, GitHubClient, LinkedInClient, load_from_file, save_to_file
from dotenv import load_dotenv
import os

load_dotenv()
#%%

discord_file = 'discord_monthly.json'
discord = DiscordClient(
    bot_token=os.getenv('DISCORD_BOT_TOKEN'),
    user_id=os.getenv('DISCORD_USER_ID')
)

# %%
data = discord.get_monthly_messages(['1333760748987613216'], True)

save_to_file(data, discord_file)
# %%
data
# %%

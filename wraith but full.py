import asyncio
import discord
from discord.ext import commands
from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel

TOKEN = "NzUwNDY4NjcxMDg3ODM3MzU0.GaDiyL.0aYxlkBgjbCzBn4aFCODFg3kTFXz9_2b8ALApk"
GUILD_ID = "1307019842410516573"
ROLE_NAME = "TikTok Live"
ANNOUNCE_CHANNEL_ID = 1308455912876282006  # Replace with your Discord channel ID for announcements

# List of TikTok users and corresponding Discord usernames
TIKTOK_USERS = [
    {"tiktok_username": "@baddiedaddyp", "discord_username": "baddiedaddyp"},
    {"tiktok_username": "@arkidd83", "discord_username": "kidd00083"},
    {"tiktok_username": "@theoryplus", "discord_username": "theoryplus"},
    {"tiktok_username": "@sykk182", "discord_username": "sykk182"},
    {"tiktok_username": "@tiktokbarryallen", "discord_username": "tiktokbarryallen"},
    {"tiktok_username": "@revenant_oc", "discord_username": "revenant_oc"},
    {"tiktok_username": "@odinz_den", "discord_username": "odinz_den"},
    {"tiktok_username": "@luvkipsy", "discord_username": "luvkipsy"},
    {"tiktok_username": "@maggdylan", "discord_username": "MaggDylan"},
    {"tiktok_username": "@tiktoknoskills", "discord_username": "n0skills_gaming"},
]

# Users with custom messages
SPECIAL_USERS = {
    "@sykk182": " @everyone 🎉 **Special Alert:** sykk182 is live! Let's go show our leader some love! 🎉",
    "@revenant_oc": " @everyone 🌟  **Special Alert:** General revenant_oc is now live! Come chill, chat and..... Brain Buffering... Please Wait... 🌟",
    "@odinz_den": " @everyone 🌟   **VIP Streamer:** odinz_den Just your not so typical phasmo/horror streamer is now live! Get in here before i get Thor after you! 🌟",
    "@tiktokbarryallen": " @everyone 🌟   **VIP Streamer:** General tiktokbarryallen is now live! Get over there fast AF Boi! 🌟",
    "@baddiedaddyp": " @everyone 🌟   **VIP Streamer:** General baddiedaddyp is live and you’re a big dill to me so get in here!  🌟",
    "@luvkipsy": " @everyone 🌟   **Special Alert:**  luvkipsy is live and ready for the vibes! Come join me!  🌟",
}

# Create a TikTokLiveClient for each user
clients = {user["tiktok_username"]: TikTokLiveClient(unique_id=user["tiktok_username"]) for user in TIKTOK_USERS}

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def monitor_tiktok(user, client):
    guild = discord.utils.get(bot.guilds, id=int(GUILD_ID))
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    member = discord.utils.get(guild.members, name=user["discord_username"])
    announce_channel = discord.utils.get(guild.text_channels, id=ANNOUNCE_CHANNEL_ID)

    if announce_channel is None:
        client.logger.error(f"Announce channel with ID {ANNOUNCE_CHANNEL_ID} not found. Please check the channel ID.")
        return

    live_status = False  # Track live status to avoid duplicate notifications

    while True:
        try:
            if not await client.is_live():
                client.logger.info(f"{user['tiktok_username']} is not live. Checking again in 60 seconds.")
                if role in member.roles:
                    await member.remove_roles(role)
                    client.logger.info(f"Removed {ROLE_NAME} role from {member.name}")
                live_status = False
                await asyncio.sleep(60)
            else:
                client.logger.info(f"{user['tiktok_username']} is live!")
                if role not in member.roles:
                    await member.add_roles(role)
                    client.logger.info(f"Added {ROLE_NAME} role to {member.name}")
                if not live_status:  # Only announce the first time they go live
                    tiktok_url = f"https://www.tiktok.com/@{user['tiktok_username'].lstrip('@')}/live"
                    if user["tiktok_username"] in SPECIAL_USERS:
                        await announce_channel.send(f"{SPECIAL_USERS[user['tiktok_username']]} \n🔴 **Watch live here:** {tiktok_url}")
                    else:
                        await announce_channel.send(f"🚨 {user['tiktok_username']} is now live on TikTok! Let's show some love! \n🔴 **Watch live here:** {tiktok_url}")
                    live_status = True
                await asyncio.sleep(60)
        except Exception as e:
            client.logger.error(f"Error monitoring {user['tiktok_username']}: {e}")
            await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    # Set up logging for each TikTokLiveClient
    for user, client in clients.items():
        client.logger.setLevel(LogLevel.INFO.value)
        # Start monitoring each TikTok user
        asyncio.create_task(monitor_tiktok(
            next(u for u in TIKTOK_USERS if u["tiktok_username"] == user),
            client
        ))

if __name__ == "__main__":
    bot.run(TOKEN)

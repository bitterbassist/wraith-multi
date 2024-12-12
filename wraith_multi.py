import asyncio
import discord
from discord.ext import commands
from TikTokLive import TikTokLiveClient
from TikTokLive.client.logger import LogLevel

# Bot token
TOKEN = "NzUwNDY4NjcxMDg3ODM3MzU0.GaDiyL.0aYxlkBgjbCzBn4aFCODFg3kTFXz9_2b8ALApk"

# Server-specific TikTok users
TIKTOK_USERS = {
    "1307019842410516573": [  # Sykk Shadows
        {"tiktok_username": "@sykk182", "discord_username": "sykk182"},
        {"tiktok_username": "@revenant_oc", "discord_username": "revenant_oc"},
        {"tiktok_username": "@odinz_den", "discord_username": "odinz_den"},
        {"tiktok_username": "@tiktokbarryallen", "discord_username": "tiktokbarryallen"},
        {"tiktok_username": "@baddiedaddyp", "discord_username": "baddiedaddyp"},
        {"tiktok_username": "@luvkipsy", "discord_username": "luvkipsy"},
        {"tiktok_username": "@maggdylan", "discord_username": "Magg Dylan"},
        {"tiktok_username": "@tiktoknoskills", "discord_username": "n0skills_gaming"},
    ],
    "768792770734981141": [  # Pickle Squad
        {"tiktok_username": "@baddiedaddyp", "discord_username": "baddiedaddyp"},
        {"tiktok_username": "@sykk182", "discord_username": "sykk182"},
        {"tiktok_username": "@revenant_oc", "discord_username": "revenant_oc"},
        {"tiktok_username": "@tiktokbarryallen", "discord_username": "tiktokbarryallen"},
        {"tiktok_username": "@tiktoknoskills", "discord_username": "n0skills_gaming"},
    ],
    "1145354259530010684": [  # Flash Server
        {"tiktok_username": "@tiktokbarryallen", "discord_username": "tiktokbarryallen"},
        {"tiktok_username": "@baddiedaddyp", "discord_username": "baddiedaddyp"},
        {"tiktok_username": "@sykk182", "discord_username": "sykk182"},
        {"tiktok_username": "@revenant_oc", "discord_username": "revenant_oc"},
        {"tiktok_username": "@tiktoknoskills", "discord_username": "n0skills_gaming"},
    ],
}

# Users with custom messages per server
SPECIAL_USERS = {
    "1307019842410516573": {  # Sykk Shadows
        "@sykk182": " @everyone 🎉 **Special Alert:** sykk182 is live! Let's go show our leader some love! 🎉",
        "@revenant_oc": " @everyone 🌟  **Special Alert:** General revenant_oc is now live! Come chill, chat and..... Brain Buffering... Please Wait... 🌟",
        "@odinz_den": " @everyone 🌟   **VIP Streamer:** odinz_den Just your not so typical phasmo/horror streamer is now live! Get in here before I get Thor after you! 🌟",
        "@tiktokbarryallen": " @everyone 🌟   **VIP Streamer:** General tiktokbarryallen is now live! Get over there fast AF Boi! 🌟",
        "@baddiedaddyp": " @everyone 🌟   **VIP Streamer:** General baddiedaddyp is live and you’re a big dill to me so get in here!  🌟",
        "@luvkipsy": " @everyone 🌟   **Special Alert:**  luvkipsy is live and ready for the vibes! Come join me!  🌟",
        "@maggdylan": " @everyone 🎉 **Special Alert:** Magg Dylan is live! Let's go show our leader and the band some love! 🎉",
    },
    "768792770734981141": {  # Pickle Squad
        "@baddiedaddyp": " @everyone 🌟 baddiedaddyp is live and you’re a big dill to me so get in here!  🌟",
        "@sykk182": " 🎉  sykk182 is live! Let's go show support! 🎉",
        "@revenant_oc": " 🌟  revenant_oc is live! Come chill, chat and..... Brain Buffering... Please Wait... 🌟",
        "@tiktokbarryallen": "  🌟  tiktokbarryallen is now live! Get over there fast AF Boi! 🌟",
    },
    "1145354259530010684": {  # Flash Server
        "@tiktokbarryallen": " @everyone  🌟  tiktokbarryallen is now live! Get over there fast AF Boi! 🌟",
        "@baddiedaddyp": "  🌟 baddiedaddyp is live and you’re a big dill to me so get in here!  🌟",
        "@sykk182": " 🎉  sykk182 is live! Let's go show support! 🎉",
        "@revenant_oc": " 🌟  revenant_oc is live! Come chill, chat and..... Brain Buffering... Please Wait... 🌟",
    },
}

# Create a TikTokLiveClient for each user per server
clients = {
    guild_id: {user["tiktok_username"]: TikTokLiveClient(unique_id=user["tiktok_username"]) for user in users}
    for guild_id, users in TIKTOK_USERS.items()
}

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Server-specific configurations
server_configs = {
    "1307019842410516573": {  # Sykk Shadows
        "announce_channel_id": 1308455912876282006,
        "role_name": "TikTok Live",
        "owner_stream_channel_id": 1316253711886061568,
        "owner_tiktok_username": "@maggdylan",
    },
    "768792770734981141": {  # Pickle Squad
        "announce_channel_id": 1306652093037285386,
        "role_name": "LIVE on TikTok",
        "owner_stream_channel_id": 1312075893274968165,
        "owner_tiktok_username": "@baddiedaddyp",
    },
    "1145354259530010684": {  # Flash Server
        "announce_channel_id": 1209176431968653442,
        "role_name": "Live on TikTok",
        "owner_stream_channel_id": 1147180719072878603,
        "owner_tiktok_username": "@tiktokbarryallen",
    },
}

async def monitor_tiktok(user, client, guild_config):
    guild_id = guild_config.get("guild_id")
    announce_channel_id = guild_config.get("announce_channel_id")
    owner_stream_channel_id = guild_config.get("owner_stream_channel_id")
    owner_tiktok_username = guild_config.get("owner_tiktok_username")
    role_name = guild_config.get("role_name")

    guild = discord.utils.get(bot.guilds, id=guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    member = discord.utils.get(guild.members, name=user["discord_username"])
    announce_channel = discord.utils.get(guild.text_channels, id=announce_channel_id)
    owner_channel = discord.utils.get(guild.text_channels, id=owner_stream_channel_id)

    live_status = False  # Track live status to avoid duplicate notifications

    # Configure logger for the client
    client.logger.setLevel(LogLevel.INFO.value)

    while True:
        try:
            if not await client.is_live():
                client.logger.info(f"{user['tiktok_username']} is not live. Checking again in 60 seconds.")
                if role in member.roles:
                    await member.remove_roles(role)
                    client.logger.info(f"Removed {role_name} role from {member.name}")
                live_status = False
                await asyncio.sleep(60)
            else:
                client.logger.info(f"{user['tiktok_username']} is live!")
                if role not in member.roles:
                    await member.add_roles(role)
                    client.logger.info(f"Added {role_name} role to {member.name}")
                if not live_status:  # Only announce the first time they go live
                    tiktok_url = f"https://www.tiktok.com/@{user['tiktok_username'].lstrip('@')}/live"

                    # Fetch the custom message for the specific server
                    server_messages = SPECIAL_USERS.get(str(guild_id), {})
                    message = server_messages.get(
                        user["tiktok_username"],
                        f"🚨 {user['tiktok_username']} is now live on TikTok! Let's show some love! \n🔴 **Watch live here:** {tiktok_url}"
                    )

                    # Include optional metadata if available
                    try:
                        metadata = await client.get_live_metadata()
                        if metadata:
                            message += f"\n📢 Title: {metadata.get('title', 'Untitled')}\n👥 Viewers: {metadata.get('viewer_count', 'N/A')}"
                    except Exception as e:
                        client.logger.warning(f"Could not fetch metadata for {user['tiktok_username']}: {e}")

                    await announce_channel.send(message)
                    client.logger.info(f"Announced live stream for {user['tiktok_username']} in channel {announce_channel.name}")

                    # If the current TikTok user is the server owner, send to their personal channel
                    if user["tiktok_username"] == owner_tiktok_username and owner_channel:
                        await owner_channel.send(f"🔴 {user['tiktok_username']} is now live on TikTok! \n🔗 Watch live: {tiktok_url}")
                        client.logger.info(f"Notified owner channel for {user['tiktok_username']}")

                    live_status = True
                await asyncio.sleep(60)
        except Exception as e:
            client.logger.error(f"Error monitoring {user['tiktok_username']}: {e}")
            await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    for guild_id, users in TIKTOK_USERS.items():
        for user in users:
            client = clients[guild_id][user["tiktok_username"]]
            client.logger.setLevel(LogLevel.INFO.value)
            asyncio.create_task(monitor_tiktok(
                user,
                client,
                {**server_configs[guild_id], "guild_id": int(guild_id)}
            ))

if __name__ == "__main__":
    bot.run(TOKEN)

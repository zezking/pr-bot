import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
BOT_ID = os.getenv("DISCORD_BOT_ID")
REVIEW_CHANNEL_ID = os.getenv("DISCORD_REVIEW_CHANNEL_ID")
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
intents.messages = True
guild = discord.Guild
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    try:
        print(f"{client.user} has connected discord server")
    except Exception as err:
        print(f"Failed to look for guild {err}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@client.event
async def on_raw_reaction_add(payload):
    emoji_action = {
        "👀": ("is reviewing"),
        "✅": ("has approved"),
    }
    members = client.get_all_members()
    membersIds = list(map(lambda member: member.id, members))
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if payload.channel_id != int(str(REVIEW_CHANNEL_ID)):
        return
    if message.author.id == payload.user_id:
        await message.remove_reaction(payload.emoji.name, payload.member)
        await channel.send("You can't review or approve your own pullrequest")
        return

    for id in membersIds:
        if id != int(str(BOT_ID)) and id != payload.user_id:
            reviewer = await client.fetch_user(id)
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await reviewer.send(
                f"{reviewer.name} {emoji_action[payload.emoji.name]} {message.jump_url}"
            )


if TOKEN:
    client.run(TOKEN)
else:
    print("Missing discord token")

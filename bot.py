import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
BOT_ID = os.getenv("DISCORD_BOT_ID")
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
        print(f"{client.user} has connected guild")
    except Exception as err:
        print(f"Failed to look for guild {err}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@client.event
async def on_raw_reaction_add(payload):
    members = client.get_all_members()
    membersIds = list(map(lambda member: member.id, members))
    if payload.emoji.name == "👀" and payload.channel_id == 1093683351300350012:
        for id in membersIds:
            if id != int(str(BOT_ID)):
                reviewer = await client.fetch_user(id)
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                print(id)
                await reviewer.send(
                    f"{reviewer.name} is looking at your motherfking PR {message.jump_url}"
                )

    if payload.emoji.name == "✅" and payload.channel_id == 1093683351300350012:
        for id in membersIds:
            if id != int(str(BOT_ID)):
                reviewer = await client.fetch_user(id)
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                print(id)
                await reviewer.send(
                    f"{reviewer.name} has approved your PR {message.jump_url}"
                )


if TOKEN:
    client.run(TOKEN)
else:
    print("Missing discord token")

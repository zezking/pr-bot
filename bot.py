import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True
intents.messages = True
guild = discord.Guild
client = discord.Client(intents=intents)

members = client.get_all_members()
membersIds = map(lambda member: member.id, members)


@client.event
async def on_ready():
    try:
        print(f"{client.user} has connected guild")
    except Exception as err:
        print(f"Failed to look for guild {err}")


@client.event
async def on_message(message):
    memberIds = [369599324054618134, 539632925675880459]
    if message.author == client.user:
        return
    if message.channel.id == 1093683351300350012 and message.content.startswith("PR"):
        print(message.content)
        for id in memberIds:
            print(id, message.author.id)
            if id != message.author.id:
                reviewer = await client.fetch_user(id)
                await reviewer.send(
                    f"{reviewer.name} is looking at your motherfking PR"
                )


@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "👀" and payload.channel_id == 1093683351300350012:
        for id in membersIds:
            if id != payload.user_id:
                reviewer = await client.fetch_user(id)
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await reviewer.send(
                    f"{reviewer.name} is looking at your motherfking PR {message.jump_url}"
                )

    if payload.emoji.name == "✅" and payload.channel_id == 1093683351300350012:
        for id in membersIds:
            if id != payload.user_id:
                reviewer = await client.fetch_user(id)
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await reviewer.send(
                    f"{reviewer.name} has approved your PR {message.jump_url}"
                )


if TOKEN:
    client.run(TOKEN)
else:
    print("Missing discord token")

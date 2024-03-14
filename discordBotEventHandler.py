from ast import If, Not
import discord
from dotenv import load_dotenv
import os

load_dotenv()
discord_server_token=os.getenv("discord_server_token")
discord_server_id=os.getenv("discord_server_token")
if discord_server_token == None :
    discord_server_token = ""

if discord_server_id == None :
    discord_server_id = ""

while (discord_server_id != None and discord_server_token != None) :
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    tree = discord.app_commands.CommandTree(client)

    # Add the guild ids in which the slash command will appear.
    # If it should be in all, remove the argument, but note that
    # it will take some time (up to an hour) to register the
    # command if it's for all guilds.
    @tree.command(
        name="commandname",
        description="My first application Command",
        guild=discord.Object(discord_server_id)
    )
    async def first_command(interaction):
        await interaction.response.send_message("Hello!")

    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(discord_server_id))
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    client.run(discord_server_token)
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import wolDiscordBot
import startServer

import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor


def restart_bot_script():
        
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")
       
        os.execv(sys.executable, ['python'] + sys.argv)

class BotCommands(commands.Cog, name="BotCommands"):
    def __init__(self, bot) -> None:
        self.bot = bot

    
    @commands.hybrid_command(
        name="testcommand",
        description="This is a testing command that does nothing.",
    )
    async def testcommand(self, context: Context) -> None:
        """
        This is a testing command that does nothing.

        :param context: The application command context.
            """
            # Do your stuff here
    
            # Don't forget to remove "pass", I added this just because there's no content in the method.
        await context.send("something")
        

    @commands.hybrid_command(
        name="restart_bot",
        description="This restarts bot on controller server. Does not have any influence on the game servers"
    )
    async def restart_bot(self, context: Context) -> None:
        print("Restart request has been sent to bot")
        await context.send("Bot is restarting, wait a moment")
        restart_bot_script()

    @commands.hybrid_command(
        name="start_host",
        description="Wake gaming server by issuing Magic Packet from controller to BoberGaming"
    )
    async def start_host(self, context: Context) -> None:
        print("Sending Magic packet to Bober Gaming")
        wolDiscordBot.wakeUp()
        await context.send("Bober Gaming should be starting in a minute, happy gaming")
    
    @commands.hybrid_command(
        name="start_server",
        description="Start game server"
    )
    @app_commands.choices(game=[
        app_commands.Choice(name='Terraria',value='terraria'),
        app_commands.Choice(name='Project Zomboid',value='zomboid')
        ]
    )
    async def start_server(self, context: Context, game: app_commands.Choice[str]) -> None:
                
        if game.value == 'zomboid':
            loop = asyncio.get_event_loop()
            block_return = await loop.run_in_executor(ThreadPoolExecutor(), startServer.startZomboid)
            #startServer.startZomboid()
            await context.send("Starting Zomboid Server on 192.168.0.143 port 21261!")
        elif game.value == 'terraria':
            loop = asyncio.get_event_loop()
            block_return = await loop.run_in_executor(ThreadPoolExecutor(), startServer.startTerraria)
            #startServer.startTerraria()
            await context.send("Starting Terraria Server on 192.168.0.143 port 7777!")
        else:
            await context.send("Wrong server name")
    
    # And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(BotCommands(bot))

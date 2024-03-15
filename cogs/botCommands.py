from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

import os
import sys

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

    
    # And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(BotCommands(bot))
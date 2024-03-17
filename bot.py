import logging
import os
import discord
import platform
import sys
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True


load_dotenv()
discord_server_token=os.getenv("discord_server_token", default="")
discord_server_id=os.getenv("discord_server_id", default="")


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.server_id = discord_server_id

    @discord.app_commands.guilds(int(discord_server_id))
    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    # async def status_task(self) -> None:
    #     """
    #     Setup the game status task of the bot.
    #     """
    #     bot_status = "I AM DA KONTROLAH!"
    #     await self.change_presence(status=discord.Status.online, activity=discord.Game(bot_status))

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        self.logger.info(f"Logged in as BudzBobera")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        # await self.init_db()
        await self.load_cogs()
        # await self.status_task()
        # self.database = DatabaseManager(
        #     connection=await aiosqlite.connect(
        #         f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
        #     )
        # )

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
        
 
        
    
        
#bot = discord.Client(intents=intents)
#tree = discord.app_commands.CommandTree(bot)

# from typing import Literal, Optional

# import discord
# from discord.ext import commands


# @bot.command()
# @commands.guild_only()
# @commands.is_owner()
# async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
#     if not guilds:
#         if spec == "~":
#             synced = await ctx.bot.tree.sync(guild=ctx.guild)
#         elif spec == "*":
#             ctx.bot.tree.copy_global_to(guild=ctx.guild)
#             synced = await ctx.bot.tree.sync(guild=ctx.guild)
#         elif spec == "^":
#             ctx.bot.tree.clear_commands(guild=ctx.guild)
#             await ctx.bot.tree.sync(guild=ctx.guild)
#             synced = []
#         else:
#             synced = await ctx.bot.tree.sync()

#         await ctx.send(
#             f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
#         )
#         return

#     ret = 0
#     for guild in guilds:
#         try:
#             await ctx.bot.tree.sync(guild=guild)
#         except discord.HTTPException:
#             pass
#         else:
#             ret += 1

#     await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

bot = DiscordBot()

while (discord_server_id != None and discord_server_token != None) :
    bot.run(discord_server_token)
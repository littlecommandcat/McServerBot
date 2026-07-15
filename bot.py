import discord
import asyncio
import os
import json
from dotenv import load_dotenv
from discord.ext import commands
from mcrcon import MCRcon
from typing import Union, List, Dict

load_dotenv()

TOKEN: Union[str, None] = os.getenv("TOKEN")
PREFIX: str = os.getenv("PREFIX") or "?"
RCON_HOST: str = os.getenv("HOST") or "localhost"
RCON_PORT: int = int(os.getenv("PORT")) or 22565
RCON_PASSWORD: Union[str, None] = os.getenv("PASSWORD")
ALLOWED_LIST: List = json.loads(os.getenv("ALLOWEDLIST")) or []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

def send_command(command: str) -> Union[str, None]:
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        response = mcr.command(command)
    
    return response

@bot.event
async def on_ready():
    print(f"Login as {bot.user.name}({bot.user.id})")

@bot.command()
async def cmd(ctx: commands.Context, *, command: str):
    if ctx.author.id not in ALLOWED_LIST:
        return
    try:
        response = send_command(command=command)
        await ctx.send(f"Executed command `{command}` with response:\n```{response if len(response) < 1900 else (response[:100] + '...')}```")
    except Exception as e:
        await ctx.send(f"Error:```{e}```")


async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
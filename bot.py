import discord
from discord.ext import commands
import os, glob
import time

owner_id = 133713371337133713

##

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def archive(ctx, arg):
    # Arg is usually a full path to a file.
    if ctx.message.author.id == owner_id:
        inc_number = 1
        file_number = f"{inc_number:03}"
        CHUNK_SIZE = 8388608
        file_to_split = arg
        await ctx.send(f"#############################")
        await ctx.send(f"Sending file: {file_to_split}")
        with open(arg, 'rb') as f:
            orig_name = os.path.basename(arg)
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                with open(orig_name + '.chunk' + str(file_number), 'w+b') as chunk_file:
                    chunk_file.write(chunk)
                    if os.path.getsize(orig_name + '.chunk' + str(file_number)) >= 1:
                        await ctx.send(file=discord.File(orig_name + '.chunk' + str(file_number)))
                    else:
                        time.sleep(3)
                        await ctx.send(file=discord.File(orig_name + '.chunk' + str(file_number)))
                inc_number += 1
                file_number = f"{inc_number:03}"
                chunk = f.read(CHUNK_SIZE)
            await ctx.send(f"#############################")
        f.close()
        for filename in glob.glob("*.chunk*"):
            os.remove(filename)


bot.run('TOKEN_HERE')

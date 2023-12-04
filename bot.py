import responses
import discord
from discord import app_commands
from discord.ext import commands
from discord import File
from diffusers import StableDiffusionPipeline
import torch


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():

    with open('pass/token.txt') as f:
        TOKEN = f.readline()
    intents = discord.Intents.all()
    
    client = commands.Bot(intents=intents, command_prefix="!")
    model_id = "dreamlike-art/dreamlike-anime-1.0"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    print(f'{client.user} has loaded AI model!')
    
    @client.command()
    async def hello(ctx):
        await ctx.send("test working")

    @client.command()
    async def generate(ctx):
        user_message = ctx.message.content
        command, *args = user_message.split()
        args_str = ' '.join(args)
        
        prompt = "anime, masterpiece, high quality, absurdres, 1girl"
        negative_prompt = 'simple background, duplicate, retro style, low quality, lowest quality, 1980s, 1990s, 2000s, 2005 2006 2007 2008 2009 2010 2011 2012 2013, bad anatomy, bad proportions, extra digits, lowres, username, artist name, error, duplicate, watermark, signature, text, extra digit, fewer digits, worst quality, jpeg artifacts, blurry'
        #image = pipe(prompt, negative_prompt=negative_prompt).images[0]
        #image.save("result.jpg")
        with open("result.jpg", "rb") as fp:
            file = discord.File(fp, filename="result.jpg")
            await ctx.send(f"Image generated from key words: {args_str}")
            await ctx.send(file=file)
        



    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    

    client.run(TOKEN)
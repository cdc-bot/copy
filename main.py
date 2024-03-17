import disnake
from disnake.ext import commands
import json
intents = disnake.Intents.all()
bot = commands.Bot(intents=intents,command_prefix="c!")
def json_write(filename,data):
    json_data = json.dumps(data)
    file = open(filename,"w")
    file.write(json_data)
    file.close()

def json_read(filename):
    file = open(filename,"r")
    file_c = file.read()
    file.close()
    data = json.loads(file_c)
    return data
    
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
@bot.slash_command()
async def paste(ctx):
    copied = json_read("./copy.json")
    copied_object = {}
    for copy in copied:
        if copy["copied_by"] == ctx.author.id:
            copied_object = copy
    #await ctx.send(f"```json\n{copied_object}\n```")
    webhooks = await ctx.channel.webhooks()
    webhook = None
    for webhook_ in webhooks:
        if webhook_.user == bot.user:
            webhook = webhook_
    if webhook == None:
        webhook = await ctx.channel.create_webhook(name="Copy Helper",reason="Create webhook for paste command.")
    copied_user = await bot.fetch_user(copied_object['copied_person'])
    copied_user_name = copied_user.name
    if copied_user.display_name != None:
        copied_user_name = copied_user.display_name
    await webhook.send(content=copied_object['copied_content'],username=copied_user_name,avatar_url=copied_user.display_avatar.url)
    await ctx.send(content="pasted",ephemeral=True)
@bot.message_command(name="Copy")
async def copy(ctx):
    copied = json_read("./copy.json")
    obj = {"copied_by":ctx.author.id,"copied_person":ctx.target.author.id,"copied_content":ctx.target.content}
    copied.append(obj)
    json_write("./copy.json",copied)
    await ctx.send("copied",ephemeral=True)

bot.run("")

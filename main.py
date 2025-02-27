import disnake
from disnake.ext import commands
import json
import os

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="c!")


def json_write(filename, data):
    json_data = json.dumps(data)
    file = open(filename, "w")
    file.write(json_data)
    file.close()


def json_read(filename):
    file = open(filename, "r")
    file_c = file.read()
    file.close()
    data = json.loads(file_c)
    return data


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    await bot.change_presence(status=disnake.Status.idle,activity=disnake.Activity(name="custom",type=disnake.ActivityType.custom,state="Apps -> Copy | /paste"))

@bot.slash_command()
async def paste(ctx):
    copied = json_read("./copy.json")
    copied_object = {}
    for copy in copied:
        if copy["copied_by"] == ctx.author.id:
            copied_object = copy
    if copied_object == {}:
        await ctx.send("<:x_:1344624265839775764> You don't have anything copied!",ephemeral=True)
        return
    # await ctx.send(f"```json\n{copied_object}\n```")
    webhooks = await ctx.channel.webhooks()
    webhook = None
    for webhook_ in webhooks:
        if webhook_.user == bot.user:
            webhook = webhook_
    if webhook == None:
        webhook = await ctx.channel.create_webhook(
            name="Copy Helper", reason="Create webhook for paste command."
        )
    copied_user = await ctx.guild.fetch_member(copied_object["copied_person"])
    copied_user_name = copied_user.name
    if copied_user.display_name != None:
        copied_user_name = copied_user.display_name
    await webhook.send(
        content=f"{copied_object["copied_content"]}",
        username=copied_user_name,
        avatar_url=copied_user.display_avatar.url,
        allowed_mentions=disnake.AllowedMentions.none(),
        embed=disnake.Embed(title=None,description=f"Pasted by {ctx.author.mention}")
    )
    await ctx.send(content="Message successfully pasted!", ephemeral=True)

@bot.slash_command(name="colon_three")
async def cthr(ctx):
    await ctx.channel.send(f":3\n-# From {ctx.author.mention}")
    await ctx.send(":3 sent",ephemeral=True)
@bot.message_command(name="Copy")
async def copy(ctx):
    if ctx.target.webhook_id != None:
        await ctx.send("<:x_:1344624265839775764> You can't copy webhooks!",ephemeral=True)
        return
    copied = json_read("./copy.json")
    obj = {
        "copied_by": ctx.author.id,
        "copied_person": ctx.target.author.id,
        "copied_content": ctx.target.content,
    }
    copied.append(obj)
    json_write("./copy.json", copied)
    await ctx.send("Message successfully copied!", ephemeral=True)
    try:
        await ctx.target.author.send(content=f"## Your message has been copied\n{ctx.author.mention} has copied your message.\n-# Message copied: {ctx.target.jump_url}")
    except:
        print("couldn't notify!")
try:
    bot.run(os.environ["COPY_TOKEN"])
except:
    print("bot.run execution failed!")
    print("This is likely because you do not have the 'COPY_TOKEN' environment variable set.")


import functools
import discord
from discord.ext import commands
from TranslateCore import Translator

import Secrets

class CacheForMenuTranslate:
    message: discord.Message
    author: discord.User
    lastLang: str

    def saveState(self, msg: discord.Message, author:discord.User, lastLang: str):
        self.author = author
        self.message = msg
        self.lastLang = lastLang

cache = CacheForMenuTranslate()

intents = discord.Intents.default()
intents.message_content = True

Transearly = commands.Bot("!", intents=intents)
translator = Translator()

@Transearly.event
async def on_ready():
    print(f'We have logged in as {Transearly.user}')
    await Transearly.tree.sync()

@Transearly.tree.command(name="translate", description="translate text to target language")
@discord.app_commands.describe(text="The source text to traslate from", targetlang="The target languages to translate to. Seperate by comma. i.e <lang1,lang2,...>")
async def translate(interaction: discord.Interaction, text: str, targetlang: str="en, zh-Hans"):
    to = targetlang.replace(" ", "").split(",")
    result = translator.translate(text, to)
    if(result is None):
        await interaction.response.send_message("Something is wrong", ephemeral=True)
        return

    replyEmbed = discord.Embed(title="Translate Result", description=text)
    replyEmbed.add_field(
        name="Source Language", 
        value=translator.getNameOfLangFromCode(result["srcLang"]) + " [" + result["srcLang"] + "]", 
        inline=False
    )
    # reply = "The source language is " + translator.getNameOfLangFromCode(result["srcLang"])
    for r in result["result"]:
        replyEmbed.add_field(name=translator.getNameOfLangFromCode(r["to"]), value=r["text"], inline=False)
        # reply += "\n" + translator.getNameOfLangFromCode(r["to"]) + ": " + r["text"]

    await interaction.response.send_message(embed=replyEmbed, ephemeral=True)

# Menu cmd
async def translateInMenu(interaction: discord.Interaction, message: discord.Message):
    text = message.content
    to = ["en", "zh-Hans"]
    result = translator.translate(text, to)
    if(result is None):
        await interaction.response.send_message("Something is wrong", ephemeral=True)
        return
    replyEmbed = discord.Embed(title="Translate Result", description=text)
    replyEmbed.add_field(
        name="Source Language", 
        value=translator.getNameOfLangFromCode(result["srcLang"]) + " [" + result["srcLang"] + "]", 
        inline=False
    )
    for r in result["result"]:
        replyEmbed.add_field(name=translator.getNameOfLangFromCode(r["to"]), value=r["text"], inline=False)

    cache.saveState(message, interaction.user, result["srcLang"])

    await interaction.response.send_message(embed=replyEmbed, ephemeral=True)

translate_menu = discord.app_commands.ContextMenu(
    name='translate',
    callback=translateInMenu,
)
Transearly.tree.add_command(translate_menu)

@Transearly.tree.command(name="reply", description="reply to the last translated message")
@discord.app_commands.describe(text="The source text to traslate from")
async def translate(interaction: discord.Interaction, text: str):
    result = translator.translate(text, [cache.lastLang])
    if(result is None):
        await interaction.response.send_message("Something is wrong", ephemeral=True)
        return
    await cache.message.reply(content=result["result"][0]["text"])

    await interaction.response.send_message("message replied", ephemeral=True)


Transearly.run(Secrets.DISCORD_APP_TOKEN)
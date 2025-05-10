import discord
from discord.ext import commands
import re
import os
from keep_alive import keep_alive

# ロールID設定
STICKER_BANNED_ROLE_ID = 1370347710468591678
EMOJI_BANNED_ROLE_ID = 1370343214048874538

# Intent設定
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot起動
bot = commands.Bot(command_prefix='!', intents=intents)

# 絵文字正規表現（カスタム&Unicode）
EMOJI_REGEX = re.compile(
    r'(<a?:[a-zA-Z0-9_]+:\d{18,}>|[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U0001F1E6-\U0001F1FF\U00002700-\U000027BF])'
)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    member = message.guild.get_member(message.author.id)
    if not member:
        return

    # ステッカー使用チェック
    if message.stickers:
        if any(role.id == STICKER_BANNED_ROLE_ID for role in member.roles):
            try:
                await message.delete()
                await message.channel.send(
                    f'🚫 {message.author.mention} is not allowed to use stickers lol',
                    delete_after=5
                )
            except discord.Forbidden:
                print('cant delete: missing perms.')

    # 絵文字使用チェック
    elif EMOJI_REGEX.search(message.content):
        if any(role.id == EMOJI_BANNED_ROLE_ID for role in member.roles):
            try:
                await message.delete()
                await message.channel.send(
                    f'🚫 {message.author.mention} aint allowed to use emojis lol.',
                    delete_after=5
                )
            except discord.Forbidden:
                print('cant delete: missing perms.')

    await bot.process_commands(message)

# Replit keep-alive
keep_alive()

# .env から TOKEN を読み込んで起動
bot.run(os.getenv("TOKEN"))

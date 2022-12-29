import datetime

import discord
from discord.ext import commands

from database.models import LevelUser


async def send_level_up(member: discord.Member, level_user: LevelUser, channel: discord.abc.Messageable):
	embed = discord.Embed(
		title='Level Up!',
		description=f'{member.mention} ist nun Level {level_user.get_level()}!',
		color=discord.Color.green(),
		timestamp=datetime.datetime.utcnow()
	)
	embed.set_thumbnail(url=member.avatar_url)
	await channel.send(embed=embed)


class ActivityListener(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.last_activities = {}

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		if message.author.bot:
			return

		if message.author.id in self.last_activities:
			if self.last_activities[message.author.id] + datetime.timedelta(seconds=60) > message.created_at:
				return

		level_user = await LevelUser(message.author.id).load()
		if await level_user.add_xp(1):
			await send_level_up(message.author, level_user, message.channel)
		self.last_activities[message.author.id] = message.created_at

def setup(bot: commands.Bot):
	bot.add_cog(ActivityListener(bot))
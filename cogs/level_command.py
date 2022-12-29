import datetime

import discord
from discord import ApplicationCommandInteraction
from discord.ext import commands

from database.models import LevelUser


class LevelCommand(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.slash_command(name='level', description='Zeigt dir dein Level an.')
	async def level(self, ctx: ApplicationCommandInteraction):
		level_user = await LevelUser(ctx.author.id).load()
		embed = discord.Embed(
			title='Level Up!',
			description=f'Du bist Level **{level_user.get_level()}** und hast aktuell `{level_user.xp}` XP.',
			color=discord.Color.green(),
			timestamp=datetime.datetime.utcnow()
		)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.respond(embed=embed, hidden=True)

def setup(bot: commands.Bot):
	bot.add_cog(LevelCommand(bot))
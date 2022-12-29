import discord
from discord.ext import commands


class SetupCommand(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.slash_command(base_name='setup', name='userinfo', description='Setup the userinfo command')
	async def setup_userinfo_command(self, ctx):
		await ctx.respond('Click the button to get your user info', components=[
			discord.Button(label='User Info', custom_id='userinfo-btn')
		])

	@commands.Cog.slash_command(base_name='setup', name='roles', description='Setup the roles command')
	async def setup_userinfo_command(self, ctx):
		await ctx.respond('Role selection!', components=[
			discord.SelectMenu(placeholder='Select your favorite role', custom_id='role-selection', max_values=3, options=[
				discord.SelectOption(label='Liebe', value='667129686131736586', emoji='❤️'),
				discord.SelectOption(label='Kälte', value='667129722995474460', emoji='❄️'),
				discord.SelectOption(label='Party', value='667129769397059596', emoji='🎉'),
			])
		])


def setup(bot):
	bot.add_cog(SetupCommand(bot))
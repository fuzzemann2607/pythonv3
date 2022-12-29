from discord import ComponentInteraction
from discord.ext import commands


class RoleSelection(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.on_select(custom_id='role-selection')
	async def role_selection_dropdown(self, ctx: ComponentInteraction, _):
		user = ctx.author
		selected_roles = ctx.data.values

		# Get the roles from the selected role IDs
		roles = [ctx.guild.get_role(int(role_id)) for role_id in selected_roles]

		# Split the roles into roles the user has and roles the user doesn't have
		roles_user_has = [role for role in roles if role in user.roles]
		roles_user_doesnt_have = [role for role in roles if role not in user.roles]

		# Add the roles to the user
		await user.add_roles(*roles_user_doesnt_have)

		# Remove the roles from the user
		await user.remove_roles(*roles_user_has)

		# Define messages
		added_message = f'Added roles: {", ".join([role.mention for role in roles_user_doesnt_have])}' if roles_user_doesnt_have else ''
		removed_message = f'Removed roles: {", ".join([role.mention for role in roles_user_has])}' if roles_user_has else ''

		# Respond to the interaction
		await ctx.respond(content=f'{ added_message }\n'
		                          f'{ removed_message }', hidden=True)


def setup(bot):
	bot.add_cog(RoleSelection(bot))
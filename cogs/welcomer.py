import discord
from discord.ext import commands


class Welcomer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(1047939460819583006)

        embed = discord.Embed(title='Willkommen auf unserem Server!',
                              description=f'Willkommen {member.mention} auf unserem Server! Wir hoffen du hast Spaß hier!\n\n'
                                          f'Du bist der {len(member.guild.members)}. User auf unserem Server!',
                              color=discord.Color.green())

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'User ID: {member.id}')

        await channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Welcomer(bot))

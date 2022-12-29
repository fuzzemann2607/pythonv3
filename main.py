import asyncio
import logging
import os
from pathlib import Path

import discord
from aiomysql import Pool
import aiofiles
from discord.ext import commands

from dotenv import load_dotenv

from database import get_pool

load_dotenv()

log = logging.getLogger('BOT-MAIN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
	command_prefix=commands.when_mentioned_or(),
	intents=intents,
	activity=discord.Activity(type=discord.ActivityType.playing, name='Hello World!'),
	status=discord.Status.online,
	sync_commands=True,
	delete_not_existing_commands=True
)

async def init_db():
	pool: Pool = await get_pool()
	async with aiofiles.open('database/structure.sql') as f:
		sql = await f.read()

	async with pool.acquire() as connection:
		async with connection.cursor() as cursor:
			for statement in sql.split(';'):
				try:
					await cursor.execute(statement)
				except Exception as e:
					log.warning(e)
					continue
	pool.close()
	await pool.wait_closed()


if __name__ == '__main__':
	print('Starting bot...')

	print('Loading cogs...')
	cogs = [file.stem for file in Path('cogs').glob('**/*.py') if not file.name.startswith('__')]
	print(f'Loading {len(cogs)} cogs...')

	for cog in cogs:
		bot.load_extension(f'cogs.{cog}')
		print(f'Loaded cog {cog}')

	token = os.getenv('BOT_TOKEN')
	bot.run(token)
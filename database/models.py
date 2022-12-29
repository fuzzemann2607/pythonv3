from aiomysql import Pool
from database import get_pool

class LevelUser:

	def __init__(self, client_id: int):
		self.client_id = client_id
		self.xp = 0

	async def load(self):
		pool: Pool = await get_pool()
		async with pool.acquire() as connection:
			async with connection.cursor() as cursor:
				await cursor.execute("SELECT * FROM level_users WHERE client_id = %s", (self.client_id,))
				result = await cursor.fetchone()
				if result:
					self.xp = result[1]
				else:
					await cursor.execute("INSERT INTO level_users (client_id) VALUES (%s)", self.client_id)
					await connection.commit()
		pool.close()
		await pool.wait_closed()
		return self

	async def save(self):
		pool: Pool = await get_pool()
		async with pool.acquire() as connection:
			async with connection.cursor() as cursor:
				await cursor.execute("UPDATE level_users SET xp = %s WHERE client_id = %s", (self.xp, self.client_id))
				await connection.commit()
		pool.close()
		await pool.wait_closed()
		return self

	async def add_xp(self, xp: int) -> bool:
		level_before = self.get_level()
		self.xp += xp
		level_after = self.get_level()
		await self.save()
		return level_after > level_before

	def get_level(self):
		return int(self.xp ** 0.3)

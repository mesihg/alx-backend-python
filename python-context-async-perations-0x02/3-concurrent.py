import asyncio
import aiosqlite


async def async_fetch_users():
    """Fetch all users asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            result = await cursor.fetchall()
            print("[DB_LOG] All users fetched")
            return result

async def async_fetch_older_users():
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            result = await cursor.fetchall()
            print("[DB_LOG] Users older than 40 fetched")
            return result


async def fetch_concurrently():
    """Run both queries at the same time"""
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\nAll users:")
    for row in results_all:
        print(row)

    print("\nUsers older than 40:")
    for row in results_older:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

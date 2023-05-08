import asyncio
import random

from query_timer import Timer
from surrealdb import Surreal

"""
This query calculates distance from Prague for each city in ascending order

SELECT center FROM city:praha).center 
- gets coordinates of Prague's center

<int> geo::distance(center, ...)/1000 AS prague_dist
- calculates the distance between Prague and another city, converting it to kilometers and int

"""


async def main():
    async with Surreal("ws://localhost:8000") as db:
        await db.signin({"user": "root", "pass": "root"})
        await db.use("NDBI040", "reviews")

        timer = Timer()
        db_times = []
        for _ in range(100):
            timer.start()
            res = await db.query(
                """
                SELECT name, 
                <int> geo::distance(center, (SELECT center FROM city:praha).center)/1000 AS prague_dist 
                FROM city 
                WHERE name != "Praha"
                ORDER BY prague_dist;
            """
            )
            timer.end()
            db_times.append(res[0]["time"])
        timer.print(
            "Select with geo function (measured by script, includes network communication, 100 repetitions)"
        )
        print("DB execution times (5 random samples)")
        print(random.choices(db_times, k=5))

        print("Result:\n", res[0]["result"])


if __name__ == "__main__":
    asyncio.run(main())

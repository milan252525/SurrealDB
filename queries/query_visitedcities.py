import asyncio
import random

from timer_util import Timer
from surrealdb import Surreal

"""
This query returns all cities visited by anyone called Jan

array::distinct(->reviewed.restaurant->located_in->city.name) AS cities 
- uses graph relation to select all cities from resturants a user reviewed
- array::distinct drops duplicate values
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
                SELECT name, surname, 
                    array::distinct(->reviewed.restaurant->located_in->city.name) AS cities 
                FROM user
                WHERE name == 'Jan';
                """
            )
            timer.end()
            db_times.append(res[0]["time"])
        timer.print(
            "Select with graph relations (measured by script, includes network communication, 100 repetitions)"
        )
        print("DB execution times (5 random samples)")
        print(random.choices(db_times, k=5))

        print("Result:\n", res[0]["result"])


if __name__ == "__main__":
    asyncio.run(main())

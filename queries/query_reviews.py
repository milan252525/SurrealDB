import asyncio
import random

from timer_util import Timer
from surrealdb import Surreal

"""
This query selects all meals containing cheese with at least 50 4+ star reviews.
It also selects restaurants where the meal is served and received a 5 star review.

array::distinct(<-(reviewed WHERE stars == 5).restaurant)
- chooses restaurants from all 5 star reviews and removes duplicates
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
                SELECT 
                    name, ingredients,
                    array::distinct(<-(reviewed WHERE stars == 5).restaurant) as restaurants
                FROM food
                WHERE count(<-(reviewed WHERE stars >= 4)) >= 50
                AND ingredients CONTAINS "cheese"
                ORDER BY name;
                """
            )
            timer.end()
            db_times.append(res[0]["time"])
        timer.print(
            "Select meals with cheese and >=50 4+ star reviews (measured by script, includes network communication, 100 repetitions)"
        )
        print("DB execution times (5 random samples)")
        print(random.choices(db_times, k=5))

        print("Result:\n", res[0]["result"])


if __name__ == "__main__":
    asyncio.run(main())

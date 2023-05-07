import asyncio
import logging
import random
import time

from surrealdb import Surreal

logger = logging.getLogger("NDBI040:surreal")
random.seed(25)

# region DATA
# fmt: off
# following data was generated by ChatGPT for testing purposes only
names = [
    "Adam", "Aiden", "Aleš", "Alice", "Amelia", "Benjamin", "Charlotte", "David", "Dominik", "Ella",
    "Eva", "Filip", "Hana", "Isabella", "Jakub", "Jan", "Jana", "Jiří", "John", "Kateřina",
    "Klára", "Liam", "Linda", "Lucie", "Markéta", "Martin", "Mia", "Michael", "Nina", "Oliver"
]
surnames = [
    "Anderson", "Baker", "Černý", "Davis", "Dvořák", "Fischer", "Garcia", "Hansen", "Havel", "Hernandez",
    "Holmes", "Horák", "Jackson", "Johnson", "Jones", "Kovář", "Kříž", "Lee", "Lopez", "Martin",
    "Meyer", "Novák", "Pospíšil", "Richter", "Smith", "Svoboda", "Taylor", "Thompson", "Veselý", "Wilson"
]

cities = [
    ("Praha", 50.0755, 14.4378),
    ("Brno", 49.1951, 16.6068),
    ("Ostrava", 49.8209, 18.2625),
    ("Bratislava", 48.1486, 17.1077),
    ("London", 51.5074, -0.1278),
    ("Paris", 48.8566, 2.3522),
    ("Berlin", 52.5200, 13.4050),
    ("Madrid", 40.4168, -3.7038),
    ("Rome", 41.9028, 12.4964),
    ("Vienna", 48.2082, 16.3738),
    ("Amsterdam", 52.3676, 4.9041),
    ("Barcelona", 41.3851, 2.1734),
    ("Munich", 48.1351, 11.5820),
    ("Hamburg", 53.5511, 9.9937),
    ("Milan", 45.4642, 9.1900),
    ("Zurich", 47.3769, 8.5417),
    ("Lisbon", 38.7223, -9.1393),
    ("Krakow", 50.0647, 19.9450),
    ("Athens", 37.9838, 23.7275),
    ("Dublin", 53.3498, -6.2603),
]

restaurants = [
    "Savor", "Noodle Nation", "Naše maso", "The Fat Duck", "Le Jardin", "U Bílé kuzelky", "La Paloma", 
    "The Ivy", "Plevel", "Heritage", "Sisters", "Mlýnec", "Mediterraneo", "Cantina", "Osteria Francescana", 
    "The Ledbury", "Ginger & Fred", "La Degustation", "Ferdinanda", "The Clove Club"
]
food_reviews = [
    ("Tasty and satisfying!", 4.5),
    ("Overpriced and underwhelming", 2.0),
    ("Delicious but greasy", 3.5),
    ("Disappointing portion size", 2.5),
    ("Mouthwatering flavors", 4.5),
    ("Undercooked and unappetizing", 1.5),
    ("Amazing service, so-so food", 3.5),
    ("Inventive and flavorful", 4.0),
    ("Lacking in seasoning", 2.0),
    ("A culinary masterpiece", 5.0),
    ("Bland and uninspired", 2.0),
    ("Satisfying but not exceptional", 3.0),
    ("Perfectly cooked and seasoned", 4.5),
    ("Terrible service ruins meal", 1.0),
    ("Delectable and satisfying", 4.0),
    ("Boring and unremarkable", 2.5),
    ("Elevated cuisine at a cost", 3.5),
    ("Poor quality ingredients", 2.0),
    ("A feast for the senses", 4.5),
    ("Not worth the hype", 2.5),
    ("Savory and comforting", 3.5),
    ("Unadventurous and dull", 2.5),
    ("Flavors clash, poor execution", 2.0),
    ("Exceptional value for money", 4.5),
    ("A total letdown", 1.5),
    ("Fresh and flavorful", 4.0),
    ("Overcooked and dry", 2.0),
    ("Unforgettable dining experience", 4.5),
    ("Lacks finesse and creativity", 3.0),
    ("Inconsistent quality", 2.5),
    ("Skvělé jídlo, příšerná obsluha", 3.5),
    ("Vynikající chuť, ale drahé", 4),
    ("Málo kořeněné, jinak dobré", 3),
    ("Nezajímavá prezentace, ale chutná", 3.5),
    ("Draze zaplacené podprůměrné jídlo", 2.5),
    ("Nadprůměrná kvalita, ale nic extra", 3.5),
    ("Vynikající ceny, dobré jídlo", 4),
    ("Slané jídlo, ale vynikající dezerty", 3.5),
    ("Přijatelná kvalita, ale drahé", 3),
    ("Skvělé jídlo, ale malé porce", 4),
    ("Chutné, ale podivná kombinace ingrediencí", 3),
    ("Překvapivá chuť, ale příliš drahé", 3),
    ("Vynikající kvalita, ale přemrštěné ceny", 4),
    ("Neobvyklé kombinace, ale výborné", 3.5),
    ("Drahé jídlo, nic extra", 2.5),
    ("Nadprůměrná kvalita, ale přemrštěné ceny", 3.5),
    ("Chutné jídlo, ale podprůměrné podávání", 3),
    ("Velké porce, ale podprůměrná chuť", 2.5),
    ("Kreativní jídlo, ale podivné", 3),
    ("Jemná chuť, ale málo kořeněné", 3.5),
    ("Výborné jídlo, ale dlouhé čekání", 4),
    ("Špatné jídlo, hrozné služby", 1.5),
    ("Podprůměrná kvalita, přemrštěné ceny", 2.5),
    ("Chutné jídlo, ale špatná prezentace", 2.5),
    ("Nezvyklá chuť, ale vynikající", 3.5),
    ("Hodně kořeněné, ale dobré", 3.5),
    ("Nepříjemná atmosféra, ale dobré jídlo", 3),
    ("Malé porce, ale skvělá chuť", 4),
    ("Nadprůměrné jídlo, ale drahé", 4),
    ("Podprůměrná kvalita, ale výborné ceny", 3.5),
    ("Vynikající dezerty, průměrné jídlo", 3),
]

restaurant_names = [
    "The Hungry Bear",
    "Salty Dog Tavern",
    "Savor the Flavor",
    "The Golden Spoon",
    "The Blue Plate",
    "The Cozy Kitchen",
    "The Rustic Table",
    "The Grill House",
    "The Farmhouse Kitchen",
    "The Tasting Room",
    "The Garden Cafe",
    "The Spice Route",
    "The Food Lab",
    "The Fork and Knife",
    "The Local Harvest",
    "The Hungry Hunter",
    "The Roasted Bean",
    "The Green Leaf",
    "The Red Pepper",
    "The Flying Fork",
    "The Copper Kettle",
    "The Urban Kitchen",
    "The Salted Caramel",
    "The Fresh Catch",
    "The Toasted Walnut",
    "The Daily Grind",
    "The Blue Apron",
    "The Lucky Rooster",
    "The Golden Hen",
    "The Meatball Shop",
]

food_ingredients = [
    "quinoa",
    "sriracha",
    "artichoke",
    "truffle",
    "chorizo",
    "kale",
    "tofu",
    "wasabi",
    "hummus",
    "balsamic vinegar",
    "goji berries",
    "harissa",
    "edamame",
    "chia seeds",
    "couscous",
    "tempeh",
    "fennel",
    "prosciutto",
    "miso",
    "fiddleheads",
    "tahini",
    "ghee",
    "saffron",
    "jicama",
    "caviar",
    "mushroom",
    "sage",
    "scallops",
    "kohlrabi",
    "dragonfruit",
]

meal_names = [
    "Stuffed Pepper Surprise",
    "Thai Peanut Noodle Bowl",
    "Cowboy Steak and Beans",
    "Roasted Veggie Frittata",
    "Taco Salad Delight",
    "Crispy Honey Glazed Chicken",
    "Baked Garlic Parmesan Salmon",
    "Loaded Baked Potato Soup",
    "The Big Kahuna Burger",
    "Mushroom and Truffle Risotto",
    "Brinner (Breakfast for Dinner)",
    "Zesty Lemon Garlic Shrimp",
    "Pineapple Fried Rice",
    "Sloppy Joe Sliders",
    "Bangers and Mash-up",
    "Sizzling Steak Fajitas",
    "Crispy Chicken Parmesan",
    "Spicy Shrimp Tacos",
    "Creamy Mushroom Risotto",
    "Tangy Lemon Pepper Chicken",
    "Savory Beef Stroganoff",
    "Smokey BBQ Ribs",
    "Cajun Blackened Fish",
    "Sweet and Sour Pork",
    "Garlic Butter Shrimp Scampi",
    "Vegetable Pad Thai",
    "Loaded Baked Potato Soup",
    "Honey Mustard Glazed Salmon",
    "Crispy Fried Chicken Sandwich",
    "Maple Bacon Pancakes",
]
# fmt: on
# endregion


class Timer:
    def __init__(self):
        self._times = []
        self._start = 0

    def start(self) -> None:
        self._start = time.time()

    def end(self) -> None:
        self._times.append((time.time() - self._start) * 1000)
        self._start = 0

    def print(self, desc: str = "") -> None:
        times = [t for t in self._times if t > 0]
        if desc:
            print(desc)
        print(f"avg {sum(times) / len(times):.2f} ms")
        print(f"max {max(times):.2f} ms")
        print(f"min {min(times):.2f} ms")

    def reset(self) -> None:
        self._times = []
        self._start = 0


async def main():
    async with Surreal("ws://localhost:8000") as db:
        await db.signin({"user": "root", "pass": "root"})
        await db.use("NDBI040", "reviews")

        logger.info("recreating database")
        await db.query("REMOVE DB reviews; DEFINE DB reviews; USE DB reviews;")

        logger.info("creating structures")
        with open("init.surql") as f:
            await db.query(f.read())

        logger.info("inserting random data")
        users = {}
        for _ in range(1000):
            name = random.choice(names)
            surname = random.choice(surnames)
            num = random.randint(1, 999999999)
            username = f"{name[:3]}{surname[:3]}{num}".lower()
            email = f"{username}@example.com"
            users[username] = {
                "name": name,
                "surname": surname,
                "email": email,
            }

        for id, obj in users.items():
            await db.create(f"user:{id}", obj)

        for name, lat, long in cities:
            await db.create(
                f"city:{name.lower()}",
                {"name": name, "center": {"type": "Point", "coordinates": [lat, long]}},
            )

        # timer = Timer()
        # for _ in range(100):
        #     timer.start()
        #     await db.query(
        #         "select name from city;"
        #     )
        #     timer.end()
        # timer.print("select without geo function")

        # timer = Timer()
        # for _ in range(100):
        #     timer.start()
        #     await db.query(
        #         "select name, <int> geo::distance(center, (select center from city:praha).center)/1000 as prague_dist from city order by prague_dist;"
        #     )
        #     timer.end()
        # timer.print("select with geo function")
        
        # timer.reset()
        # for _ in range(100):
        #     timer.start()
        #     await db.query(
        #         "select name from user WHERE string::startsWith(name, 'b');"
        #     )
        #     timer.end()
        # timer.print("select everything")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )
    asyncio.run(main())

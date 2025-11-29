import time
import random
from utils import get_logger

logger = get_logger("MockFeed")

class MockGoalFeed:
    def __init__(self):
        self.matches = [
            ("Arsenal", "Chelsea"),
            ("Barcelona", "Real Madrid"),
            ("Liverpool", "Man City"),
            ("Bayern", "Dortmund"),
            ("Juventus", "Inter")
        ]
        self.scores = {}

    def start(self, handler):
        logger.info("Mock goal feed running")

        while True:
            home, away = random.choice(self.matches)
            match_id = f"{home}_{away}"

            if match_id not in self.scores:
                self.scores[match_id] = [0, 0]

            h, a = self.scores[match_id]

            if random.random() < 0.5:
                h += 1
                scorer = home
            else:
                a += 1
                scorer = away

            self.scores[match_id] = [h, a]

            event = {
                "match_id": match_id,
                "home": home,
                "away": away,
                "team": scorer,
                "score": (h, a),
                "minute": random.randint(1, 90)
            }

            logger.info(f"Goal: {home} {h}-{a} {away} | {scorer}")

            handler(event)
            time.sleep(random.randint(4, 7))

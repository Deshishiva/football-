from utils import get_logger
import config

logger = get_logger("Trader")

class Trader:
    def __init__(self, price_feed, matcher):
        self.price_feed = price_feed
        self.matcher = matcher

    def process_goal(self, event):
        print("EVENT RECEIVED:", event)  # debug

        match_id = event["match_id"]
        home = event["home"]
        away = event["away"]
        team = event["team"]

        market = self.matcher.get_market(match_id)

        if not market:
            self.matcher.register_match(match_id, home, away)
            market = self.matcher.get_market(match_id)

        base_prob = self.matcher.get_team_prob(team)
        price = self.price_feed.get_price(market)

        if base_prob < config.UNDERDOG_THRESHOLD and price < config.UNDERDOG_THRESHOLD:
            logger.info(f"Underdog scored -> BUY | Team={team} | base_prob={base_prob} | price={price}")
            self.execute_order(market, price)
        else:
            logger.info(f"No trade | Team={team} | base_prob={base_prob} | price={price}")

    def execute_order(self, market_id, price):
        logger.info(f"Order executed | market={market_id} | size={config.TRADE_SIZE} | price={price}")

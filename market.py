import random

class MarketPriceFeed:
    def get_price(self, market_id):
        return round(random.uniform(0.30, 0.70), 2)

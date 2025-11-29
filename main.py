from mock_feed import MockGoalFeed
from trader import Trader
from matcher import MatchRegistry
from price_feed import PriceFeed
from utils import get_logger

logger = get_logger("Main")


def handle(event):
    trader.process_goal(event)


def main():
    feed = MockGoalFeed()
    feed.start(handle)


if __name__ == "__main__":
    price_feed = PriceFeed()
    matcher = MatchRegistry()
    trader = Trader(price_feed, matcher)

    main()

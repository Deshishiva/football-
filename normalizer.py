class EventNormalizer:
    def normalize(self, raw):
        """Convert raw feed data into a clean, unified event structure."""

        return {
            "id": raw.get("match_id"),
            "home": raw.get("home"),
            "away": raw.get("away"),
            "team": raw.get("scorer"),
            "score": raw.get("score"),
            "league": raw.get("league"),
            "minute": raw.get("minute")
        }

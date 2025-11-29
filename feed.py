import websocket
import json
import time
from utils import get_logger

logger = get_logger("Feed")

class LiveGoalFeed:
    def __init__(self, api_key, timezone):
        self.url = f"wss://wss.allsportsapi.com/live_events?APIkey={api_key}&timezone={timezone}"
        self.previous_scores = {}

    def _on_open(self, ws):
        logger.info("Connected to AllSportsAPI WebSocket")

    def _on_message(self, ws, msg):
        try:
            data = json.loads(msg)
        except Exception:
            return
        for match in data:
            mid = match.get("event_key")
            home = match.get("event_home_team")
            away = match.get("event_away_team")
            raw = match.get("event_final_result", "0 - 0")
            try:
                hs, as_ = raw.replace(" ", "").split("-")
                hs, as_ = int(hs), int(as_)
            except:
                continue
            prev = self.previous_scores.get(mid, (hs, as_))
            self.previous_scores[mid] = (hs, as_)
            if (hs, as_) != prev:
                scorer = home if hs > prev[0] else away
                event = {
                    "match_id": mid,
                    "home": home,
                    "away": away,
                    "scorer": scorer,
                    "score": (hs, as_),
                    "league": match.get("league_name", ""),
                    "minute": match.get("event_status", "")
                }
                logger.info(f"Goal detected: {home} {hs}-{as_} {away} | Scorer: {scorer}")
                self.callback(event)

    def _on_error(self, ws, err):
        logger.error(f"WebSocket error: {err}")

    def _on_close(self, ws, *_):
        logger.warning("WebSocket closed")

    def start(self, callback):
        self.callback = callback
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        while True:
            try:
                ws.run_forever()
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Connection dropped: {e}")
                time.sleep(3)

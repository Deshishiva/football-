class MatchRegistry:
    def __init__(self):
        self.matches = {}
        self.team_probs = {}

    def register_match(self, match_id, home, away):
        self.matches[match_id] = f"MKT_{home}_{away}"
        self.team_probs[home] = 0.45
        self.team_probs[away] = 0.55

    def get_market(self, match_id):
        return self.matches.get(match_id)

    def get_team_prob(self, team):
        return self.team_probs.get(team, 0.5)

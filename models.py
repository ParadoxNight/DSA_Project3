from dataclasses import dataclass
@dataclass
class player_record:
	person_id: int
	first_name: str
	last_name: str
	games_played: int = 0
	total_points: int = 0
	total_assists: int = 0
	total_blocks: int = 0
	total_steals: int = 0
	total_rebounds: int = 0
	total_turnovers: int = 0
	total_plus_minus: int = 0
	total_minutes: float = 0.0
	def metric_value(self, metric_name):
		if metric_name == "points_total":
			return self.total_points
		if metric_name == "assists_total":
			return self.total_assists
		if metric_name == "rebounds_total":
			return self.total_rebounds
		if metric_name == "blocks_total":
			return self.total_blocks
		if metric_name == "steals_total":
			return self.total_steals
		if metric_name == "turnovers_total":
			return self.total_turnovers
		if metric_name == "plus_minus_total":
			return self.total_plus_minus
		if metric_name == "minutes_total":
			return self.total_minutes
		if self.games_played == 0:
			return 0
		if metric_name == "points_per_game":
			return self.total_points / self.games_played
		if metric_name == "assists_per_game":
			return self.total_assists / self.games_played
		if metric_name == "rebounds_per_game":
			return self.total_rebounds / self.games_played
		if metric_name == "blocks_per_game":
			return self.total_blocks / self.games_played
		if metric_name == "steals_per_game":
			return self.total_steals / self.games_played
		if metric_name == "turnovers_per_game":
			return self.total_turnovers / self.games_played
		if metric_name == "plus_minus_per_game":
			return self.total_plus_minus / self.games_played
		if metric_name == "minutes_per_game":
			return self.total_minutes / self.games_played
		return 0
	def full_name(self):
		return f"{self.first_name} {self.last_name}"


# This class acts as the player node definition, where the values in given player are stored

import csv
from models import player_record
class aggregator:
	def __init__(self):
		self.players = {}
	def load_csv(self, file_path):
		self.players = {}
		with open(file_path, "r", newline="", encoding="utf-8") as file:
			reader = csv.DictReader(file)
			for row in reader:
				person_id = self._to_int(row.get("personId", 0))
				if person_id not in self.players:
					self.players[person_id] = player_record(
						person_id=person_id,
						first_name=row.get("firstName", "").strip(),
						last_name=row.get("lastName", "").strip()
					)
				player = self.players[person_id]
				player.games_played += 1
				player.total_points += self._to_int(row.get("points", 0))
				player.total_assists += self._to_int(row.get("assists", 0))
				player.total_blocks += self._to_int(row.get("blocks", 0))
				player.total_steals += self._to_int(row.get("steals", 0))
				player.total_rebounds += self._to_int(row.get("reboundsTotal", 0))
				player.total_turnovers += self._to_int(row.get("turnovers", 0))
				player.total_plus_minus += self._to_int(row.get("plusMinusPoints", 0))
				player.total_minutes += self._to_float(row.get("numMinutes", 0))
		return list(self.players.values())
	def _to_int(self, value):
		try:
			return int(float(value))
		except:
			return 0
	def _to_float(self, value):
		try:
			return float(value)
		except:
			return 0.0

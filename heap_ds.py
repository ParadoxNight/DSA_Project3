import copy
class max_heap_node:
	def __init__(self, player, metric_name):
		self.player = player
		self.metric_name = metric_name
		self.key = (player.metric_value(metric_name), player.person_id)
class binary_max_heap:
	def __init__(self, metric_name):
		self.metric_name = metric_name
		self.data = []
	def _key(self, node):
		return node.key
	def insert(self, player):
		node = max_heap_node(player, self.metric_name)
		self.data.append(node)
		self.heapify_up(len(self.data) - 1)
	def build_from_players(self, players):
		self.data = [max_heap_node(player, self.metric_name) for player in players]
		for index in range(len(self.data) // 2 - 1, -1, -1):
			self.heapify_down(index)
	def heapify_up(self, index):
		while index > 0:
			parent = (index - 1) // 2
			if self._key(self.data[index]) > self._key(self.data[parent]):
				self.data[index], self.data[parent] = self.data[parent], self.data[index]
				index = parent
			else:
				break
	def heapify_down(self, index):
		size = len(self.data)
		while True:
			left = 2 * index + 1
			right = 2 * index + 2
			largest = index
			if left < size and self._key(self.data[left]) > self._key(self.data[largest]):
				largest = left
			if right < size and self._key(self.data[right]) > self._key(self.data[largest]):
				largest = right
			if largest != index:
				self.data[index], self.data[largest] = self.data[largest], self.data[index]
				index = largest
			else:
				break
	def extract_max(self):
		if not self.data:
			return None
		if len(self.data) == 1:
			return self.data.pop()
		root = self.data[0]
		self.data[0] = self.data.pop()
		self.heapify_down(0)
		return root
	def top_k(self, k):
		temp_heap = copy.deepcopy(self)
		result = []
		for _ in range(min(k, len(temp_heap.data))):
			node = temp_heap.extract_max()
			if node is not None:
				result.append(node.player)
		return result

class rb_node:
	def __init__(self, player=None, key=None, color="black", left=None, right=None, parent=None):
		self.player = player
		self.key = key
		self.color = color
		self.left = left
		self.right = right
		self.parent = parent
class red_black_tree:
	def __init__(self, metric_name):
		self.metric_name = metric_name
		self.nil = rb_node()
		self.nil.left = self.nil
		self.nil.right = self.nil
		self.nil.parent = self.nil
		self.root = self.nil
		self.size = 0
	def make_key(self, player):
		return (player.metric_value(self.metric_name), player.person_id)
	def left_rotate(self, x):
		y = x.right
		x.right = y.left
		if y.left != self.nil:
			y.left.parent = x
		y.parent = x.parent
		if x.parent == self.nil:
			self.root = y
		elif x == x.parent.left:
			x.parent.left = y
		else:
			x.parent.right = y
		y.left = x
		x.parent = y
	def right_rotate(self, y):
		x = y.left
		y.left = x.right
		if x.right != self.nil:
			x.right.parent = y
		x.parent = y.parent
		if y.parent == self.nil:
			self.root = x
		elif y == y.parent.right:
			y.parent.right = x
		else:
			y.parent.left = x
		x.right = y
		y.parent = x
	def insert(self, player):
		node = rb_node(player=player, key=self.make_key(player), color="red", left=self.nil, right=self.nil, parent=self.nil)
		parent = self.nil
		current = self.root
		while current != self.nil:
			parent = current
			if node.key < current.key:
				current = current.left
			else:
				current = current.right
		node.parent = parent
		if parent == self.nil:
			self.root = node
		elif node.key < parent.key:
			parent.left = node
		else:
			parent.right = node
		self.size += 1
		self.insert_fixup(node)
	def insert_fixup(self, node):
		while node.parent.color == "red":
			if node.parent == node.parent.parent.left:
				uncle = node.parent.parent.right
				if uncle.color == "red":
					node.parent.color = "black"
					uncle.color = "black"
					node.parent.parent.color = "red"
					node = node.parent.parent
				else:
					if node == node.parent.right:
						node = node.parent
						self.left_rotate(node)
					node.parent.color = "black"
					node.parent.parent.color = "red"
					self.right_rotate(node.parent.parent)
			else:
				uncle = node.parent.parent.left
				if uncle.color == "red":
					node.parent.color = "black"
					uncle.color = "black"
					node.parent.parent.color = "red"
					node = node.parent.parent
				else:
					if node == node.parent.left:
						node = node.parent
						self.right_rotate(node)
					node.parent.color = "black"
					node.parent.parent.color = "red"
					self.left_rotate(node.parent.parent)
		self.root.color = "black"
	def build_from_players(self, players):
		self.root = self.nil
		self.size = 0
		for player in players:
			self.insert(player)
	def reverse_inorder_top_k(self, k):
		result = []
		self._reverse_inorder(self.root, result, k)
		return result
	def _reverse_inorder(self, node, result, k):
		if node == self.nil or len(result) >= k:
			return
		self._reverse_inorder(node.right, result, k)
		if len(result) < k:
			result.append(node.player)
		self._reverse_inorder(node.left, result, k)

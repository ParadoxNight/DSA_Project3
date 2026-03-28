import math
import tkinter as tk
import os

class structure_visualizer(tk.Toplevel):
	def __init__(self, master, structure, structure_type, metric_name):
		super().__init__(master)
		self.title(f"{structure_type} visualization")
		self.geometry("1400x900")
		self.structure = structure
		self.structure_type = structure_type
		self.metric_name = metric_name
		self.node_radius = 34
		self.level_gap = 130
		self.top_margin = 90
		self.side_margin = 80
		self.max_tree_depth = 8
		self.max_heap_nodes = 189
		self.container = tk.Frame(self)
		self.container.pack(fill="both", expand=True)
		self.h_scroll = tk.Scrollbar(self.container, orient="horizontal")
		self.h_scroll.pack(side="bottom", fill="x")
		self.v_scroll = tk.Scrollbar(self.container, orient="vertical")
		self.v_scroll.pack(side="right", fill="y")
		self.canvas = tk.Canvas(
			self.container,
			bg="#f2f2f2",
			xscrollcommand=self.h_scroll.set,
			yscrollcommand=self.v_scroll.set
		)
		self.canvas.pack(side="left", fill="both", expand=True)
		self.h_scroll.config(command=self.canvas.xview)
		self.v_scroll.config(command=self.canvas.yview)
		self.canvas.bind("<ButtonPress-1>", self.start_pan)
		self.canvas.bind("<B1-Motion>", self.do_pan)
		self.canvas.bind("<Configure>", self.redraw)
		self.redraw()
		self.lift()
		self.attributes('-topmost', True)
		self.after(100, lambda: self.attributes('-topmost', False))
		self.focus_force()
		self.after(0, self.bring_to_front)

	def bring_to_front(self):
		try:
			self.update_idletasks()
			self.lift()
			self.focus_force()
			self.grab_set()
			self.grab_release()
			os.system(
				'osascript -e \'tell application "System Events" to set frontmost of the first process whose unix id is %d to true\'' % os.getpid())
		except:
			pass

	def start_pan(self, event):
		self.canvas.scan_mark(event.x, event.y)

	def center_view(self, canvas_width, canvas_height):
		self.update_idletasks()
		view_width = self.canvas.winfo_width()
		x = (canvas_width / 2 - view_width / 2) / canvas_width
		y = 0
		self.canvas.xview_moveto(max(0, min(1, x)))
		self.canvas.yview_moveto(max(0, min(1, y)))

	def do_pan(self, event):
		self.canvas.scan_dragto(event.x, event.y, gain=1)

	def redraw(self, event=None):
		self.canvas.delete("all")
		if self.structure_type == "heap":
			self.draw_heap()
		else:
			self.draw_rbtree()

	def draw_heap(self):
		nodes = self.structure.data[:self.max_heap_nodes]
		canvas_width = 1600
		canvas_height = 900

		if not nodes:
			self.canvas.create_text(300, 120, text="Heap is empty", font=("Arial", 18, "bold"))
			self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
			self.center_view(canvas_width, canvas_height)
			return

		max_level = int(math.log2(len(nodes))) if nodes else 0
		canvas_width = max(1600, 220 * (2 ** max_level))
		canvas_height = max(900, self.top_margin + (max_level + 2) * self.level_gap)

		positions = {}
		for index in range(len(nodes)):
			level = int(math.log2(index + 1))
			first_index_in_level = 2 ** level - 1
			position_in_level = index - first_index_in_level
			nodes_in_level = 2 ** level
			x = canvas_width * (position_in_level + 1) / (nodes_in_level + 1)
			y = self.top_margin + level * self.level_gap
			positions[index] = (x, y)

		for index in range(1, len(nodes)):
			parent_index = (index - 1) // 2
			parent_x, parent_y = positions[parent_index]
			child_x, child_y = positions[index]
			x1, y1, x2, y2 = self.edge_to_edge_line(parent_x, parent_y, child_x, child_y)
			self.canvas.create_line(x1, y1, x2, y2, fill="#666666", width=3)

		for index, node in enumerate(nodes):
			x, y = positions[index]
			self.draw_node(x, y, node.player.last_name, node.player.metric_value(self.metric_name), "#2b2b2b")

		self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
		self.center_view(canvas_width, canvas_height)

	def draw_rbtree(self):
		if self.structure.root == self.structure.nil:
			canvas_width = 1200
			canvas_height = 900
			self.canvas.create_text(300, 120, text="Tree is empty", font=("Arial", 18, "bold"))
			self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
			self.center_view(canvas_width, canvas_height)
			return

		self.rb_subtree_widths = {}
		self.compute_subtree_width(self.structure.root, self.structure.nil, 0)

		root_width = self.rb_subtree_widths[self.structure.root]
		canvas_width = max(2400, root_width + 2 * self.side_margin)
		canvas_height = max(1000, self.top_margin + (self.max_tree_depth + 2) * self.level_gap)

		self.draw_rbtree_node(
			self.structure.root,
			self.structure.nil,
			self.side_margin,
			self.top_margin,
			0
		)

		self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
		self.center_view(canvas_width, canvas_height)

	def draw_rbtree_node(self, node, nil, left_x, y, depth):
		if node == nil or depth > self.max_tree_depth:
			return
		total_width = self.rb_subtree_widths[node]
		left_width = 0
		right_width = 0

		if node.left != nil and depth < self.max_tree_depth:
			left_width = self.rb_subtree_widths.get(node.left, self.node_radius * 2 + 20)
		else:
			left_width = self.node_radius * 2 + 20

		if node.right != nil and depth < self.max_tree_depth:
			right_width = self.rb_subtree_widths.get(node.right, self.node_radius * 2 + 20)
		else:
			right_width = self.node_radius * 2 + 20

		x = left_x + total_width / 2
		child_y = y + self.level_gap

		if node.left != nil and depth < self.max_tree_depth:
			left_child_total = self.rb_subtree_widths[node.left]
			left_child_x = left_x + left_child_total / 2
			x1, y1, x2, y2 = self.edge_to_edge_line(x, y, left_child_x, child_y)
			self.canvas.create_line(x1, y1, x2, y2, fill="#666666", width=3)
			self.draw_rbtree_node(node.left, nil, left_x, child_y, depth + 1)

		if node.right != nil and depth < self.max_tree_depth:
			right_child_left_x = left_x + left_width + 40
			right_child_total = self.rb_subtree_widths[node.right]
			right_child_x = right_child_left_x + right_child_total / 2
			x1, y1, x2, y2 = self.edge_to_edge_line(x, y, right_child_x, child_y)
			self.canvas.create_line(x1, y1, x2, y2, fill="#666666", width=3)
			self.draw_rbtree_node(node.right, nil, right_child_left_x, child_y, depth + 1)

		fill_color = "red" if node.color == "red" else "#2b2b2b"
		self.draw_node(x, y, node.player.last_name, node.player.metric_value(self.metric_name), fill_color)

	def draw_node(self, x, y, name, value, fill_color):
		display_name = name if len(name) <= 12 else name[:12]
		label = f"{display_name}\n{value:.2f}"
		self.canvas.create_oval(
			x - self.node_radius,
			y - self.node_radius,
			x + self.node_radius,
			y + self.node_radius,
			fill=fill_color,
			outline="white",
			width=2
		)
		self.canvas.create_text(
			x,
			y,
			text=label,
			fill="white",
			font=("Arial", 9, "bold")
		)

	def edge_to_edge_line(self, x1, y1, x2, y2):
		dx = x2 - x1
		dy = y2 - y1
		distance = math.sqrt(dx * dx + dy * dy)
		if distance == 0:
			return x1, y1, x2, y2
		ux = dx / distance
		uy = dy / distance
		start_x = x1 + ux * self.node_radius
		start_y = y1 + uy * self.node_radius
		end_x = x2 - ux * self.node_radius
		end_y = y2 - uy * self.node_radius
		return start_x, start_y, end_x, end_y

	def compute_subtree_width(self, node, nil, depth):
		if node == nil or depth > self.max_tree_depth:
			return 0

		left_width = self.compute_subtree_width(node.left, nil, depth + 1)
		right_width = self.compute_subtree_width(node.right, nil, depth + 1)

		if left_width == 0:
			left_width = self.node_radius * 2 + 20
		if right_width == 0:
			right_width = self.node_radius * 2 + 20

		total_width = left_width + right_width + 40
		self.rb_subtree_widths[node] = total_width
		return total_width

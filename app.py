import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from aggregator import aggregator
from benchmark import benchmark_runner
from visualizer import structure_visualizer
class leaderboard_app:
	def __init__(self, root):
		self.root = root
		self.root.title("Top-N Basketball Leaders")
		self.root.geometry("1100x760")
		self.data_loader = aggregator()
		self.players = []
		self.heap = None
		self.tree = None
		self.heap_result = None
		self.tree_result = None
		self.metric_var = tk.StringVar(value="points_total")
		self.k_var = tk.StringVar(value="10")
		self.status_var = tk.StringVar(value="Load a dataset to begin")
		self._build_ui()
	def _build_ui(self):
		control_frame = ttk.Frame(self.root, padding=10)
		control_frame.pack(fill="x")
		button_load = ttk.Button(control_frame, text="Load dataset", command=self.load_dataset)
		button_load.grid(row=0, column=0, padx=5, pady=5)
		metric_label = ttk.Label(control_frame, text="Metric")
		metric_label.grid(row=0, column=1, padx=5, pady=5)
		metric_box = ttk.Combobox(control_frame, textvariable=self.metric_var, state="readonly", width=20)
		metric_box["values"] = (
			"points_total",
			"assists_total",
			"rebounds_total",
			"blocks_total",
			"steals_total",
			"turnovers_total",
			"plus_minus_total",
			"minutes_total",
			"points_per_game",
			"assists_per_game",
			"rebounds_per_game"
		)
		metric_box.grid(row=0, column=2, padx=5, pady=5)
		ttk.Label(control_frame, text="K").grid(row=0, column=3, padx=5, pady=5)
		k_entry = ttk.Entry(control_frame, textvariable=self.k_var, width=10)
		k_entry.grid(row=0, column=4, padx=5, pady=5)
		button_heap = ttk.Button(control_frame, text="Run max-heap", command=self.run_heap)
		button_heap.grid(row=0, column=5, padx=5, pady=5)
		button_tree = ttk.Button(control_frame, text="Run red-black tree", command=self.run_tree)
		button_tree.grid(row=0, column=6, padx=5, pady=5)
		button_compare = ttk.Button(control_frame, text="Compare both", command=self.compare_both)
		button_compare.grid(row=0, column=7, padx=5, pady=5)
		button_heap_view = ttk.Button(control_frame, text="Visualize heap", command=self.visualize_heap)
		button_heap_view.grid(row=0, column=8, padx=5, pady=5)
		button_tree_view = ttk.Button(control_frame, text="Visualize tree", command=self.visualize_tree)
		button_tree_view.grid(row=0, column=9, padx=5, pady=5)
		status_label = ttk.Label(self.root, textvariable=self.status_var, padding=10)
		status_label.pack(fill="x")
		results_frame = ttk.Frame(self.root, padding=10)
		results_frame.pack(fill="both", expand=True)
		left_frame = ttk.LabelFrame(results_frame, text="Heap results", padding=10)
		left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
		right_frame = ttk.LabelFrame(results_frame, text="Red-black tree results", padding=10)
		right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
		self.heap_text = tk.Text(left_frame, wrap="word")
		self.heap_text.pack(fill="both", expand=True)
		self.tree_text = tk.Text(right_frame, wrap="word")
		self.tree_text.pack(fill="both", expand=True)
	def load_dataset(self):
		default_path = os.path.join("archive", "PlayerStatistics.csv")
		file_path = filedialog.askopenfilename(initialdir="archive", initialfile="PlayerStatistics.csv", filetypes=[("CSV files", "*.csv")])
		if not file_path:
			file_path = default_path
		try:
			self.players = self.data_loader.load_csv(file_path)
			self.heap = None
			self.tree = None
			self.heap_result = None
			self.tree_result = None
			self.heap_text.delete("1.0", tk.END)
			self.tree_text.delete("1.0", tk.END)
		except Exception as error:
			messagebox.showerror("Load error", str(error))
	def run_heap(self):
		if not self.players:
			messagebox.showwarning("No data", "Load a dataset first")
			return
		runner = benchmark_runner(self.players)
		self.heap, self.heap_result = runner.run_heap(self.metric_var.get(), int(self.k_var.get()))
		self._show_result(self.heap_text, self.heap_result, "Max-Heap")
		self.status_var.set("Max-heap completed")
	def run_tree(self):
		if not self.players:
			messagebox.showwarning("No data", "Load a dataset first")
			return
		runner = benchmark_runner(self.players)
		self.tree, self.tree_result = runner.run_rbtree(self.metric_var.get(), int(self.k_var.get()))
		self._show_result(self.tree_text, self.tree_result, "Red-Black Tree")
		self.status_var.set("Red-black tree completed")
	def compare_both(self):
		self.run_heap()
		self.run_tree()
		if self.heap_result is None or self.tree_result is None:
			return
		heap_ids = [player.person_id for player in self.heap_result.output_players]
		tree_ids = [player.person_id for player in self.tree_result.output_players]
		match = heap_ids == tree_ids
		self.status_var.set(f"Compared both structures | same output: {match} | heap build {self.heap_result.build_time:.6f}s | tree build {self.tree_result.build_time:.6f}s")
	def _show_result(self, widget, result, title):
		widget.delete("1.0", tk.END)
		widget.insert(tk.END, f"{title}\n")
		widget.insert(tk.END, f"Build time: {result.build_time:.6f} seconds\n")
		widget.insert(tk.END, f"Query time: {result.query_time:.6f} seconds\n\n")
		for index, player in enumerate(result.output_players, start=1):
			value = player.metric_value(self.metric_var.get())
			widget.insert(tk.END, f"{index}. {player.full_name()} | {value:.2f} | games: {player.games_played}\n")
	def visualize_heap(self):
		if self.heap is None:
			messagebox.showwarning("No heap", "Run the heap first")
			return
		structure_visualizer(self.root, self.heap, "heap", self.metric_var.get())
	def visualize_tree(self):
		if self.tree is None:
			messagebox.showwarning("No tree", "Run the red-black tree first")
			return
		structure_visualizer(self.root, self.tree, "tree", self.metric_var.get())
def main():
	root = tk.Tk()
	leaderboard_app(root)
	root.mainloop()

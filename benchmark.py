import time
from heap_ds import binary_max_heap
from rbtree_ds import red_black_tree
class benchmark_result:
	def __init__(self, build_time, query_time, output_players):
		self.build_time = build_time
		self.query_time = query_time
		self.output_players = output_players
class benchmark_runner:
	def __init__(self, players):
		self.players = players
	def run_heap(self, metric_name, k):
		start_build = time.perf_counter()
		heap = binary_max_heap(metric_name)
		heap.build_from_players(self.players)
		end_build = time.perf_counter()
		start_query = time.perf_counter()
		output_players = heap.top_k(k)
		end_query = time.perf_counter()
		return heap, benchmark_result(end_build - start_build, end_query - start_query, output_players)
	def run_rbtree(self, metric_name, k):
		start_build = time.perf_counter()
		tree = red_black_tree(metric_name)
		tree.build_from_players(self.players)
		end_build = time.perf_counter()
		start_query = time.perf_counter()
		output_players = tree.reverse_inorder_top_k(k)
		end_query = time.perf_counter()
		return tree, benchmark_result(end_build - start_build, end_query - start_query, output_players)

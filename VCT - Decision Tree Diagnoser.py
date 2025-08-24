from itertools import combinations
class Node:
	def __init__(self, data, positive_child=None, negative_child=None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child


class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms


def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records


class Diagnoser:
	def __init__(self, root: Node):
		self.root = root

	def diagnose(self, symptoms):
		root = self.root
		while root.positive_child is not None and root.negative_child is not None:
			if root.data in symptoms:
					root = root.positive_child
			elif root.data not in symptoms:
					root = root.negative_child
		return root.data


	def calculate_success_rate(self, records):
		if len(records) == 0:
			raise ValueError("record was 0 ")
		else:
			count = 0
			for record in records :
				if self.diagnose(record.symptoms) == record.illness:
					count +=1
		return count/ len(records)


	def all_illnesses(self):
		root = self.root
		lst = []
		lst1=self.all_illnesses_helper(root,lst)
		dic_ill = dict()
		for ill in lst1:
			if ill in dic_ill:
				dic_ill[ill] += 1
			else:
				dic_ill[ill] = 1
		sorted_dict = reversed(sorted(dic_ill.items(), key=lambda kv: kv[1]) )# todo: check list
		ill_lst = []
		for tup in sorted_dict:
			if tup[0] is not None:
				ill_lst.append(tup[0])
		return ill_lst




	def all_illnesses_helper(self,root,lst_illnesses):
		if root.positive_child is None:
			lst_illnesses.append(root.data)
		else:
			self.all_illnesses_helper(root.positive_child,lst_illnesses)
			self.all_illnesses_helper(root.negative_child,lst_illnesses)
		return lst_illnesses


	def paths_to_illness(self, illness):
		paths = self.paths_to_illness_helper(illness,self.root,lst_path=[],finally_lst=[])
		return paths


	def paths_to_illness_helper(self,illness,root,lst_path,finally_lst):
		if  root.negative_child is None:
			if root.data == illness:
				finally_lst.append(lst_path)
				return finally_lst
			else:
				# finally_lst.append([])
				return finally_lst
		if root is None and illness is None :
			finally_lst.append(lst_path)
			return finally_lst
		else:
			self.paths_to_illness_helper(illness,root.negative_child,lst_path+[False],finally_lst)
			self.paths_to_illness_helper(illness,root.positive_child,lst_path+[True],finally_lst)
			return finally_lst


	def minimize_helper(self, node, remove):
		if node.positive_child is None and node.negative_child is None:
			return node
		r = self.minimize_helper(node.positive_child, remove)
		l = self.minimize_helper(node.negative_child, remove)
		if remove:
			if r.data is None:
				return l
			if l.data is None:
				return r
		if check(r, l):
			return r
		return Node(node.data, r, l)

	def minimize(self, remove_empty=False):
		self.root = self.minimize_helper(self.root, remove_empty)

def check(sub_tree1, sub_tree2):
	if sub_tree1.positive_child is None and sub_tree1.negative_child is None and sub_tree2.positive_child is None and sub_tree2.negative_child is None:
		return sub_tree1.data == sub_tree2.data
	if sub_tree1.data != sub_tree2.data:
		return False
	return check(sub_tree1.positive_child, sub_tree2.positive_child) and check(sub_tree1.negative_child, sub_tree2.negative_child)

def build_tree(records, symptoms):
	if len(symptoms) == 0:
		ills_dict = {}
		for rec in records:  # get the legal records
			if rec.illness in ills_dict:
				ills_dict[rec.illness] += 1
			else:
				ills_dict[rec.illness] = 1
		sorted_dict = sorted(ills_dict.items(), key=lambda kv: kv[1])  # todo: check list
		if len(sorted_dict)!=0:
			return Diagnoser(Node(sorted_dict[-1][0]))

		else:
			return Diagnoser(Node(None))
	for symptom in symptoms:
		if type(symptom) != str:
			raise TypeError("is should be a string")
	for rec in records:
		if type(rec) != Record:
			raise TypeError("it have to be Record type")
	r = build_tree_without_records(symptoms)
	build_tree_helper(r,[],records,r)
	return Diagnoser(r)


def build_tree_helper(root,path,records,main_root):
	if root: # gets all the possible paths
		build_tree_helper(root.positive_child,path + [(root.data,True)], records, main_root)
		build_tree_helper(root.negative_child,path + [(root.data,False)], records, main_root)
	else:
		ills_dict= {}
		for rec in records: # get the legal records
			if match_illness_to_path(rec,path):
				if rec.illness in ills_dict:
					ills_dict[rec.illness] += 1
				else:
					ills_dict[rec.illness] = 1
		sorted_dict = sorted(ills_dict.items(), key=lambda kv: kv[1]) # todo: check list
		if len(sorted_dict)!=0:
			add_illness_to_path(main_root,path,sorted_dict[-1][0])
		else:
			add_illness_to_path(main_root,path,None)


def add_illness_to_path(root,path,illness):
	for tup in path[:-1]:
		if tup[1]:
			root = root.positive_child
		else:
			root = root.negative_child
	if path[-1][1]:
		root.positive_child = Node(illness)
	else:
		root.negative_child = Node(illness)


def match_illness_to_path(record,path):
	pos = []
	neg = []
	for tup in path: # gets the positive and negative paths
		if tup[1]:
			pos.append(tup[0])
		else:
			neg.append(tup[0])
	for symptom in neg: # check if we have correct symptoms
		if symptom in record.symptoms:
			return False
	for symptom in pos:
		if symptom not in record.symptoms:
			return False
	return True

def build_tree_without_records(symptoms):
	if len(symptoms) == 0:
		return None
	return Node(symptoms[0],build_tree_without_records(symptoms[1:]),build_tree_without_records(symptoms[1:]))




def optimal_tree(records, symptoms, depth):
	lst= []
	lst_rate = []
	sym_set = set(symptoms)
	if len(symptoms) < depth or depth < 0:
		raise ValueError("invalid value")
	if len(sym_set) != len(symptoms):
		raise ValueError("invalid symptoms")
	lst_symptoms = list(combinations(symptoms, depth))
	for symptom in lst_symptoms:
		trees = build_tree(records,symptom)
		lst.append(trees)
	dic_trees = dict()
	for tree in lst:
		dic_trees[tree]=(tree.calculate_success_rate(records))
	max_rate = sorted(dic_trees.items(), key=lambda kv: kv[1])
	return max_rate[-1][0]














if __name__ == "__main__":

	# Manually build a simple tree.
	#                cough
	#          Yes /       \ No
	#        fever           healthy
	#   Yes /     \ No
	# covid-19   cold

	flu_leaf = Node("covid-19", None, None)
	cold_leaf = Node("cold", None, None)
	inner_vertex = Node("fever", flu_leaf, cold_leaf)
	healthy_leaf = Node("healthy", None, None)
	root = Node("cough", inner_vertex, healthy_leaf)

	diagnoser = Diagnoser(root)
	diagnoser.all_illnesses()

	# Simple test
	# diagnosis = diagnoser.diagnose(["cough"])
	# if diagnosis == "cold":
	# 	print("Test passed")
	# else:
	# 	print("Test failed. Should have printed cold, printed: ", diagnosis)

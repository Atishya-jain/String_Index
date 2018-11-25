import threading

class Node:
	def __init__(self):
		# dictionary of pointers to child indexed by alphabet
		self.children = dict()
		# to check how many instances of same string the datastruture has. This also has timestamp of string
		# additions to recognize which string was added after the query for result generation
		self.is_end_of_word = [0,False,()]

class Result:
	def __init__(self, strs, sizes, time):
		self.num_str = sizes
		self.strings = strs
		self.time_stamp = time

	def size(self):
		return self.num_str

	def remove(self, str_obj):
		deleted = 0
		for x in self.strings:
			deleted = deleted + str_obj.delete(x, self.time_stamp)
		self.num_str = 0
		return deleted

class StringIndex:
	def __init__(self):
		# Root of prefix tree
		self.root_pref = Node()
		# root of inverted prefix tree
		self.root_suff = Node()
		# Timestamp the inserted string
		self.timestamp = 0

	# end is my special end character
	def insert(self, ins_str):
		self.timestamp = self.timestamp + 1
		# Insert the word in prefix tree
		curr_pref_node = self.root_pref
		size = len(ins_str)
		ans = 0
		# Loop over word length
		for i in range(size):
			if ins_str[i] in curr_pref_node.children:
				curr_pref_node = curr_pref_node.children[ins_str[i]]
			else:
				curr_pref_node.children[ins_str[i]] = Node()
				curr_pref_node = curr_pref_node.children[ins_str[i]]
			
			# Inserting end pointer and maintaing count of duplicates
			if i == size-1:
				curr_pref_node.children["end"] = Node()
				curr_pref_node.children["end"].is_end_of_word[2] = curr_pref_node.children["end"].is_end_of_word[2] + (self.timestamp,)
				curr_pref_node.children["end"].is_end_of_word[1] = True
				curr_pref_node.children["end"].is_end_of_word[0] = curr_pref_node.children["end"].is_end_of_word[0] + 1
				ans = curr_pref_node.children["end"].is_end_of_word[0] - 1
		
		# Insert the word in inverted prefix tree i.e prefix tree of inverted strings
		curr_suff_node = self.root_suff
		# Invert the string
		rev_ins_str = ins_str[::-1]
		for i in range(size):
			if rev_ins_str[i] in curr_suff_node.children:
				curr_suff_node = curr_suff_node.children[rev_ins_str[i]]
			else:
				curr_suff_node.children[rev_ins_str[i]] = Node()
				curr_suff_node = curr_suff_node.children[rev_ins_str[i]]
			
			# Inserting end pointer and maintaining the ocunt of duplicates
			if i == size-1:
				curr_suff_node.children["end"] = Node()
				curr_suff_node.children["end"].is_end_of_word[2] = curr_suff_node.children["end"].is_end_of_word[2] + (self.timestamp,)
				curr_suff_node.children["end"].is_end_of_word[1] = True
				curr_suff_node.children["end"].is_end_of_word[0] = curr_suff_node.children["end"].is_end_of_word[0] + 1

		return ans			

	def stringsWithPrefix (self, ins_str):
		# Tree Root
		curr_pref_node = self.root_pref
		size = len(ins_str)
		
		# To check if given prefix exists or not. If exists, bring pointer to node
		found = True
		for i in range(size):
			if ins_str[i] in curr_pref_node.children:
				curr_pref_node = curr_pref_node.children[ins_str[i]]
			else:
				found = False
				break

		# If found recurse on children to out pur Result strings and their count
		if found:
			[strs, sizes] = self.recurse (curr_pref_node, ins_str, 0)
			res = Result(strs, sizes, self.timestamp)
		else:
			res = Result((), 0, self.timestamp)

		return res

	def stringsWithSuffix (self, ins_str):
		# invert the string to search in inverted prefix tree
		rev_ins_str = ins_str[::-1]

		# Tree Root
		curr_suff_node = self.root_suff
		size = len(rev_ins_str)
		
		# To check if given prefix exists or not. If exists, bring pointer to node
		found = True
		for i in range(size):
			if rev_ins_str[i] in curr_suff_node.children:
				curr_suff_node = curr_suff_node.children[rev_ins_str[i]]
			else:
				found = False
				break

		# If found recurse on children to out pur Result strings and their count
		if found:
			[strs, sizes] = self.recurse (curr_suff_node, rev_ins_str, 1)
			res = Result(strs, sizes, self.timestamp)
		else:
			res = Result((), 0, self.timestamp)

		return res
	
	def recurse (self, node, string, is_suff):
		# We return a tuple of strings and number of strings
		to_ret = [(), 0]
		size = len(node.children)
		
		# Traverse on children
		for key in node.children:
			# Temporary variable
			temp_str = string
			# If the only key is end it means this is end of a word and there are no other children. 
			#Just Return string + number of duplicates
			#else recurse on children
			if (key == "end") and (size == 1):
				# revert back the string if suffix tree was being traversed
				if is_suff:
					return [(temp_str[::-1],), node.children["end"].is_end_of_word[0]]
				else:
					return [(temp_str,), node.children["end"].is_end_of_word[0]]
			elif key == "end" and size != 1: 
				to_ret[0] = to_ret[0] + (temp_str,)
				to_ret[1] = to_ret[1] + 1
			else:
				temp_str = temp_str + key
				var = self.recurse(node.children[key], temp_str, is_suff)
				to_ret[0] = to_ret[0] + var[0]
				to_ret[1] = to_ret[1] + var[1]
		# return
		return to_ret

	def delete (self, del_str, time_stamp):
		curr_pref_node = self.root_pref
		curr_suff_node = self.root_suff
		pref_del = self.delete_help (curr_pref_node, del_str, time_stamp)
		inv_del_str = del_str[::-1]
		suff_del = self.delete_help (curr_suff_node, inv_del_str, time_stamp)
		
		if pref_del[1] != suff_del[1]:
			print ("There has been some delete error")
			print (str(pref_del[1]) + " " + str(suff_del[1]))
		return pref_del[1]	

	def delete_help (self, node, del_str, time_stamp):
		# Base case: empty string
		if len(del_str) == 0:
			if "end" in node.children:
				count = 0
				# delete the string instances before timestamp
				for times in node.children["end"].is_end_of_word[2]:
					if(times <= time_stamp):
						count += 1			
				
				# Count of deletions is exactly equal to number of timestamps -> delete this node as well
				if count == len(node.children["end"].is_end_of_word[2]):
					del node.children["end"]
					# if no nodes left and count deleted
					if len(node.children) == 0:
						return (0, count)
					else:
						return (1, count)
				else:
					# splice the timestamp tuple from count as all before timestamps have been deleted
					node.children["end"].is_end_of_word[2] = node.children["end"].is_end_of_word[2][count:]
					# signal of nodes left underneath and how many deleted
					return (1,count)
			else:
				return (1,0)
		else:
			# if the first character is in children recurse else retuen no deletion
			if del_str[0] in node.children:
				# Recursion
				var = self.delete_help(node.children[del_str[0]], del_str[1:], time_stamp)
				
				# My child says delete me if var[0] = 0
				if (var[0] == 0):
					del node.children[del_str[0]]
					
					# if I am left with no children I send my parent a signal to delete me
					if len(node.children) == 0:
						return (0,var[1])
					else:
						return (1, var[1])
				else:
					return var
			else:
				return (1,0)

if __name__ == '__main__':
	
	# Synchronous benchtest
	test = StringIndex()
	test.insert("atishya")
	test.insert("ati")
	test.insert("avaljot")
	test.insert("aval")
	test.insert("mayank")
	test.insert("maya")
	test.insert("mankaran")
	test.insert("manku")
	test.insert("banana")
	test.insert("ant")

	obj0 = test.stringsWithPrefix("ma")
	for s in obj0.strings:
		print (s,end = " ")
		print()
	print (obj0.size())
	print ("-----------------------------------------------------")

	obj1 = test.stringsWithSuffix("ot")
	for s in obj1.strings:
		print (s,end = " ")
		print()
	print(obj1.size())

	print ("-----------------------------------------------------")

	obj2 = test.stringsWithSuffix("ya")
	for s in obj2.strings:
		print (s,end = " ")
		print()
	print("obj2 size: " + str(obj2.size()))
	print("maya removal: " + str(obj2.remove(test)))
	print("obj0 initial size: " + str(obj0.size()))
	print("obj0 removals: " + str(obj0.remove(test)))
	print("obj0 after removals: " + str(obj0.size()))

	print ("-----------------------------------------------------")
	
	obj21 = test.stringsWithPrefix("ma")
	for s in obj21.strings:
		print (s,end = " ")
		print()
	print (obj21.size())

	print ("-----------------------------------------------------")

	obj3 = test.stringsWithPrefix("av")
	for s in obj3.strings:
		print (s,end = " ")
		print()
	print (obj3.size())
	print ("-----------------------------------------------------")
	
	obj4 = test.stringsWithPrefix("at")
	for s in obj4.strings:
		print (s,end = " ")
		print()
	print (obj4.size())


	# Asynchrounous testing
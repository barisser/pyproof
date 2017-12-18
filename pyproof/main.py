import copy
import hashlib
import math

# Cryptographic Accumulators

def mod_exp(a, b, n):
	"""
	Returns the result of
	(a ^ b) mod n
	"""
	result = 1
	while True:
		if b % 2 == 1:
			result = (a * result) % n
		
		b = b / 2
		
		if b == 0:
			break 		
		
		a = (a * a) % n

	return result


def increment_membership_accumulator(acc, value, n):
	return mod_exp(acc, value, n)

def verify_membership(acc, value, witness, n):
	expected_acc= increment_membership_accumulator(witness, value, n)
	return acc == expected_acc


# Merkle Trees

def sha256(value):
	return hashlib.sha256(value).hexdigest()

def do_hash(value, algo='sha256'):
	if algo == 'sha256':
		return sha256(value)
	else:
		raise Exception("Unknown hash algo: {0}".format(algo))


def int_to_address(n, length):
	return "{0:b}".format(n).zfill(length)

def parent_address(address):
	if len(address) >= 1:
		return address[0:-1]
	else:
		return ''


class MerkleTree:
	def __init__(self, values, algo='sha256'):
		self.algo = algo
		self.nodes = {}
		self.addresses = {}
		self.unresolved_nodes = []
		self.address_length = int(math.ceil(math.log(len(values), 2.0)))

		for n, v in enumerate(values):
			h = do_hash(v, self.algo)
			self.nodes[h] = {'parent': None, 'address': int_to_address(n, self.address_length)}
			self.unresolved_nodes.append(h)
			self.addresses[self.nodes[h]['address']] = h

		self.root = None

		while len(self.unresolved_nodes) > 0:
			self.build_tree()
			self.root = self.addresses['']


	def find_sibling(self, hashv):
		address = self.nodes[hashv]['address']
		if address == '':
			return None, None
		addr_n = int(address, 2)
		if addr_n % 2 == 1:
			sibl_n = addr_n - 1
			left_sibl = True
		else:
			sibl_n = addr_n + 1
			left_sibl = False
		sibl_address = int_to_address(sibl_n, len(address))
		if sibl_address in self.addresses:
			return self.addresses[sibl_address], left_sibl
		else:
			return hashv, False


	def find_path(self, start):
		"""
		Finds a path from a node hash to the root.
		If it does not exists it throws an exception.
		A path is structured in the following format:
		A list of steps:
		   - Each step shows [left_hash, right_hash, next_hash]
		   - next_hash must be either the left or right hash in the next step.
		   - Within each step, left_hash + right_hash must hash to next_hash.
		"""
		path = []
		leaf = start
		seen_nodes = []
		while True:
			if self.nodes[leaf]['address'] == '':
				return path
			
			left = leaf if self.nodes[leaf]['left'] else self.nodes[leaf]['sibling']
			right = leaf if not self.nodes[leaf]['left'] else self.nodes[leaf]['sibling']
			next_hash = do_hash(left + right, self.algo)
			leaf = self.nodes[leaf]['parent']
			assert leaf == next_hash
			assert not next_hash in seen_nodes
			assert next_hash in self.nodes
			step = [left, right, next_hash]
			path.append(step)



	def build_tree(self):
		resolved_nodes = []
		for nodeh in self.unresolved_nodes:
			sibling, left_sibl = self.find_sibling(nodeh)
			
			if nodeh in resolved_nodes:
				continue

			if sibling:
				self.nodes[nodeh]['sibling'] = sibling
				self.nodes[nodeh]['left'] = not left_sibl
				self.nodes[sibling]['left'] = left_sibl
				self.nodes[sibling]['sibling'] = nodeh

				if left_sibl:
					parent = do_hash(sibling + nodeh, self.algo)
				else:
					parent = do_hash(nodeh + sibling, self.algo)
				self.nodes[sibling]['parent'] = parent
				self.nodes[nodeh]['parent'] = parent
				resolved_nodes.append(nodeh)
				resolved_nodes.append(sibling)

				paddress = parent_address(self.nodes[nodeh]['address'])
				self.nodes[parent] = {'address': paddress}
				self.addresses[paddress] = parent
				if paddress != '':
					self.unresolved_nodes.append(parent)
			else:
				self.nodes[nodeh]['address'] = parent_address(self.nodes[nodeh]['address'])
		self.unresolved_nodes = list(set(self.unresolved_nodes) - set(resolved_nodes))


def verify_path(path, leaf, root, algo='sha256'):
	"""
	Verifes a Merkle Path for correctness.
	If false, throws an error.
	If true, returns the binary address of the Merkle Path.
	"""	
	last_parent = leaf
	assert leaf in path[0][:1]
	address = ''
	for left, right, parent in path:
		assert do_hash(left + right, algo) == parent
		if last_parent == left:
			address = "0" + address
		elif last_parent == right:
			address = "1" + address
		else:
			assert False 
		last_parent = parent

	assert last_parent == root
	return address

# def find_path(paths, leaf_value):
# 	"""
# 	For a given leaf and datastructure representing all paths,
# 	find the path from the specified leaf to the root.
# 	The path will be represented by a list of lists.
# 	Each list is a step, ie [LEFT_HASH, RIGHT_HASH, PARENT_HASH]
# 	"""
# 	path = []
# 	leaf = hashlib.sha256(leaf_value).hexdigest()
# 	assert leaf in paths

# 	while True:
# 		if leaf in paths:
# 			step = paths[leaf]
# 			path.append(step)
# 			leaf = step[2]
# 			print leaf
# 		else:
# 			return path
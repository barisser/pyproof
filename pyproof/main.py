import copy
import hashlib

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

def leaf_n_to_address(n):
	"""
	Takes the nth leaf node, starting at 0 and going left to right,
	and translates it into an address format.
	"""
	return "{0:b}".format(n)

def find_parent_address(address):
	return leaf_n_to_address(int(address, 2) / 2)

def find_sibling(address, nodes, addresses):
	n = int(address, 2)
	if n % 1 == 0:
		sibling_n = n + 1
	else:
		sibling_n = n - 1
	sibling_address = leaf_n_to_address(sibling_n)
	if sibling_address in addresses:
		return addresses[sibling_address]
	else:
		return None

def make_parent_hash(address1, address2, addresses):
	n1 = int(address1, 2)
	n2 = int(address2, 2)
	assert n1 != n2
	h1 = addresses[address1]
	h2 = addresses[address2]
	if n1 < n2:
		return hashlib.sha256("{0}{1}".format(h1, h2)).hexdigest()
	elif n1 > n2:
		return hashlib.sha256("{0}{1}".format(h2, h1)).hexdigest()



def make_tree(leaf_values):
	leaf_hashes = [hashlib.sha256(x).hexdigest() for x in leaf_values]

	nodes = dict([(lhash, {'address': leaf_n_to_address(n), 'parent': None, 'sibling': None}) for n, lhash in enumerate(leaf_hashes)])
	addresses = dict([(nodes[lhash]['address'], lhash) for lhash in nodes])

	level_hashes = copy.copy(leaf_hashes)
	while len(level_hashes) > 1:
		new_level_hashes = []
		for lhash in level_hashes:
			sibling_hash = find_sibling(nodes[lhash]['address'], nodes, addresses)
			print sibling_hash
			if sibling_hash:
				new_hash = make_parent_hash(nodes[lhash]['address'], nodes[sibling_hash]['address'], addresses)
				nodes[lhash]['sibling'] = sibling_hash
				nodes[sibling_hash]['sibling'] = lhash
				nodes[lhash]['parent'] = new_hash
			else:
				new_hash = lhash

			new_level_hashes.append(new_hash)
			nodes[new_hash] = {'address': find_parent_address(nodes[lhash]['address']), 'parent': None, 'sibling': None}


		level_hashes = list(set(new_level_hashes))
		#import pdb;pdb.set_trace()

	return level_hashes[0]
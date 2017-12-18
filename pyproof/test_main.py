import hashlib
import random

import main


def test_mod_exp():
	for _ in range(100):
		a = random.randint(1, 10**5)
		b = random.randint(1, 10**4)
		n = random.randint(1, 1000)

		# test for reasonably small numbers
		assert main.mod_exp(a, b, n) == (a ** b) % n

def test_membership():
	# These are not secure or realistic values.
	for _ in range(10):
		acc = random.randint(1, 10**100)
		value = random.randint(1, acc - 1)
		n = random.randint(10**100, 10**101)
		new_acc = main.increment_membership_accumulator(acc, value, n)
		assert main.verify_membership(new_acc, value, acc, n)

def test_tree():
	values = [str(x) for x in range(4)]
	tree = main.MerkleTree(values)
	assert tree.root == '862532e6a3c9aafc2016810598ed0cc3025af5640db73224f586b6f1138385f4'

	values2 = [str(x) for x in range(3)] # we can verify this by hand
	tree2 = main.MerkleTree(values2)
	assert tree2.root == 'd32c0dae8492cecc66b77c89843c6c92dbedded6642ef9985f86edf6b5494a8f'

	values3 = [str(x) for x in range(2**10-1)]
	tree3 = main.MerkleTree(values3)
	assert tree3.root == 'd0810b120c0cb59503f7ee8dadbecafa5385ad15a921fec94641649d78a328bf'
	assert tree3.unresolved_nodes == []

	n = 100
	leaf = hashlib.sha256(str(n)).hexdigest()
	path = tree3.find_path(leaf)
	assert path[4] == ['37e433a20c048adb15baa66856c8d22d1b381b0a3a4294f42d4b8c36856aebea',
		'5b778c221e4823dbbe790975debe5b43ebec78f7473d782d3e164e117f3a1d41',
		'a8af985a08cdd57e1188fe1a111361c7a3f7fbad26aad82fe741090d2f42d9bd']

	assert path[-1][-1] == tree3.root

	address = main.verify_path(path, leaf, tree3.root)
	assert int(address, 2) == int(n)

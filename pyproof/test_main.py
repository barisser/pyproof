import main
import random

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


def test_make_tree():
	values = [str(x) for x in range(113)]
	tree = main.make_tree(values)
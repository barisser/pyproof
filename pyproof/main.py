

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

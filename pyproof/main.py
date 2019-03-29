"""Main Library for Pyproofs"""
import hashlib
import math

from Crypto.Util import number

def get_prime(digits=512, strong=True):
    if strong:
        return number.getStrongPrime(digits)
    else:
        return number.getPrime(digits)

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


def verify_hash_membership(acc, value, witness, n):
    expected_acc = increment_membership_accumulator(witness, value, n)
    return acc == expected_acc


def add_many_memberships(acc, values, n):
    witnesses = {}
    u = acc
    cumulative_witnesses = []
    reverse_cumulative_witnesses = []

    asc_acc = acc
    desc_acc = acc
    for i in range(len(values)):
        my_witness = acc
        for j in range(len(values)): # inefficient
            if i == j:
                continue
            else:
                my_witness = increment_membership_accumulator(my_witness, values[j], n)
        witnesses[values[i]] = my_witness
        u = increment_membership_accumulator(u, values[i], n)

    for value in witnesses:
        assert verify_hash_membership(u, value, witnesses[value], n)

    return u, witnesses


def compute_non_membership_witness(acc, value, g, n, values):
    # WIP, CURRENTLY BROKEN
    
    # https://www.cs.purdue.edu/homes/ninghui/papers/accumulator_acns07.pdf
    
    # u = multiple of all values in set
    # all values are primes
    # non-member value is X
    # gcd(x, u) == 1
    # thus there exists some ax + bu = 1
    # let a2 = a + kx and let b2 = b + ku
    # then a2 * u + b2 * x = 1
    # let d = g ^ -b2 mod n
    # nonmembership witness is (a, d)
    # let c = g^u = our membership accumulator value
    # separately we have
    # (c^a = g^(u*a) = g^(1-bx) = g^(-bx) * g = d^x * g ) mod n
    # if above is true with given witness (a, d), nonmembership is true
    # to verify just show that c^a mod n == d^x * g mod n

    assert not value in values
    
    u = 1
    for x in values:
        u = u * x

    gcd, a, b = xgcd(value, u)
    assert gcd == 1
    if a < 0:
        a_diff = -a / u + 1
    else:
        a_diff = 0
    if b > 0:
        b_diff = b / value + 1
    else:
        b_diff = 0
    k = max(a_diff, b_diff)
    a2 = a + k * u
    b2 = b - k * value
    
    try:
        assert b2 > 0
        assert a2 > 0
    except:
        import pdb; pdb.set_trace()
    try:
        assert a2 * value + b2 * u == 1
    except:
        import pdb; pdb.set_trace()
    assert a * value + b * u == 1

    d = mod_inverse(mod_exp(g, b2, n), n)
   # import pdb;pdb.set_trace()
    assert verify_non_membership(acc, a2, d, value, g, n)
    return a2, d

def verify_non_membership_old(acc, witness_a, witness_d, value, g, n):
    left = mod_exp(acc, witness_a, n)
    right = (mod_exp(witness_d, value, n) * (g % n)) % n
    import pdb; pdb.set_trace()
    return left == right


# Merkle Trees

def sha256(value):
    """Because I prefer this format."""
    return hashlib.sha256(value).hexdigest()


def do_hash(value, algo='sha256'):
    """
    Handles computation of all hashes.
    Support other hash algorithms later.
    """
    if algo == 'sha256':
        return sha256(value)
    else:
        raise Exception("Unknown hash algo: {0}".format(algo))


def int_to_address(n, length):
    """
    Convert an index location to a binary representation
    of address.  Length refers to the binary length
    of the string.  This corresponds to max depth of tree.
    """
    return "{0:b}".format(n).zfill(length)


def parent_address(address):
    """
    For a given address, compute the address of the parent.
    """
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

        for n, value in enumerate(values):
            hashv = do_hash(value, self.algo)
            self.nodes[hashv] = {
                'parent': None, 'address': int_to_address(n, self.address_length)}
            self.unresolved_nodes.append(hashv)
            self.addresses[self.nodes[hashv]['address']] = hashv

        self.root = None

        while len(self.unresolved_nodes) > 0:
            self.build_tree()
            self.root = self.addresses['']

    def find_sibling(self, hashv):
        """
        For a given node hash, finds a sibling of that hash
        if one exists.  If it does not exist, creates a duplicate
        of this node (as per Merkle Tree algorithm).
        """
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

            left = leaf if self.nodes[leaf][
                'left'] else self.nodes[leaf]['sibling']
            right = leaf if not self.nodes[leaf][
                'left'] else self.nodes[leaf]['sibling']
            next_hash = do_hash(left + right, self.algo)
            leaf = self.nodes[leaf]['parent']
            assert leaf == next_hash
            assert next_hash not in seen_nodes
            assert next_hash in self.nodes
            step = [left, right, next_hash]
            path.append(step)

    def build_tree(self):
        """
        Resolves unresolved nodes in the merkle tree.
        This function progressively stitches the tree together
        until it reaches the root node.
        """
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
                self.nodes[nodeh]['address'] = parent_address(
                    self.nodes[nodeh]['address'])
        self.unresolved_nodes = list(
            set(self.unresolved_nodes) - set(resolved_nodes))


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

# other

def xgcd(b, n):
    """
    Performs Extended Euclidian Algorithm.
    Returns GCD(X, Y), A, B for equation
    X*A + Y*B = GCD(X, Y) where X, Y, A, B are all integers.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def mod_inverse(a, n):
    # ax + by = gcd(a, b)
    # a * x mod b = 1
    # b * y mod a = 1
    #
    # mod_inverse(a) * a mod n = 1

    # solve for X where a=a and b=n
    gcd, x, y = xgcd(a, n)
    assert gcd == 1 # this only works for coprime numbers
    return x

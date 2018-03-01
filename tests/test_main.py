"""Tests functions in main.py"""
import hashlib
import random

#from pyproof import main
import pyproof


def test_mod_exp():
    for _ in range(100):
        a = random.randint(1, 10**5)
        b = random.randint(1, 10**4)
        n = random.randint(1, 1000)

        # test for reasonably small numbers
        assert pyproof.mod_exp(a, b, n) == (a ** b) % n


def test_membership():
    # These are not secure or realistic values.
    for _ in range(10):
        acc = random.randint(1, 10**100)
        value = random.randint(1, acc - 1)
        n = random.randint(10**100, 10**101)
        new_acc = pyproof.increment_membership_accumulator(acc, value, n)
        assert pyproof.verify_membership(new_acc, value, acc, n)


def test_many_memberships():
    acc = random.randint(10**80, 10**85)
    iterations = 20
    values = {}
    n = random.randint(10**80, 10**85)
    for _ in range(iterations):
        value = random.randint(10**80, 10**85)
        for v in values:
            values[v] = pyproof.increment_membership_accumulator(
                values[v], value, n)
        values[value] = acc
        acc = pyproof.increment_membership_accumulator(acc, value, n)

    for v in values:
        assert pyproof.verify_membership(acc, v, values[v], n)

def test_add_many_memberships():
    digits = 64
    acc = pyproof.get_prime(digits=digits, strong=False)
    n = pyproof.get_prime(digits=digits, strong=False)
    values = [pyproof.get_prime(digits=digits, strong=False) for _ in range(10)]

    new_acc, witnesses = pyproof.add_many_memberships(acc, values, n)


def test_tree():
    values = [str(x) for x in range(4)]
    tree = pyproof.MerkleTree(values)
    assert tree.root == '862532e6a3c9aafc2016810598ed0cc3025af5640db73224f586b6f1138385f4'

    values2 = [str(x) for x in range(3)]  # we can verify this by hand
    tree2 = pyproof.MerkleTree(values2)
    assert tree2.root == 'd32c0dae8492cecc66b77c89843c6c92dbedded6642ef9985f86edf6b5494a8f'

    values3 = [str(x) for x in range(2**10 - 1)]
    tree3 = pyproof.MerkleTree(values3)
    assert tree3.root == 'd0810b120c0cb59503f7ee8dadbecafa5385ad15a921fec94641649d78a328bf'
    assert tree3.unresolved_nodes == []

    n = 100
    leaf = hashlib.sha256(str(n)).hexdigest()
    path = tree3.find_path(leaf)
    assert path[
        4] == ['37e433a20c048adb15baa66856c8d22d1b381b0a3a4294f42d4b8c36856aebea',
               '5b778c221e4823dbbe790975debe5b43ebec78f7473d782d3e164e117f3a1d41',
               'a8af985a08cdd57e1188fe1a111361c7a3f7fbad26aad82fe741090d2f42d9bd']

    assert path[-1][-1] == tree3.root

    address = pyproof.verify_path(path, leaf, tree3.root)
    assert int(address, 2) == int(n)

import random

import numpy as np

import pyproof


def test_orthogonal_vector():
    dims = 100
    vectors = []
    for i in range(dims - 1):
        random_vector = np.random.random((dims))
        vectors.append(random_vector / np.linalg.norm(random_vector))

    ortho_vector = pyproof.orthogonal_vector(vectors)
    tolerance = 10**-10
    for vector in vectors:
        assert abs(np.dot(ortho_vector, vector)) < tolerance
        

def test_ortho_data():
    n = 300
    data = [str(random.random()) for _ in range(n)]
    ovector, vectors = pyproof.data_to_orthogonal(data)

    for vector in vectors:
        assert pyproof.verify_membership_vector(ovector, vector, tolerance=10**-12)
        assert not pyproof.verify_nonmembership_vector(ovector, vector)
    assert np.allclose(np.linalg.norm(ovector), 1.0)

    data2 = [str(random.random()) for _ in range(n)]
    vectors2 = [pyproof.data_to_vector(x, n + 1) for x in data2]
    assert np.allclose(pyproof.datalist_to_vectors(data2),
            vectors2)

    for vector in vectors2:
        assert pyproof.verify_nonmembership_vector(ovector, vector)
        assert not pyproof.verify_membership_vector(ovector, vector)

    for d in data2:
        assert not pyproof.verify_membership(ovector, d)
        assert pyproof.verify_nonmembership(ovector, d)
    for d in data:
        assert pyproof.verify_membership(ovector, d)
        assert not pyproof.verify_nonmembership(ovector, d)
#    assert False

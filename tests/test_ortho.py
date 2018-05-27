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
        assert pyproof.verify_membership(ovector, vector, tolerance=10**-12)
    assert np.allclose(np.linalg.norm(ovector), 1.0)
    assert False
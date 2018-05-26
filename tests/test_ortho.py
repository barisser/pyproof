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

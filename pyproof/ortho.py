import copy
import math

import numpy as np

def orthogonal_vector(vectors):
    """
    Finds a vector that is orthogonal to all given vectors.
    """
    n_dimensions = len(vectors) + 1
    assert n_dimensions == len(vectors[0])

    v = np.array(vectors)
    ortho_vector = []

    for n in range(n_dimensions):
        sign = math.pow(-1, n)
        matrix_a = v[:, :n]
        matrix_b = v[:, n+1:]        
        my_matrix = np.append(matrix_a, matrix_b, axis=1)
        slog, slogv = np.linalg.slogdet(my_matrix)
        vs = np.exp(slogv) * slog * sign
        ortho_vector.append(vs)

    q =  np.array(ortho_vector)
    return q / np.linalg.norm(q)

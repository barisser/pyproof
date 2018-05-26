import copy

import numpy as np
import sympy as sp

def orthogonal_vector(vectors):
    """
    Finds a vector that is orthogonal to all given vectors.
    """
    n_dimensions = len(vectors) + 1

    bases = sp.symbols('d0:{0}'.format(n_dimensions))
    #vects = copy.copy(vectors)
    #vects.append(bases)
    #vects = vects[::-1]
    v = np.array(vectors)
    #v = sp.Matrix(vects)
    ortho_vector = []
    for n, base in enumerate(bases):
        sign = -1 ** n
        matrix_a = v[:, :n]
        matrix_b = v[:, n+1:]        
        my_matrix = np.append(matrix_a, matrix_b, axis=1)
        #import pdb;pdb.set_trace()
        ortho_vector.append(np.linalg.det(my_matrix) * sign)

    return np.array(ortho_vector)
    # import pdb;pdb.set_trace()
    # ortho_vector_sym = v.det()
    # d = ortho_vector_sym.as_coefficients_dict()
    # return np.array([d.get(k, 0) for k in bases])

def custom_det(matrix):
    """
    Assumes certain matrix structure.  Not generalized!
    """
    return



def set_dims(n):
    dims = sp.Matrix(sp.symbols('x0:{0}'.format(n)))
    return dims

n_dimensions = 5
dims = set_dims(n_dimensions)

v = []
for i in range(n_dimensions-1):
    v.append(np.random.random((n_dimensions)))


def symbolize(vector):
    if len(vector) > n_dimensions:
        set_dims(len(vector))

    sv = sp.Matrix(vector).dot(sp.Matrix(dims[:len(vector)]).transpose())
    return sv
  #  sd = sv.as_coefficients_dict()
  #  v = [sd[k] for k in dims if k in sd]
  #  return sp.Matrix(v)

def choose_cp(degree_dict, dimensions):
    if len(degree_dict) <= 1:
        return None

    d = list(set(dimensions) - set(degree_dict.keys()))
    assert len(d) == 1
    return d[0]
    
def cross_product(vector1, vector2, dimensions=dims):
    v1 = symbolize(vector1)
    v2 = symbolize(vector2)
    v = (v1*v2).expand()
    ortho = sp.sympify("0")
    cd = v.as_coefficients_dict()

    for term in cd.keys():
        symbols = term.free_symbols
        degrees = {}
        for symbol in symbols:
            degree = sp.degree(term, symbol)
            degrees[symbol] = degree
        new_dim = choose_cp(degrees, dimensions)
        if new_dim:
            ortho = ortho + cd[term] * new_dim
            
#        import pdb;pdb.set_trace()
    import pdb;pdb.set_trace()
import time
t=time.time()
q = orthogonal_vector(v)
print time.time()-t
print ''
for x in v:
    print np.dot(q, x)
print ''
print q
#a=symbolize(v[3])
# a.as_coefficients_dict()

#cross_product(v[0], v[1])

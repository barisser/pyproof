import copy
import math

import numpy as np
import sympy as sp

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
        ortho_vector.append(np.linalg.det(my_matrix) * sign)

    q =  np.array(ortho_vector)
    return q / np.linalg.norm(q)

def symbolic_orthogonal_vector(vectors):
    """
    Finds a vector that is orthogonal to all given vectors.
    """
    n_dimensions = len(vectors) + 1

    bases = sp.symbols('d0:{0}'.format(n_dimensions))
    vects = copy.copy(vectors)
    vects.append(bases)
    v = sp.Matrix(vects)

    ortho_vector_sym = v.det()
    d = ortho_vector_sym.as_coefficients_dict()
    return np.array([d.get(k, 0) for k in bases])


def custom_det(matrix):
    """
    Assumes certain matrix structure.  Not generalized!
    """
    return



def set_dims(n):
    dims = sp.Matrix(sp.symbols('x0:{0}'.format(n)))
    return dims

n_dimensions = 100
dims = set_dims(n_dimensions)

v = []
for i in range(n_dimensions-1):
    r = np.random.random((n_dimensions))
    v.append(r / np.linalg.norm(r))


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
print "numerical {0}".format(time.time()-t)
t2 = time.time()

#sv = symbolic_orthogonal_vector(v)
#print "symbolic: {0}".format(time.time()-t2)
print ''
diffs = []
for x in v:
    diff = np.dot(q, x)
    diffs.append(diff)
    if diff  > 10**-10:
        print "large diff " + str(diff)
 #   assert np.dot(sv, x) < 0.000000000001
#    print np.dot(q, x)
print "biggest diff: {0}".format(max(diffs))
print ''
#print q
#print sv


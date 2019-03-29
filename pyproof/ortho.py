import copy
import hashlib
import logging
import math

import numpy as np


DEFAULT_TOLERANCE = 10**-12
DEFAULT_SPACE = 100


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

def data_to_vector(data, dimensions, space=DEFAULT_SPACE):
    """
    Converts a string into a vector in an N-dimensional space.
    The vector will be a unit vector.
    It will occupy the +x0 hemisphere only, by construction.

    The algorithm works as follows:
        Convert the data point into an integer X 
        Convert the integer X into a list of N integers through
        modulo division by M.
        If there are unused dimensions, take the sha256 hash of the input data, use this
        to populate the remaining dimensions. 
    """
    mylist = data_to_list(data, space, dimensions)
    return np.array(mylist) / np.linalg.norm(mylist)


def datalist_to_vectors(datalist, space=DEFAULT_SPACE):
    """
    Take a datalist of length N and force it into N elements with N+1 dimensions
    """
    # ints = map(data_to_int, datalist)
    target_dimensions = len(datalist) + 1
    # lists = [int_to_list(x, space, length=target_dimensions - 1) for x in ints]
    lists = [data_to_list(data, space, target_dimensions) for data in datalist]
    v = []
    for l in lists:
        d = np.linalg.norm(l)
        v.append(np.array(l) / d)
    return np.array(v)


def data_to_orthogonal(datalist, space=DEFAULT_SPACE):
    vectors = datalist_to_vectors(datalist, space=space)
    return orthogonal_vector(vectors), vectors


def spherical_to_cartesian(r, arr):
    """
    Lifted from
    https://stackoverflow.com/questions/20133318/n-sphere-coordinate-system-to-cartesian-coordinate-system
    """
    a = np.concatenate((np.array([2*np.pi]), arr))
    si = np.sin(a)
    si[0] = 1
    si = np.cumprod(si)
    co = np.cos(a)
    co = np.roll(co, -1)
    return si * co * r

def data_to_list(data, space, length):
    l = []
    while len(l) < length:
        i = data_to_int(data)
        templist = int_to_list(i, space)
        l += templist
        data = hashlib.sha256(data).hexdigest()
    l = l[:length]
    return l

def data_to_int(data):
    return int(hashlib.sha256(data).hexdigest(), 16)


def int_to_list(myint, space):
    mylist = []
    while myint > 0:
        v = myint % space
        mylist.append(v)
        myint -= v
        myint = myint / space

    return mylist

def verify_membership_vector(ovector, vector, tolerance=DEFAULT_TOLERANCE):
    diff = abs(np.dot(ovector, vector))
    return diff < tolerance 

def verify_nonmembership_vector(ovector, vector, tolerance=DEFAULT_TOLERANCE):
    diff = abs(np.dot(ovector, vector))
    return diff >= tolerance

def verify_membership(ovector, data, tolerance=DEFAULT_TOLERANCE):
    vector = data_to_vector(data, len(ovector))
    return verify_membership_vector(ovector, vector, tolerance)

def verify_nonmembership(ovector, data, tolerance=DEFAULT_TOLERANCE):
    vector = data_to_vector(data, len(ovector))
    return verify_nonmembership_vector(ovector, vector, tolerance)

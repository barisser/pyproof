import copy
import hashlib
import logging
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

def convert_data_to_hemispherical_vector(data, dimensions, angular_granularity=1.0):
    """
    Converts a string into a vector in an N-dimensional space.
    The vector will be a unit vector.
    It will occupy the +x0 hemisphere only, by construction.

    The algorithm works as follows:
        Convert the data point into an integer X 
        Convert the integer X into a list of N integers through
        modulo division by M.
        M is computed from 180 / angular_granularity.
        Convert the list of N integers into N floats by
        multiplying by angular granularity, you should have N floats
        between 0 and 180.  These constitute spherical coordinates
        in N dimensions.  Convert these to Cartesian coordinates.

        If there are leftover values of data, raise an exception (more dimensions are needed).
        If there are unused dimensions, take the sha256 hash of the input data, use this
        to populate the remaining dimensions. 
    """
    mylist = data_to_list(data, space, dimensions)
    my_angles = [x*angular_granularity / (2 * np.pi) for x in mylist]
    coords = spherical_to_cartesian(1.0, my_angles)
    return coords

def datalist_to_vectors(datalist, angular_granularity=1.0):
    """
    Take a datalist of length N and force it into N elements with N+1 dimensions
    """
    # ints = map(data_to_int, datalist)
    space = int(180.0 / angular_granularity)
    target_dimensions = len(datalist) + 1
    # lists = [int_to_list(x, space, length=target_dimensions - 1) for x in ints]
    lists = [data_to_list(data, space, target_dimensions) for data in datalist]
    v = []
    for l in lists:
        d = np.linalg.norm(l)
        v.append(np.array(l) / d)
    return np.array(v)
    #angles = [[x * angular_granularity / (2 * np.pi) for x in l] for l in lists]

    #import pdb;pdb.set_trace()
    
    #return [spherical_to_cartesian(1.0, angle) for angle in angles]


def data_to_orthogonal(datalist, angular_granularity=1.0):
    vectors = datalist_to_vectors(datalist, angular_granularity=angular_granularity)
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

def verify_membership(ovector, vector, tolerance=10**-12):
    diff = abs(np.dot(ovector, vector))
    if diff >= tolerance:
        logging.error("Large diff seen {0}".format(diff))
    return diff < tolerance 
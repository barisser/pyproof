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
    myint = data_to_int(data)
    space = int(180.0 / angular_granularity)
    mylist = int_to_list(myint, space)
    if len(mylist) > dimensions:
        raise Exception("")
    my_angles = [x*angular_granularity / (2 * np.pi) for x in mylist]
    coords = spherical_to_cartesian(1.0, my_angles)
    return coords


def data_to_vectors(datalist, angular_granularity=1.0):
    dimensions = 2 * max([len(x) for x in datalist]) # HACK
    return [
        convert_data_to_hemispherical_vector(data, dimensions, angular_granularity)
        for data in datalist
    ]


def data_to_orthogonal(datalist, angular_granularity=1.0):
    vectors = data_to_vectors(datalist, angular_granularity=angular_granularity)
    return orthogonal_vector(vectors)


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


seed_primes = [7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471,1481,1483,1487,1489,1493,1499,1511,1523,1531,1543,1549,1553,1559,1567,1571,1579,1583,1597,1601,1607,1609,1613,1619,1621,1627,1637,1657,1663,1667,1669,1693,1697,1699,1709,1721,1723,1733,1741,1747,1753,1759,1777,1783,1787,1789,1801,1811,1823,1831,1847,1861,1867,1871,1873,1877,1879,1889,1901,1907,1913,1931,1933,1949,1951,1973,1979,1987,1993,1997,1999,2003,2011,2017,2027,2029,2039,2053,2063,2069,2081]

def data_to_int(data):
    return reduce(lambda x, y: x * y, map(lambda x: seed_primes[ord(x)], data))

def int_to_list(myint, space):
    mylist = []
    while myint > 0:
        v = myint % space
        mylist.append(v)
        myint -= v
        myint = myint / space
    return mylist

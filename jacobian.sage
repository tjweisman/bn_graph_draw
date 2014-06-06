#!/usr/bin/python

def get_jacobian(A):
    #assuming A is a square array
    n = len(A)
    M = MatrixSpace(IntegerRing(),n,n)
    Q = M(A)
    return Q.elementary_divisors()[:-1]

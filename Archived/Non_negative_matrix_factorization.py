'''1. NMF factors a ndarray into W and H, of dimensions (n,rank) and (rank,m)
    respectively, where (n,m) is the dimensions of the original ndarray.
    For a meaningful factorization, choose rank < min(m,n).
    Every entry in both W and H is guaranteed to be non-negative.
    Input = ndarray, rank
    Output = W, H (ndarrays of dim (n,r) and (r,m) respectively)
    Note: NMF replaces nan values with 0 using replace_placeholder()
2. NMF_plot is specific for traffic problem. It takes in traffic data, runs NMF
    on it with rank=1. Then plots W values corresponding to specified day of
    the week.
    Input = ndarray (with periodicity of 7 days),
            rank,
            day (int value in 0-6)
    Output = plot of W values correspondint to day of week. Use
            matplotlib.pyplot.show() in main.py to see graph.
'''

from numpy import array, dot, multiply, sum, around, floor, copy, concatenate
from numpy import ones, zeros, identity, nanmean
from random import random
from matplotlib.pyplot import plot, show
from math import sqrt

from Data_matrix import replace_placeholder


def NMF(data, RANK=1):
    data = array(data)
    # Replace all the nans with overall mean. (Seems to be better than replacing
    # nan enties with column-wise means.)
    data = replace_placeholder(data,value = nanmean(data))
    # Initialize to random matrices. It is important to not have any symmetry
    # in the initializations as this would impose an unwitting symmetry on the
    # factors.
    W = array([random() for i in
               range(len(data)*RANK)]).reshape(len(data),RANK)
    H = array([random() for i in
               range(RANK*len(data.T))]).reshape(RANK, len(data.T))

    # dot() represents usual matrix multiplication.
    # dot(a,b)[i,j] = sum_k(a[i,k]*b[k,j])
    # multiply() represents term-by-term product of two matrices of equal
    # dimensions.
    # multiply(a,b)[i,j] = a[i,j]*b[i,j].
    for iterations in range(1000):
        Term_1 = dot(data, H.T)
        Term_2 = dot(W, dot(H, H.T))
        W = multiply(multiply(W,Term_1), 1./Term_2)

        Term_3 = dot(W.T, data)
        Term_4 = dot(dot(W.T, W), H)
        H = multiply(multiply(H,Term_3), 1./Term_4)

        # Following is the error term, which is derived from the matrix norm.
        print sum(multiply(data - dot(W,H), data - dot(W,H)))/sum(data)
    #print sum(H)
    #return sum(H)
    return array(W), array(H)

def NMF2(data, RANK=1, beta=0.1, eta=0.1):
    data = array(data)
    data = replace_placeholder(data, value = 0)
    # Initialize to random matrices. It is important to not have any symmetry
    # in the initializations as this would impose an unwitting symmetry on the
    # factors.
    W = array([random() for i in
               range(len(data)*RANK)]).reshape(len(data),RANK)
    H = array([random() for i in
               range(RANK*len(data.T))]).reshape(RANK, len(data.T))

    # dot() represents usual matrix multiplication.
    # dot(a,b)[i,j] = sum_k(a[i,k]*b[k,j])
    # multiply() represents term-by-term product of two matrices of equal
    # dimensions.
    # multiply(a,b)[i,j] = a[i,j]*b[i,j].
    
    for iterations in range(1000):
        H1 = concatenate((copy(H), sqrt(eta)*identity(RANK)), axis=1)
        D1 = concatenate((copy(data), zeros((len(data),RANK))),axis=1)
        
        Term_1 = dot(D1, H1.T)
        Term_2 = dot(W, dot(H1, H1.T))
        W = multiply(multiply(W,Term_1), 1./Term_2)

        W2 = concatenate((copy(W), sqrt(beta)*ones((1,RANK))))
        D2 = concatenate((copy(data), zeros((1,len(data.T)))))
        
        Term_3 = dot(W2.T, D2)
        Term_4 = dot(dot(W2.T, W2), H)
        H = multiply(multiply(H,Term_3), 1./Term_4)

        # Following is the error term, which is derived from the matrix norm.
    print sum(multiply(data - dot(W,H), data - dot(W,H)))
    #print sum(H)
    #return sum(H)
    return array(W), array(H)

def NMF_plot(data, RANK = 1, day = 0):
    W, H = NMF(data, RANK)
    return plot(W[day*24 : (day+1)*24],'ko-')
    #plot(sum(W[24*day:24*(day+1)], axis=1))
    #return None

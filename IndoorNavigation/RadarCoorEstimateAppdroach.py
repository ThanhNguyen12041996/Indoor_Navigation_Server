
import numpy as np
import math
def Radar(P_Signatures, SignatureLocs, P_Test,k):
    M = len(P_Signatures[:,1])
    N = len(P_Test[:,1])

    Euclidean_dist = []
    X = []

    for i in range(0, N):
        for j in range(0, M):
            result = [math.sqrt(((P_Test[i, :] - P_Signatures[j, :]) ** 2).sum(axis=0))]
            if i == N-1:
                Euclidean_dist = np.append(Euclidean_dist, result)
                if j == 86:
                     print("")
                a = [Euclidean_dist.argsort(axis=0)]
    SelectedLocs = [SignatureLocs[[a[0][0],a[0][1]], :]]
    X = [np.average(SelectedLocs,axis=1)]
    return np.matrix(np.array(X))

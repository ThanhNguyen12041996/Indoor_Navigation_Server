import scipy.io
import numpy as np
import math

mat = scipy.io.loadmat('IndoorNav2018.mat')

Xq = mat['WKNNP_Signature']
Yq = mat['WKNN_Locs']
DataTest = mat['Ahihi']


def WKNN(P_Signatures, SignatureLocs, P_Test, k):
    M = len(P_Signatures[:, 1])
    N = len(P_Test[:, 1])
    Euclidean_dist = []
    a = []
    weightKNN = []

    for i in range(0, N):
        for j in range(0, M):
            result = [math.sqrt(((P_Test[i, :] - P_Signatures[j, :]) ** 2).sum(axis=0))]
            if i == N - 1:
                Euclidean_dist = np.append(Euclidean_dist, result)
                if j == 87:
                    print("")
                a = [Euclidean_dist.argsort(axis=0)]
                b = [sorted(Euclidean_dist)]
    a = np.matrix(np.array(a))
    b = np.matrix(np.array(b))
    zeroIdx = b[0, 0] == 0
    zeroIdx1 = b[0, 1] == 0
    zeros = [np.append(zeroIdx, zeroIdx1)]
    zeros = np.matrix(np.array(zeros))
    if zeros.sum(axis=1) == False:
        SelectedLocs = [SignatureLocs[[a[0, 0], a[0, 1]], :]]
        sumweight =  (b[0,0])**(-1)+(b[0,1])**(-1)
        weight1 = np.divide((b[0, 0] ** (-1)), sumweight)
        weight2 = np.divide((b[0, 1] ** (-1)), sumweight)
        weightKNN = np.append(weightKNN, weight1)
        weightKNN = np.append(weightKNN, weight2)

        weight = np.matrix(np.array(weightKNN))
        SelectedLocs = np.matrix(np.array(SelectedLocs))

        weightLocs0 = weight[0, 0] * SelectedLocs[0, :]
        weightLocs1 = weight[0, 1] * SelectedLocs[1, :]

        weightLocsx = np.concatenate((weightLocs0, weightLocs1), axis=0)
        X = weightLocsx.sum(axis=0)
    else:
        for m in range(0, 2):
            if zeros[0,m] == True:
                    SelectedLocs = [SignatureLocs[a[0,m],:]]
        X = [np.average(SelectedLocs,axis=0)]
    print(X)

WKNN(Xq, Yq, DataTest, 2)


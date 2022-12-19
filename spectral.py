import numpy as np
import random
import matplotlib.pyplot as plt
import time
import math


def build_r_graph(N, p_i, p_o, gs):
    np.random.seed()
    random.seed(7) # 5 6 7
                    #98
    matr = [[0 for i in range(N)] for j in range(N)]

    sz = N//gs

    for i in range(N):
        for j in range(N):
            if i == j:
                pass
            else:
                ran = random.random()
                if i // sz == j // sz:
                    matr[i][j] = 1 if ran < p_i else 0
                else:
                    matr[i][j] = 1 if ran < p_o else 0
    matr = np.array(matr)
    p = np.random.permutation(N)
    matr = matr[p, :]
    matr = matr[:, p]

    return matr

def m_laplacian(G):
    lapl = [[0 for i in range(len(G))] for j in range(len(G))]
    for i in range(len(G)):
        row_out = 0
        for j in range(len(G)):
            if G[i][j] == 1:
                lapl[i][j] = -1
                row_out += 1
        lapl[i][i] = row_out
    return np.array(lapl)

def condense(cand):
    new_cand = []
    curr_beg = 0
    i = 0
    while i < len(cand) - 1:
        if cand[i][1] >= cand[i + 1][0]:
            pass
        else:
            new_cand.append((cand[curr_beg][0], cand[i][1]))
            curr_beg = i + 1
        i += 1
    new_cand.append((cand[curr_beg][0], cand[i][1]))

    return new_cand[1:-1]

def find_partitions(A, f_vec):
    avg_slope = (f_vec[-1] - f_vec[0]) / len(f_vec)

    fil_len = 4**math.ceil(np.log10(len(f_vec)))

    cand = []
    for i in range(0, len(f_vec) - fil_len, 1):
        if (f_vec[i + fil_len] - f_vec[i])/fil_len > avg_slope:
            cand.append((i, i + fil_len))

    cand = condense(cand)

    for i in range(len(cand) - 1, -1, -1):
        if (cand[i][1] - cand[i][0] < 1.5 * fil_len):
            cand.pop(i)

    xs = np.linspace(0, len(f_vec), 1000)
    b = f_vec[0]
    ys = avg_slope * xs + b

    maxslope = (f_vec[cand[0][1]] - f_vec[cand[0][0]]) / (cand[0][1] - cand[0][0])
    max_i = 0
    for i in range(len(cand)):
        if (f_vec[cand[i][1]] - f_vec[cand[i][0]]) / (cand[i][1] - cand[i][0]) > maxslope:
            max_i = i
            maxslope = (f_vec[cand[i][1]] - f_vec[cand[i][0]]) / (cand[i][1] - cand[i][0])

    for pai in cand:
        lefts = [pai[0], pai[0]]
        rights = [pai[1], pai[1]]
        ys = [min(f_vec), max(f_vec)]

        plt.plot(lefts, ys, 'b', rights, ys, 'g')


    plt.plot(f_vec, '.-')

    part_1 = math.ceil((cand[max_i][0] + cand[max_i][1])/2) + 5

    plt.plot([part_1, part_1], [min(f_vec), max(f_vec)], 'r')

    plt.show()



    return part_1


def find_graph_quality(A, f_vec):
    partitions = find_partitions(A, f_vec)


    return partitions


def run_part(N, plot = False):
    G = build_r_graph(N, .5, .1, 4)
    lapl = m_laplacian(G)

    st = time.time()
    w, v = np.linalg.eigh(lapl)
    ei_v = np.argsort(w)

    tim_e = time.time() - st
    w_sort = w[ei_v]
    uniq = set(abs(w))
    uniq.remove(min(uniq))

    neg = np.where(w == min(uniq))[0]
    pos = np.where(w == -1 * min(uniq))[0]

    if len(neg) == 0:
        sec_min_ind = pos[-1]
    else:
        sec_min_ind = neg[-1]

    p = np.argsort(v[:,sec_min_ind])
    A = lapl[:, p]
    A = A[p, :]

    tim_s = time.time() - st

    lam = find_graph_quality(A, sorted(v[:, sec_min_ind]))

    tim_f = time.time() - st
    if plot:
        msize = 0.005
        plt.figure(1)
        plt.subplot(211)
        plt.plot(sorted(v[:,sec_min_ind]), '.-')
        plt.title(f"Second largest eigenvalue - {w[sec_min_ind]}")
        plt.subplot(212)
        plt.spy(A, markersize=msize)
        plt.show()


    return tim_e, tim_s, tim_f, lam

print(run_part(1000, plot=True))

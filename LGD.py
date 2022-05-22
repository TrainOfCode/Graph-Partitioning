
from scipy.io import mmread
import numpy as np
import math
import random

def get_order(num, st):
    if st == "random":
        return random.sample([i for i in range(num)], k = num)


def w(part, C):
    return 1 - (len(part) / C)


def LGD(mtx, k, C, stream_type="random"):

    partitions = {i:[] for i in range(k)}
    order = get_order(mtx.shape[0], stream_type)

    count = 0
    for ent in order:
        print("ent: ", ent)
        neighbors = mtx.getrow(ent).indices
        print("neighbors: ", neighbors)
        cand = []
        for part in partitions:
            partition = partitions[part]
            P_to_t = 0
            for i in range(len(neighbors) - 1, -1, -1):
                if neighbors[i] in partition:
                    P_to_t += 1
                    neighbors = np.delete(neighbors, i)
            cand.append(P_to_t * w(partition, C))

        print("cand: ", cand)
        best_c = max(cand)
        choices = []
        for i in range(len(cand)):
            if cand[i] == best_c:
                choices.append(i)
        print("choices: ", choices)
        sizes = [len(partitions[part]) for part in choices]
        print("sizes:", sizes)
        small = min(sizes)
        smallest = []
        for i in range(len(sizes)):
            if sizes[i] == small:
                smallest.append(choices[i])
        print("smallest: ", smallest)
        choice = random.choice(smallest)

        partitions[choice].append(ent)

        print(partitions)
        print()

        count += 1
        # if count == 8:
        #     break
    return partitions




def main():
    # mtx = mmread('3elt/3elt.mtx')
    random.seed(37)

    mtx = mmread('ibm32.mtx')
    num_nodes = mtx.shape[0]
    k = 5
    C = math.ceil(num_nodes / k)
    # print(num_nodes)
    # print(k)
    # print(C)
    # print(mtx.todense())
    part = LGD(mtx, k, C, stream_type="random")

    for par in part:
        print(len(part[par]))
        print(part[par])

    



if __name__ == "__main__":
    main()

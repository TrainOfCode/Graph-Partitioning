from scipy.io import mmread
import numpy as np
import math
import random
from pyvis.network import Network
import argparse

COLORS = ["blue", "green", "red", "yellow", "orange", "purple", "pink"]

def get_order(num, st):
    if st == "random":
        return random.sample([i for i in range(num)], k = num)
    elif st == "DFS":
        pass

def w(part, C):
    return 1 - (len(part) / C)


def LGD(mtx, k, C, stream_type="random"):
    lookup = {}
    partitions = {i:[] for i in range(k)}
    order = get_order(mtx.shape[0], stream_type)

    count = 0
    for ent in order:
        # print("ent: ", ent)
        neighbors = mtx.getrow(ent).indices
        # print("neighbors: ", neighbors)
        cand = []
        for part in partitions:
            partition = partitions[part]
            P_to_t = 0
            for i in range(len(neighbors) - 1, -1, -1):
                if neighbors[i] in partition:
                    P_to_t += 1
                    neighbors = np.delete(neighbors, i)
            cand.append(P_to_t * w(partition, C))

        # print("cand: ", cand)
        best_c = max(cand)
        choices = []
        for i in range(len(cand)):
            if cand[i] == best_c:
                choices.append(i)
        # print("choices: ", choices)
        sizes = [len(partitions[part]) for part in choices]
        # print("sizes:", sizes)
        small = min(sizes)
        smallest = []
        for i in range(len(sizes)):
            if sizes[i] == small:
                smallest.append(choices[i])
        # print("smallest: ", smallest)
        choice = random.choice(smallest)

        partitions[choice].append(ent)
        lookup[ent] = choice

        # print(partitions)
        # print()

        count += 1
        # if count == 8:
        #     break
    return partitions, lookup


def disp(part, mtx, lookup, out):
    nt = Network()
    k = len(part)
    x = 300
    y = 0
    theta = (2 * math.pi / k)
    for part_id in part:
        x, y = x * math.cos(theta) - y * math.sin(theta), y * math.cos(theta) + x * math.sin(theta)
        for i in range(len(part[part_id])):
            nt.add_node(n_id = part[part_id][i] ,
                        label = str(part[part_id][i]),
                        color = COLORS[part_id],
                        value = 1,
                        x = (x + random.random()* 300 - 150),
                        y = (y + random.random() * 300 - 150),
                        physics = False)



    for i in range(mtx.shape[0]):
        for other in mtx.getrow(i).indices:
            if i == other:
                continue
            # elif lookup[i] == lookup[int(other)]:
            #     continue
            else:
                nt.add_edge(i, int(other))

    nt.show(out + '.html')


def find_quality(mtx, lookup, stream):
    count = 0
    total = 0
    for i in range(mtx.shape[0]):
        for other in mtx.getrow(i).indices:
            if lookup[i] != lookup[int(other)]:
                count += 1
            total += 1
    print(f"{stream}: {count / total:.2f}")



def main(inp, out, stream):
    # mtx = mmread('3elt/3elt.mtx')
    random.seed(37)

    mtx = mmread(inp + '.mtx')
    num_nodes = mtx.shape[0]
    k = 5
    C = math.ceil(num_nodes / k)
    # print(num_nodes)
    # print(k)
    # print(C)
    # print(mtx.todense())
    part, lookup = LGD(mtx, k, C, stream_type=stream)

    # print("PARTITIONS:")
    # for par in part:
    #     print(len(part[par]))
    #     print(part[par])
    # print()

    find_quality(mtx, lookup, stream)

    disp(part, mtx, lookup, out)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Basic graph partitioning algorithm testing')
    parser.add_argument('-input', '-i', type= str, help = "The name of file to be input, no file extension required, expected to be a .mtx file")
    parser.add_argument('-output', '-o', type= str, help = "The name of file to be output, no file extension required",
                            default = "LGD.html")
    parser.add_argument('-stream', '-s', type=str,
                            help="How nodes are streamed in, choices, random, DFS, and BFS",
                            choices = ["random", "DFS", "BFS", "all"], default = "all")
    args = parser.parse_args()
    if args.input is None or args.output is None:
        print("incorrect arguments, please run with -h flag for help")
    elif args.parse == "all":
        # main(args.input, args.output, args.stream)
        print("heh not yet")
    else:
        main(args.input, args.output, args.stream)

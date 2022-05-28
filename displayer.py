from pyvis.network import Network
import math
import random

COLORS = ["blue", "green", "red", "yellow", "orange", "purple", "pink"]

def disp(part, mtx, lookup, out):
    nt = Network()
    k = len(part)
    x = 300
    y = 0
    theta = (2 * math.pi / k)
    for part_id in part:
        x, y = x * math.cos(theta) - y * math.sin(theta), y * math.cos(theta) + x * math.sin(theta)
        for i in range(len(part[part_id])):
            nt.add_node(n_id = int(part[part_id][i]) ,
                        label = str(part[part_id][i]),
                        color = COLORS[part_id] if part_id < len(COLORS) else "%06x" % random.randint(0, 0xFFFFFF),
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

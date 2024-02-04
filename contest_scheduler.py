# -*- coding: utf-8 -*-
"""Contest_Scheduler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GK78MnlQVqyJXG3UB8sIL2BQ3eHGFT4j
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

sites = ['Tryhackme', 'Geeksforgeeks', 'HackerRank', 'HackerEarth', 'CodeChef', 'AtCoder', 'Kick Start', 'LeetCode', 'CodeForces', 'codeit04']

d = {i: sites[i] for i in range(len(sites))}

colors = ["lime", "yellow", "powderblue", "lavender", "navajowhite", "springgreen", "slategrey", "dimgrey", "lightsteelblue", "bisque", "darkorange", "burlywood", "mediumblue", "antiquewhite", "tan", "forestgreen", "limegreen", "darkgreen", "cornflowerblue", "green", "grey", "royalblue", "ghostwhite", "midnightblue", "blanchedalmond", "papayawhip", "darkgray", "darkgrey", "silver", "lightgray lightgrey", "gainsboro", "whitesmoke", "navy", "darkblue", "moccasin", "orange", "black", "mediumseagreen", "mintcream", "mediumspringgreen", "mediumaquamarine", "aquamarine", "turquoise", "lightseagreen mediumturquoise", "wheat", "blue", "white", "oldlace", "floralwhite", "darkgoldenrod", "goldenrod", "slateblue", "darkslateblue", "mediumslateblue", "snow", "rosybrown", "lightcoral", "indianred", "cornsilk", "azure", "mediumpurple", "rebeccapurple", "blueviolet", "gold", "lemonchiffon", "brown", "indigo", "firebrick", "khaki", "lightcyan", "paleturquoise", "darkslategray", "darkslategrey", "teal", "darkorchid", "maroon", "darkviolet", "palegoldenrod", "darkkhaki", "darkred", "mediumorchid", "red", "darkcyan", "thistle", "aqua", "mistyrose", "salmon", "plum", "violet", "tomato", "darksalmon", "purple", "darkmagenta", "fuchsia", "coral", "orangered", "lightsalmon", "sienna", "ivory", "beige", "lightyellow", "lightgoldenrodyellow", "olive", "olivedrab", "yellowgreen", "darkolivegreen", "greenyellow", "chartreuse", "lawngreen", "honeydew", "darkseagreen", "palegreen", "cyan", "darkturquoise", "cadetblue", "lightblue", "deepskyblue", "skyblue", "lightskyblue", "steelblue", "magenta", "orchid", "seashell", "mediumvioletred", "deeppink", "hotpink", "lavenderblush", "chocolate", "saddlebrown", "aliceblue", "sandybrown", "peachpuff", "palevioletred", "crimson", "dodgerblue", "lightslategray", "lightslategrey"]

def isComplete(g):
    degrees = dict(g.degree).values()
    for i in degrees:
        if i == g.number_of_nodes() - 1:
            continue
        else:
            return False
    return True

def mex(s):
    m = 0
    while m in s:
        m += 1
    return m

def color(g, constraints):
    maxdegree = max(dict(g.degree).values())
    lists = list(random.sample(colors, maxdegree))
    blacklisted = set()

    if isComplete(g):
        lists = list(random.sample(colors, g.number_of_nodes()))
        color = 0
        for i in (g.nodes()):
            g.nodes[i]['color'] = lists[color]
            color += 1
        return

    if len(list(g.nodes)) == 0:
        return

    colorx = [i for i in range(maxdegree)]
    for i in list(g.nodes):
        x = g.adj[i]
        k = []
        for j in x:
            if g.nodes[j]['color'] is not None:
                k.append(g.nodes[j]['color'])
        if len(k) == 0:
            g.nodes[i]['color'] = colorx[0]
        else:
            available_colors = set(colorx) - set(k)
            for constraint in constraints:
                if i == constraint[0] and g.nodes[constraint[1]]['color'] in available_colors:
                    available_colors.remove(g.nodes[constraint[1]]['color'])
                elif i == constraint[1] and g.nodes[constraint[0]]['color'] in available_colors:
                    available_colors.remove(g.nodes[constraint[0]]['color'])
            g.nodes[i]['color'] = min(available_colors) if available_colors else mex(set(k))

def distinctColors(g):
    colors = set()
    for i in g.nodes():
        colors.add(g.nodes[i]['color'])
    return len(colors)

G = nx.Graph()

vertices_list = [(i, {"color": None}) for i in range(10)]
random_list = []
i = 0
constraint = []

number_of_constraints = int(input("Enter the number of constraints: "))
for i in range(number_of_constraints):
    my_tuple = tuple(input('Enter space-separated words: ').split())
    my_tuple = list(my_tuple)
    my_tuple[0] = list(d.values()).index(my_tuple[0])
    my_tuple[1] = list(d.values()).index(my_tuple[1])
    mytuple = tuple(my_tuple)
    constraint.append(mytuple)
    random_list.append(mytuple)

while i < 10:
    X = np.random.randint(0, len(vertices_list), size=2)
    Tuple_1 = tuple(X)
    Tuple_2 = (Tuple_1[1], Tuple_1[0])
    if Tuple_1[0] == Tuple_1[1] or Tuple_1 in random_list or Tuple_2 in random_list or Tuple_1 in constraint:
        continue
    else:
        i += 1
        random_list.append(Tuple_1)

G.add_nodes_from(vertices_list)
G.add_edges_from(random_list)

color(G, constraint)
print("\nNumber of slots required to conduct the contest:", distinctColors(G))

colors_nodes = [colors[data['color']] for v, data in G.nodes(data=True)]
colors_number = [data['color'] for v, data in G.nodes(data=True)]

nx.draw(G, node_color=colors_nodes, with_labels=True)

print("\n")
for i in range(distinctColors(G)):
    print("\n\nSlot ", i + 1, ":- \n")
    for j in range(len(colors_number)):
        if colors_number[j] == i:
            print(sites[j])

#import sys.argv
import argparse
import random
#import collections.deque

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type = int, default = None, help='Τιμή σπόρου αλλιώς τυχαία')
    parser.add_argument('graph', type = str, help='Αρχειο που περιέχει το γράφο')
    parser.add_argument('k', type=int, help='Ο αριθμός των κόμβων που θέλουμε να επιλέξουμε ως σπόρους')
    parser.add_argument('method', choices=['greedy', 'max_degree'], help='Μέθοδος που θα εκτελείται')
    parser.add_argument('probability', type=float, help='Η πιθανότητα μετάβασης σε κάποιον κόμβο')
    parser.add_argument('mc', type=int, help='O αριθμός επαναλήψεων στη μέθοδο Monte Carlo')
    return parser.parse_args()
    
def read_graph(graph):
    g = {}
    with open(graph) as graph_input:
        for line in graph_input:
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
                continue
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            g[nodes[0]].append(nodes[1])
            
    return g

vargs = args()
graph = read_graph(vargs.graph)
r = vargs.r
if r is not None:
    random.seed(r)
k = vargs.k
method = vargs.method
probability = vargs.probability
mc = vargs.mc

'''
def monte_carlo(G, S, p, mc):
    𝑘 = 0
    nc = 0
    infl = [0] * len(S)
    for i in range(mc):
        for node in S:
            if random.random() < p:
                𝑘 += 1
                break
        else:
            nc += 1
    return 𝑘, nc
'''
def monte_carlo(G, S, p, mc):
    infl = [0] * len(S)
    for i in range(mc):
        for idx, seed in enumerate(S):
            active = {seed}
            new_active = {seed}
            influence = 0
            while new_active:
                next_active = set()
                for node in new_active:
                    for neighbor in G.get(node, []):
                        if neighbor not in active and random.random() < p:
                            next_active.add(neighbor)
                            active.add(neighbor)
                influence += len(new_active)
                new_active = next_active
            infl[idx] += influence
    infl = [round(influence / (mc), 3) for influence in infl]
    for i in range(1, len(infl)):
        infl[i] = round(infl[i] + infl[i-1], 3)
    return infl

def MaximizeInfluence(G, p, k):
    S = []
    for i in range(k):
        s = SelectSeed(G, S, p, k)
        S.append(s)
    return S


def SelectSeed(G, S, p, k):
    if method == 'max_degree':
        max_degree = -1
        max_node = None
        for node in G:
            if node not in S:
                degree = len(G[node])
                if degree > max_degree:
                    max_degree = degree
                    max_node = node
                elif degree == max_degree:
                    max_node = min(max_node, node)
        return max_node
    elif method == 'greedy':
        best_increase = -1
        best_node = None
        for node in G:
            if node not in S:
                temp_S = S + [node]
                infl = monte_carlo(G, temp_S, p, 1000)
                increase = infl[-1]
                if increase > best_increase:
                    best_increase = increase
                    best_node = node
        return best_node


seeds = MaximizeInfluence(graph, probability, k)
total = monte_carlo(graph, seeds, probability, mc)
average_influence = [infl / (mc) for infl in total]

# Εμφάνιση αποτελεσμάτων
print("Seeds:", seeds)
print("Influences", total)

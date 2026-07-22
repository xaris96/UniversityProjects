import argparse
import math
from collections import deque

MAX_INT = float('inf')

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type= float, default = 2.0, help = 'int or double')
    parser.add_argument('-g', type= float, default= 1.0, help = 'int or double')
    parser.add_argument('-d', action= 'store_true', help= ' Διαγνωστικά')
    parser.add_argument('algorithm', choices=['viterbi', 'trellis'], help= 'Επιλογή αλγορίθμου')
    parser.add_argument('offsets_file', type=str, help='Αρχειο που περιεχει τα δεδομενα')
    return parser.parse_args()

def read_offsets(offset):
    with open(offset, 'r') as file:
        f = file.read()
        numbers = f.split()
        numbers = [float(num) for num in numbers]
        return numbers

vargs = args()
offset = read_offsets(vargs.offsets_file)
GAMMA = vargs.g
d = vargs.d
S = vargs.s

# Σε περιπτωση που δεν ειναι σωστα
offset.sort()

# Δημιουργω τα Χ1, Χ2, ..., Χν
dist = []
for i in range(len(offset) - 1):
    disti = offset[i+1] - offset[i]
    dist.append(disti)
T = offset[-1] - offset[0]

def conditions(S, dist, T):
    x = 1 / min(dist)
    k = 1 + math.log(T, S) + math.log(x, S)
    return k

# Καλω την συναρτηση που θα περιγραψει το συστημα με καταστασεις
z = conditions(S, dist, T)
k = math.ceil(z)
n = len(dist)
g = T / n

L = [S**i / g for i in range(k)]


# Μεσος χρονος εκπομπης
Average = [L[0] ** -1]
for i in range(1, k):
    Average.append(Average[i-1] * (1/S))


# Χωριζω τα x σε καταστασεις
Xt = [[] for _ in range(k)]
for i in range(n):
    closest_index = min(range(k), key=lambda j: abs(dist[i] - Average[j]))
    Xt[closest_index].append(dist[i])


# Συνάρτηση πυκνότητας πιθανότητας
def f(t, j):
    x = dist[t]
    value = L[j] * math.exp(-L[j] * x)
    
    return max(value, 1e-10)

# Κόστος μετάβασης
def cost(i, j):
    if j > i:
        return GAMMA * (j - i) * math.log(n)
    else:
        return 0

# Ελάχιστο κόστος μιας ακολουθίας
def C(t, j, Cgrid):
    if t <= 0:
        return 0 if j == 0 else MAX_INT
    if Cgrid[t][j] != MAX_INT:
        return Cgrid[t][j]
    
    min_cost = MAX_INT
    for i in range(k):
        transition_cost = cost(i, j)
        current_cost = C(t - 1, i, Cgrid) + transition_cost
        min_cost = min(min_cost, current_cost)
    Cgrid[t][j] = -math.log(f(t - 1, j)) + min_cost
    return Cgrid[t][j]

def viterbi(d=False):
    point = 0
    Cgrid = [[MAX_INT] * k for _ in range(n + 1)]
    Cgrid[0][0] = 0
    P = [[0] * (n + 1) for _ in range(k)]
    # Υπολογισμός του κόστους και του μονοπατιού για κάθε χρονικό βήμα
    for t in range(1, n + 1):
        for s in range(k):
            min_cost = MAX_INT
            min_state = 0
            for i in range(k):
                c = C(t - 1, i, Cgrid) + cost(i, s)
                if c < min_cost:
                    min_cost = c
                    min_state = i
            Cgrid[t][s] = -math.log(f(t - 1, s)) + min_cost
            P[s][t] = min_state
        
    
    # Διαγνωστικά μηνύματα
        if d:
            if point == 0:
                print("[" + ", ".join("{:.0f}".format(x) for x in Cgrid[0]) + "]")
                point += 1
            print("[" + ", ".join("{:.2f}".format(x) for x in Cgrid[t]) + "]")
    # Εύρεση της βέλτιστης κατάστασης για το τελευταίο μήνυμα
    min_final_cost = min((Cgrid[n][j], j) for j in range(k))
    final_state = min_final_cost[1]
    
    # Φτιαχνω την ακολουθια (path)
    path = [final_state]
    for t in range(n, 0, -1):
        path.append(P[path[-1]][t])
    path.reverse()
    if d:
        print(len(path), path)
    return path

def create_graph():
    nodes = []
    edges = {}
    for t in range(n + 1):
        for i in range(k):
            nodes.append((t, i))
            if t < n:
                edges[(t, i)] = [((t + 1, j), -math.log(f(t, j)) + cost(i, j)) for j in range(k)]
            else:
                edges[(t, i)] = []  # Προσθέτω μια κενή λίστα για να αποφύγουμε το KeyError
                
    return nodes, edges

def bellman_ford(d = False):
    nodes, edges = create_graph()
    dists = {node: MAX_INT for node in nodes}
    preds = {node: None for node in nodes}
    dists[(0, 0)] = 0
    relaxations = []
    for _ in range(n):
        for node in nodes:
            for next_node, edge_cost in edges[node]:
                transition_cost = cost(node[1], next_node[1])
                emission_cost = -math.log(f(node[0], next_node[1]))
                
                if dists[node] + edge_cost < dists[next_node]:
                    if d:
                        relaxation_info = (f"({next_node[0]}, {next_node[1]}) {dists[next_node]:.2f} -> {dists[node] + edge_cost:.2f} "f"from ({node[0]}, {node[1]}) {dists[node]:.2f} + {transition_cost:.2f} + {emission_cost:.2f}")
                        relaxations.append(relaxation_info)
                    dists[next_node] = dists[node] + edge_cost
                    preds[next_node] = node
    if d:
        for relaxation in relaxations:
            print(relaxation)
    final_costs = [(dists[(n, j)], j) for j in range(k)]
    final_costs.sort()
    best_state = final_costs[0][1]
    path = []
    current_node = (n, best_state)
    while current_node is not None:
        path.append(current_node[1])
        current_node = preds[current_node]
    path.reverse()
    if d:
        print(len(path), path)
    return path

# Εκτύπωση αποτελεσμάτων
if vargs.algorithm == 'viterbi':
    z = viterbi(d)
elif vargs.algorithm == 'trellis':
    z = bellman_ford(d)


def merge_cells(z, offset):
    # Αρχικοποιούμε νέους πίνακες για τα συγχωνευμένα αποτελέσματα
    merged_z = []
    merged_start_offset = []
    merged_end_offset = []
    
    # Ξεκινάμε με την πρώτη τιμή και απόσταση
    current_value = z[0]
    start_offset = offset[0]
    
    for i in range(1, len(z)):
        if z[i] != current_value:
            # Αν η τρέχουσα τιμή είναι διαφορετική, αποθηκεύουμε τα δεδομένα
            merged_z.append(current_value)
            merged_start_offset.append(start_offset)
            merged_end_offset.append(offset[i - 1])
            
            # Ενημερώνουμε το current_value και start_offset με τις νέες τιμές
            current_value = z[i]
            start_offset = offset[i - 1]
    
    # Προσθέτουμε την τελευταία συσσωρευμένη τιμή και απόσταση
    merged_z.append(current_value)
    merged_start_offset.append(start_offset)
    merged_end_offset.append(offset[-1])
    
    return merged_z, merged_start_offset, merged_end_offset

merged_z, merged_start_offset, merged_end_offset = merge_cells(z, offset)

# Τελική εκτύπωση ιδια με το παράδειγμα
for i in range(len(merged_z)):
    if i < len(merged_z) - 1:
        print(f"{merged_z[i]} [{merged_start_offset[i]} {merged_start_offset[i + 1]})")
    else:
        print(f"{merged_z[i]} [{merged_start_offset[i]} {merged_end_offset[i]})")

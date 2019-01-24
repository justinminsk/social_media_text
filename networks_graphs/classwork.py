import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# n!/k!(n - k)! = number of sets in a list where n is number of entries and k is size of set
# ie [0, 1, 2, 3, 4, 5] and you want sets of 2 
# 6!/2!(6 - 2)! = number of sets

# G.add_node("v1")
# print(G.number_of_nodes())

# G.add_nodes_from({"v1", "v2"})
# G.add_edge("v1", "v2")
# nx.draw(G, with_labels=True)
# print(nx.info(G))
# plt.show()

# G.add_nodes_from([1, 2, 3, 4, 5])
# G.add_edges_from([(1, 2), (1, 3), (2, 4)])
# nx.draw(G, with_labels=True)
# print(nx.has_path(G, 3, 5))
# plt.show()



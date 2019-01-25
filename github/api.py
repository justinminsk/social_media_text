import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
from github import Github


ACCESS_TOKEN = ''

USER = 'ptwobrussell'
REPO = 'Mining-the-Social-Web-2nd-Edition'

print("--Start--")

client = Github(ACCESS_TOKEN, per_page=100)
user = client.get_user(USER)
repo = user.get_repo(REPO)

# Comment out this to avoid ratelimit

stargazers = [ s for s in repo.get_stargazers() ]

print("Stargazers Added to List")

g = nx.DiGraph()

g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)

for sg in stargazers:
    g.add_node(sg.login + '(user)', type='user')
    g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')

print("Graph made")

# To Here
# Comment out write if file is made and uncomment read
nx.write_edgelist(g, "github1.edgelist")
# g=nx.read_edgelist("github1.edgelist")

print("Graph Read or Written Out")

print()
print("Question 1:")
print("Nodes:", len(g.nodes()))
print("Edges:", len(g.edges()))
print()

# Comment out this to avoid ratelimit

for i, sg in enumerate(stargazers):
    for follower in sg.get_followers():
                if follower.login + '(user)' in g:
                    g.add_edge(follower.login + '(user)', sg.login + '(user)', 
                            type='follows')

print("Followers Connections Made")

# To Here 
# Comment out write if file is made and uncomment read
nx.write_edgelist(g, "github2.edgelist")
# g=nx.read_edgelist("github2.edgelist")

print("Full Graph Written or Read")

print()
print("Question 2:")
print("Nodes:", len(g.nodes()))
print("Edges:", len(g.edges()))
print()

h = g.copy()

h.remove_node('Mining-the-Social-Web-2nd-Edition(repo)')
# Comment out write if file is made and uncomment read
nx.write_edgelist(h, "followers.edgelist")
# h=nx.read_edgelist("followers.edgelist")

print("Follower Only List Read or Written")
print()

dc = sorted(nx.degree_centrality(h).items(), 
            key=itemgetter(1), reverse=True)

print("Question 3:")
print("Degree Centrality")
print(dc[:10])
print()

bc = sorted(nx.betweenness_centrality(h).items(), 
            key=itemgetter(1), reverse=True)

print("Betweenness Centrality")
print(bc[:10])
print()

print("Closeness Centrality")
cc = sorted(nx.closeness_centrality(h).items(), 
            key=itemgetter(1), reverse=True)
print(cc[:10])

print()

print("--End--")

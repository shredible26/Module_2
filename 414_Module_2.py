import pandas as pd
import networkx as nx
import re

df = pd.read_csv('reddit_comments.csv')

# Remove deleted / removed authors
df = df[~df['author'].isin(['[deleted]', '[removed]'])]

# Filter out bot accounts matching 'bot', 'auto', and 'moderator'
bot_pattern = re.compile(r'(bot|auto|moderator)', re.IGNORECASE)
df = df[~df['author'].str.contains(bot_pattern)]

# Create directed edges between parent commenters and child commenters
id_to_author = dict(zip(df['id'], df['author']))

edges = []
for _, row in df.iterrows():
    parent_id = row['parent_id'].replace('t1_', '')  # remove the Reddit prefix
    if parent_id in id_to_author:
        source = id_to_author[parent_id]
        target = row['author']
        edges.append((source, target))

# Create the directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Analysis + Centrality metrics

# Degree centrality
in_deg_counts = dict(G.in_degree())

# PageRank
pagerank_scores = nx.pagerank(G, alpha=0.85)

# Betweenness centrality
betweenness_scores = nx.betweenness_centrality(G, normalized=True)

# Top users and values for each metric
def top_item(score_dict):
    user = max(score_dict, key=score_dict.get)
    return user, score_dict[user]

top_in_user, top_in_val = top_item(in_deg_counts)
top_pr_user, top_pr_val = top_item(pagerank_scores)
top_bw_user, top_bw_val = top_item(betweenness_scores)

# Results in table display
results = pd.DataFrame({
    "Metric": ["In‑Degree Centrality", "PageRank", "Betweenness"],
    "Top User": [top_in_user, top_pr_user, top_bw_user],
    "Value": [top_in_val, round(top_pr_val, 5), round(top_bw_val, 5)]
})

print(results.to_string(index=False))
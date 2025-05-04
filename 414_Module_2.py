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
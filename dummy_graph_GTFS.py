#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import pandas as pd
import numpy as np
from geopy.distance import distance
from tqdm.notebook import tqdm
from multiprocessing import Pool


# In[ ]:


def get_trip(rt):
    df = stop_times[stop_times.trip_id == trips[trips.route_id == rt].trip_id.values[0]]
    df['trip_id'] = rt
    return df.values


# In[ ]:


stops = pd.read_csv('stops.txt')
routes = pd.read_csv('routes.txt')
stop_times = pd.read_csv('stop_times.txt')
trips = pd.read_csv('trips.txt')


# In[ ]:


stop_times_st = []
with Pool() as p:
    r = list(tqdm(p.imap(get_trip, routes.route_id), total = len(routes)))
t = list(itertools.chain.from_iterable(r))
stop_times_st = pd.DataFrame(t, columns = stop_times.columns)


# In[22]:


G = nx.DiGraph()


# In[23]:


for i in tqdm(range(1, len(stop_times)), total = len(stop_times)):
    s1, s2 = stop_times.loc[i-1, 'stop_id'], stop_times.loc[i, 'stop_id']
#     print(s1, s2)
    d = distance(stops[stops.stop_id == s1][['stop_lat', 'stop_lon']].values                 , stops[stops.stop_id == s2][['stop_lat', 'stop_lon']].values).km
    G.add_edges_from([(s1,s2,{'distance':d})])


# In[ ]:


nx.write_gpickle('bus_graph.pkl')


import numpy as np
import math
import networkx as nx
from geopy.distance import distance
def find_buses_within_radius(query_coords, df, radius):
    # radius in kilometers
    """
    given the query coordinates, realtime data df and radius (in km), the function returns the dataframe of vehicles
    within radius of the queried coordinates
    :param query_coords: tuple of lat, long
    :param df: stops data dataframe
    :param radius: distance threshold in km
    :return: dataframe of stops records within radius of given query coords
    """
    q_lat = query_coords[0]
    q_lng = query_coords[1]

    vehicle_lats = df['stop_lat'].values.astype(float)
    vehicle_lngs = df['stop_lon'].values.astype(float)

    stst = 6367 * 2 * np.arcsin(np.sqrt(
        np.sin((np.radians(vehicle_lats) - math.radians(q_lat)) / 2) ** 2 + math.cos(
            math.radians(q_lat)) * np.cos(np.radians(vehicle_lats)) * np.sin(
            (np.radians(vehicle_lngs) - math.radians(q_lng)) / 2) ** 2))
    bus_record_indices_within_radius = np.where(stst <= radius)[0]
    return df.iloc[bus_record_indices_within_radius]

def bus_distance(loc1, loc2):
    init_dist = 0.3
    test = True
    while(test):
        n_src = find_buses_within_radius(loc1, bus_stops, init_dist)
        n_dest = find_buses_within_radius(loc2, bus_stops, init_dist)
        flag = 0
        for idx, val_src in n_src.iterrows():
            for idy, val_dest in n_dest.iterrows():
                try:
                    dist = nx.shortest_path_length(G, val_src['stop_id'], val_dest['stop_id'], weight = 'distance')
                    path_seq = nx.shortest_path(G, val_src['stop_id'], val_dest['stop_id'], weight='distance')
                    src_dist = distance(loc1, [val_src['stop_lat'], val_src['stop_lon']]).km
                    dest_dist = distance(loc2, [val_dest['stop_lat'], val_dest['stop_lon']]).km
                    test = False
                    flag = 1
                except:
                    continue
                if flag == 1:
                    break
            if flag == 1:
                break
    return src_dist + dist + dest_dist


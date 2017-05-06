#
# geogrouper.py
#

import re, string
from utils import scientific_match_ratio, sanitize_sample_descriptions
from itertools import combinations
from python_mcl.mcl.mcl_clustering import mcl
from acronyms import get_acronyms, get_keywords, get_acronyms
import numpy as np


MCL_INFLATE_FACTOR = 7      # This is a high constant because MCL deals with a fully-connected graph
MIN_MCL_INFLATE_FACTOR = 1  # This is the lowest value the MCL inflate factor is allowed to go to
MCL_MAX_LOOP = 100          # MCL Max Loop

def cluster_descriptions(data_description_text_list, abstract_text, data_description_ids=None):
    """
    Clusters the descriptions of the samples corresponding to a particular abstract based on the
    acronyms corresponding to them.

    :param: abstract_text - The text in the abstract
    :param: data_description_text_list - A list of descriptions for each sample
    :param: data_description_ids - A list of ids for each of the sample, corresponding in index to
                                   the elements of data_description_text_list. If not specified,
                                   the function uses data_description_text_list as the
                                   data_description_ids
    :return: a dictionary mapping a tuple (the acronym category) to lists of sample description text
    """

    if data_description_ids == None:
        data_description_ids = data_description_text_list

    filtered_data_desc_text_list = sanitize_sample_descriptions(data_description_text_list)
    keywords = get_acronyms(abstract_text, filtered_data_desc_text_list)

    # Calculate and store all pairwise edit distances
    match_ratio_dict = {}
    for desc1, desc2 in combinations(data_description_text_list, 2):
        match_ratio = scientific_match_ratio(desc1, desc2, keywords)
        key = tuple(sorted([desc1, desc2]))
        match_ratio_dict[key] = match_ratio

    # Matrixify the data
    mtx = []
    for i, desc1 in enumerate(data_description_text_list):
        mtx.append([])
        for j, desc2 in enumerate(data_description_text_list):
            if i != j:
                key = tuple(sorted([desc1, desc2]))
                mtx[i].append(match_ratio_dict[key])
            else:
                mtx[i].append(0.0)

    mtx = np.array(mtx)

    # Execute MCL clustering
    inflate_factor = MCL_INFLATE_FACTOR
    num_clust = len(data_description_text_list)
    while num_clust == len(data_description_text_list) and inflate_factor >= MIN_MCL_INFLATE_FACTOR:
        M, clusters = mcl(mtx, inflate_factor=inflate_factor, max_loop=MCL_MAX_LOOP)
        num_clust = len(clusters)
        inflate_factor -= 1

    # Label all the clusters
    labeled_clusters = set()
    for cluster, description_indices in clusters.items():
        current_cluster = []
        for desc_index in description_indices:
            current_cluster.append(data_description_ids[desc_index])
        labeled_clusters.add(tuple(current_cluster))

    return labeled_clusters, mtx
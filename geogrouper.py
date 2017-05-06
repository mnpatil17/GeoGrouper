#
# geogrouper.py
#

import pandas as pd
import re, string
from geo_io import get_all_series_ids, get_all_sample_titles_for_series, get_abstract_for_series
from utils import scientific_match_ratio, sanitize_sample_descriptions
from itertools import combinations
from python_mcl.mcl.mcl_clustering import mcl
from keywords import get_acronyms, get_common_words
import numpy as np


MCL_INFLATE_FACTOR = 7      # This is a high constant because MCL deals with a fully-connected graph
MIN_MCL_INFLATE_FACTOR = 1  # This is the lowest value the MCL inflate factor is allowed to go to
MCL_MAX_LOOP = 100          # MCL Max Loop


def cluster_descriptions_from_file(datafile, should_print_output=False, print_series_sample_size=0):
    """
    The primary method of this package, which takes in a datafile and outputs the clustered
    descriptions in a dictionary format.

    :param: datafile - The path to the file that contains the pandas-readable data
    :param: should_print_output - [Optional] True if output should be printed immediately after
                                  calculation, False otherwises
    :param: print_series_sample_size - The least number of samples a series must have to be printed.
                                       For example, if print_series_sample_size is 5, then only
                                       series with 5 or more samples will be printed

    Returns a dictionary mapping a series_id to its final cluster
    """

    table = pd.read_table(datafile, index_col=0, low_memory=False)
    all_series_ids = get_all_series_ids(table)

    final_clusters_list = []
    for series_id in all_series_ids:
        sample_ids, all_sample_titles = get_all_sample_titles_for_series(table, series_id)
        sample_abstract = get_abstract_for_series(table, series_id)
        final_clusters = cluster_descriptions(all_sample_titles, sample_abstract)[0]
        final_clusters_list.append(final_clusters)

        # For printing purposes only
        if should_print_output and len(all_sample_titles) >= print_series_sample_size:
            print '-------------------------------------------------------------------------\n'
            print 'SERIES: {0}'.format(series_id)
            for cluster in final_clusters:
                print cluster

    return dict(zip(all_series_ids, final_clusters_list))



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


if __name__ == '__main__':
    print cluster_descriptions_from_file('../all_meta.txt', should_print_output=True,
                                         print_series_sample_size=5)

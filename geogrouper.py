#
# geogrouper.py
#

import re, string
from utils import is_majority_uppercase, string_edit_dist, string_match_ratio, word_count, remove_numbers, scientific_match_ratio
from collections import defaultdict
from itertools import combinations
from python_mcl.mcl.mcl_clustering import mcl
from acronyms import get_acronyms, get_keywords, get_numberless_acronyms
import numpy as np


MCL_INFLATE_FACTOR = 7   # This is a high constant because MCL deals with a fully-connected graph
MCL_MAX_LOOP = 100       # MCL Max Loop

## TODO: handle the case where one acronym is a substring of another acronym! (i.e. mRNA and RNA)
def cluster_descriptions(data_description_text_list, abstract_text, data_description_ids=None):
    """
    Clusters the descriptions of the samples corresponding to a particular abstract based on the
    acronyms corresponding to them.

    :param: abstract_text - The text in the abstract
    :param: data_description_text_list - A list of descriptions for each sample
    :return: a dictionary mapping a tuple (the acronym category) to lists of sample description text
    """

    # TODO: use the keywords
    # TODO: ignore the numbers
    # TODO: keyword weighted distance
    # TODO: do it many times at different MCL_INFLATE_FACTOR values. If something has more than
    #       25% of the number of text, then it should be eliminated


    if data_description_ids == None:
        data_description_ids = data_description_text_list


    # Filters in the following way:
    # 1. Removes numbers
    # 2. Converts '_' to ' '
    # 3. Strips leading and trailing spaces
    filtered_data_desc_text_list = []
    for text in data_description_text_list:
        filtered_data_desc_text_list.append(remove_numbers(text).replace('_', ' ').strip())

    keywords = get_numberless_acronyms(abstract_text, filtered_data_desc_text_list)
    # keywords = get_keywords(data_description_text_list)
    print "KEYWORDS: ", keywords

    # Calculate and store all pairwise edit distances
    match_ratio_dict = {}
    for desc1, desc2 in combinations(data_description_text_list, 2):

        # use acronyms for now
        # desc1_numberless = remove_numbers(desc1)
        # desc2_numberless = remove_numbers(desc2)
        # match_ratio = string_match_ratio(desc1_numberless, desc2_numberless)

        match_ratio = scientific_match_ratio(desc1, desc2, keywords)
        # print "Match Ratio: {0} and {1} is {2}".format(desc1, desc2, match_ratio)


        # if desc1 == 'KUa113' and desc2 == 'KUa164':
        #     print "MATCH: ", match_ratio
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

    # print mtx

    ## DEBUG
    # print '\n\n-- MATRIX --\n', mtx

    # Execute MCL clustering
    inflate_factor = MCL_INFLATE_FACTOR
    num_clusters = len(data_description_text_list)
    while num_clusters == len(data_description_text_list) or inflate_factor == 1:
        M, clusters = mcl(mtx, inflate_factor=inflate_factor, max_loop=MCL_MAX_LOOP)
        num_clusters = len(clusters)
        inflate_factor -= 1


    ## DEBUG
    # print '\n\n-- FINAL MATRIX --\n', M
    # print '\n\n-- CLUSTERS --\n', clusters

    # Label all the clusters
    labeled_clusters = set()
    for cluster, description_indices in clusters.items():
        current_cluster = []
        for desc_index in description_indices:
            current_cluster.append(data_description_ids[desc_index])
        labeled_clusters.add(tuple(current_cluster))

    return labeled_clusters, mtx


    ## ORIGINAL IMPLEMENTATION
def cluster_groups(abstract_text, data_description_text_list):
    final_acronyms = get_acronyms(abstract_text, data_description_text_list)
    final_clusters = dict(group_descriptions_by_acronyms(final_acronyms, data_description_text_list))
    return final_clusters.values()


def group_descriptions_by_acronyms(acronyms, data_description_text_list):
    """
    Given the acronyms, groups the sample descriptions based on them.

    :param: acronyms - A set of acronyms (strings)
    :param: data_description_text_list - A list of descriptions for each sample
    :return: a dictionary mapping a tuple (the acronym category) to lists of sample description text
    """

    # split on camel case, split on

    desc_dict = {}
    for desc_text in data_description_text_list:
        filtered_desc_text = desc_text.replace('_', ' ')
        acronyms_found_set = set()
        for acronym in acronyms:
            if acronym in filtered_desc_text:
                acronyms_found_set.add(acronym)

        if len(acronyms_found_set) == 0:
            desc_dict[desc_text] = tuple()
        else:
            desc_dict[desc_text] = tuple(sorted(acronyms_found_set))

    category_dict = defaultdict(list)
    all_categories = desc_dict.values()
    for desc_text, category in desc_dict.items():
        category_dict[category].append(desc_text)


    return category_dict


#
# For debugging
#
if __name__ == '__main__':

    # TODO: might have to edit-distance cluster within acronym groupings to allow for cases like
    #       DNA and RNA having only an edit distance of 1, even tho they're different

    # TODO: need to adjust MCL_INFLATE_FACTOR based on the variance of the matches

    # abs_text = 'this is some (abstract) text that I have written. Here is tRNA an acronym' + \
    #            '(NASA) and N.A.S.A.'
    desc1 = 'DEN_2_HC'
    desc2 = 'DEN_5_HC'
    desc3 = 'DEN_7_HC'
    desc4 = 'RNA_2_HC'
    desc5 = 'RNA_5_HC'
    desc6 = 'RNA_7_HC'
    desc_list = [desc1, desc2, desc3, desc4, desc5, desc6]
    desc_ids = ['desc1', 'desc2', 'desc3', 'desc4', 'desc5', 'desc6']
    cluster_descriptions(desc_ids, desc_list)

    # potential_acronyms = get_potential_acronyms(abs_text)
    # final_acronyms = get_valid_acronyms(potential_acronyms, desc_list)
    # print 'Potential acronyms: {0}'.format(potential_acronyms)
    # print 'Final acronyms: {0}'.format(final_acronyms)
    # print 'Final grouping: {0}', group_descriptions_by_acronyms(final_acronyms, desc_list)


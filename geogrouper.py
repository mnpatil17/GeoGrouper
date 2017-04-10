#
# geogrouper.py
#

import re, string
from utils import is_majority_uppercase, string_edit_dist, string_match_ratio
from collections import defaultdict
from itertools import combinations
from python_mcl.mcl.mcl_clustering import mcl
import numpy as np


MAX_ACRONYM_LENGTH = 2

## TODO: handle the case where one acronym is a substring of another acronym! (i.e. mRNA and RNA)
def cluster_descriptions(data_description_ids, data_description_text_list):
    """
    Clusters the descriptions of the samples corresponding to a particular abstract based on the
    acronyms corresponding to them.

    :param: abstract_text - The text in the abstract
    :param: data_description_text_list - A list of descriptions for each sample
    :return: a dictionary mapping a tuple (the acronym category) to lists of sample description text
    """


    # Calculate and store all pairwise edit distances
    match_ratio_dict = {}
    for desc1, desc2 in combinations(data_description_text_list, 2):
        match_ratio = string_match_ratio(desc1, desc2)
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
    print '\n\n-- MATRIX --\n', mtx


    ## NOTICE
    ## You're going to need a high inflation constant! This is because you have a fully connected
    ## graph and you don't want to have that stuff go down.

    # Execute MCL clustering
    M, clusters = mcl(mtx, inflate_factor = 3, max_loop = 100)

    print '\n\n-- FINAL MATRIX --\n', M
    print '\n\n-- CLUSTERS --\n', clusters

    ## ORIGINAL IMPLEMENTATION
    # potential_acronyms = get_potential_acronyms(abstract_text)
    # final_acronyms = get_valid_acronyms(potential_acronyms, data_description_text_list)
    # return dict(group_descriptions_by_acronyms(final_acronyms, data_description_text_list))


def get_potential_acronyms(abstract_text):
    """
    This function returns a list of all the acronyms from the text of the abstract paragraph.

    A 'potential acronym' is defined as a majority uppercase string of length at least
    MAX_ACRONYM_LENGTH

    :param: abstract_text - The text of the abstract
    :return: a set of potential acronyms
    """

    all_abstract_text_words = re.sub('\(|\)', '', abstract_text).split(' ')
    all_paren_strings = re.findall('(?<=\()[^\(\)]*(?=\))', abstract_text) # does not include parens

    # To qualify as a potential acronym, we say that the string has to be majority uppercase
    all_potential_acronyms = set()
    for text in all_paren_strings:
        if is_majority_uppercase(text):
            all_potential_acronyms.add(text)

    # deal with the rest of the words
    for word in all_abstract_text_words:
        striped_word = word.strip(string.punctuation)
        if len(striped_word) > MAX_ACRONYM_LENGTH and is_majority_uppercase(striped_word):
            all_potential_acronyms.add(striped_word)

    return all_potential_acronyms


def get_valid_acronyms(potential_acronyms, data_description_text_list):
    """
    :param: potential_acronyms - A list of potential acronyms (strings)
    :param: data_description_text_list - A list of descriptions for each sample

    :return: a set of valid acronyms
    """
    acronyms_found = set()

    for desc_text in data_description_text_list:
        for acronym in potential_acronyms:
            if acronym.lower() in desc_text.lower():
                acronyms_found.add(acronym)

        if len(acronyms_found) == len(potential_acronyms):
            return acronyms_found

    return acronyms_found


def group_descriptions_by_acronyms(acronyms, data_description_text_list):
    """
    Given the acronyms, groups the sample descriptions based on them.

    :param: acronyms - A set of acronyms (strings)
    :param: data_description_text_list - A list of descriptions for each sample
    :return: a dictionary mapping a tuple (the acronym category) to lists of sample description text
    """
    desc_dict = {}
    for desc_text in data_description_text_list:
        acronyms_found_set = set()
        for acronym in acronyms:
            if acronym in desc_text:
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


###############
# keywords.py #
###############

####################################################################################################
# Programmer's Notes
#
# This file contains the logic to find keywords from GEO data. Currently there are two methods:
#
#  1. get_acronyms
#  2. get_common_words
#
# Please note that changing the way the main algorithm finds keywords will change the
# effectiveness of the algorithm. Therefore, to iterate on this algorithm, changing the way
# keywords are found is a great way to improve performance.
#
####################################################################################################

import re, string, operator
from utils import is_majority_uppercase, word_count, sanitize_sample_descriptions, sanitize_text

MIN_ACRONYM_LENGTH = 2   # The shortest an acronym can be

#
# Exposed Methods
#

def get_acronyms(abstract_text, data_description_text_list):
    """
    Given an abstract and a description list, this method finds all the relevant acronyms that are
    available in the description.
    """
    potential_acronyms = get_potential_acronyms(sanitize_text(abstract_text))
    return list(get_valid_acronyms(potential_acronyms, data_description_text_list))


def get_common_words(data_description_text_list):
    """
    Returns the common words among the text descriptions in the input list.
    """
    processed_description_text_list = sanitize_sample_descriptions(data_description_text_list)
    all_text = ' '.join(processed_description_text_list)
    counts = word_count(all_text)
    return [text for text, count in sorted(counts.items(), key=operator.itemgetter(1))[::-1]]


#
# Helper Methods
#

def get_potential_acronyms(abstract_text):
    """
    This function returns a list of all the acronyms from the text of the abstract paragraph.

    A 'potential acronym' is defined as a majority uppercase string of length at least
    MIN_ACRONYM_LENGTH

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

    # Deal with the rest of the words
    for word in all_abstract_text_words:
        striped_word = word.strip(string.punctuation)
        if len(striped_word) > MIN_ACRONYM_LENGTH and is_majority_uppercase(striped_word):
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
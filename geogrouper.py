import re, string
from utils import is_majority_uppercase
from collections import defaultdict

MAX_ACRONYM_LENGTH = 2

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
    desc_dict = {}
    for desc_text in data_description_text_list:
        acronyms_found_set = set()
        for acronym in acronyms:
            if acronym in desc_text:
                acronyms_found_set.add(acronym)

        desc_dict[desc_text] = tuple(sorted(acronyms_found_set))

    category_dict = defaultdict(list)
    all_categories = desc_dict.values()
    for desc_text, category in desc_dict.items():
        category_dict[category].append(desc_text)


    return category_dict


if __name__ == '__main__':

    # one test
    abs_text = 'this is some (abstract) text that I have written. Here is tRNA an acronym (NASA) and N.A.S.A.'
    desc1 = 'this is from N.A.S.A.'
    desc2 = 'this is tRNA'
    desc3 = 'this is tRNA and N.A.S.A. 1'
    desc4 = 'this is tRNA and N.A.S.A. 2'
    desc_list = [desc1, desc2, desc3, desc4]

    potential_acronyms = get_potential_acronyms(abs_text)
    final_acronyms = get_valid_acronyms(potential_acronyms, desc_list)
    print 'Potential acronyms: {0}'.format(potential_acronyms)
    print 'Final acronyms: {0}'.format(final_acronyms)
    print '\n'
    print group_descriptions_by_acronyms(final_acronyms, desc_list)


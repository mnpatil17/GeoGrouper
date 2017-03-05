import re, string
from utils import is_majority_uppercase

MAX_ACRONYM_LENGTH = 2

def get_potential_acronyms(abstract_text):
    """
    This function returns a list of all the acronyms from the text of the abstract paragraph.

    A 'potential acronym'

    :param: abstract_text - The text of the abstract
    """
    # TODO: what about common acronyms, like tRNA, or mRNA, that everyone knows? They probably won't be in parenthesis


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


# TODO: get out the descriptions, combinatorially classified.

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


if __name__ == '__main__':

    # one test
    abs_text = 'this is some (abstract) text that I have written. Here is tRNA an acronym (NASA) and N.A.S.A.'
    desc1 = 'this is from N.A.S.A.'
    desc2 = 'this is tRNA'
    desc_list = [desc1, desc2]

    potential_acronyms = get_potential_acronyms(abs_text)
    final_acronyms = get_valid_acronyms(potential_acronyms, desc_list)
    print 'Potential acronyms: {0}'.format(potential_acronyms)
    print 'Final acronyms: {0}'.format(final_acronyms)
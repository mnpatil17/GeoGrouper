# Step 1, get the words in paranthesis
import re

def get_potential_acronyms(abstract_text):
    """
    This function returns a list of all the acronyms from the text of the abstract paragraph.

    :param: abstract_text - The text of the abstract
    """
    # TODO: what about common acronyms, like tRNA, or mRNA, that everyone knows? They probably won't be in parenthesis


    all_paren_strings = re.findall('(?<=\()[^\(\)]*(?=\))', abstract_text)  # does not include parens

    # To qualify as a potential acronym, we say that the string has to be majority uppercase
    all_potential_acronyms = set()
    for text in all_paren_strings:
        num_uppercase = 0
        num_lowercase = 0
        for character in text:
            if is_uppercase(character):
                num_uppercase += 1
            elif is_lowercase(character):
                num_lowercase += 1

        if num_uppercase >= num_lowercase:
            all_potential_acronyms.add(text)

    return all_potential_acronyms


def is_uppercase(character):
    return 'A' <= character <= 'Z'

def is_lowercase(character):
    return 'a' <= character <= 'z'




def get_valid_acronyms(potential_acronyms, data_description_text_list):
    """
    :param: potential_acronyms - A list of potential acronyms (strings)
    :param: data_description_text_list - A list of descriptions for each sample

    :return: a set of valid acronyms
    """
    acronyms_found = set()

    for desc_text in data_description_text_list:
        for acronym in potential_acronyms:
            if acronym in desc_text:
                acronyms_found.add(acronym)

        if len(acronyms_found) == len(potential_acronyms):
            return acronyms_found

    return acronyms_found


if __name__ == '__main__':

    # one test
    abs_text = 'this is some (abstract) text that I have written. Here is an acronym (NASA) and (N.A.S.A.s) and (tRNA).'
    desc1 = 'this is from NASA'
    desc2 = 'this is tRNA'
    desc_list = [desc1, desc2]

    potential_acronyms = get_potential_acronyms(abs_text)
    final_acronyms = get_valid_acronyms(potential_acronyms, desc_list)
    print 'Potential acronyms: {0}'.format(potential_acronyms)
    print 'Final acronyms: {0}'.format(final_acronyms)
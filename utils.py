#
# Various utility functions
# utils.py
#

import edit_distance


def is_uppercase(character):
    """
    Checks if the given input character is an uppercase character
    """
    return 'A' <= character <= 'Z'


def is_lowercase(character):
    """
    Checks if the given input character is a lowercase character
    """
    return 'a' <= character <= 'z'


def is_majority_uppercase(text, tie_ok=False):
    """
    Checks if a piece of text (string) is majority uppercase. Non-letters are not considered
    uppercase or lowercase (i.e. they are left out of the math entirely).

    :param: text - The string to check for majority uppercase status
    :param: tie_ok - If true, allows for a non-strict majority (i.e. equal number of uppercase
                     and lowercase string). If false, requires a strict majority.
    :return: true if there is a majority (strict or non-strict, as defined by tie_ok). Else, false.
    """
    num_uppercase, num_lowercase = 0, 0
    for character in text:
        if is_uppercase(character):
            num_uppercase += 1
        elif is_lowercase(character):
            num_lowercase += 1

    return num_uppercase + int(tie_ok) > num_lowercase


def string_edit_dist(str1, str2):
    """
    The raw number of MISMATCHES
    """
    sm = edit_distance.SequenceMatcher(a=str1, b=str2)
    return sm.distance()

def string_match_ratio(str1, str2):
    """
    The ratio of MATCHES.
    """
    sm = edit_distance.SequenceMatcher(a=str1, b=str2)
    return sm.ratio()

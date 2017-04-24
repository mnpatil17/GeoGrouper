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

def string_num_matches(str1, str2):
    """
    The raw number of MISMATCHES
    """
    sm = edit_distance.SequenceMatcher(a=str1, b=str2)
    return sm.matches()


def string_match_ratio(str1, str2):
    """
    The ratio of MATCHES.
    """
    sm = edit_distance.SequenceMatcher(a=str1, b=str2)
    return sm.ratio()

def scientific_match_ratio(str1, str2, keywords):
    """
    Note the keywords may just be acronyms
    """

    # Get rid of the numbers
    str1_numberless = remove_numbers(str1)
    str2_numberless = remove_numbers(str2)

    str1_keywords, str1_remainder = get_keywords_in_description(str1_numberless, keywords)
    str2_keywords, str2_remainder = get_keywords_in_description(str2_numberless, keywords)

    remainder_dist = string_num_matches(str1_remainder, str2_remainder)
    common_keywords = str1_keywords.intersection(str2_keywords)

    common_keyword_total_len = 0
    for common_kword in common_keywords:
        common_keyword_total_len += len(common_kword)

    return (remainder_dist + common_keyword_total_len) * 1.0 / max(len(str1_numberless), len(str2_numberless))


def get_keywords_in_description(text, keywords):
    """
    """
    text_copy = str(text)
    text_keywords = set()

    if len(keywords) == 0:
        return set(), text_copy
    keywords.sort(key=len, reverse=True)

    for keyword in keywords:
        if keyword in text_copy:
            text_keywords.add(keyword)
            text_copy = text_copy.replace(keyword, '', 1).strip()

    return text_keywords, text_copy


def word_count(input_str):
    counts = dict()
    words = input_str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def remove_numbers(text):
    return ''.join([i for i in text if not i.isdigit()])

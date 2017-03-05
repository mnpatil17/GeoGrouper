#
# Various Utility Functions
#


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
    num_uppercase, num_lowercase = 0, 0
    for character in text:
        if is_uppercase(character):
            num_uppercase += 1
        elif is_lowercase(character):
            num_lowercase += 1

    return num_uppercase + int(tie_ok) > num_lowercase
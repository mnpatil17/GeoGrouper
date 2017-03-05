#
# Various utility functions for testing
# spec_utils.py
#

def sort_dictionary_list_values(dict_with_list_values):
    """
    Given a dictionary with lists for its values, it returns a new dictionary that is a copy of
    the input, except these lists are sorted.
    """

    dict_with_sorted_list_values = {}
    for key, lst_value in dict_with_list_values.items():
        dict_with_sorted_list_values[key] = sorted(lst_value)

    return dict_with_sorted_list_values
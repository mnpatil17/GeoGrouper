

def sort_dictionary_list_values(dict_with_list_values):

	dict_with_sorted_list_values = {}
	for key, lst_value in dict_with_list_values.items():
		dict_with_sorted_list_values[key] = sorted(lst_value)

	return dict_with_sorted_list_values
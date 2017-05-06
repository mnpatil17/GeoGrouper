import pandas as pd

#
# Code to read the table
#

def get_abstract_for_series(data_table, series_id):
    """
    Returns a rough version of an abstract for a series that's an amalgamation of all of its samples
    """
    abstract = ''
    for sample_id in get_all_samples_in_series(data_table, series_id):
        abstract += get_abstract_for_sample(data_table, sample_id) + ' '

    return abstract

def get_all_sample_titles_for_series(data_table, series_id):
    """
    Returns every single sample title corresponding to a particular series
    """
    titles = []
    sample_ids = get_all_samples_in_series(data_table, series_id)
    for sample_id in sample_ids:
        titles.append(get_title_for_sample(data_table, sample_id))

    return sample_ids, titles

def get_abstract_for_sample(data_table, sample_id):
    """
    Returns all the non-title data that corresponds to a particular sample
    """
    return ' '.join(str(x) for x in data_table[sample_id]).replace('nan', '').strip()

def get_all_samples_in_series(data_table, series_id):
    """
    Returns a list of all the samples corresponding to a series
    """
    return data_table.loc[:, data_table.loc['Series'] == series_id].columns

def get_title_for_sample(data_table, sample_id):
    """
    Returns the title for a given sample id
    """
    return data_table.loc['title', sample_id]

def get_all_series_ids(data_table):
    """
    Gets all the series in the table
    """
    return data_table.loc['Series'].unique()



import pandas as pd
from geogrouper import cluster_descriptions





# Example Data Manipulations

# table.loc['Treatment-Protocol', 'GSM1556206']
# table.loc[:, table.loc['Series'] == 'GSE23316'].columns
# table.loc['Series']   # gets you all the series


def get_abstract_for_series(data_table, series_id):
    """
    Get's a rough version of an abstract for a series that's an amalgamation of all of its samples
    """
    abstract = ''
    for sample_id in get_all_samples_in_series(data_table, series_id):
        abstract += get_abstract_for_sample(data_table, sample_id) + ' '

    return abstract

def get_all_sample_titles_for_series(data_table, series_id):
    """

    """
    titles = []
    sample_ids = get_all_samples_in_series(data_table, series_id)
    for sample_id in sample_ids:
        titles.append(get_title_for_sample(data_table, sample_id))

    return sample_ids, titles

def get_abstract_for_sample(data_table, sample_id):
    return ' '.join(str(x) for x in data_table[sample_id]).replace('nan', '').strip()

def get_all_samples_in_series(data_table, series_id):
    return data_table.loc[:, data_table.loc['Series'] == series_id].columns

def get_title_for_sample(data_table, sample_id):
    return data_table.loc['title', sample_id]

def get_all_series(data_table):
    return table.loc['Series']


if __name__ == '__main__':
    table = pd.read_table('../all_meta.txt', index_col=0)
    temp_series_id = 'GSE63726'
    abstract = get_abstract_for_series(table, temp_series_id)
    temp_sample_ids, all_sample_titles = get_all_sample_titles_for_series(table, temp_series_id)
    print cluster_descriptions(abstract, all_sample_titles)

    # TODO: switch to an eedit distance model.




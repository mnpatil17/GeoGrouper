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

def get_all_series_ids(data_table):
    return table.loc['Series'].unique()


# WORKS FOR: 'GSE64520', 'GSE70485'


# BAD: GSE80463, GSE70091, GSE81074, GSE83438, GSE63126, GSE63124
if __name__ == '__main__':
    # table = pd.read_table('../all_meta.txt', index_col=0, low_memory=False)
    # temp_series_id = 'GSE70485'
    # temp_sample_ids, all_sample_titles = get_all_sample_titles_for_series(table, temp_series_id)

    # print 'Number of Samples: {0}\n'.format(len(all_sample_titles))
    # for cluster in cluster_descriptions(all_sample_titles, all_sample_titles):
    #     print cluster

    table = pd.read_table('../all_meta.txt', index_col=0, low_memory=False)

    for series_id in get_all_series_ids(table):
        sample_ids, all_sample_titles = get_all_sample_titles_for_series(table, series_id)

        print '-------------------------------------------------------------------------\n'
        print 'SERIES: {0}'.format(series_id)
        print 'NUM SAMPLES: {0}\n\n'.format(len(all_sample_titles))

        if len(all_sample_titles) > 5:
            cluster_desc, org_mtx = cluster_descriptions(all_sample_titles, all_sample_titles)
            for cluster in cluster_desc:
                print cluster
                # print 'Min: {0}, Max: {1}'.format(min(), max())
        else:
            print 'Insufficient samples to process this.'


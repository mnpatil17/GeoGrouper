# GeoGrouper
Groups Geo data by clustering based on keywords

### Installation

To install the `geogrouper` package, follow the following steps. The latter steps (5-8) involve the
installation of `python_mcl`, the MCL clustering algorithm implementation in python that this
uses.

1. `cd <path/to/your/working/directory>`
2. `git clone https://github.com/mnpatil17/GeoGrouper`
3. `cd GeoGrouper`
4. `pip install -e .`
5. `git clone https://github.com/koteth/python_mcl       # do this inside the outer GeoGrouper directory`
6. `cd python_mcl`
7. `python setup.py install`
8. `cd ..`


### Usage

Using the `geogrouper` package is very simple. The primary method is `cluster_descriptions_from_file`

To cluster from a file:

	from geogrouper import cluster_descriptions_from_file
	clusters_for_each_series = cluster_descriptions_from_file(path_to_data_file)


To cluster from a file AND **print** to terminal as you go:

	from geogrouper import cluster_descriptions_from_file
	clusters_for_each_series = cluster_descriptions_from_file(path_to_data_file, should_print_output=True)
	

To cluster from a file AND **print** to terminal only the series that have at least `N` samples:

	from geogrouper import cluster_descriptions_from_file
	clusters_for_each_series = cluster_descriptions_from_file(path_to_data_file, should_print_output=True, print_series_sample_size=N)
	

To cluster a list of sample descriptions with some additional description text (`abstract_text`):

	from geogrouper import cluster_descriptions
	clusters, mcl_matrix = cluster_descriptions(sample_titles_list, abstract_text)


### Modules

1. `geo_id.py`: handles reading from a specified datatable
2. `keywords.py`: has multiple methods for finding keywords for a series (not all are used)
3. `geogrouper.py`: the primary file, which handles the clustering. `cluster_descriptions_from_file`
					is the **primary method**
4. `utils.py`: various utility functions


### Potential Future Optimizations

The file `keywords.py` contains the logic to find keywords from GEO data. Currently there are two methods:

1. `get_acronyms()`
2. `get_common_words()`

**Changing the way the main algorithm finds keywords will change the effectiveness of the algorithm.**
Therefore, to iterate on this algorithm, changing the way keywords are found is
a great way to improve performance.




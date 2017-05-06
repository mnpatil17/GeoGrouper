# GeoGrouper
Groups Geo data by clustering based on acronyms

### Modules

1. `geo_id.py`: handles reading from a specified datatable
2. `keywords.py`: has multiple methods for finding keywords for a series (not all are used)
3. `geogrouper.py`: the primary file, which handles the clustering. `cluster_descriptions_from_file`
					is the **primary method**
4. `utils.py`: various utility functions


### Potential Future Optimizations

The file `keywords.py` contains the logic to find keywords from GEO data. Currently there are two methods:

1. `get_acronyms`
2. `get_common_words`

**Changing the way the main algorithm finds keywords will change the effectiveness of the algorithm.**
Therefore, to iterate on this algorithm, changing the way keywords are found is
a great way to improve performance.




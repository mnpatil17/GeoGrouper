# GeoGrouper
Groups Geo data by clustering based on acronyms

### Current Status

- [x] Basic acronym clustering algorithm
	- [x] Planning
	- [x] Algorithm
- [x] Handling numbers and replicates
	- [x] Planning
	- [x] Algorithm
- [ ] Integration with GeoPy

### Potential Future Optimizations

The file `keywords.py` contains the logic to find keywords from GEO data. Currently there are two methods:

1. `get_acronyms`
2. `get_common_words`

**Changing the way the main algorithm finds keywords will change the effectiveness of the algorithm.**
Therefore, to iterate on this algorithm, changing the way keywords are found is
a great way to improve performance.




from geogrouper import cluster_descriptions
from spec_utils import sort_dictionary_list_values
import unittest


class BasicClusteringTests(unittest.TestCase):
    """
    Tests for the Clustering model
    """

    def test_basic_clustering(self):

        # setup
        abs_text = 'This abstract is with tRNA samples. I like Unrelated Textual Sentence (UTS).'

        desc1 = 'UTS 1'
        desc2 = 'UTS 2'
        desc3 = 'tRNA 1'
        desc4 = 'tRNA 2'
        desc_list = [desc1, desc2, desc3, desc4]

        # run tests
        actual_clustering_result = sort_dictionary_list_values(cluster_descriptions(abs_text,
                                                                                    desc_list))
        expected_clustering_result = {
            ('UTS',): sorted([desc1, desc2]),
            ('tRNA',): sorted([desc3, desc4]),
        }

        # final check
        test = unittest.TestCase('assertEqual')
        test.assertDictEqual(expected_clustering_result, actual_clustering_result)


    def test_ignore_irrelevent_acroynms(self):

        # setup
        abs_text = 'This abstract is with tRNA samples. I like Unrelated Textual Sentence ' + \
                   '(UTS). The cool thing of this project is that it is sponsored by NASA.'

        desc1 = 'UTS 1'
        desc2 = 'UTS 2'
        desc3 = 'tRNA 1'
        desc4 = 'tRNA 2'
        desc_list = [desc1, desc2, desc3, desc4]

        # run tests
        actual_clustering_result = sort_dictionary_list_values(cluster_descriptions(abs_text,
                                                                                    desc_list))
        expected_clustering_result = {
            ('UTS',): sorted([desc1, desc2]),
            ('tRNA',): sorted([desc3, desc4]),
        }

        # final check
        test = unittest.TestCase('assertEqual')
        test.assertDictEqual(expected_clustering_result, actual_clustering_result)


    def test_combinatorial_acronym_categories(self):

        # setup
        abs_text = 'This abstract is with tRNA samples. I like Unrelated Textual Sentence ' + \
                   '(UTS). The cool thing of this project also has mRNA and rRNA.'

        desc1 = 'rRNA 1'
        desc2 = 'rRNA 2'
        desc3 = 'tRNA 1 with UTS'
        desc4 = 'tRNA 2 with UTS'
        desc5 = 'mRNA 1 with UTS copied from tRNA 1'
        desc6 = 'mRNA 2 with UTS copied from tRNA 2'
        desc_list = [desc1, desc2, desc3, desc4, desc5, desc6]

        # run tests
        actual_clustering_result = sort_dictionary_list_values(cluster_descriptions(abs_text,
                                                                                    desc_list))
        expected_clustering_result = {
            ('rRNA',): sorted([desc1, desc2]),
            ('UTS', 'tRNA'): sorted([desc3, desc4]),
            ('UTS', 'mRNA', 'tRNA'): sorted([desc5, desc6]),
        }

        print actual_clustering_result
        print expected_clustering_result

        # final check
        test = unittest.TestCase('assertEqual')
        test.assertDictEqual(expected_clustering_result, actual_clustering_result)


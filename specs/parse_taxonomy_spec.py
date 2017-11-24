import os, sys
import unittest

dir = os.path.dirname(__file__)
sys.path.append(os.path.join(dir,'..'))
from parse_taxonomy import parse_taxonomy_form_file, tree_to_file

HAPPY_TAXONOMY = '../Data/T1.csv'
TEXT_WRITE_TAXONOMY = 'T1_test.csv'

class parse_taxonomy_spec(unittest.TestCase):

    def test_parse_write_parse_new_match(self):
        tree_1 = parse_taxonomy_form_file(os.path.join(dir, HAPPY_TAXONOMY))
        tree_to_file(tree_1, os.path.join(dir, TEXT_WRITE_TAXONOMY))

if __name__ == '__main__':
    unittest.main()

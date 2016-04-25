# -*- coding: utf-8 -*-
"""
@author: Kristofer
Lesson 6: Case Study: OpenStreetMap Data
Quiz 1: Iterative Parsing
"""

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        # YOUR CODE HERE
     
def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

if __name__ == "__main__":
    test()
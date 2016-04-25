# -*- coding: utf-8 -*-
"""
@author: Kristofer
Lesson 6: Case Study: OpenStreetMap Data
Quiz 3: Tag Types
"""

import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        print(element.attrib["k"])
        myText = element.attrib["k"]
        if problemchars.search(myText):
            keys["problemchars"] = keys["problemchars"] + 1
        elif lower_colon.search(myText):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif lower.search(myText):
            keys["lower"] += 1
        else:
            keys["other"] = keys["other"] + 1       
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()
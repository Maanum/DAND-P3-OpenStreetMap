# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:26:12 2016

@author: Kristofer
"""

#==============================================================================
# Script #3 for review of Singapore data for P3
#   - List and count "sub-tag" values of "k" and "v" for each location type
#   - Result to be exported to CSV
#==============================================================================

import xml.etree.cElementTree as ET
import pprint
import csv
    
DATA_FILE = 'singapore.osm'
relevant_tags = ["node", "way", "relation"]

def process_map(filename):
    
    data_set = {}
    for item in relevant_tags:
        data_set[item + "_data_type"] = {}

    for event, elem in ET.iterparse(filename):
        if elem.tag in relevant_tags:
            for tag in elem.iter("tag"):
                if tag.attrib["k"] in data_set[elem.tag + "_data_type"]:
                    data_set[elem.tag + "_data_type"][tag.attrib["k"]] = data_set[elem.tag + "_data_type"][tag.attrib["k"]] + 1
                else:
                    data_set[elem.tag + "_data_type"][tag.attrib["k"]] = 1

    return data_set


def test():
    data_types = process_map(DATA_FILE)
    pprint.pprint(data_types)
    with open('attributes.csv', 'w', encoding='utf8') as wf:
        loadWriter = csv.writer(wf, delimiter=',',lineterminator='\n')
        for key, subdict in data_types.items():
            for subkey, value in subdict.items():
                loadWriter.writerow([key, subkey, value]) 
            
if __name__ == "__main__":
    test()
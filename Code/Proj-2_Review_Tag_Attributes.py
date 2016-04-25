# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 19:26:12 2016

@author: Kristofer
"""

#==============================================================================
#Script #2 for review of Singapore data for P3
#Review attributes included in the OSM tags.
#==============================================================================


import xml.etree.cElementTree as ET
import pprint
    
DATA_FILE = 'singapore.osm'
relevant_tags = ["node", "way", "relation"]

data_set = {}
for item in relevant_tags:
    data_set[item] = {}
    data_set[item]["attributes"] = set()
    data_set[item]["tag_attributes"] = set()
    
data_set["way"]["nd_attributes"] = set()
data_set["relation"]["member_attributes"] = set()
    

for event, elem in ET.iterparse(DATA_FILE):
    if elem.tag in relevant_tags:
        for attr, value in elem.attrib.items():
            data_set[elem.tag]["attributes"].add(attr)
            
        for tag in elem.iter():
            for attr, value in tag.attrib.items():
                if tag.tag != elem.tag:
                    data_set[elem.tag][tag.tag + "_attributes"].add(attr)

pprint.pprint(data_set)

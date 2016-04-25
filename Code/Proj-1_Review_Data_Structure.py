import xml.etree.cElementTree as ET
import pprint

#==============================================================================
#Script #1 for review of Singapore data for P3
#
#Check XML structure of data, such as what tags are there and what 
# structure are these tags in.
#==============================================================================

DATA_FILE = 'singapore.osm'
    
element_types = {}

for _, element in ET.iterparse(DATA_FILE):
    if element.tag not in element_types.keys():
            element_types[element.tag] = {}
    for tag in element.iter():
        if tag.tag != element.tag:
            if tag.tag in element_types[element.tag].keys():
                element_types[element.tag][tag.tag] += 1
            else:
                element_types[element.tag][tag.tag] = 1
                
pprint.pprint(element_types)

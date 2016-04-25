# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:15:29 2016

@author: Kristofer
"""

#==============================================================================
# Script for converting Singapore OSM data to JSON format.
#  Also included are handlers to clean the structure and data
#
#==============================================================================

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import pprint
import codecs
import json
import unicodedata
from collections import defaultdict

DATA_IN_FILE= "sample.osm"
osm_file = open(DATA_IN_FILE, "r")

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\t\r\n]')


# Set root tags
relevant_tags = ["node", "way", "relation"]

# Set attributes to be included in "created" group
created_attribs = ["version", "changeset", "timestamp", "user", "uid"]

# Set tag groups other than "created".  These will be identified by "K" tags with "V" having
#  a nested structure (e.g. a V attribute of "addr:street_name" will be converted to a field
#  "street_name" under "addr" group)
data_groups = ["addr", "building", "seamark", "is_in"]

# Identify tags to be included in the "name" group.  This is called separately as the name values don't have
#  a standard naming convention (e.g. not all names "V" values are in the format "name:[VALUE]" )
name_attribs = ["name", "name:en", "name:zh", "name:ja", "name:ms", "alt_name", "alt_name:ms", "old_name"]

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)


# Set up name abbreviations replacements.  Generally, English street identifiers come at the end of the street
# name and Bahasa street identifiers come at the start.
mapping_end = { "Rd": "Road", "Ave": "Avenue", "Avebue" : "Avenue", "Cresent":"Crescent", "St":"Street", 
               "road":"Road","street":"Street", "terrace":"Terrace"}
mapping_start = {"Jl.": "Jalan", "Jln.":"Jalan", "Jln":"Jalan", "jalan":"Jalan", "Lor":"Lorong"}


def shape_element(element):
    node = {}
    created = {}
    pos = []
    node_refs = []
    ref_members = []
    data_group_dict = {}
    names = {}
    addl_info = {}
    
    if element.tag in relevant_tags:
        node["type"] = element.tag
        
        for group in data_groups:
            data_group_dict[group] = {}
    
        for attr, value in element.attrib.items():
            if attr in created_attribs:
                created[attr] = value
            elif attr == "lat":
                pos.insert(0,float(value))
            elif attr == "lon":
                pos.insert(1,float(value))
            else:
                node[attr] = value
        if created:
            node["created"] = created
        if pos:
            node["pos"] = pos


        for tag in element.iter("nd"):
            node_refs.append(tag.attrib["ref"])
        if node_refs:
            node["node_refs"] = node_refs

        for tag in element.iter("member"):
            new_member = {}
            for attr, value in tag.attrib.items():
                new_member[attr] = value
            ref_members.append(new_member)
        if ref_members:    
            node["members"] = ref_members    


        for tag in element.iter("tag"):
            tagValue = tag.attrib["v"]
            tagKey = ""
            
            for group in data_groups:
                group_len = len(group)+1              
                if tag.attrib["k"][0:group_len] == group + ":":
                    
                    if tag.attrib["k"] == "addr:street":
                        tagValue = street_handler(tagValue)
                    tagKey = clean_key(group_len, tag.attrib["k"])
                    data_group_dict[group][tagKey] = tagValue
            
            if tagKey == "":
                tagKey = tag.attrib["k"]
                if tagKey in name_attribs:
                    names[tagKey] = tagValue
                else:
                    addl_info[tagKey] = tagValue

        # Names handler
        if names:
            name_main, name_alt = name_handler(names)
            node["name"] = name_main
            if name_alt:
                node["alt_names"] = name_alt

        for group in data_groups:
            if data_group_dict[group]:
                node[group] = data_group_dict[group]
        
        # Move all other values to "addl_info"
        if addl_info:
            node["addl_info"] = addl_info
        
        return node
        
    else:
        return None


def name_handler(names):
# This handler will select a main "name" for the location.  The remaining
#  names will be moved under "alt_names".  The main name will be in Latin 
#  characters only unless there are no other options.
    
    # Check if "name" tag exists in names.  If not, created one.
    if "name" not in names.keys():
        if names:
            key, names["name"] = names.popitem()
        else:
            return None, names

    # Select "name" tag as the main name.  Remove the duplicate from "names".
    main_name = names["name"]
    del names["name"]

    # Check if main_name contains non-Latin characters.
    isCJK = False    
    for ch in main_name:
        if unicodedata.category(ch) in ("Lo", "Mn"):
            isCJK = True
            print (main_name, ":",  ch, ":", unicodedata.category(ch))
            
    #if main_name contains non-Latin characters, switch to another name (if one exists)
    if isCJK:
        print (main_name, names)
        if names:
            key, name_new = names.popitem()
            names["name_CJK"] = main_name
            main_name = name_new

    return main_name, names

def street_handler(street_name):
# Check if street name includes an abbreviation.  If so, replace with full name.
    
    last_word = street_name.rpartition(' ')[2]
    first_word = street_name.partition(' ')[0]

    if last_word in mapping_end.keys():
        street_name = street_name.rpartition(' ')[0] + " " + mapping_end[last_word]
    
    if first_word in mapping_start.keys():
        street_name = mapping_start[first_word] + " " + street_name.partition(' ')[2]
        
    return street_name


def clean_key(group_len, key):
    
    sub_key = key[group_len:] 
    colon_loc = sub_key.find(":")
       
    if colon_loc == -1:
        key = sub_key
    else:
        key = sub_key[colon_loc+1:]
        
    return key
    
def process_map(file_in):
    data = []
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            data.append(el)
    return data

def convert_format():
    data = process_map(DATA_IN_FILE)
    file_out = "{0}.json".format(DATA_IN_FILE)
    with codecs.open(file_out, "w", encoding='utf8') as fo:
            fo.write(json.dumps(data, indent=2, ensure_ascii=False) +"\n")
            
if __name__ == "__main__":
	convert_format()

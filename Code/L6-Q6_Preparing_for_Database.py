# -*- coding: utf-8 -*-
"""
@author: Kristofer
Lesson 6: Case Study: OpenStreetMap Data
Quiz 6: Preparing for Database
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
#problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\t\r\n]')


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    import pprint
    
    node = {}
    created = {}
    pos = []
    addr = {}
    node_refs = []
    if element.tag == "node" or element.tag == "way" :
        if element.tag == "node":
            node["type"] = "node"
        else:
            node["type"] = "way"
                 
        for attr, value in element.attrib.items():
            if attr in CREATED:
                created[attr] = value
            elif attr == "lat":
                pos.insert(0,float(value))
            elif attr == "lon":
                pos.insert(1,float(value))
            else:
                node[attr] = value
        for tag in element.iter("tag"):
            tagVal = tag.attrib["v"]
            tagTag = tag.attrib["k"]
            if problemchars.search(tagVal):
                print("Problem: ", tagVal, problemchars.search(tagVal))
                
            else:  
                if tagTag[0:5] == "addr:":
                    if tagTag[5:].find(":") == -1:
                        addr[tagTag[5:]] = tagVal
                        print(tagTag[5:].find(":"))
                else:
                    node[tagTag] = tagVal

        for tag in element.iter("nd"):
            node_refs.append(tag.attrib["ref"])

        if created:
            node["created"] = created
        if pos:
            node["pos"] = pos
        if addr:
            node["address"] = addr
        if node_refs:
            node["node_refs"] = node_refs
        pprint.pprint(node)
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('example.osm', True)
    #pprint.pprint(data)
    
    correct_first_elem = {
        "id": "261114295", 
        "visible": "true", 
        "type": "node", 
        "pos": [41.9730791, -87.6866303], 
        "created": {
            "changeset": "11129782", 
            "user": "bbmiller", 
            "version": "7", 
            "uid": "451048", 
            "timestamp": "2012-03-28T18:31:23Z"
        }
    }
    assert data[0] == correct_first_elem
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]

if __name__ == "__main__":
    test()
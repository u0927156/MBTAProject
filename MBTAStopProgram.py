# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:40:54 2021

@author: Spencer Peterson
"""

import requests



def getSubwayLines(key):
    """
    Get all active subway lines

    Parameters
    ----------
    key : string
        The api key.

    Returns
    -------
    List of dicts
        List of dictionaries containing the information of subway lines.

    """
    # Request all of the line information and include . 
    r = requests.get("https://api-v3.mbta.com/routes?fields[type]", headers={'x-api-key': key})
    
    # I'm going to filter information locally. I chose to do this because I want to
    # keep my requests to a minimum and it shouldn't be computationally intensive
    # on my end.

    
    if r.status_code != 200:
        return []
        
        
    data = r.json()['data']
    
    subway_lines = []
    
    for datum in data:
        
        if datum['attributes']['type'] == 0 or datum['attributes']['type'] == 1:
            subway_lines.append(datum)
    
    return subway_lines
    
def getStops(lineID, key):
    
    
    r = requests.get(f"https://api-v3.mbta.com/stops?filter%5Broute%5D={lineID}", headers={'x-api-key': key})
    
    stops = r.json()['data']

    return stops    
def main():
    # read in my API key. Keep it secret, keep it safe.
    f = open('key.txt', 'r')
    key = f.read()
    f.close()
    
    
   
    subway_lines = getSubwayLines(key)
            
    for line in subway_lines:
        print(line['attributes']['long_name'])
        


if __name__ == "__main__":
    main()
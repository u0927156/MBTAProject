# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:40:54 2021

@author: Spencer Peterson
"""

import requests


def main():
    # read in my API key. Keep it secret, keep it safe.
    f = open('key.txt', 'r')
    key = f.read()
    f.close()
    
    
    # Request all of the line information and include . 
    r = requests.get("https://api-v3.mbta.com/routes?fields[type]", headers={'x-api-key': key})
    
    # I'm going to filter information locally. I chose to do this because I want to
    # keep my requests to a minimum and it shouldn't be computationally intensive
    # on my end.

    
    if r.status_code != 200:
        print('Something went wrong with the request.')
    else:
        print('Filtering routes')
        
        
    data = r.json()['data']
    
    subway_lines = []
    
    for datum in data:
        
        if datum['attributes']['type'] == 0 or datum['attributes']['type'] == 1:
            subway_lines.append(datum)
            
            
    for line in subway_lines:
        print(line['attributes']['long_name'])
        


if __name__ == "__main__":
    main()
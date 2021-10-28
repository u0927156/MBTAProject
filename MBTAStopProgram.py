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
    

def findMinAndMaxStopLines(lineID, lines_to_stops):
    # find the maximum and minimum number of stops
    max_stops_line = lineID
    max_stops = len(lines_to_stops[lineID])
    
    min_stops_line = lineID        
    min_stops = len(lines_to_stops[lineID])    
        
    for key in lines_to_stops.keys():
        num_stops = len(lines_to_stops[key])  
        
        if num_stops > max_stops:
            max_stops = num_stops
            max_stops_line = key
            
        if num_stops < min_stops:
            min_stops = num_stops
            min_stops_line = key
            
    return max_stops_line, max_stops, min_stops_line, min_stops


def findStopNameToLines(lines_to_stops):
    stop_name_to_lines = dict()
    for key in lines_to_stops.keys():
         
         for stop in lines_to_stops[key]:
             stop_name = stop['attributes']['name']
             
             if stop_name in stop_name_to_lines:
                 stop_name_to_lines[stop_name].append(key)
             else:
                 stop_name_to_lines[stop_name] = [key]
                 
    return stop_name_to_lines


             
def FindRoute(curr_routes, end_routes, previous_routes, lines_to_stops, stop_name_to_lines):
    
    for end_route in end_routes:
        if end_route in curr_routes:
            print(*previous_routes, sep=', ', end=' ')
            print(end_route)
            return previous_routes.append(end_route)
        
    for curr_route in curr_routes:
    
        curr_connects_to = set()
        for stops in lines_to_stops[curr_route]:
            stop_name = stops['attributes']['name']
            
            for line in stop_name_to_lines[stop_name]:
                if line not in curr_routes:
                    curr_connects_to.add(line)
                
        
                
        previous_routes.append(curr_route)
        return FindRoute(curr_connects_to, end_routes, previous_routes, lines_to_stops, stop_name_to_lines)
    
def main():
    # read in my API key. Keep it secret, keep it safe.
    f = open('key.txt', 'r')
    key = f.read()
    f.close()
    
    
    # Gets all of the subway lines using the API key
    subway_lines = getSubwayLines(key)
        
    # Prints the lines and then gets all stops associated with the lines
    lines_to_stops = dict()    
    for line in subway_lines:
        lineID = line['id']
        print(lineID)
        
        
        # gets the stops
        stops = getStops(lineID, key)
        
        # makes a dictionary that connects line ID to associated stops 
        lines_to_stops[lineID] = stops
        
        
    # find the line with most and least stops
    max_stops_line, max_stops, min_stops_line, min_stops = findMinAndMaxStopLines(lineID, lines_to_stops)
            
    print(f'Line with most stops: {max_stops_line}, number of stops {max_stops}')
    print(f'Line with least stops: {min_stops_line}, number of stops {min_stops}')
        
    # Make a dictionary with the stop name and all associated lines 
    stop_name_to_lines = findStopNameToLines(lines_to_stops)
      
    for stop_name in stop_name_to_lines.keys():
        if len(stop_name_to_lines[stop_name]) > 1:
            print(stop_name + ' connects lines ', end = '')
            print(*stop_name_to_lines[stop_name], sep=', ')

    
    start_stop = 'Wonderland'
    
    end_stop = 'Oak Grove'
    
    print('\nEnter the stop you are departing from: ')
    start_stop = input()
    
    
    print('\nEnter your destination stop: ')
    end_stop = input()
    
    
    if start_stop not in stop_name_to_lines:
        print('Start stop not found.')
        return
    
    if end_stop not in stop_name_to_lines:
        print('End stop not found.')
        return
    
    start_routes = stop_name_to_lines[start_stop]
    
    end_routes = stop_name_to_lines[end_stop]


    
    FindRoute(start_routes, end_routes, [], lines_to_stops, stop_name_to_lines)

 

if __name__ == "__main__":
    main()
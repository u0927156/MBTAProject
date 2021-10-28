# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:40:54 2021

@author: Spencer Peterson
"""
import sys,os
import requests

print(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))


f = open('key.txt', 'r')
key = f.read()
f.close()

r = requests.get("https://api-v3.mbta.com/lines")
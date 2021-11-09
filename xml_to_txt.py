# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:28:53 2021

@author: ngz117
"""
import re

filename = input('Enter filename: ')+'.xml'
output = filename[:filename.find('.')]+'.txt'

f = open(filename,'r',encoding='utf-8')
o = open(output,'w',encoding='utf-8')        

for line in f:
    line = re.sub("<.*?>", "", line)
    o.write(line)

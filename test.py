# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 19:16:16 2018

@author: AT-IL
"""

import os.path

if os.path.isfile("./temp/test.txt"):
    print('found test.txt')
else:
    print('file dne')
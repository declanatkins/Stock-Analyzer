"""
Author Declan Atkins
Last Changed: 24/08/17

This module is used to parse the data from graphs 
that are taken in.

"""
import sys
sys.path.append("../C-Modules/ParsedImageSearch")
import ParsedImageSearch as imgSearch
import cv2
import numpy as np
import copy
import matplotlib.pyplot as pyp
from newspaper import Article

class GraphHandler:

    def __init__(self, companyName):
        self.name = companyName
        self.valsList = []


    def pullGraph(self):
        pass
    
    def getXY(self):
        img = cv2.imread(self.graphFilename)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([0,120,150])
        upper = np.array([255,255,255])

        mask = cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(img,img,mask=mask)

        resOuterArray = imgSearch.intArrayArray(len(res))
        for pixel in res:
            thisResPixel = imgSearch.intArray(len(pixel))
            for i in range(len(pixel)):
                thisResPixel[i] = pixel[i]
        
        self.xyArray = imgSearch.get_xy_values(resOuterArray)


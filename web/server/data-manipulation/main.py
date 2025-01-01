import numpy as np
import urllib.request
import cv2
import sys
import json
from shapely.geometry import Polygon, LineString, Point
import networkx as nx
import matplotlib.pyplot as plt
import heapq

def url_to_image(url):
    # open a connection with url
    response = urllib.request.urlopen(url)

    # convert the raw image into numpy array
    image = np.asarray(bytearray(response.read()), dtype="uint8")

    # transform the image into something opencv can work with
    # cv2.IMREAD_COLOR - makes sure the image is in 3-channels color format (RGB)
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    return image


def process_image(imageURL):
    image = url_to_image(imageURL);

    _,threshold = cv2.threshold(image, 100, 255,  
                            cv2.THRESH_BINARY) 

    # extract the contours
    # RETR_TREE - retrieval mode to get the contours and arrange them in a tree hierarchy
    # CHAIN_APPROX_SIMPLE - contour approximation mode for compression - efficiency
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    polygons = []
    for cnt in contours : 
        area = cv2.contourArea(cnt) 
        # remove noise from the image 
        if area > 1000:
            print(f"area: {area}")

        # take only the largest polygons
        if area > 5000 and area < 7000000:  
            approx = cv2.approxPolyDP(cnt, 0.001 * cv2.arcLength(cnt, True), True) 
            print(f"len polygon: {len(approx)}")
            # make sure the polygon has at least 5 edges (have to reconsider this condition)
            if(len(approx) > 5):  
                polygons.append(approx)

                cv2.drawContours(image, [approx], 0, (255, 0, 0), 5) 


    # create an image with the polygon
    canvas = np.zeros_like(image)
    polygon_points = polygons[0].reshape((-1, 1, 2)).astype(np.int32)

    cv2.polylines(canvas, [polygon_points], isClosed=True, color=(255, 255, 255), thickness=2)
    cv2.imwrite('data-output/processed_overlay.png', canvas)
    print("Number of contours detected:",len(contours))


    return 1;

if __name__== "__main__":
    # argv[1] - imageURL
    process_image(sys.argv[1]);



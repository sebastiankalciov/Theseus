import numpy as np
import urllib.request
import cv2
import sys
import json

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def process_image(imageURL):
    image = url_to_image(imageURL);

    edges = cv2.Canny(image, 100, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    paths = [contour.tolist() for contour in contours]

    with open('data-output/processed_data.json', 'w') as f:
        json.dump(paths, f)


    overlay = cv2.drawContours(np.zeros_like(image), contours, -1, (255, 255, 255), 1)
    cv2.imwrite('data-output/processed_overlay.png', overlay)

    return 1;


if __name__== "__main__":
    # argv[1] - imageURL
    process_image(sys.argv[1]);



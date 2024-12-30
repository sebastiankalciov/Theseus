import numpy as np
import urllib
import cv2
import sys

def url_to_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def process_image(imageURL, output_file_path):
    image = url_to_image(imageURL);
    print(image)


if __name__== "__main__":
    # argv[1] - imageURL
    # argv[2] - output file path
    process_image(sys.argv[1], "./");



import cv2
import pandas as pd 
from measure import smart_measure
from crop import box_crop
from resize import resizer
from padding import pad
from dominant_color import colorify
from color_profiler import profiler
from contour import contour_area

test_image = '/Users/jinuaugustine/Downloads/test4.jpeg'
detected_leaf_coordinates = '/Users/jinuaugustine/Downloads/conoor.csv'

df = pd.read_csv(detected_leaf_coordinates)
no_leaves = len(df.index)

calibration = smart_measure(test_image)
print("Detected Calibration: {} pixel/cm2".format(calibration))

print("\n\nCropping Detected {} Leaves.....".format(no_leaves))
box_crop(test_image, detected_leaf_coordinates)

print("\n\nStarting Pre-Processing of Cropped Leaves.....")

j = 1
for x in range(no_leaves):
    img_path = "/Users/jinuaugustine/Documents/Fine Leaf/Processing/detected_leaf_"+str(j)+".jpg"
    img = cv2.imread(img_path)

    print("Analysing Color Profile of Leaf {}".format(j))
    profiler(img)

    print("Resizing Leaf {}".format(j))
    resized_img = resizer(img)

    print("Padding Leaf {}".format(j))
    padded_image = pad(resized_img)

    print("Finding Dominant Color of Leaf {}".format(j))
    colored_img = colorify(padded_image)

    print("Finding Contour and Area of Leaf {}".format(j))
    contour_area(colored_img)

    









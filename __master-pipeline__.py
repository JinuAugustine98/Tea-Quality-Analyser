import os
import cv2
import pandas as pd 
import mysql.connector
from mysql.connector import connect, Error
from measure import smart_measure
from crop import box_crop
from color_profiler import DominantColors
from resize import resizer
from padding import pad
from dominant_color import colorify
from contour import contour_area


try:
    with connect(
        host="soli-db.ciksb20swlbf.ap-south-1.rds.amazonaws.com",
        user='teaquality',
        password='Quality@123',
        database="db_tea_quality_record",
    ) as connection:
        print("MySQL Database Connected Successfully!")
except Error as e:
    print(e)

test_image = '/Users/jinuaugustine/Downloads/test4.jpeg'
detected_leaf_coordinates = '/Users/jinuaugustine/Downloads/conoor.csv'

df = pd.read_csv(detected_leaf_coordinates)
no_leaves = len(df.index)
batch = 1

parent_dir1 = "/Users/jinuaugustine/Documents/Tea-Quality-Analyser/Processing"
directory1 = "Leaf Batch {}".format(batch)
path = os.path.join(parent_dir1, directory1)
os.mkdir(path)
print("\nDirectory {} created".format(directory1))

parent_dir2 = "/Users/jinuaugustine/Documents/Tea-Quality-Analyser/Processing/Leaf Batch {}".format(batch)

calibration = smart_measure(test_image, parent_dir2)
print("\nDetected Calibration: {}pixel/cm2".format(calibration))

print("\n\nCropping Detected {} Leaves.....".format(no_leaves))
box_crop(test_image, detected_leaf_coordinates, parent_dir2)

print("\n\nStarting Pre-Processing of Cropped Leaves.....")

j = 1
for x in range(no_leaves):

    img_path = "/Users/jinuaugustine/Documents/Tea-Quality-Analyser/Processing/Leaf Batch {}/Leaf No. {}".format(batch, j)

    profile_path = img_path+"/detected_leaf.jpg"
    print("\nAnalysing Color Profile of Leaf {}".format(j))

    clusters = 5
    dc = DominantColors(profile_path, img_path, clusters)
    colors = dc.dominantColors()
    print(colors)
    hist = dc.plotHistogram()

    c_prof = colors.tolist()
    
    dr1 = c_prof[0][0]
    dg1 = c_prof[0][1]
    db1 = c_prof[0][2]

    dr2 = c_prof[1][0]
    dg2 = c_prof[1][1]
    db2 = c_prof[1][2]

    dr3 = c_prof[2][0]
    dg3 = c_prof[2][1]
    db3 = c_prof[2][2]

    dr4 = c_prof[3][0]
    dg4 = c_prof[3][1]
    db4 = c_prof[3][2]

    dr5 = c_prof[4][0]
    dg5 = c_prof[4][1]
    db5 = c_prof[4][2]

    print("\nResizing Leaf {}".format(j))
    resizer(profile_path, img_path)

    pad_path = img_path+'/resized.png'
    print("\nPadding Leaf {}".format(j))
    pad(pad_path, img_path)

    color_path = img_path+'/padded.png'
    print("\nFinding Dominant Color of Leaf {}".format(j))
    colorify(color_path, img_path)

    contour_path = img_path+'/dominant_color.jpg'
    print("\nFinding Contour and Area of Leaf {}".format(j))
    contour_area(contour_path, img_path)

    j+=1

    








